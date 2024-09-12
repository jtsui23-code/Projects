import sys
import pygame
from scripts.beings import physicsBeing
from scripts.util import loadImage

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

        # dictionary for player's stuff
        self.assets = {
            # uses function from util script
            'player': loadImage('entities/player.png')
        }

        self.player = physicsBeing(self, 'player', (300,20), (10, 14))

    def run(self):
        while True:

            self.display.fill((40,120,88))
            # this updates the player's movement on the x axis
            self.player.update((self.movement[1] - self.movement[0],0))

            # updates the screen
            self.player.render(self.display)
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
