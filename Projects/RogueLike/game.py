import sys
import pygame
from utils import loadImage, loadImages
from character import Character, Player, Enemy
from tilemap import Tilemap
import random
import math

"""
Game

Description:
    This class represents the main game loop for a rogue-like game implemented 
    using Pygame. It initializes the game window, assets, player, tilemap, and 
    handles input, rendering, and game logic. The class also defines the player's 
    movement and updates the display at a set frame rate.

Public Methods:
    - __init__()              Initializes the game, loads assets, and sets up the player and tilemap.
    - run()                   Starts the game loop, handles user input, updates the player, 
                              renders the game environment, and manages the frame rate.

Usage:
    - Instantiate the class: Game()
    - Call the run() method: Game().run() to start the game.
"""

class Game:

    # Sets up the game windows, framerate, player, and other assets
    def __init__(self):

        # Starts up Pygame
        pygame.init()

        # Sets the name of the window icon to "Rogue-like"
        pygame.display.set_caption('Rogue-Like')

        # Creating a screen variable with the window dimension variables set above
        # when setting window dimensions have to do .set_mode( (_,_) )
        # Treat the (_,_) as order pairs inside of ( (_,_) )
        self.screen = pygame.display.set_mode((640, 480))

        self.display = pygame.Surface((320, 240))


        # Acts as the 'Camera' position
        self.scroll = [0,0]

        self.clock = pygame.time.Clock()

        # This is a list of 4 booleans
        # movement[0] - Left movement
        # movement[1] - Right movement
        # movement[2] - Up movement
        # movement[3] - Down movement
        self.movement = [False, False, False, False]
        
        # Dictionary for loading assets in the game makes it more organized and 
        # accessable for the Tilemap class
        self.assets = {
            'background':pygame.transform.scale(loadImage('background.png'), (1240,840)),
            'newGrass': loadImages('tiles/newGrass'),
            'grass': loadImages('tiles/grass'),
            'stone': loadImages('tiles/stone'),
            'player': pygame.transform.scale(loadImage('Player/slashCharacter.png'), (16, 20)),  # Adjust the size to match the tiles
            'slashRight':pygame.transform.scale(loadImage('slashAttack/slashRight.png').convert_alpha(), (16,20)),
            'slashLeft':pygame.transform.scale(loadImage('slashAttack/slashLeft.png').convert_alpha(), (16,20)),
            'healthBarBorder':pygame.Surface((104,14)),
            'redHealthBar':pygame.Surface((100,10)),
            'greenHealthBar':pygame.Surface((100,10)),
            'enemy': pygame.transform.scale(loadImage('Enemy/enemy2.png'), (16,20))
        }

        # Sets up the health bar to have a dark gray border
        self.assets['healthBarBorder'].fill((40,40,40))
        # Fills the rectangle surface with red and the other one with green.
        self.assets['redHealthBar'].fill((255,0,0))
        self.assets['greenHealthBar'].fill((0,255,0))

        # Creating a player
        # Pass in a game, name, position and size
        self.player = Player(self, (300, 240), (10, 17))
        
        # Creating a tilemap object with the specified tile size
        self.tilemap = Tilemap(self, tileSize=16)

        # Loads the first map of the game.
        self.loadMap(0)

        
        # Setting up enmey spawning.
        self.enemies = []
        self.enemyTimer = 0
        self.enemySpawnDelay = 180
        self.minSpawnDistance = 150
        self.maxSpawnDistance = 250
        self.maxEnemy = 5

    def spawnEnemy(self):

        # Do not spawn anymore enemies if reached max enmey count
        if len(self.enemies) > self.maxEnemy:
            return
        

        # Randomly generates an angle of position for the 
        # enemy to spawn around the player.
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(self.minSpawnDistance, self.maxSpawnDistance)

        spawnX = self.player.rect().centerx + math.cos(angle) * distance
        spawnY = self.player.rect().centery + math.sin(angle) * distance

        newEnemy = Enemy(self, (spawnX, spawnY), (16,20))
        self.enemies.append(newEnemy)

    def updateEnemy(self):

        # Delays the spawning of enemies so there are not too many
        # of them at once.
        self.enemyTimer += 1
        if self.enemyTimer > self.enemySpawnDelay:
            self.spawnEnemy()
            self.enemyTimer = 0

        # [:] creates a temporary copy of the enemies list to 
        # iterate over the copied list because if you iterate over the 
        # original enemy while deleting elements in the list
        # this could cause problems since the list's length is 
        # changing with each iteration.
        for enemy in self.enemies[:]:
            enemy.update(self.tilemap, self.player)
            
            # Removes enemy from the map and game if their health hits zero.
            if enemy.currentHealth <= 0:
                self.enemies.remove(enemy)


    def loadMap(self, path):

        print('Successful map load')
        self.tilemap.load('Media/levels/' + str(path) + '.json')
        
    def run(self):
        while True:


            # Sets the background to an image at the position (0,0)
            self.display.blit(self.assets['background'], (0,0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30

            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            # Draws the tiles on the window
            self.tilemap.render(self.display, offset=renderScroll)
            
            # Makes the player move on the window 
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], self.movement[3] - self.movement[2]))
            self.player.render(self.display, offset=renderScroll)
            
            # Displays and updates the health bar.
            self.player.renderHealthBar(self.display, renderScroll)

            self.updateEnemy()



            for enemy in self.enemies:
                enemy.render(self.display, offset=renderScroll)
            # Checks for user input
            for event in pygame.event.get():

                # Checks specifically for input on the exit button 
                # On top right of winow
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 1:
                        self.player.attack(offset=renderScroll)
                
                # Checks if any keys have been pressed
                # Making the index in the movement
                # array equal to True indicates movement
                # also boolean statements True and False 
                # can be converted to numbers 
                # 1 for True and 0 for False
                if event.type == pygame.KEYDOWN:


                    if event.key ==pygame.K_LSHIFT:
                        self.player.speedUp(1.5)

                    # If the A key or left arrow key has been pressed
                    # Change the movement array accordingly
                    if event.key == pygame.K_a:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = True

                    if event.key == pygame.K_LEFT:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = True

                    if event.key == pygame.K_d:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = True

                    if event.key == pygame.K_RIGHT:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = True

                    # Adding key input for upward movement of player
                    # movement[3] - Upward movement
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    
                    if event.key == pygame.K_UP:
                        self.movement[2] = True

                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = True


                if event.type == pygame.KEYUP:

                    

                    if event.key == pygame.K_LSHIFT:
                        self.player.speedUp(1)
                    # If the A key or left arrow key has been pressed
                    # Change the movement array accordingly
                    if event.key == pygame.K_a:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = False 

                    if event.key == pygame.K_LEFT:
                        # movement[0] in the array 
                        # represents leftward movement
                        self.movement[0] = False

                    if event.key == pygame.K_d:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = False
                        
                    if event.key == pygame.K_RIGHT:
                        # movement[1] in the array 
                        # represents righward movement
                        self.movement[1] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False
            
                    if event.key == pygame.K_UP:
                        self.movement[2] = False

                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    
                    if event.key == pygame.K_DOWN:
                        self.movement[3] = False
            
            
            # .blit() draws whatever object on the window
            # in this case screen is the main game window
            # .blit( [Object want to draw on window], (x - position of object on window, y - position of object on window) ) 
            # pygame.transform.scale() makes the screen zoom closer to the player
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))


            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()