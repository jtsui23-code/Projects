import pygame

imagePath = 'Projects/platformer/data/images/'

def loadImage(path):
    # .convert() optimizes the image for faster performance
    img = pygame.image.load(imagePath + path).convert()
    img.set_colorkey((0,0,0))
    return img