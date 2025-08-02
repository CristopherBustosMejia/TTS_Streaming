import requests
import tempfile
import os
import time
from utils.audio import AudioPlayer
from tss.base import TTSBase
from config import ELEVELELABS_API_KEY, ELEVENLABS_VOICE

class ElevenLabsTTS(TTSBase):
    def __init__(self, voice=ELEVENLABS_VOICE):
        self.api_key = ELEVELELABS_API_KEY
        self.voice = voice
        self.mediaPlayer = AudioPlayer()
        
    
    def speak(self, text: str):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }
        res = requests.post(url, json=data, headers=headers)
        if res.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tempAudio:
                tempAudio.write(res.content)
                tempAudioPath = tempAudio.name
            try:
                self.mediaPlayer.playAudio(tempAudioPath)
            except Exception as e:
                print(f"[ERROR] Error playing audio: {e}")
            finally:
                try:
                    os.unlink(tempAudioPath)
                except OSError as e:
                    print(f"[ERROR] Error deleting temporary audio file: {e}")
        else:
            print(f"Error: {res.status_code} - {res.text}")