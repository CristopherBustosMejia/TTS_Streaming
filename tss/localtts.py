import pyttsx3
from tss.base import TTSBase

class LocalTTS(TTSBase):
    def __init__(self, rate=150, volume=1.0):
        self.rate = rate
        self.volume = volume

    def speak(self, text: str):
        engine = pyttsx3.init()
        engine.setProperty('rate', self.rate)
        engine.setProperty('volume', self.volume)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    def setRate(self, rate: int):
        self.rate = rate

    def setVolume(self, volume: float):
        self.volume = volume