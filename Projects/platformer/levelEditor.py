import sys
import pygame
from scripts.util import loadImages
from scripts.tilemap import tilemap

RENDERSCALE = 2.0

class editor:

    def __init__(self):
        
        # initiates pygame
        pygame.init()

        pygame.display.set_caption("Editor")
        # create screen object
        self.screen = pygame.display.set_mode((640,480))

        # used for fps
        self.clock = pygame.time.Clock()

        # makes a small display ontop of the screen 
        self.display = pygame.Surface((320, 240))


        # dictionary for assets
        self.assets = {
            
            'decor' : loadImages('tiles/decor'),
            'grass' : loadImages('tiles/grass'),
            'large_decor' : loadImages('tiles/large_decor'),
            'stone' : loadImages('tiles/stone'),
           
        }

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False, False, False]

        self.tilemap = tilemap(self, tilesize=16)

        # this creates a list of the keys inside the 
        # assets map to each tile/asset
        self.tileList = list(self.assets)

        # self.tileGroup will serve as a variable 
        # of the index for self.tileList
        # so if self.tileGroup is 1 then the tile that 
        # is being selected is 'grass'
        self.tileGroup = 0
        self.tileVar = 0

        self.scroll = [0,0]

        self.leftClick = False
        self.rightClick = False
        self.shift = False

    def run(self):
        while True:
            self.display.fill((0,0,0))

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=renderScroll)

            # the self.tileList has all of the keys to self.assets map
            # so doing self.tileList[self.tileGroup] specifies which 
            # tile is being selected in self.assets 
            # then the additional [self.tileVar] dictates which 
            # version/variant of the tile is being selected
            # the reason for the .copy() is efficiency when rendering
            # no reason to not have the .copy() at the end
            currentTileImg = self.assets[self.tileList[self.tileGroup]][self.tileVar].copy()

            # alpha is transparacy of image that is being drag and 
            # selected on the editor screen
            # the number passed inside of .set_alpha dictates how
            # transparent the image will be 
            # 0 is fully transparent 255 is NOT transparent at all
            currentTileImg.set_alpha(100)

            # gets pixal coordinates of mouse 
            mousePos = pygame.mouse.get_pos()
            mousePos = (mousePos[0] / RENDERSCALE, mousePos[1] / RENDERSCALE)

            tilePos = (int((mousePos[0] + self.scroll[0]) / self.tilemap.tileSize), (int((mousePos[1]) / self.tilemap.tileSize)))

            # dispay the tile before actually placing it down.
            self.display.blit(currentTileImg, (tilePos[0] * self.tilemap.tileSize - self.scroll[0], tilePos[1] * self.tilemap.tileSize - self.scroll[1]))
            
            if self.leftClick:
                self.tilemap.tilemap[str(tilePos[0]) + ';' + str(tilePos[1])] = {
                    'type': self.tileList[self.tileGroup], 'variant': self.tileVar, 'pos': tilePos
                }
            if self.rightClick:
                # creating a variable to store the tile position
                tileLoc = str(tilePos[0]) + ';' + str(tilePos[1])

                # if there is a tile at the tile position,
                # delete it when right clicking on mouse.
                if tileLoc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tileLoc]

            self.display.blit(currentTileImg, (5,5))

            # pygame.event.get() gets the user's input
            for event in pygame.event.get():
                #checks if the user pressed x button on top right
                if event.type == pygame.QUIT:
                    #closes out of pygames
                    pygame.quit()
                    #closes out of systems
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # button 1 is left click on mouse
                    # button 2 is pressing scroll wheel
                    # button 3 is right click
                    # button 4 is scroll up 
                    # button 5 is scroll down
                    if event.button == 1:
                        self.leftClick = True
                    if event.button == 3:
                        self.rightClick = True
                    
                    if self.shift:
                        if event.button == 4:
                            # if left shift is being held then scroll through the 
                            # variants of the tiles instead 
                            # self.assets[self.tileList[self.tileGroup]] gets to 
                            # the list of variants 
                            self.tileVar = (self.tileVar - 1) % len(self.assets[self.tileList[self.tileGroup]])
                        if event.button == 5:
                            self.tileVar = (self.tileVar + 1) % len(self.assets[self.tileList[self.tileGroup]])
                    else:
                        if event.button == 4:
                            # self.tileGroup - 1 goes to backwards in the list
                            # since Python allows for -1 to represent back of list
                            # % len(self.tileList) makes sure that this operation 
                            # loops within the index of the self.tileList
                            self.tileGroup = (self.tileGroup - 1) % len(self.tileList)
                            self.tileVar = 0
                        if event.button == 5:
                            # moves the through the index forward when scrolling down
                            self.tileGroup = (self.tileGroup + 1) % len(self.tileList)
                            self.tileVar = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.leftClick = False
                    if event.button == 3: 
                        self.rightClick = False
                

                # checks if keys are being pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_UP:
                        self.movement[2] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                
                # if you let go of the key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_UP:
                        self.movement[2] = False
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
