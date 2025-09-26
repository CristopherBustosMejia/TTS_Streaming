import webbrowser
import time
from auth.oauth import buildAuthorizationURL, startLocalServer, getToken
from chatClients.twitchChat import TwitchChat
from chatClients.tiktokChat import TikTokChat
from tts.elevellabs import ElevenLabsTTS
from tts.googletts import GoogleTTS
from utils.logger import Logger
from queue import Empty
from config import TTS_ENGINE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, SCOPES, USER_NAME, CHANNEL_NAME, SOURCE_ROOM_ID , TIKTOK_USERNAME

def main():
    engine = getTTS()
    if engine is None:
        Logger.addToLog("error", "Error: No TTS engine configured, exiting.")
        return
    activeTwitchChat = verifyConfigTwitch()
    activeTikTokChat = verifyConfigTikTok()
    if not activeTwitchChat and not activeTikTokChat:
        Logger.addToLog("error", "Error: No chat clients configured, exiting.")
        return
    
    # Authenticate with Twitch if configured
    if activeTwitchChat:
        authorizationCode = None
        authUrl = buildAuthorizationURL(CLIENT_ID, REDIRECT_URI, SCOPES)
        print(f"Opening authorization URL: {authUrl}")
        webbrowser.open(authUrl)
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
            sourceRoom = SOURCE_ROOM_ID
        )
        twitchClient.connect()
        print(f"Connected to Twitch chat as {USER_NAME} in channel {CHANNEL_NAME}")
        twitchClient.startReading()
        print("Started reading Twitch chat messages.")
    
    # Start TikTok chat if configured
    if activeTikTokChat:
        tiktokClient = TikTokChat(
            username=TIKTOK_USERNAME
        )
        print(f"Connected to TikTok {TIKTOK_USERNAME} chat")
        tiktokClient.startReading()
        print("Started reading TikTok chat messages.")

    while True:
        try:
            if activeTwitchChat:
                user, message = twitchClient.messageQueue.get(timeout=0.1)
                processMessage(engine, user, message, "Twitch")
        except Empty:
            pass
        try:
            if activeTikTokChat:
                user, message = tiktokClient.message_queue.get(timeout=0.1)
                processMessage(engine, user, message, "TikTok")
        except Empty:
            pass
        engine.mediaPlayer.stayActive()

def processMessage(engine, user, message, platform):
    if platform == "Twitch":
        engine = getTTS()
        if message is None or message.strip() == "":
            return
        aux = engine.speak(f"[{platform}] {user} says: {message}")
        if aux == -1:
            engine = GoogleTTS()
            Logger.addToLog("info", "Switching to gTTS due to an error with ElevenLabs.")
            engine.speak(f"[{platform}] {user} says: {message}")
    elif platform == "TikTok":
        engine = GoogleTTS()
        engine.speak(f"[{platform}] {user} says: {message}")

def getTTS():
    if TTS_ENGINE == "elevenlabs":
        print(f"Using ElevenLabs TTS Engine")
        return ElevenLabsTTS()
    elif TTS_ENGINE == "gtts":
        print(f"Using gTTS Engine")
        return GoogleTTS()
    else:
        print(f"No valid TTS engine configured in .env file. Please set TTS_ENGINE")
        return None
        
def verifyConfigTwitch():
    if(CLIENT_ID is None or CLIENT_ID.strip() == ""):
        Logger.addToLog("warning","Warning: No CLIENT_ID in the config.py file or .env file.")
        return False
    if(CLIENT_SECRET is None or CLIENT_SECRET.strip() == ""):
        Logger.addToLog("warning","Warning: No CLIENT_SECRET in the config.py file or .env file.")
        return False
    if(REDIRECT_URI is None or REDIRECT_URI.strip() == ""):
        Logger.addToLog("warning","Warning: No REDIRECT_URI in the config.py file or .env file.")
        return False
    if(SCOPES is None or len(SCOPES) == 0):
        Logger.addToLog("warning","Warning: No SCOPES in the config.py file or .env file.")
        return False
    if(USER_NAME is None or USER_NAME.strip() == ""):
        Logger.addToLog("warning","Warning: No USER_NAME in the config.py file or .env file.")
        return False
    if(CHANNEL_NAME is None or CHANNEL_NAME.strip() == ""):
        Logger.addToLog("warning","Warning: No CHANNEL_NAME in the config.py file or .env file.")
        return False
    return True

def verifyConfigTikTok():
    if(TIKTOK_USERNAME is None or TIKTOK_USERNAME.strip() == ""):
        Logger.addToLog("warning","Warning: No TIKTOK_USERNAME in the config.py file or .env file.")
        return False
    return True

if __name__ == "__main__":
    main()