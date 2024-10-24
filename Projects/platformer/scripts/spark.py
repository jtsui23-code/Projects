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
            (self.pos[0] + math.cos(self.angle * self.speed))
        ]
        pygame.draw.polygon(surf, (255, 255, 255), renderPoints)