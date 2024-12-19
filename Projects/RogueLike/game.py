import sys

import pygame

from utils import loadImage, loadImages
from character import Character
from tilemap import Tilemap

class Game:

    # Sets up the game windows, framerate, player, and other assets
    def __init__(self):

        # Starts up Pygame
        pygame.init()

        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption('Rogue-Like')

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) )
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {
            
            'player': loadImage('Player/player.png')
        }
        
        self.player = Character(self, 'player', (50, 50), (8, 15))
        
        self.tilemap = Tilemap(self, tile_size=16)
        
    def run(self):
        while True:

            # Sets the background color based of of RGB (14, 219,248)
            # the color is black is (0,0,0)
            self.display.fill((14, 219, 248))
            
            self.tilemap.render(self.display)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)
            
            # Checks for user input
            for event in pygame.event.get():

                # Checks specifically for input on the exit button 
                # On top right of winow
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Checks if any keys have been pressed
                # Making the index in the movement
                # array equal to True indicates movement
                # also boolean statements True and False 
                # can be converted to numbers 
                # 1 for True and 0 for False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            
            # .blit() draws whatever object on the window
            # in this case screen is the main game window
            # .blit( [Object want to draw on window], (x - position of object on window, y - position of object on window) ) 
            # pygame.transform.scale() makes the screen zoom closer to the player
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))


            pygame.display.update()
            self.clock.tick(60)

Game().run()