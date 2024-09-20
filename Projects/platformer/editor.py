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
        self.screen = pygame.display.set_mode((1200,800))

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

    def run(self):
        while True:
            self.display.fill((0,0,0))

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

                # button 1 is left click on mouse
                # checks if keys are being pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
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
                    if event.key == pygame.K.s:
                        self.movement[3] = True
                
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
