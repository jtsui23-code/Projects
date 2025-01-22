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

        self.trailLength = 10
        self.attackFlip = False

        # There are two slash images because the slah will be directed.
        self.slashImgRight = self.game.assets['slashRight']
        self.slashImgLeft = self.game.assets['slashLeft']
        
        self.attackAngle = 0

        self.maxHealth = 100
        self.currentHealth = self.maxHealth

        # Adding invulernable variable for powerups and 
        # invulerablity frames after being hit to prevent
        # player from taking too much damage at once.
        self.invulernable = False
        self.invulernableTimer = 0
        self.invulernableDuration = 1000

    def takeDamage(self, amount):
        
        # Player will take damage then gain invulernable frames for a short period.
        if not self.invulernable:
            self.currentHealth = max(0, self.currentHealth - amount)
            self.invulernable = True
            self.invulernableTimer = pygame.time.get_ticks()
            if self.currentHealth <=0:
                print("Player has died")


    def heal(self,amount):
        # This will allow the player to heal until their max health.
        self.currentHealth = min(self.maxHealth, self.currentHealth + amount)

    
    
    def attack(self,offset=(0,0)):

        if self.cooldownCounter <= 0 and not self.attacking:
            self.attacking = True
            self.attackFrame = 0

            # Need mouse posiiton to determine where the slash attack will be directed.
            mousePos = pygame.mouse.get_pos()
            playerRect = self.rect()

            # Account for the scaling of the screen and display in the game.
            # If do not account for the scaling of the scrren and the display, the 
            # slash attack will not occur for upward and leftward slashes.
            scaleFactor = self.game.screen.get_width() / self.game.display.get_width()
            # Need to account for offset because of the moving 'camera'
            playerCenterX = (playerRect.centerx - offset[0]) * scaleFactor
            playerCenterY = (playerRect.centery - offset[1]) * scaleFactor

            # Calculating angle between the player and the mouse.
            dx = mousePos[0] - playerCenterX
            dy = mousePos[1] - playerCenterY

           
            # Arc Tan2 is used because it gives you the angle opposite and adjacent distances between the 
            # player and the mouse position. 
            # The attack angle derived from arc tan will be where the slash attack occurs. 
            self.attackAngle = math.atan2(dy, dx)

            # Determines to flip the slash attack depending on the distance between the player 
            # and the mouse position.
            self.attackFlip = dx < 0
        

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


            # Swing arc is how large of an angle the slash is being swong
            # which is this case it will be 90 degrees in radians since pygame uses radians.
            swingArc = math.pi / 2
            
            # The attack angle is the angle between the player and the mouse position whch is where the 
            # slash attack will start.
            # The reason the attackAngle is subtracted with (swingArc / 2) or 45 degrees is 
            # to have the swing pull back from the player making a full swing animation.
            # In other words, self.attackAngle - (swingArc / 2) offsets the beginning of the slash attack
            # to create a full slash attack while (swingArc * swingProgress) increments the slash attack 
            # based on the attack frames.
            currentAngle = (
                self.attackAngle - (swingArc / 2)  + (swingArc * swingProgress)
            )

            # offsets are for where the hitboxs should be located during the swing attack
            # which changes dynamically.
            offsetX = math.cos(currentAngle) * self.attackRadius
            offsetY = math.sin(currentAngle) * self.attackRadius
            
            # # Need to get the rect of the player for finding the player's center position.
            # playerRect = self.rect()

            # Updates the position of the hitbox of the swing attack based on the 
            # position of the player when doing the slash attack 
            #  + self.size[0]/2 serve to calcuate the center of the player
            # since self.playerStartPos[0] is the top left of the player's x - position.
            self.attackHitbox.centerx = (
                self.pos[0] + self.size[0]/2
            )
            self.attackHitbox.centery = (
                self.pos[1] + self.size[1]/2
            )


            # This a temp slash varaible for appending to the slashTrail based on if the character is flipped.
            currentSlash = self.slashImgLeft if self.attackFlip else self.slashImgRight


            # Stores the current hitbox and slash image into the slashTrail so the collision for the 
            # trail remains after the next slash is rendered. This is needed or the previous 
            # slash images will not detect collision with enemies.
            # Need 'angle' for proper rotation of the slash attack.
            self.slashTrail.append( {'hitbox':self.attackHitbox.copy(),
                                     'slash':currentSlash,
                                     'angle': currentAngle,
                                    # Without slash offset, the slashes will not be rotated in the 
                                    # correct direction.
                                     'slashOffset': (offsetX, offsetY)})

            # This makes the slash trail tapper off if it gets to be too long 
            # making the slash attack shorter the longer the attack lasts.
            if len(self.slashTrail) > self.trailLength:
                self.slashTrail.pop(0)

            # If the attack finishes, stop attacking and go into cooldown.
            if self.attackFrame >= self.attackDuration:
                self.attacking = False
                self.cooldownCounter = self.attackCooldown

                # Rests the slash trail to none or else the slash will remain on the window even after
                # the slash attack is over.
                self.slashTrail.clear()

    
    def update(self, tilemap, movement=(0,0)):

        super().update(tilemap, movement)
        self.updateAttack()

        # Checks if the duration of the invulernable frames are over to 
        # prevent permant invulernability.
        currentTime = pygame.time.get_ticks()
        if self.invulernable:
            if currentTime - self.invulernableTimer > self.invulernableDuration:
                self.invulernable = False

        # Flips player based off of horizontal movement.
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True


    def renderHealthBar(self, surface, offset=(0,0)):
        barPos = (10,10)

        # The order of the rendering matters because it determines what is overlayed ontop.
        # There is a slight offset to the bar position for the health bar red and the 
        # the health bar borders because the borders should be visable not overlayed.
        surface.blit(self.game.assets['healthBarBorder'], barPos)     
        surface.blit(self.game.assets['redHealthBar'], (barPos[0] + 2, barPos[1] + 2))   
        
        # Calculates the width of the health bar based on current health.
        healthBarPercentage = self.currentHealth/ self.maxHealth
        healthBarWidth = int(100 * healthBarPercentage)

        # The green health bar will be rendered as long the health is not zero.
        if healthBarWidth > 0:

            # Creating a subsurface so it can create a shrinking and enlarging effect of the health bar.
            # .subsurface((x-pos, y-pos, width, height))
            greenHealthBar = self.game.assets['greenHealthBar'].subsurface((0,0, healthBarWidth, 10))
            surface.blit(greenHealthBar, (barPos[0] + 2, barPos[1] + 2))

        # Number of health display.
        if pygame.font.get_init():  
            font = pygame.font.Font(None,20)
            healthNum = f"{int(self.currentHealth)}/{self.maxHealth}"
            hpDisplay = font.render(healthNum, True, (255,255,255))
            hpPos = (barPos[0] + 110, barPos[1] + 2)
            surface.blit(hpDisplay, hpPos)

    def render(self, surface, offset=(0,0)):
        # Call the parent (Character) class's render method to draw the player sprite
        super().render(surface, offset)

        # Only render attack-related visuals if we're currently attacking
        if self.attacking:

            for slashPos in self.slashTrail:

                slashImg = slashPos['slash']
                
                # Gets the width and the height of each slash image 
                # needed for positioning their hitboxes properly.
                slashWidth = slashPos['slash'].get_width()
                slashHeight = slashPos['slash'].get_height()

                # Positions slash image based on the center of its hit box which is 
                # why the slash image's width is divided by 2 to get the middle of the image.
                # Without the addition of self.size[0]/2, the position of the slashes would be
                # off since positions in Pygame are at the top left of objects.
                # and the offset is for the 'camera'
                # and current position to prevent inconsistent slash lengths.
                renderX = (
                    self.pos[0] + self.size[0]/ 2 +  slashPos['slashOffset'][0]
                    - offset[0] - slashWidth//2
                )

                renderY = (
                    self.pos[1] + self.size[1]/ 2 +  slashPos['slashOffset'][1]
                    - offset[1] - slashHeight//2
                )

                # Renders the slash image's position based on the rotated angle of the image to the player.
                angle = math.degrees(slashPos['angle'])


                # Need to rotate the image so the slash can face upwards and downwards depending on the mouse position. 
                # Also need to account for a flipped player where the slash will be rotated to the left horizontally. 
                # Have to use negative angle for none flipped player because pygame's rotation is backwards. 
                # Positive angles go clockwise in Pygame while normally in math positive angles go counterclockwise
                if self.attackFlip:
                    rotatedSlash = pygame.transform.rotate(slashImg, angle + 180)
                else:
                    rotatedSlash = pygame.transform.rotate(slashImg, -angle)

                # Adjust the positioning of the slashes based on the rotation or else there 
                # will be inconsistent slash lengths based on different rotated slashes.
                # The // 2 is there to center the position of the rotatedSlash
                rotatedSlashWidth = rotatedSlash.get_width()
                rotatedSlashHeight = rotatedSlash.get_height()
                renderX -= (rotatedSlashWidth - slashWidth) // 2
                renderY -= (rotatedSlashHeight - slashHeight)  // 2

                surface.blit(rotatedSlash, (renderX, renderY))
                
