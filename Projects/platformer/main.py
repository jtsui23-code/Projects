import random
import math
from scripts.particle import Particle
import sys
import pygame
from scripts.beings import physicsBeing, Player, Enemy
from scripts.util import loadImage, loadImages, animation
from scripts.tilemap import tilemap
from scripts.clouds import cloudz
from scripts.spark import Spark

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
        self.display = pygame.Surface((320, 240))

        # up is bound to [0] down is bound to [1] 
        self.movement = [False, False]

        # dictionary for assets
        self.assets = {
            
            'decor' : loadImages('tiles/decor'),
            'grass' : loadImages('tiles/grass'),
            'large_decor' : loadImages('tiles/large_decor'),
            'stone' : loadImages('tiles/stone'),
            # uses function from util script
            'enemy/idle': animation(loadImages('entities/enemy/idle'), imgDur=6),
            'enemy/run': animation(loadImages('entities/enemy/run'), imgDur=4),
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
            'gun': loadImage('gun.png'),
            'projectile':loadImage('projectile.png'),
        }

        self.clouds = cloudz(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50,50), (8, 15))

        self.tilemap = tilemap(self, tilesize=16)

        self.screenshake = 0
        self.levelCounter = 0
        self.loadMap(0)
    # this method loads in a map/level
    # this method recieves the name of the level/map that is 
    # being desired to be loaded 
    def loadMap(self, mapName):
        self.tilemap.load('levels/' + str(mapName) + '.json')
        self.leafSpawner = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            # This looks at every tree so it can determine where to 
            # spawn in the leaves. The leaves will be offsetted a bit 
            # from where the tree actually is
            self.leafSpawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.enemies = []
        # gets the enemy assets from the spawner's folder containing them
        # 'spawners', 0 is for spawning player
        # 'spawners', 1 is for spawning enemy
        # made a copy of the spawners so don't disrupt ths 
        # size of the dictionary while running 
        for player in list(self.tilemap.extract([('spawners',0)])):
            self.player.pos = player['pos']
            self.player.airTime = 0
            self.player.airTimeThreshold = 0

        for spawner in list(self.tilemap.extract([('spawners', 1)])):
            self.enemies.append(Enemy(self, spawner['pos'], (8,15)))

        self.projectiles = []
        self.particles = []
        self.scroll = [0,0]
        self.sparks = []
        self.transition = -30
        self.dead = 0

    def run(self):
        while True:
            if len(self.enemies) == 0:
                self.transition += 1
                if self.transition >= 1:
                    self.levelCounter += 1 
                    if self.levelCounter > 3:
                        pygame.quit()
                        print("\nCongratulations, You beated the game!\n")
                    self.loadMap(self.levelCounter)

            if self.transition < 0:
                self.transition += 1

            self.display.blit(self.assets['background'], (0,0))

            self.screenshake = max(0, self.screenshake - 1)

            # checks if the player has been hit by a projectile
            # Then after 40 frames the player will
            # respawn in the first stage
            if self.dead:
                self.dead += 1
                if self.dead == 40:
                    self.loadMap(0)
                    self.levelCounter = 0

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

            for enemy in self.enemies.copy():
                # giving enemy a default movement of 0
                kill = enemy.update(self.tilemap, (0,0))
                enemy.render(self.display, offset=renderScroll)
                if kill:
                    self.enemies.remove(enemy)

            # this respawns the player in the map if the player
            # is has not died yet or if the player is respawning 
            # after being hit by a projectile
            if not self.dead:
                # this updates the player's movement on the x axis
                self.player.update(self.tilemap,(self.movement[1] - self.movement[0],0))

                # updates the screen    
                self.player.render(self.display, offset=renderScroll)

            # projectile is a list of a list of attributes pertaining
            # to a projectile
            # [ [(x,y), direction, timer]]
            # coordinate is the first item [0]
            # direction of projectile is second item [1]
            for projectile in self.projectiles:
                # giving movement to the projectile
                # according to its direction
                projectile[0][0] += projectile[1]

                # increments counter for the projectile
                projectile[2] +=1

                img = self.assets['projectile']
                # (projectile[0][0] - img.get_width()) / 2
                # centers the image of the projectile
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - renderScroll[0], projectile[0][1] - img.get_height() / 2 - renderScroll[1]))
                # checks if the projectile is hiting a solid thing
                if self.tilemap.surfCheck(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):                  # projectile[1] is direction so the spark effects go left if projectile moves right making an bouncing effect 
                                                                                            # random.random() range of [0,1] so 2 + random.random() is [2,3]
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))

                # if the tile has existed 360 frames or 6 seconds
                # delete it 
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(25, self.screenshake)
                        for i in range(30):
                            # gives random angle in 360 degree circle
                            angle = random.random() * math.pi * 2
                            # random speed 
                            speed = random.random() * 5
                            # creates spark effects when hitting the player
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))                    
                            # makes a particle effect that goes off in opposite direction to spark when hiting the player    # + math.pi makes the particle shoot off in different direction to the spark     
                            self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5]))
            
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=renderScroll)
                if kill:
                    self.sparks.remove(spark)
                    
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

            # inplementing level transition animation

            if self.transition:
                # pygame.Surface(self.display.get_size())
                # makes a black surface overlay over the game screen
                
                transitionSurf = pygame.Surface(self.display.get_size())
                
                # this draws a circle over the black transition surface
                # to create the level transition effect/animation
                # the circle will be white and be positioned in the 
                # middle of the screen                                                          # 30 comes from the selected self.transtion = 30 
                pygame.draw.circle(transitionSurf, (255,255,255), (self.display.get_width()//2, self.display.get_height()//2), (30 - abs(self.transition)) * 8)
                
                # the color key makes it to where the specificed 
                # color will be transparent on the surface/display
                # meaning the circle will be transparent
                transitionSurf.set_colorkey((255,255,255))
                self.display.blit(transitionSurf, (0,0))


            # the screenOfset will be half of the self.screenshake
            # both positive and negative 
            # ex) self.screenshot = 100 then screenOffset = (-50,50)
            screenShakeOffset = (random.random() * self.screenshake - self.screenshake/2, random.random() * self.screenshake - self.screenshake/2)
            # rendering the display(small sreen) at 0,0
            # rescales the screen so like zooms in so player is not tiny
            # pygame.transform.scale([thing want to scale], [how much 
            # want to scale])
            self.screen.blit(pygame.transform.scale(self.display,self.screen.get_size()), screenShakeOffset)
            # Updates the screen
            pygame.display.update()
            # forces loop to run at 60 fphs
            self.clock.tick(60)


# creates game object and uses run method
game().run()


