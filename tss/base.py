from abc import ABC, abstractmethod

class TTSBase(ABC):
    @abstractmethod
    def speak(self, text: str):
        """Convert text to speech."""
        pass