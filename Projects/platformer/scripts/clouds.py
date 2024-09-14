import pygame
import random

class cloud:
    def __init__(self, pos, img, speed, dept):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.dept = dept
    def update(self):
        self.pos[0] += self.speed

    # offset is taking consideration of camera
    # surf short for surfance
    def render(self, surf, offset=(0,0)):
        
        # the depth of the cloud in the sky will 
        # change how much the cloud has to move 
        # to keep up with the camera
        renderPos = (self.pos[0] - offset[0] * self.dept, self.pos[1] - offset[1] * self.dept)
        surf.blit(self.img,(renderPos[0] % (surf.get_width + self.img.get_width) - self.img.get_width, renderPos[1] % (surf.get_height + self.img.get_height) - self.img.get_height))

class cloudz:
    def __init__(self, cloudImg, count=16):
        self.clouds = []

        # this will make 16 clouds at random positions,
        # , images, speed, and dept
        for i in range(count):          #pos
            self.clouds.append(cloud((random.random()* 99999, random.random() * 99999), random.choice(cloudImg), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))
        
        # this sorts the list of clouds by depth
        # lambda is temp function
        # for every cloud x in the list 
        # sort by the depth
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()
    def render(self, surf, offset=(0,0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)