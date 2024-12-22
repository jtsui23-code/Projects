import sys
import pygame
from utils import loadImages
from tilemap import Tilemap

class LevelEditor:

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

        self.clicking = False

        self.clock = pygame.time.Clock()


        # For Camera Movement
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
        }

        
        # Creating a tilemap object with the specified tile size
        self.tilemap = Tilemap(self, tileSize=16)

        # This is an array of the keys in the self.assets dictionary
        # so the list would contain ['newGrass', 'grass', 'stone']
        self.assetTypes = list(self.assets)

        # This variable will be used for indexing the 
        # keys in the self.assets or the 
        # elements in the self.assetsType list.
        self.indexType = 0

        # While this variable will be used to index through the paired 
        # item in self.assets or the variant of the tiles in the 
        # self.assetTypes
        self.indexVariant = 0
        
    def run(self):
        while True:
            
            # Sets the background to an image at the position (0,0)
            self.display.fill((0,0,0))

            # Retrieves the current tile image from the assets dictionary using the type and variant indices,
            # and creates a copy of it to avoid modifying the original image.
            currentTileImg = self.assets[self.assetTypes[self.indexType]][self.indexVariant].copy()

            # Sets the tile image to be semi - transparent 
            # 0 is fully transparent while 255 is zero transparency 
            currentTileImg.set_alpha(100)

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

                    # Checks for mouse left click
                    # event.button = 1 is left click
                    # event.button = 3 is right click
                    # event.button = 2 is scroll
                    if event.key == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.clicking = True

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

LevelEditor().run()