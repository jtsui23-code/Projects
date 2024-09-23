import sys
import pygame
from scripts.util import loadImages
from scripts.tilemap import tilemap

RENDERSCALE = 2.0

class editor:

    def __init__(self):
        
        # initiates pygame
        pygame.init()

        pygame.display.set_caption("editor")
        # create screen object
        self.screen = pygame.display.set_mode((640,480))

        # used for fps
        self.clock = pygame.time.Clock()

        # makes a small display ontop of the screen 
        self.display = pygame.Surface((320, 200))

        # up is bound to [0] down is bound to [1] 

        # dictionary for assets
        self.assets = {
            
            'decor' : loadImages('tiles/decor'),
            'grass' : loadImages('tiles/grass'),
            'large_decor' : loadImages('tiles/large_decor'),
            'stone' : loadImages('tiles/stone'),
            
        }
        # movement for camera
        self.movement = [False, False, False, False]

        self.tilemap = tilemap(self, tilesize=16)

        self.scroll = [0,0]

        # creates a selection of tiles to choose from for 
        # lvl editor
        self.tileList = list(self.assets)
        self.tileGroup = 0
        self.tileVar = 0

        self.leftClick = False
        self.rightClick = False

        self.shift = False

    def run(self):
        while True:
            self.display.fill((0,0,0))

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=renderScroll)

            # self.tileList is an array that stores all of 
            # the keys inside of self.assets. 
            # self.tileGroup stores the indexes of each key
            # so the value self.tileGroup = 1 would be
            # 'grass'
            # so by doing self.assets[self.tileList[self.tileGroup]]
            # you are picking which tile type you want from the dictionary
            # assets then you add [self.tileVar] to specify which variant 
            # of the tile you want like a different grass tile
            currentTileImg = self.assets[self.tileList[self.tileGroup]][self.tileVar].copy()

            # this makes the currently selected tile transparent
            # 0 is completely transparent
            # 255 is zero transparency
            currentTileImg.set_alpha(100)

            # stores position of mouse 
            # using pygame cordinates
            mousePos = pygame.mouse.get_pos()

            # current position/pixel is scaled up so would
            # give wrong cordinates so have to convert back normal pixels
            mousePos = (mousePos[0] / RENDERSCALE, 
                        mousePos[1] / RENDERSCALE)

            

            # mousePos[] is added with self.scroll[] because 
            # depending on the scroll will change tile/asset 
            # so the mouse position will be offseted a little bit
            # then the sum of the mouse position and scroll
            # is divided by self.tilemap.tileSize to convert
            # the readjusted pixels cordinates to 
            # the tile unit 
            tilePos = (int((mousePos[0] + self.scroll[0]) // self.tilemap.tileSize), 
                       int((mousePos[1] + self.scroll[1]) // self.tilemap.tileSize))

            if self.leftClick:

                # self.tilemap.tilemap[] is the index of the array/list
                # that of the tilemaps
                # then the stuff behind the equal sign are the elements in 
                # the specific index of the array
                # this allows to place down tiles on the screen
                self.tilemap.tilemap[str(tilePos[0]) + ';' + str(tilePos[1])] = {'type': self.tileList[self.tileGroup], 'variant': self.tileVar, 'pos':tilePos}



            # .blit([what you want to render], [where you want to render])
            self.display.blit(currentTileImg, (5,5))

            
            # pygame.event.get() gets the user's input
            for event in pygame.event.get():
                #checks if the user pressed x button on top right
                if event.type == pygame.QUIT:
                    #closes out of pygames
                    pygame.quit()
                    #closes out of systems
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftClick = False
                    if event.button == 3: 
                        self.rightClick = False

                # button 1 is left click on mouse
                # button 2 is mouse wheel
                # button 3 is right click
                # button 4 is scroll up 
                # button 5 is scroll down
                # checks if keys are being pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.leftClick = True
                    if event.button == 3:
                    # button 4 is scroll up
                    # self.tileGroup -1 goes up the list of tiles
                        self.rightClick = True
                    
                    if self.shift:
                        # button 5 is scroll down
                        # self.tileGroup + 1 goes down the list of tiles
                        if event.button == 5:
                            # self.assets[self.tileList[self.tileGroup]]
                            # gives you the specific tile variant 
                            # self.tileList holds all of the keys for each of the tile
                            # variant while self.tileGroup holds the index of the variant
                            # so by doing self.assets[self.tileList[self.tileGroup]]
                            # you are choosing a specific tile variant
                            # and doing the len() of that gives the size of the dictionary
                            # containing the tile variants allowing you to 
                            # loop through all of the tile variants using modulo
                            self.tileVar = (self.tileGroup +1) % len(self.assets[self.tileList[self.tileGroup]])
                        if event.button == 4:
                            self.tileVar = (self.tileGroup -1) % len(self.assets[self.tileList[self.tileGroup]])
                    else:
                        if event.button == 5:
                            self.tileGroup = (self.tileGroup + 1) % len(self.tileList)
                            # ensures looking at the defualt variant of tile
                            self.tileVar = 0
                        if event.button == 4:
                            self.tileGroup = (self.tileGroup - 1) % len(self.tileList)
                            self.tileVar = 0
                
                    
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                
                # if you let go of the key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            # rendering the display(small sreen) at 0,0
            # rescales the screen so like zooms in so player is not tiny
            # pygame.transform.scale([thing want to scale], [how much 
            # want to scale])
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            # Updates the screen
            pygame.display.update()
            # forces loop to run at 60 fphs
            self.clock.tick(60)


# creates game object and uses run method
editor().run()
