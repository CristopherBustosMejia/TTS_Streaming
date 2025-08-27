import tempfile
import os
from gtts import gTTS
from tts.base import TTSBase
from utils.audio import AudioPlayer
from utils.logger import Logger

class GoogleTTS(TTSBase):
    def __init__(self, lang='es'):
        self.tts = gTTS
        self.lang = lang
        self.mediaPlayer = AudioPlayer()
    
    def speak(self, text):
        text = text.strip()
        if not text:
            print("[TTS] Texto vacío. No se generará audio.")
            return
        print(f"[TTS] Generando audio para: {text}")
        try:
            tts = self.tts(text, lang=self.lang)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tempAudio:
                tts.save(tempAudio.name)
                tempAudioPath = tempAudio.name
            if os.path.getsize(tempAudioPath) == 0:
                print("[TTS] El archivo de audio generado está vacío.")
                return
            self.mediaPlayer.playAudio(tempAudioPath)
        except Exception as e:
            print(f"[ERROR] Error generating or playing audio: {e}")
            Logger.addToLog("error", f"Error generating or playing audio: {e}")
        finally:
            try:
                os.unlink(tempAudioPath)
            except OSError as e:
                print(f"[ERROR] Error deleting temporary audio file: {e}")
                Logger.addToLog("error", f"Error deleting temporary audio file: {e}")