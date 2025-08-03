import pygame
import time

class AudioPlayer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TTS Twitch Bot")
        pygame.display.set_mode((300, 100))

    def playAudio(self, path: str):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            pygame.mixer.quit()
        except Exception as e:
            print(f"[ERROR] Error al reproducir el audio: {e}")
    
    def stayActive(self):
        pygame.event.pump()