import sys 
import pygame


class Game:
    def __init__(self):

        pygame.init()

        pygame.display.set_caption("Rogue-Like")

        self.sreen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'player': loadImages('media/Assets/Player/player.png')

        }

        self.player = Characters(self, 'player', (50,50), (8,15))

        self.tilemap = Tilemap(self, tileSize=16)

    def run(self):
        while True:
            self.display.fill((14,219,248))
            self.tilemap.render(self.display)
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.render(self.display)
