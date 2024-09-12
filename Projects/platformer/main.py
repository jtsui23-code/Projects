import sys
import pygame

# initiates pygame
pygame.init()

pygame.display.set_caption("祝福")
# create screen object
screen = pygame.display.set_mode((640,400))

# used for fps
clock = pygame.time.Clock()

while True:
    # pygame.event.get() gets the user's input
    for event in pygame.event.get():
        #checks if the user pressed x button on top right
        if event.type == pygame.QUIT:
            #closes out of pygames
            pygame.quit()
            #closes out of systems
            sys.exit()

    # Updates the screen
    pygame.display.update()
    # forces loop to run at 60 fphs
    clock.tick(60)
