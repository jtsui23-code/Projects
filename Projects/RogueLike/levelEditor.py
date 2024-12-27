import sys
import pygame
from utils import loadImages
from tilemap import Tilemap


# This is how much the images are being scaled up by to the window. 
# If the RENDERSCALE is 2.0 then the images on the window are being 
# enlarge by a factor of 2.
# Caution when cauculating the mouse position have to account for this 
# RENDERSCALE as well or the tiles will not be placed where the mouse
# clicks on the level editor.
RENDERSCALE = 2.0
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

        self.leftClicking = False

        self.rightClicking = False

        self.holdShift = False

        self.onGrid = True

       

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


         # Attemps the load a premade map for continuation of level editing without crashing the program.
        try:
            self.tilemap.load()
        except FileNotFoundError:
            pass

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

            # Allows the camera to be moved with the WASD or arrow keys
            # which is important when wanting to create levels that go beyond the base
            # window size.
            # movement[0] - Left movement
            # movement[1] - Right movement
            # movement[2] - Up movement
            # movement[3] - Down movement
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            
            # Displays the tilemap onto the level editor with the camera offset.
            # The camera offset is needed to move the camera posiiton in the level editor. 
            renderScroll = ( int(self.scroll[0]), int(self.scroll[1]) )
            self.tilemap.render(self.display,offset=renderScroll)

            # Retrieves the current tile image from the assets dictionary using the type and variant indices,
            # and creates a copy of it to avoid modifying the original image.
            currentTileImg = self.assets[self.assetTypes[self.indexType]][self.indexVariant].copy()

            # Sets the tile image to be semi - transparent 
            # 0 is fully transparent while 255 is zero transparency 
            currentTileImg.set_alpha(100)
            
            # To correctly get the mouse position have to divide by how much the 
            # images on the window are scaled up so if the images are scaled up by 2 
            # then the mouse position has to be divided by 2 or the mouse position 
            # will have an incorrect offset and be inaccurate.
            mousePos = pygame.mouse.get_pos()
            
            mousePos = (mousePos[0]/ RENDERSCALE, mousePos[1] / RENDERSCALE)

            # Calcuates the tile position on the window of the level editor by 
            # account for the scroll of the camera and converting the mouse position 
            # which is in units in pixals to tile size units.
            # If the conversion is not done then the tiles that are placed are very 
            # small then usual. 
            tilePos = ( int(mousePos[0] + self.scroll[0]) // self.tilemap.tileSize , int(mousePos[1] + self.scroll[1]) // self.tilemap.tileSize)

            if self.onGrid:
                # This makes the semi-transparent choosen tile hover along with the mouse to allow the user to see which tile and 
                # where the tile will be placed in the level editor. 
                # Can't just use mousePos because want the current tile image to be aligned with the grid. 
                # tilePos is already aligned with the grid while the mousePos is not. 
                # Have to reconvert the tilePos back to pixals and account for any camera offset that will
                # make the tile placements off once the camera is moved.
                self.display.blit(currentTileImg, (tilePos[0] * self.tilemap.tileSize - self.scroll[0], tilePos[1] * self.tilemap.tileSize - self.scroll[1]))
            
            else:
                # Displays the current image tile on the offgrid which the mouse position is in. 
                self.display.blit(currentTileImg, mousePos)
            
            # Once the player left clicks then that tile is placed down onto the screen and the tilemap and places on the grid.
            if self.leftClicking and self.onGrid:
                self.tilemap.tilemap[str(tilePos[0]) + ';' + str(tilePos[1])] = {'type': self.assetTypes[self.indexType], 'variant': self.indexVariant, 'pos': tilePos}

            # If the user right clicks and there exists a tile there, 
            # delete that tile off the screen and the tilemap. 
            # This is needed for if the user makes a mistake while using 
            # the level editor.
            if self.rightClicking:
                tileLoc = str(tilePos[0]) + ';' + str(tilePos[1])
                if tileLoc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tileLoc]
                
                # A copy is made of the off grid tiles because the offgrid tile that is touching the right clicked mouse is getting 
                # deleted.
                for tile in self.tilemap.offgridTiles.copy():
                    # Need to get the image of the off grid tiles because 
                    # some of the aseets will be larger then others and this will influence how 
                    # the off grid tile deletion works.
                    tileImg = self.assets[tile['type']][tile['variant']]

                    # Makes the off grid tile image a pygame rectangle for collision detection.
                    tileRect = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tileImg.get_width(), tileImg.get_height())
                    # Checks if the off grid tile is colliding with the mouse. 
                    if tileRect.collidepoint(mousePos):
                        self.tilemap.offgridTiles.remove(tile)

            # Checks for user input
            for event in pygame.event.get():

                # Checks specifically for input on the exit button 
                # On top right of winow
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


                # Checks for mouse left click
                # event.button = 1 is left click
                # event.button = 2 is scroll wheel click
                # event.button = 3 is right click
                # event.button = 4 is scroll up
                # event.button = 5 is scroll up
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftClicking = True
                        # If the on grid is not toggled, then place the tiles off the grid.
                        if not self.onGrid:
                            self.tilemap.offgridTiles.append({'type':self.assetTypes[self.indexType], 'variant': self.indexVariant, 'pos': (mousePos[0] + self.scroll[0], mousePos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.rightClicking = True

                    # If hold down left shift, then scroll through different 
                    # variants of tiles instead.
                    if self.holdShift:
                         # If you scroll up go through different variants of tiles forward.
                        if event.button == 4:
                            # Increment the indexVariant to cycle through the list of variants for the current tile type.
                            # The index wraps around to 0 when it exceeds the number of variants using the modulo operator (%).
                            # - self.assetTypes[self.indexType]: Gets the key of the currently selected tile type (e.g., 'grass', 'stone').
                            # - self.assets[self.assetTypes[self.indexType]]: Retrieves the list of variants for the current tile type.
                            # - len(self.assets[self.assetTypes[self.indexType]]): Gets the total number of variants for the current tile type.
                            self.indexVariant = (self.indexVariant + 1) % len(self.assets[self.assetTypes[self.indexType]])
                        
                         # If you scroll up go through different variants of tiles backwards.
                        if event.button == 5:
                            # Increment the indexVariant to cycle through the list of variants for the current tile type.
                            # The index wraps around to 0 when it exceeds the number of variants using the modulo operator (%).
                            # - self.assetTypes[self.indexType]: Gets the key of the currently selected tile type (e.g., 'grass', 'stone').
                            # - self.assets[self.assetTypes[self.indexType]]: Retrieves the list of variants for the current tile type.
                            # - len(self.assets[self.assetTypes[self.indexType]]): Gets the total number of variants for the current tile type.
                            self.indexVariant = (self.indexVariant - 1) % len(self.assets[self.assetTypes[self.indexType]])

                    else:
                        # If you scroll up go through the list of tile types forward.
                        if event.button == 4:
                            # Increment the indexType to cycle through the list of tile types.
                            # The index wraps around to 0 when it exceeds the number of tile types using the modulo operator (%).
                            # - self.assetTypes: A list containing all the keys from the self.assets dictionary (e.g., ['newGrass', 'grass', 'stone']).
                            # - len(self.assetTypes): Gets the total number of tile types in the assetTypes list.
                            self.indexType = (self.indexType + 1) % len(self.assetTypes)
                            self.indexVariant = 0
                        
                        # If you scroll down go through the list of tile types backwards.
                        if event.button == 5:
                            # Increment the indexType to cycle through the list of tile types.
                            # The index wraps around to 0 when it exceeds the number of tile types using the modulo operator (%).
                            # - self.assetTypes: A list containing all the keys from the self.assets dictionary (e.g., ['newGrass', 'grass', 'stone']).
                            # - len(self.assetTypes): Gets the total number of tile types in the assetTypes list.
                            self.indexType = (self.indexType - 1) % len(self.assetTypes)
                            self.indexVariant = 0


                
                # event.button = 1 is left click
                # event.button = 2 is scroll wheel click
                # event.button = 3 is right click
                # event.button = 4 is scroll up
                # event.button = 5 is scroll up
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftClicking = False
                    if event.button == 3:
                        self.rightClicking = False
                
                # Checks if any keys have been pressed
                # Making the index in the movement
                # array equal to True indicates movement
                # also boolean statements True and False 
                # can be converted to numbers 
                # 1 for True and 0 for False
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_o:
                        self.tilemap.save('map.json')

                    # Pressing g toggles between placing tiles ongrid and off.
                    if event.key == pygame.K_g:
                        self.onGrid = not self.onGrid

                    if event.key == pygame.K_LSHIFT:
                        self.holdShift = True

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
                        self.holdShift = False

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
