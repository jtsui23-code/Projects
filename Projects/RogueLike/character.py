import pygame
import math

class Character:
    # Main character class that handles all entity movement, collision detection, and rendering
    # Designed to be flexible enough to handle both player and NPC characters in a top-down game

    def __init__(self, game, eType, pos, size):
        # Initialize a new character with basic properties needed for movement and collision
        # The game parameter allows access to global game state and resources
        self.game = game  # Reference to main game class for accessing shared resources
        self.type = eType  # Character type identifier (e.g., 'player', 'enemy') for behavior differentiation
        self.pos = list(pos)  # Position stored as list for mutable updates during movement
        self.speed = 2  # Base movement speed - kept as separate value for easy balancing
        self.size = size  # Character hitbox dimensions for collision detection
        self.velocity = [0, 0]  # Separate from position for physics-based movement (e.g., knockback)
        
        # Collision flags for each direction - useful for gameplay mechanics and preventing movement
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
    
    def rect(self):
        # Creates a pygame Rect for collision detection
        # Separated into method to ensure rect always matches current position
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def update(self, tilemap, movement=(0, 0)):
        # Handles character movement and collision detection
        # Takes desired movement and adjusts it based on collisions with the environment
        
        # Reset collision flags each frame to ensure accurate collision state
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # Convert movement tuple to list for modification during collision resolution
        frameMovement = list(movement)


        # Normalize diagonal movement to prevent faster diagonal speed
        if frameMovement[0] != 0 and frameMovement[1] != 0:
                # Calculate the magnitude of diagonal movement vector
                # Without this, diagonal movement would be √2 times faster than cardinal movement
                diagonal = math.sqrt(frameMovement[0] **2 + frameMovement[1] **2)
        
                # Normalize the movement vector to maintain consistent speed in all directions
                # This ensures diagonal movement isn't faster than cardinal movement
                frameMovement[0] /= diagonal
                frameMovement[1] /= diagonal

        self.speedUp()

        # Apply character's base speed to movement
        frameMovement[0] *= self.speed
        frameMovement[1] *= self.speed
        
        # Handle horizontal movement and collisions first
        self.pos[0] += frameMovement[0]
        entityRect = self.rect()

        # Check collisions with nearby tiles for optimization
        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):
                # Right collision - Push character left to edge of obstacle
                if frameMovement[0] > 0:
                    entityRect.right = rect.left
                    self.collisions['right'] = True
                
                # Left collision - Push character right to edge of obstacle
                if frameMovement[0] < 0:
                    entityRect.left = rect.right
                    self.collisions['left'] = True
                
                # Update position after collision resolution to prevent clipping
                self.pos[0] = entityRect.x
        
        # Handle vertical movement and collisions second
        # Split from horizontal to handle corner cases correctly
        self.pos[1] += frameMovement[1]
        entityRect = self.rect()

        # Check collisions with nearby tiles again for vertical movement
        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):
                # Bottom collision - Push character up to edge of obstacle
                if frameMovement[1] > 0:
                    entityRect.bottom = rect.top
                    self.collisions['down'] = True
                
                # Top collision - Push character down to edge of obstacle
                if frameMovement[1] < 0:
                    entityRect.top = rect.bottom
                    self.collisions['up'] = True

                # Update position after collision resolution
                self.pos[1] = entityRect.y

        # Reset vertical velocity on collision
        # This prevents velocity from accumulating when colliding with surfaces
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
        
    def render(self, surf, offset=(0,0)):
        # Draws the character sprite at its current position
        # Uses the game's asset system for sprite management
        # self.pos[0] - offset[0] accounts for the 'camera' movmement
        surf.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))
    
    def speedUp(self, speed=1):
        self.speed *= speed
