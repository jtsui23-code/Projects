import pygame
import math

"""
Character

Description:
    This class represents a character in a game, providing functionality for movement, 
    collision detection, and rendering. It is designed to be flexible, supporting both 
    player and non-player characters (NPCs) in a top-down game. It interacts with a tilemap 
    for collision resolution and can render its position relative to a camera offset.

Public Methods:
    - __init__(game, eType, pos, size)           Initializes the character with its type, position, size, and other 
                                                 properties needed for movement and collision handling.
    - rect()                                     Returns a pygame.Rect object representing the character's current position 
                                                 and size for collision detection.
    - update(tilemap, movement=(0, 0))          Updates the character's position based on movement and resolves collisions 
                                                 with tiles in the provided tilemap.
    - render(surf, offset=(0, 0))               Renders the character's sprite on a given surface, accounting for camera offset.
    - speedUp(speed=1)                          Increases the character's speed by a multiplier.

Usage:
    - Instantiate the Character class: character = Character(game_instance, 'player', (x, y), (width, height))
    - Update movement and collision: character.update(tilemap_instance, movement=(x_movement, y_movement))
    - Render the character: character.render(surface, offset=(camera_x, camera_y))
    - Adjust speed: character.speedUp(1.5)  # Example multiplier
"""

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

        self.flip = False
    
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


class Player(Character):

    def __init__(self, game, pos, size):
        super().__init__(game,'player', pos, size)

        self.attacking = False

        # Counter for how long an attack is continuing.
        self.attackFrame = 0

        # Ceiling for how long an attack lasts.
        self.attackDuration = 20

        self.attackCooldown = 30
        self.cooldownCounter = 0
        self.attackRadius = 40
        self.attackDmg = 10
        self.attackHitbox = pygame.Rect(0,0, 20, 20)

        self.slashTrail = []

        self.trailLength = 5


        # Debug visualization



        self.debugSurfaces = pygame.Surface((20, 20))
        self.debugSurfaces.fill((255, 0, 0))
        self.debugSurfaces.set_alpha(128)

    
    def attack(self):

        if self.cooldownCounter <= 0 and not self.attacking:
            self.attacking = True
            self.attackFrame = 0

            # Deletes the trails of the slash attack.
            self.slashTrail.clear()

    def updateAttack(self):

        if self.cooldownCounter > 0:
            self.cooldownCounter -= 1

        if self.attacking:
            self.attackFrame += 1

            # This calculates the ratio of progression for the basic attack
            # and is needed for calulating how far the swing has moved.
            swingProgress = self.attackFrame / self.attackDuration

            # Adding -45 to have the swing pull back from the player. 
            # This is in degrees not radians.
            currentAngle = -45 + (90 * swingProgress)

            angleRadian = math.radians(currentAngle)

            # You minus by the angleRadian instead of adding because you 
            # want the swing to start from lower 3rd quadrant. 
            # The sword's swing begins behind the player and arcs forward.
            if self.flip:
                angleRadian = math.pi - angleRadian
            
            # offsets are for where the hitboxs should be located during the swing attack
            # which changes dynamically.
            offsetX = math.cos(angleRadian) * self.attackRadius
            offsetY = math.sin(angleRadian) * self.attackRadius
            
            # Need to get the rect of the player for finding the player's center position.
            playerRect = self.rect()

            # Updates the position of the hitbox of the swing attack.
            self.attackHitbox.centerx = playerRect.centerx + offsetX
            self.attackHitbox.centery = playerRect.centery + offsetY


            # Stores the current hitbox into the slashTrail so the collision for the 
            # trail remains after the next slash is rendered. This is needed or the previous 
            # slash images will not detect collision with enemies.
            self.slashTrail.append(self.attackHitbox.copy())

            # If the attack finishes, stop attacking and go into cooldown.
            if self.attackFrame >= self.attackDuration:
                self.attacking = False
                self.cooldownCounter = self.attackCooldown

    
    def update(self, tilemap, movement=(0,0)):

        super().update(tilemap, movement)
        self.updateAttack()

        # Checks the direction the player is moving to flip the swing attack.
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

    def render(self, surface, offset=(0,0)):
        # Call the parent (Character) class's render method to draw the player sprite
        super().render(surface, offset)

        # Only render attack-related visuals if we're currently attacking
        if self.attacking:
        
            # Draw the red semi-transparent attack hitbox
            # Offset is subtracted to account for camera movement/screen scroll
            surface.blit(self.debugSurfaces,
                         (self.attackHitbox.x - offset[0], 
                          self.attackHitbox.y - offset[1]))
        
        # Get the player's rectangle for positioning calculations
        playerRect = self.rect()
        # Calculate the center point of the player on screen
        # Subtract offset to convert world coordinates to screen coordinates
        centerX = playerRect.centerx - offset[0]
        centerY = playerRect.centery - offset[1]

        # # Draw the debug visualization of the full swing arc
        # # Loop through angles from -45 to +45 degrees in steps of 5
        # for angle in range(-45,46,5):

        #     # Convert the current angle from degrees to radians for math calculations
        #     rad = math.radians(angle)

        #     # If player is facing right, use the angle as is
        #     if not self.flip:

        #         # Calculate point on the arc using trigonometry
        #         # cos(angle) * radius = x position on the circle
        #         # sin(angle) * radius = y position on the circle
        #         x = centerX + math.cos(rad) * self.attackRadius
        #         y = centerY + math.sin(rad) * self.attackRadius

        #     # If player is facing left, mirror the arc
        #     else:

        #         # π - angle mirrors the arc horizontally
        #         rad = math.pi - rad
                
        #         # Calculate mirrored point on the arc
        #         x = centerX + math.cos(rad) * self.attackRadius
        #         y = centerY + math.sin(rad) * self.attackRadius

        # # Draw a small green circle at each point along the arc
        # # Points must be integers for pygame's draw function
        # pygame.draw.circle(surface, (0, 255, 0), (int(x), int(y)), 2)