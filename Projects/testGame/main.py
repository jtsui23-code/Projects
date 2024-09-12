# import pygame

# #makes in instance of pygame object
# pygame.init()

# #set resolution of screen
# screenWidth = 800
# screenHeight = 600
# floorHeight = 50

# #creates screen object
# screen = pygame.display.set_mode((screenWidth, screenHeight))

# #creates player object (x,y, width, height)
# player = pygame.Rect((300, 400, 60, 60))

# # creates a floor (x, y, width, height)
# floor = pygame.Rect((0, screenHeight -floorHeight, screenWidth, floorHeight))

# #bool for keeping the screen open
# run = True
# while run:

#     #refreshes the screen so player does not leave tracks on the screen
#     screen.fill((0,0,0))
    
#     #draws player on screen(which gui, color, which player)
#     pygame.draw.rect(screen, (134, 72, 30), player)

#     # this draws the floor
#     pygame.draw.rect(screen,(200, 77, 143), floor)

#     if player.bottom != floor.top:
#         player.move_ip(0, 50)

#     # Is an array of all of the possible key presses in pygames
#     # so key[pygame.K_a] pygame.K_a is like the index in the key
#     # array which contains the key for pressing a
#     key = pygame.key.get_pressed()
#     if key[pygame.K_a]==True:
#         player.move_ip(-2,0)
#     elif key[pygame.K_d]==True:
#         player.move_ip(2,0)
#     elif key[pygame.K_w]==True:
#         player.move_ip(0,-30)
#     elif key[pygame.K_s]==True:
#         player.move_ip(0,2)
    
#     # this conditional checks if the player is colliding with the floor
#     # and prevents the player from going through the floor
#     if player.colliderect(floor):
#         player.bottom = floor.top

# #checks if the player presses x-button on top right
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     #updates screen so player appears on it
#     pygame.display.update()
# pygame.

