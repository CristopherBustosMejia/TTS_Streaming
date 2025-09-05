from abc import ABC, abstractmethod

class ClientBase(ABC):
    @abstractmethod
    def startReading(self):
        """Convert text to speech."""
        pass
    def stopReading(self):
        """Convert text to speech."""
        pass