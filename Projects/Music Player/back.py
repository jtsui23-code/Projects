import pygame

class musicPlayer:
    def __init__(self):
        pygame.mixer.init()
        
    def loadSong(self, path):
        pygame.mixer.music.load(path)

    def startSong(self):
        pygame.mixer.music.play()

    def pauseSong(self):
        pygame.mixer.music.pause()

    def unpauseSong(self):
        pygame.mixer.music.unpause()
    
    def endSong(self):
        pygame.mixer.music.stop()
    
    def volume(self,volume):
        pygame.mixer.music.set_volume(volume)