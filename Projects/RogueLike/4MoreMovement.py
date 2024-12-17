import pygame   # Importing Pygame library
import sys      # Importing sys library to properly close the game

# Starts up Pygame
pygame.init()

# Setting the game window's dimensions
screenWidth = 800
screenHeight = 600

# Creating a screen variable with the window dimension variables set above
# when setting window dimensions have to do .set_mode( (_,_) )

# Treat the (_,_) as order pairs inside of ( (_,_) )
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Sets the name of the window icon to "Rogue-like"
pygame.display.set_caption("Rogue-Like")

# Sets the background color based of of RGB (255,255,255)
# the color is black is (0,0,0)
backgroundColor = (0,0,0)

running = True



# player is an image
# To load an image need to add directory or location of 
# image inside of .load( [Directory/location of image] )
player = pygame.image.load("media/Assets/Player/player.png")


# Making player sprite smaller
playerSize = [100,100]

# .transform.scale() changes how big an image/sprite is
# To use .transform.scale(),    .transform([object want to change size of])
player = pygame.transform.scale(player, (playerSize[0], playerSize[1]))

# (0,0) coordinate is not at the center of the window
# (0,0) position is at the top left of the window
# Higher Y - coordinate means lower on the screen
# Higher X - coordinate means further right on the screen
# playerPos[0] represents x - axis movement
# while playerPos[1] represents y - axis movement
playerPos = [50, 100]


# New 
##############################################################################
#
# This is a list of 4 booleans
# movement[0] - Left movement
# movement[1] - Right movement
# movement[2] - Up movement
# movement[3] - Down movement
movement = [False, False, False, False]

#
#
##############################################################################



while running:

   
    # movement[1] is any key input to move the player righward like D key or right arrow
    # movement[0] is any key input to move the player leftward like A key or left arrow
    #
    # If the right key is pressed then movement[1] is equal to 1 and
    # 1 - 0 is 1 making the player move rightward
    # If the left key is pressed then movement[1] remains 0
    # while movement[0] is equal to 1 and 0 - 1 is -1 making the 
    # player move leftward 

    # the player position is changed depending on which key is pressed 
    # playerPos[0] represents x - axis movement
    # while playerPos[1] represents y - axis movement
    playerPos[0] += (movement[1] - movement[0]) * 1

     # New 
    ##############################################################################
    #
    #

    playerPos[1] += (movement[3] - movement[2]) * 1
    #
    ##############################################################################



    # Checks for user input
    for event in pygame.event.get():
       
       # Checks specifically for input on the exit button 
       # On top right of winow
       if event.type == pygame.QUIT:
          # Stops the game if the user clicks the exit button
          pygame.quit()
          sys.exit()
          running = False


   
    # Checks if any keys have been pressed
    # Making the index in the movement
    # array equal to True indicates movement
    # also boolean statements True and False 
    # can be converted to numbers 
    # 1 for True and 0 for False
    if event.type == pygame.KEYDOWN:

        # If the A key or left arrow key has been pressed
        # Change the movement array accordingly
       

        if event.key == pygame.K_a:
            # movement[0] in the array 
            # represents leftward movement
            movement[0] = True

        if event.key == pygame.K_LEFT:
            # movement[0] in the array 
            # represents leftward movement
            movement[0] = True

        if event.key == pygame.K_d:
            # movement[1] in the array 
            # represents righward movement
            movement[1] = True

        if event.key == pygame.K_RIGHT:
            # movement[1] in the array 
            # represents righward movement
            movement[1] = True

        # New 
        ##############################################################################
        #
        #

        # Adding key input for upward movement of player
        # movement[3] - Upward movement
        if event.key == pygame.K_w:
            movement[2] = True
        
        if event.key == pygame.K_UP:
            movement[2] = True

        if event.key == pygame.K_s:
            movement[3] = True
        
        if event.key == pygame.K_DOWN:
            movement[3] = True
        #
        #
        ##############################################################################


    # Checks if any keys have been pressed
    # Making the index in the movement
    # array equal to True indicates movement
    # also boolean statements True and False 
    # can be converted to numbers 
    # 1 for True and 0 for False
    if event.type == pygame.KEYUP:

        # If the A key or left arrow key has been pressed
        # Change the movement array accordingly
        if event.key == pygame.K_a:
            # movement[0] in the array 
            # represents leftward movement
            movement[0] = False 

        if event.key == pygame.K_LEFT:
            # movement[0] in the array 
            # represents leftward movement
            movement[0] = False

        if event.key == pygame.K_d:
            # movement[1] in the array 
            # represents righward movement
            movement[1] = False
            
        if event.key == pygame.K_RIGHT:
            # movement[1] in the array 
            # represents righward movement
            movement[1] = False

        # New 
        ##############################################################################
        #
        #
        if event.key == pygame.K_w:
            movement[2] = False
        
        if event.key == pygame.K_UP:
            movement[2] = False

        if event.key == pygame.K_s:
            movement[3] = False
        
        if event.key == pygame.K_DOWN:
            movement[3] = False
        #
        #
        ##############################################################################


    
    # Fills the window with the background color otherwise
    screen.fill(backgroundColor)
   

  
   # .blit() draws whatever object on the window
   # in this case screen is the main game window 
   # create in line 15 and looks like this 
   # screen = pygame.display.set_mode((screenWidth, screenHeight))
   # The .blit is used as followed
   # .blit( [Object want to draw on window], (x - position of object on window, y - position of object on window) )
   # Note that the position of the object is an ordered pair (x,y) inside of .blit(player, (x,y) )
    screen.blit(player, (playerPos[0], playerPos[1]))


    # Updates every single window might want to 
    # change to pygame.display.update() to only update one window
    pygame.display.flip()




