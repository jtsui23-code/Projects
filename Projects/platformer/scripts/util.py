import pygame
#gives access to file explore
import os

imagePath = 'Projects/platformer/data/images/'

def loadImage(path):
    # .convert() optimizes the image for faster performance
    img = pygame.image.load(imagePath + path).convert()
    img.set_colorkey((0,0,0))
    return img

def loadImages(path):
    images = []

    # goes through all of the files based on the directory passed
    # into the function
    for imgName in os.listdir(imagePath + path):
        #addes each image to images list
        images.append(loadImage(path + '/' +imgName))

    return images

class animation():
    def __init__(self, images, imgDur=5, loop=True):
        self.images = images
        self.imgDur = imgDur
        self.loop = loop

        # checks if animation is finished
        self.done = False