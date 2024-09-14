import pygame
import random

class clouds:
    def __init__(self, pos, img, speed, dept):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.dept = dept
    def update(self):
        self.pos[0] += self.speed

    # offset is taking consideration of camera
    def render(self, img, offset=(0,0)):
        
        # the depth of the cloud in the sky will 
        # change how much the cloud has to move 
        # to keep up with the camera
        renderPos = (self.pos[0] - offset[0] * self.dept)