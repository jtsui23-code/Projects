import pygame
import math

class Character:

    def __init__(self, game, eType, pos, size):
        self.game = game
        self.type = eType
        self.pos = list(pos)
        self.speed = 5
        self.size = size
        self.velocity = [0, 0]
        
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        frameMovement = list(movement)

        frameMovement[0] * self.speed
        frameMovement[1] * self.speed

        if frameMovement[0] != 0 and frameMovement[1] != 0:

                # Ex) If player is moving diagonal with frameMovement[0] = 1 and frameMovement[1] = 1
                # then the diagonal speed would be 
                # srt(1 * 1 + 1 * 1) = sqrt(2) = 1.41
                # This would mean that the player's diagonal speed is higher than 
                # their horizontal and vertical speed

                diagonal = math.sqrt(frameMovement[0] * frameMovement[0] + frameMovement[1] * frameMovement[1])
        
                # Using the same example of frameMovement[0] = 1 and frameMovement[1] = 1 
                # To fix the imbalance of diagonal speed
                # divide both frameMovement[0] and frameMovement[1] by diagonal speed
                # so the new calculation would be 
                # sqrt(1/sqr(2) * 1/sqr(2) + 1/sqr(2) * 1/sqr(2))
                # which simpilfies to 
                # sqrt( 1/2 + 1/2) = 1 
                # fixing the issue with the imbalance speed
                frameMovement[0] = frameMovement[0] / diagonal
                frameMovement[1] = frameMovement[1] / diagonal
        
        self.pos[0] += frameMovement[0]
        entityRect = self.rect()

        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):

                # If the character is moving from the right 
                # Then the character must collide with the left 
                # side of the object with the right side of the character
                if frameMovement[0] > 0:
                    entityRect.right = rect.left
                    self.collisions['right'] = True
                
                # If the character is moving from the left 
                # Then the character must collide with the right 
                # side of the object the left side of the character
                if frameMovement[0] < 0:
                    entityRect.left = rect.right
                    self.collisions['left'] = True
                
                # Updates the position of the character based on the position of 
                # the Rectangle
                self.pos[0] = entityRect.x
        

        self.pos[1] += frameMovement[1]
        entityRect = self.rect()

        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):

                # If the character is moving downwards
                # Then the character must collide with the top 
                # part of the object with the bottom side of the character
                if frameMovement[1] > 0:
                    entityRect.bottom = rect.top
                    self.collisions['down'] = True
                
                # If the character is moving upwards
                # Then the character must collide with the top 
                # part of the object with the bottom side of the character
                if frameMovement[1] < 0:
                    entityRect.top = rect.bottom
                    self.collisions['up'] = True

                # Updates the position of the character based on the position of 
                # the Rectangle
                self.pos[1] = entityRect.y

             

        
        # Gravity need to delete later
        # self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        

    def render(self, surf):
        surf.blit(self.game.assets['player'], self.pos)
        