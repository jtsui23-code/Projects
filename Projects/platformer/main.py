import sys
import pygame


class game:

    def __init__(self):
        
        # initiates pygame
        pygame.init()

        pygame.display.set_caption("祝福")
        # create screen object
        self.screen = pygame.display.set_mode((640,400))

        # used for fps
        self.clock = pygame.time.Clock()

        # varible that contains cloud image
        self.img = pygame.image.load('Projects/platformer/data/images/clouds/cloud_2.png')

        self.imgPos = [300,200]

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False]

    def run(self):
        while True:

            # sets the y coordinates of cloud accordinging to the 
            # movement array
            self.imgPos[1] += self.movement[1] - self.movement[0]
            # blit renders/draws the img on the coordinates
            # (0,0) starts on top left like reading english
            self.screen.blit(self.img, self.imgPos)

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
                    # if pressing w key then set movemement[0] to true
                    if event.key == pygame.K_w:
                        self.movement[0] = True
                    if event.key == pygame.K_s:
                    # you set movement[1] to true because if both w & s
                    # are pressed then there is no movement
                        self.movement[1] = True
                
                # if you let go of the key
                if event.type == pygame.KEYUP:
                    # if you let go of the w or s key set movement
                    # stops movement
                    # to false. movement contains a bool that can 
                    # be converted to an int 0 for false 1 for true
                    if event.key == pygame.K_w:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.movement[1] = False

            # Updates the screen
            pygame.display.update()
            # forces loop to run at 60 fphs
            self.clock.tick(60)

# creates game object and uses run method
game().run()
