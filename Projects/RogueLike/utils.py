import os
import pygame

# Store the base asset path as a constant to avoid repetition and make path updates easier
# This also makes the code more maintainable as you only need to change the path in one place
BasePath = 'Media/Assets/'

def loadImage(path):
    # Load a single image and prepare it for game use
    # Convert the image for faster rendering - critical for performance in pygame
    img = pygame.image.load(BasePath + path).convert()
    
    # Set black as the transparent color (0,0,0)
    # This ensures sprites with black backgrounds display correctly in the game
    img.set_colorkey((0, 0, 0))
    return img

def loadImages(path):
    # Load multiple images from a directory into a list
    # Useful for animations or sprite collections that need to be loaded together
    images = []
    
    # os.listdir returns files in arbitrary order, so we sort them
    # This ensures animations or sprite sequences load in the correct order
    # particularly important for numbered sprite sequences (e.g., walk1.png, walk2.png)
    for imgName in sorted(os.listdir(BasePath + path)):
        # Construct the full path and load each image
        # The '/' joining is used to maintain proper path format across different operating systems
        images.append(loadImage(path + '/' + imgName))
    return images