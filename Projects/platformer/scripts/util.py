import pygame
#gives access to file explore
import os

imagePath = 'data/images/'

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
        self.frame = 0
    
    # copying animations to be used in many instances
    # will conserve memory since self.images is passed by reference
    # so there are not many copies of self.image list/array
    def copy(self):
        return animation(self.images, self.imgDur,self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.imgDur * len(self.images))
        else:
            self.frame = min(self.frame+1, self.imgDur * len(self.images) -1)
            if self.frame >= self.imgDur * len(self.imgDur)-1:
                self.done = True
    
    def img(self):
        # self.frame refers to frame of the game
        return self.images[int(self.frame/self.imgDur)]
    