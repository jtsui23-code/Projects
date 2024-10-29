import math
import pygame

class Spark:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
    
    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 1)
        return not self.speed

    def render(self, surf, offset=(0,0)):
        renderPoints = [
            # this is the spark effect for infront of the sprite
            (self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1]),
            # this is the spark effect up 90 degrees
            (self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0], self.pos[1] + math.sin(self.angle + math.pi * 0.5) * 0.5 - offset[1]),
            # this is the spark effect 180 degrees 
            (self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0], self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1]),
            # this is the spark effect at 270 degrees
            (self.pos[0] + math.cos(self.angle + math.pi * 3/2) * self.speed * 0.5 -offset[0], self.pos[1] * math.sin(self.angle + math.pi * 3/2) * self.speed * 0.5 - offset[1])
        ]
        pygame.draw.polygon(surf, (255, 255, 255), renderPoints)