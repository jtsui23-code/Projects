import random
import pygame
import math
from scripts.particle import Particle

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

        self.action = ''
        # there needs to be a player offset because 
        # when the player is rendered into the world
        # the player's outline is cut off
        self.animOffset = (-3,-3)
        # lets player look left or right
        self.flip = False
        self.setAction('idle')
        self.lastMovement = [0,0]
        
    def setAction(self,action):
        #checks if the current action is up to date
        if action != self.action:
            self.action = action
            # this holds the frame/image of the character that is being 
            # animated. self.type refers to which character sprite that 
            # is being animated the '/' is for directory with 
            # self.action which is a string that will specifty which 
            # image/animation to choose 
            # .copy() makes sure each entity has their own animation
            # and are not just sharing the same frame
            self.animation = self.game.assets[self.type + '/' + self.action].copy()
            
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

        # if the entity is moving right don't flip the sprit
        if movement[0] > 0:
            self.flip = False
        # if the entity is moving left flip the sprit
        if movement[0] < 0:
            self.flip = True

        self.lastMovement = movement

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

        if self.collision['down']:
            self.jumps = 2

        self.animation.update()
    
    def render(self, surf, offset=(0,0)):
        # pygame.transform.flip([thing want to flip], flip on x, flip on y)
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.animOffset[0], self.pos[1] - offset[1] + self.animOffset[1]))
        
        # original render 
        # pygame.transform.flip(self.animation.img, self.flip, False)
        # replaced self.game.assets['player'] because this is
        # more versatile for every entity not just player
        # pygame.transform.flip() checks if entity needs to be flip
        # then does all of the positioning
        # there is an addional + self.animOffset[] now because the
        # player sprits are cut off when rendered into the world
        #surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))

class player(physicsBeing):
    def __init__(self, game, pos, size):
        # does init for physicsBeing class
        super().__init__(game, 'player', pos, size)
        # self.airTime = 0

        self.jumps = 2
        self.dashing = 0

    def update(self, tilemap, movement=(0,0)):
        # uses movement method from physicsBeing 
        # but uses the values specific to the player
        super().update(tilemap, movement=movement)

        self.wallSlide = False
        # If player is touching the wall from the right or left and in the 
        # air then go into the wall jump animation
        if (self.collision['right'] or self.collision['left']) and (self.velocity[1] > 0):
            self.wallSlide = True
            # caps the vertical velocity at 0.5
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collision['right']:
                self.flip = False
            else: 
                self.flip = True
            self.setAction('wallSlide')
        
        # generates 20 bursts of particles for the first 
        # 10 frames of the dash
        if (self.dashing) in {60, 50}:
            for i in range(20):
                # generates a random angle from 0 to 2pi
                angle = random.random() * math.pi * 2
                speed = random.random() * 0.5 + 0.5
                # generates random random particle velocity 
                # based of random angles & speed of (cos, sin)
                particleVelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=particleVelocity, frame=random.randint(0,7)))
                
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing +1)
        # for the first 10 frames of the dashing
        # change the velocity by a magnitube of 8
        # since abs(self.dashing)/ self.dashing 
        # will just be 1 or -1 then 
        # that product is * by 8 so the x - axis 
        # velocity is initialize to the + or - 8
        # of the first 10 frames
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing)/ self.dashing * 8
            # slows down the velocity of the dash 
            # at the end of the 10 frames of the dash
            # the rest of the 50 for the self.dashing 
            # works as a cooldown of 50 frames for the dashing
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

            # this makes the x - axis particle velocity be from 
            # [-3, 3] and the y-axis particle velocity zero
            particleVelocity = [abs(self.dashing)/self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=particleVelocity, frame=random.randint(0,7)))
        
        if not self.wallSlide:
            # # checks if the player is on the ground
            # if self.collision['down']:
            #     self.airTime = 0

            # if the player is moving/jumping then 
            # toggle jumping animation
            if self.velocity[1] < 0:
                self.setAction('jump')
                # self.airTime += 1

            # if the player is not standing still
            # horizontally, then toggle running animation
            elif movement[0] != 0:
                self.setAction('run')

            # if not jumping or running then make player 
            # do the idle animatino
            else:
                self.setAction('idle')
        # slows down the x - axis velocity depending
        # on which direction the player is moving right or left
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)
    
    # this overrides the render method in the parent class 
    # physicBeings with the player child class's render method
    # after the first 10 frames of the dash call the render
    # method of the parent class and pass in the 
    # parameters from the player's render method 
    def render(self, surf, offset=(0,0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset)

    def jump(self):
        if self.wallSlide:
            # if the player is moving from
            # the right then walljump to then wall jump to
            # the left 
            if self.flip and self.lastMovement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                # decrements number of jumps by 1
                # lets player jump even if used all of jumps
                self.jumps = max(0, self.jumps - 1)
                return True
            # if the player is wall jumping from the right then 
            # wall jump to the left 
            elif not self.flip and self.lastMovement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps > 0:
            self.velocity[1] = -3
            self.jumps -= 1
            return True
    def dash(self):
        if not self.dashing:
            # if the player is facing left 
            # make dashing -60
            # |60| is how long dash will last for 
            if self.flip:
                self.dashing = -60
            else:
            # if player is facing right then 
            # make dash 60
                self.dashing = 60