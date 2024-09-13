import sys
import pygame
from scripts.beings import physicsBeing
from scripts.util import loadImage, loadImages
from scripts.tilemap import tilemap

class game:

    def __init__(self):
        
        # initiates pygame
        pygame.init()

        pygame.display.set_caption("祝福")
        # create screen object
        self.screen = pygame.display.set_mode((640,400))

        # used for fps
        self.clock = pygame.time.Clock()

        # makes a small display ontop of the screen 
        self.display = pygame.Surface((320, 200))

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False]

        # dictionary for assets
        self.assets = {
            
            'decor' : loadImages('tiles/decor'),
            'grass' : loadImages('tiles/grass'),
            'large_decor' : loadImages('tiles/large_decor'),
            'stone' : loadImages('tiles/stone'),
            # uses function from util script
            'player': loadImage('entities/player.png')
        }

        self.player = physicsBeing(self, 'player', (100,20), (10, 14))

        self.tilemap = tilemap(self, tilesize=16)

        self.scroll = [0,0]

    def run(self):
        while True:
            
            # if you set scroll to just the player's center
            # then the player will be set to the top left 
            # since the scroll is initially at the top left corner
            # if you only subtract with the width/heigh of display 
            # then the player will be stuck on the right instead
            # (self.player.rect().centerx - self.display.get_width()/2) is 
            # essentially the location where we want the camera to be and 
            # the - self.scroll[0] in
            # (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
            # is where the camera is currently located so by adding the distance of 
            # where how far away we want the camera is to where we want it to be
            # we get a moving camera that is centered at the player's position
            # the /30 at the end makes the camera move faster as the player is farther 
            # away
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1])/30

            self.display.fill((40,120,88))

            self.tilemap.render(self.display,offset=self.scroll)
            # this updates the player's movement on the x axis
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))

            # updates the screen
            self.player.render(self.display, offset=self.scroll)
            # pygame.event.get() gets the user's input
            for event in pygame.event.get():
                #checks if the user pressed x button on top right
                if event.type == pygame.QUIT:
                    #closes out of pygames
                    pygame.quit()
                    #closes out of systems
                    sys.exit()

                # checks if keys are being pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                
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
game().run()