class Enemy(Character):

    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.maxHealth = 50
        self.currentHealth = self.maxHealth

        # Amount of damamge the enemy will do. 
        self.damage = 10
        self.attackCooldown = 60
        self.attackTimer = 0
        self.speed = 1

    def takeDamage(self, amount):

        # Updates the current health according to the damaged taken 
        # until health reaches 0.
        self.currentHealth = max(0, self.currentHealth - amount)

        if self.currentHealth <= 0:
            
            print("Enemy defeated")

            return True
        
        return False

    def update(self, tilemap, player):
        # Calculating distance between enemy and player so 
        # the enemy can pursue the player.
        dx = player.pos[0] - self.pos[0]
        dy = player.pos[1] - self.pos[1]

        distance = math.sqrt(dx * dx + dy * dy)

        movement = [0,0]

        # Have the divide by distance or the 
        # diagonal movement of the enemy will be faster then
        # horizontal and vertical movement.
        movement[0] = dx / distance
        movement[1] = dy / distance


        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0: 
            self.flip = True


        # The enemy attacks the player only when in range
        # to prevent enemy from attack across the map.
        if distance < 30 and self.attackTimer <= 0:
            player.takeDamage(self.damage)
            self.attackTimer = self.attackCooldown

        if self.attackTimer > 0:
            self.attackTimer -= 1

        # Inherits from the character class after defining how the enemy should move
        # because the character update method handles physics not the movement AI of the 
        # enemy.
        super().update(tilemap, movement)

    def render(self, surface, offset=(0,0)):

        enemyImg = self.game.assets['enemy']
        # Flips the enemy sprite if the enemy is moving left.
        if self.flip:
            pygame.transform.flip(self.game.assets['enemy'], True, False)

        surface.blit(enemyImg, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        
           

       