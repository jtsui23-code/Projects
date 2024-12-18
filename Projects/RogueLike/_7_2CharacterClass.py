import math     # Import for physics/movement
import pygame   # Importing Pygame library


class Character:

    # This sets up a basic character
    def __init__(self, image_path, size, initial_pos, speed):
        # player is an image
        # To load an image need to add directory or location of 
        # image inside of .load( [Directory/location of image] )
        self.sprite = pygame.image.load(image_path)
        
        self.size = list(size)
        # Making sprite smaller
        # .transform.scale() changes how big an image/sprite is
        # To use .transform.scale(), .transform([object want to change size of])
        self.sprite = pygame.transform.scale(self.sprite, (size[0], size[1]))
        
        # (0,0) coordinate is not at the center of the window
        # (0,0) position is at the top left of the window
        # Higher Y - coordinate means lower on the screen
        # Higher X - coordinate means further right on the screen
        # position[0] represents x - axis movement
        # while position[1] represents y - axis movement
        self.position = list(initial_pos)
        self.speed = speed
        
        # This is a list of 4 booleans
        # movement[0] - Left movement
        # movement[1] - Right movement
        # movement[2] - Up movement
        # movement[3] - Down movement
        self.movement = [False, False, False, False]

    # This method is for updating the movement of characters on the screen
    def update_position(self):
        # movement[1] - rightward movement
        # movement[0] - leftward movement
        #
        # If the right key is pressed then movement[1] is equal to 1 and
        # 1 - 0 is 1 making the player move rightward
        # If the left key is pressed then movement[1] remains 0
        # while movement[0] is equal to 1 and 0 - 1 is -1 making the 
        # player move leftward 
        dx = self.movement[1] - self.movement[0]
        
        # movement[3] - Downward movement
        # movement[2] - Upward movement
        # position[1] - vertical movement
        # If the player presses Up arrow then the numbers would be
        # (0 - 1) , which is a negative number
        # A negative number results in an upward movement for the player because 
        # (0,0) origin is at the top left corner of the window meaning to move down the screen
        # the player's y-value must go upward/increase
        # and for the player to move down their y-value must approach 0
        # or decrease
        dy = self.movement[3] - self.movement[2]

        # checks if moving diagonally to slow down the diagonal movement
        if dx != 0 and dy != 0:
            # Ex) If moving diagonal with dx = 1 and dy = 1
            # then the diagonal speed would be 
            # srt(1 * 1 + 1 * 1) = sqrt(2) = 1.41
            # This would mean that the diagonal speed is higher than 
            # horizontal and vertical speed
            diagonal = math.sqrt(dx * dx + dy * dy)
            
            # Using the same example of dx = 1 and dy = 1 
            # To fix the imbalance of diagonal speed
            # divide both dx and dy by diagonal speed
            dx = dx / diagonal
            dy = dy / diagonal

        self.position[0] += dx * self.speed
        self.position[1] += dy * self.speed

    # New 
    ############################################################################################################################################################
    #
    #
    # This slowly recenters the character to winow to create a camera moving effect
    # offset=(0,0) is where the currently the camera is located
    # the =(0,0) are default values in place just incase a offset is not passed into the
    # render method 
    def render(self, surface, offset=(0,0)):

        surface.blit(self.sprite, ( self.position[0] - offset[0], self.position[1] - offset[1] ))
    
    # This method makes a rectangle based off of the size and posiiton of the character
    # which is useful if you want to find the center location of a character
    def rect(self):
        
        # Returns a Pygame rectangle based off of the player's position and width and height
        # To use pygame.Rect([x - position of character], [y - position of character], [width of character], [height of character])
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
    #
    ############################################################################################################################################################


# The Player class inherits from the Character class many of its methods/attributes
class Player(Character):
    def __init__(self):
        super().__init__(
            "media/Assets/Player/player.png",
            [100, 100],  # playerSize
            [50, 100],   # initial position
            5            # speed
        )
    
    # This method handles user input to move the player
    def handle_input(self, event):
        # Checks if any keys have been pressed
        # Making the index in the movement array equal to True indicates movement
        # also boolean statements True and False can be converted to numbers 
        # 1 for True and 0 for False
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                self.movement[0] = True
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.movement[1] = True
            elif event.key in [pygame.K_w, pygame.K_UP]:
                self.movement[2] = True
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                self.movement[3] = True
                
        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_LEFT]:
                self.movement[0] = False
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                self.movement[1] = False
            elif event.key in [pygame.K_w, pygame.K_UP]:
                self.movement[2] = False
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                self.movement[3] = False

    # New 
    ############################################################################################################################################################
    #
    #
    # This slowly recenters the Player to winow to create a camera moving effect
    # offset=(0,0) is where the currently the camera is located
    # the =(0,0) are default values in place just incase a offset is not passed into the
    # render method 
    def render(self, surface, offset=(0,0)):
        # This overrides the render method in the Character Class
        # and passes in the surface and offset values that the Player's render method got to the 
        # Character render method
        super().render(surface, offset)
    
    
    #
    ############################################################################################################################################################
