import sys
import pygame
from utils import loadImage, loadImages
from character import Character
from tilemap import Tilemap

"""
Game

Description:
    This class represents the main game loop for a rogue-like game implemented 
    using Pygame. It initializes the game window, assets, player, tilemap, and 
    handles input, rendering, and game logic. The class also defines the player's 
    movement and updates the display at a set frame rate.

Public Methods:
    - __init__()              Initializes the game, loads assets, and sets up the player and tilemap.
    - run()                   Starts the game loop, handles user input, updates the player, 
                              renders the game environment, and manages the frame rate.

Private Methods:
    None (all methods are public due to Python conventions).

Usage:
    - Instantiate the class: Game()
    - Call the run() method: Game().run() to start the game.
"""

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

        # Acts as the 'Camera' position
        self.scroll = [0,0]

        self.clock = pygame.time.Clock()

        # This is a list of 4 booleans
        # movement[0] - Left movement
        # movement[1] - Right movement
        # movement[2] - Up movement
        # movement[3] - Down movement
        self.movement = [False, False, False, False]
        
        # Dictionary for loading assets in the game makes it more organized and 
        # accessable for the Tilemap class
        self.assets = {
            'background':pygame.transform.scale(loadImage('background.png'), (1240,840)),
            'newGrass':loadImages('tiles/newGrass'),
            'grass': loadImages('tiles/grass'),
            'stone': loadImages('tiles/stone'),
            'player': pygame.transform.scale(loadImage('Player/edelgard.png'), (16, 20))  # Adjust the size to match the tiles
        }

        # Creating a player
        # Pass in a game, name, position and size
        self.player = Character(self, 'player', (50, 50), (10, 17))
        
        # Creating a tilemap object with the specified tile size
        self.tilemap = Tilemap(self, tileSize=16)
        
    def run(self):
        while True:

            # Sets the background to an image at the position (0,0)
            self.display.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # Draws the tiles on the window
            self.tilemap.render(self.display, offset=renderScroll)
            
            # Makes the player move on the window 
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.player.render(self.display, renderScroll)
            
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

                    if event.key ==pygame.K_LSHIFT:
                        self.player.speedUp(1.5)

                    # If the A key or left arrow key has been pressed
                    # Change the movement array accordingly
                    if event.key == pygame.K_a:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = True

                    if event.key == pygame.K_LEFT:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = True

                    if event.key == pygame.K_d:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = True

                    if event.key == pygame.K_RIGHT:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = True

                    # Adding key input for upward movement of player
                    # movement[3] - Upward movement
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    
                    if event.key == pygame.K_UP:
                        self.movement[2] = True

                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True


                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LSHIFT:
                        self.player.speedUp(1)
                    # If the A key or left arrow key has been pressed
                    # Change the movement array accordingly
                    if event.key == pygame.K_a:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = False 

                    if event.key == pygame.K_LEFT:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = False

                    if event.key == pygame.K_d:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = False
                        
                    if event.key == pygame.K_RIGHT:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False
            
                    if event.key == pygame.K_UP:
                        self.movement[2] = False

                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
            
            
            # .blit() draws whatever object on the window
            # in this case screen is the main game window
            # .blit( [Object want to draw on window], (x - position of object on window, y - position of object on window) ) 
            # pygame.transform.scale() makes the screen zoom closer to the player
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))


            pygame.display.update()
            self.clock.tick(60)

Game().run()