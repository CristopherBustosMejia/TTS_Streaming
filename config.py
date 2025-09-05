from dotenv import load_dotenv
import os

load_dotenv()

# config.py
TTS_ENGINE = os.getenv("TTS_ENGINE")

# Twitch API Configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = ['chat:read', 'chat:edit']

# ElevelLabs Configuration
ELEVELELABS_API_KEY = os.getenv("ELEVELELABS_API_KEY")
ELEVENLABS_VOICE = os.getenv("ELEVENLABS_VOICE")

# User and Channel Configuration for Twitch
USER_NAME = os.getenv("USER_NAME")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")

# User and Channel Configuration for TikTok
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")