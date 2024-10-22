import random
import math
from scripts.particle import Particle
import sys
import pygame
from scripts.beings import physicsBeing, player
from scripts.util import loadImage, loadImages, animation
from scripts.tilemap import tilemap
from scripts.clouds import cloudz

class game:

    def __init__(self):
        
        # initiates pygame
        pygame.init()

        pygame.display.set_caption("祝福")
        # create screen object
        self.screen = pygame.display.set_mode((640,480))

        # used for fps
        self.clock = pygame.time.Clock()

        # makes a small display ontop of the screen 
        self.display = pygame.Surface((320, 200))

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False]

        # dictionary for assets
        self.assets = {
            
            'decor' : loadImages('tiles/decor'),
            'grass' : loadImages('tiles/grass'),
            'large_decor' : loadImages('tiles/large_decor'),
            'stone' : loadImages('tiles/stone'),
            # uses function from util script
            'player': loadImage('entities/player.png'),
            'background': loadImage('background.png'),
            'clouds': loadImages('clouds/'),
            'player/idle': animation(loadImages('entities/player/idle'), imgDur=6),
            'player/run': animation(loadImages('entities/player/run'),imgDur=4),
            'player/jump': animation(loadImages('entities/player/jump')),
            'player/slide': animation(loadImages('entities/player/slide')),
            'player/wallSlide':animation(loadImages("entities/player/wall_slide")),
            'particle/leaf': animation(loadImages('particles/leaf'), imgDur=20, loop=False),
            'particle/particle': animation(loadImages('particles/particle'), imgDur=6, loop=False),
            'spawners': loadImages('tiles/spawners'),

        }

        self.clouds = cloudz(self.assets['clouds'], count=16)
        
        self.player = player(self, (100,20), (8, 15))

        self.tilemap = tilemap(self, tilesize=16)
        self.tilemap.load('levels/map.json')

        self.leafSpawner = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            # This looks at every tree so it can determine where to 
            # spawn in the leaves. The leaves will be offsetted a bit 
            # from where the tree actually is
            self.leafSpawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        # gets the enemy assets from the spawner's folder containing them
        # 'spawners', 0 is for spawning player
        # 'spawners', 1 is for spawning enemy
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners',1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                print(f'Enemy Position: {spawner['pos']}')
        
        self.particles = []

        self.scroll = [0,0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0,0))

            # if you set scroll to just the player's center
            # then the player will be set to the top left 
            # since the scroll is initially at the top left corner
            # if you only subtract with the width/heigh of display 
            # then the player will be stuck on the right instead
            # (self.player.rect().centerx - self.display.get_width()/2) is 
            # essentially the location where we want the camera to be and 
            # the - self.scroll[0] in
            # (self.player.rect().centerx - self.display.get_width()/2 - self.scroll[0])
            # is where the camera is currently located so by adding the distance of 
            # where how far away we want the camera is to where we want it to be
            # we get a moving camera that is centered at the player's position
            # the /30 at the end makes the camera move faster as the player is farther 
            # away because the larger the distance between player and camera
            # the greater the quiotient making the camera movement faster
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() /2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() /2 - self.scroll[1])/30

            # since the scroll and player position are floats
            # the camera centering is inconsistant because of rounding
            # therefore need to turn camera positioning into int
            renderScroll = (int(self.scroll[0]), int(self.scroll[1]))


            # spawns in particles at random
            # the particle type is leaf
            # the range of the velocity is -0.1
            # to 0.3 and can spawn in frame 0 to 20
            for rect in self.leafSpawner:
                # multiplying random.radnom() by a big number 
                # makes it to where the leaf particles are not 
                # spawned in at every frame so the larger the number
                # the less frequent the leaves spawn
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0,20)))

            self.clouds.update()
            self.clouds.render(self.display, renderScroll)

            self.tilemap.render(self.display,offset=renderScroll)


            # this updates the player's movement on the x axis
            self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))

            # updates the screen    
            self.player.render(self.display, offset=renderScroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=renderScroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # pygame.event.get() gets the user's input
            for event in pygame.event.get():
                #checks if the user pressed x button on top right
                if event.type == pygame.QUIT:
                    #closes out of pygames
                    pygame.quit()
                    #closes out of systems
                    sys.exit()

                # checks if keys are being pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player.jump()
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_SPACE:
                        self.player.dash()
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                
                # if you let go of the key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            # rendering the display(small sreen) at 0,0
            # rescales the screen so like zooms in so player is not tiny
            # pygame.transform.scale([thing want to scale], [how much 
            # want to scale])
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), (0,0))
            # Updates the screen
            pygame.display.update()
            # forces loop to run at 60 fphs
            self.clock.tick(60)


# creates game object and uses run method
game().run()
