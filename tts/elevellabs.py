import requests
import tempfile
import os
import time
from utils.audio import AudioPlayer
from tts.base import TTSBase
from utils.logger import Logger
from config import ELEVELELABS_API_KEY, ELEVENLABS_VOICE

class ElevenLabsTTS(TTSBase):
    def __init__(self, voice=ELEVENLABS_VOICE):
        self.api_key = ELEVELELABS_API_KEY
        self.voice = voice
        self.mediaPlayer = AudioPlayer()
    
    def speak(self, text: str):
        text = text.strip()
        if not text:
            print("[TTS] Texto vacío. No se generará audio.")
            return
        print(f"[TTS] Generando audio para: {text}")
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
        if res.status_code != 200:
            print(f"Error: {res.status_code} - {res.text}")
            if res.status_code == 401:
                print("[TTS] El limite de tokens ha sido alcanzado, Cambiando a engine secundario.")
            return text
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tempAudio:
                tempAudio.write(res.content)
                tempAudioPath = tempAudio.name
            if os.path.getsize(tempAudioPath) == 0:
                print("[TTS] El archivo de audio generado está vacío.")
                return
            self.mediaPlayer.playAudio(tempAudioPath)
        except Exception as e:
            print(f"[ERROR] Error playing audio: {e}")
            Logger.addToLog("error", f"Error playing audio: {e}")
        finally:
            try:
                os.unlink(tempAudioPath)
            except OSError as e:
                print(f"[ERROR] Error deleting temporary audio file: {e}")
                Logger.addToLog("error", f"Error deleting temporary audio file: {e}")