import os

import pygame

BasePath = 'Media/Assets/'

def loadImage(path):
    img = pygame.image.load(BasePath + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def loadImages(path):
    images = []
    for imgName in sorted(os.listdir(BasePath + path)):
        images.append(loadImage(path + '/' + imgName))
    return images