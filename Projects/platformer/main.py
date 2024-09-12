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

        # for the image it will look for the color (0,0,0) or black
        # and make it transparent so the image will match the background
        self.img.set_colorkey((0,0,0))

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False, False, False]

    def run(self):
        while True:

            self.screen.fill((40,120,88))

            # sets the x and y coordinates of cloud accordinging to the 
            # movement array. Treats bool as int false is 0
            # true is 1

            # self.movement[1] or pressing s goes first because
            # if you want to move down you have to add to y - coordinates
            # since (0,0) starts on the top left of the screen
            self.imgPos[1] += (self.movement[1] - self.movement[0])* 10

            self.imgPos[0] += (self.movement[3] - self.movement[2])* 10
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
                    if event.key == pygame.K_w:
                        self.movement[0] = False
                    if event.key == pygame.K_s:
                        self.movement[1] = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[2] = True
                    if event.key == pygame.K_d:
                        self.movement[3] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[2] = False
                    if event.key == pygame.K_d:
                        self.movement[3] = False

            # Updates the screen
            pygame.display.update()
            # forces loop to run at 60 fphs
            self.clock.tick(60)


# creates game object and uses run method
game().run()
