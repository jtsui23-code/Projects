import pygame   # Importing Pygame library
import sys      # Importing sys library to properly close the game
import math     # Import for physics/movement
from _7_2CharacterClass import Player  # Getting the Player class from the other script


# New 
############################################################################################################################################################
#
#
class Game:

    # Sets up the game windows, framerate, player, and other assets
    def __init__(self):
        # Starts up Pygame
        pygame.init()
        
        # Setting the game window's dimensions
        self.screen_width = 800
        self.screen_height = 600
        
        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) )
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption("Rogue-Like")
        
        # Sets the background color based of of RGB (255,255,255)
        # the color is black is (0,0,0)
        self.background_color = (0, 0, 0)
        
        # Set framerate for game
        self.clock = pygame.time.Clock()
        
        # Making a player using the Player class imported 
        self.player = Player()
        self.running = True

    # This method checks if the user has clicked the top right x button on the window
    # if so the game is closed
    def handle_events(self):
        for event in pygame.event.get():
            # Checks specifically for input on the exit button 
            # On top right of window
            if event.type == pygame.QUIT:
                # Stops the game if the user clicks the exit button
                pygame.quit()
                sys.exit()
                self.running = False
            
            self.player.handle_input(event)

    # This method updates the position of the player on the window
    def update(self):
        self.player.update_position()

    # This method renders the background of the game window, player on the window, and updates the window
    def render(self):
        # Fills the window with the background color
        self.screen.fill(self.background_color)
        
        # .blit() draws whatever object on the window
        # in this case screen is the main game window 
        # The .blit is used as followed
        # .blit( [Object want to draw on window], (x - position of object on window, y - position of object on window) )
        # Note that the position of the object is an ordered pair (x,y) inside of .blit(player, (x,y) )
        self.screen.blit(self.player.sprite, (self.player.position[0], self.player.position[1]))
        
        # Updates every single window might want to 
        # change to pygame.display.update() to only update one window
        pygame.display.flip()

    # This method is the game loop 
    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.render()

if __name__ == "__main__":
    game = Game()
    game.run()

#
#
############################################################################################################################################################