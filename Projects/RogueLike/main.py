import pygame
import sys

pygame.init()

screenWidth = 800
screenHeight = 600

screen = pygame.display.set_mode(screenWidth, screenHeight)

pygame.display.set_caption("Rogue-Like")

backgroundColor = (0,0,0)

running = True

while running:
    for event in pygame.event.get():
       if event.type() == pygame.quit():
          running = False
    
    screen.fill(backgroundColor)

    #Updates every single window might want to 
    # change to pygame.display.update() to only update one window
    pygame.display.flip()
