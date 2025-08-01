import webbrowser
import time
import pyttsx3
from auth.oauth import buildAuthorizationURL, startLocalServer, getToken
from twitch.twitch_chat import TwitchChat
from queue import Empty
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES

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
        nickname='crisred07',
        token='oauth:' + accessToken,
        channel='crisred07',  
    )
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)
    twitchClient.connect()
    print(f"Connected to channel: {twitchClient.channel}")
    twitchClient.startReading()
    while True:
        try:
            user, message = twitchClient.messageQueue.get(timeout=1)
            engine.say(f"{user} say: {message}")
            engine.runAndWait()
        except Empty:
            pass  

if __name__ == "__main__":
    main()