import webbrowser
import time
from auth.oauth import buildAuthorizationURL, startLocalServer, getToken
from twitch.twitch_chat import TwitchChat
from tss.localtts import LocalTTS
from tss.elevellabs import ElevenLabsTTS
from queue import Empty
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES, TTS_ENGINE, USER_NAME, CHANNEL_NAME

authorizationCode = None

def main():

    authorizationCode = None
    auth_url = buildAuthorizationURL(CLIENT_ID, REDIRECT_URI, SCOPES)
    print(f"Opening authorization URL: {auth_url}")
    webbrowser.open(auth_url)
    server = startLocalServer()
    while not hasattr(server, 'authorizationCode'):
        time.sleep(1)
    authorizationCode = server.authorizationCode
    print(f"Authorization code received: {authorizationCode}")
    tokeInfo = getToken(CLIENT_ID, CLIENT_SECRET, authorizationCode, REDIRECT_URI)
    accessToken = tokeInfo.get('access_token')
    print(f"Access Token: {accessToken}")
    twitchClient = TwitchChat(
        server='irc.chat.twitch.tv',
        port=6667,
        nickname = USER_NAME,
        token='oauth:' + accessToken,
        channel = CHANNEL_NAME,  
    )
    engine = getTTS()
    twitchClient.connect()
    print(f"Connected to channel: {twitchClient.channel}")
    twitchClient.startReading()
    while True:
        try:
            user, message = twitchClient.messageQueue.get(timeout=0.1)
            engine.speak(f"{user} say: {message}")
        except Empty:
            pass  
        engine.mediaPlayer.stayActive()

def getTTS():
    if TTS_ENGINE == "elevenlabs":
        print(f"Using ElevenLabs TTS Engine")
        return ElevenLabsTTS()
    else:
        print(f"Using Local TTS Engine")
        return LocalTTS()

if __name__ == "__main__":
    main()