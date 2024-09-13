import pygame

class physicsBeing:
    def __init__(self,game, btype, pos, size):
        self.game = game
        self.type = btype
        # if you don't specify list type 
        # then self.pos will be a point to a list of coordinates
        # if many beings are at the same coordinate then self.pos
        # would chnage all of them at once like a copy construct when
        # dealing with pointers
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]


    def update(self, movement=(0,0)):
        framerMovement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # movement for x
        self.pos[0] += framerMovement[0]
        #movement for y
        self.pos[1] += framerMovement[1]

        # This creates gravity, the max value for velocity will be 5
        self.velocity[1] = min(5, self.velocity[1] + 0.1) 
    
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        