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

            # Sets the background color based of of RGB (14, 219,248)
            # the color is black is (0,0,0)
            self.display.fill((14, 219, 248))
            
            # Draws the tiles on the window
            self.tilemap.render(self.display, offsett=self.scroll)
            
            # Makes the player move on the window 
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
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