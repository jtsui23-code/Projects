import pygame

class physicsBeing:
    def __init__(self, game, btype, pos, size):
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
        self.collision = {'up': False, 'down': False, 'right':False, 'left': False}

    def rect(self):
        #self.pos[0] and self.pos[1] are the top left of the rectangle
        # not the center of the rectangle
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap,movement=(0,0)):
        self.collision ={'up': False, 'down': False, 'right':False, 'left':False}
        framerMovement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        # movement for x
        self.pos[0] += framerMovement[0]

        #creates rect object
        beingRect = self.rect()

        # if the rect object is colliding with a physicsTile
        # register collision
        # check the direction of the collision to do the correct
        # collision direction
        for rect in tilemap.physicsRectAround(self.pos):
            if beingRect.colliderect(rect):
                if framerMovement[0] >0:    # if collision coming from right
                    beingRect.right = rect.left
                    self.collision['right'] = True
                if framerMovement[0] < 0:
                    beingRect.left = rect.right #if collision coming from leftside
                    self.collision['left'] = True
                #sets postion of rect
                # using pos[0] because Rect()
                # only works with int
                self.pos[0] = beingRect.x

        #movement for y
        self.pos[1] += framerMovement[1]
        beingRect = self.rect()
        for rect in tilemap.physicsRectAround(self.pos):
            if beingRect.colliderect(rect):
                if framerMovement[1] > 0:
                    beingRect.bottom = rect.top
                    self.collision['down'] = True
                if framerMovement[1] <0:
                    beingRect.top = rect.bottom
                    self.collision['top'] = True
                self.pos[1] = beingRect.y

        # This creates gravity, the max value for velocity will be 5
        self.velocity[1] = min(5, self.velocity[1] + 0.1) 

        # rests the velocity of falling when touch ground or platform
        if self.collision['down'] or self.collision['up']:
            self.velocity[1] = 0
    
    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        