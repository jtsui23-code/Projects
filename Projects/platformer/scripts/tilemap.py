import json
import pygame

# the key is a sorted array to ensure that no matter what the 
# order of coordinates used it will be matched with the same thing
# also the sorted list is converted to a tuple because 
# an array can't be a key for a map while a tuple can
autoTileMap = {
    # position    variant of tile
    tuple(sorted([(1,0), (0,1)])): 0,
    tuple(sorted([(1,0), (0,-1)])): 1,

}
# this list contains all the possible offset of coordinates
# around a pixal
neighborOffSet = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0),(0,0), (-1,1),(0,1),(1,1)]

# This is a set since there is no labling
# sets are faster than list and ordering doesn't matter
physicTiles = {'grass','stone'}
autoTile = {'grass', 'stone'}

class tilemap:
    def __init__ (self, game, tilesize=16):
        self.game = game
        self.tileSize = tilesize
        # using a dictionary for title mapping because 
        # don't have to fill in every single tile if want 
        # two islands far apart from each other
        self.tilemap = {}
        self.offGridT = []
    def save(self,path):
        # open the file
        # 'w' stands for write in the file
        f = open(path, 'w') 
        # dump the map into the file as json
        json.dump({'tilemap':self.tilemap, 'tileSize': self.tileSize, 'offgrid':self.offGridT},f)
        f.close()
    
    def load(self,path):
        # open file in path and read it in
        # 'r' stands for read
        f = open(path, 'r')

        # stores map data
        mapData = json.load(f)
        f.close()
        self.tilemap = mapData['tilemap']
        self.tileSize = mapData['tileSize']
        self.offGridT = mapData['offgrid']

    # method for autotiling based on surround tiles in editor
    def autoTile(self):
        # checks if the location of the tile exist
        for loc in self.tilemap:
            # stores the position on the location of the tile
            tile = self.tilemap[loc]
            neighborSet = set()
            # looks at surround positions to the tile
            for shift in [(1,0), (-1,0), (0,-1), (0,1)]:
                # stores the surrounding position
                checkLocation = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                # checks if surrounding position exists 
                if checkLocation in self.tilemap:
                    pass
    # this function returns all of the tiles that are around the player
    def tilesAround(self, pos):
        tile = []
        #This converts pixal postion to grid
        # requires integer conversion AND integer devision
        # because if only use one number will be unconsistant 
        # with negative numbers
        tileLoc = [int(pos[0]//self.tileSize), int(pos[1]//self.tileSize)]

        for offset in neighborOffSet:

            #checks the surround pixal that was passed in using the
            # neighborOffSet array so 9 pixals
            # checkLoc is a string because 
            # self.tilemap's index is a string
            # ex) self.tilemap['10;5]
            checkLoc = str(tileLoc[0]+offset[0]) + ';' + str(tileLoc[1]+offset[1])
            #if the pixal that is being checked exists in the tilemap object
            # as in the pixal is not just empty space
            # then add the checked pixal to the tile list
            if checkLoc in self.tilemap:
                tile.append(checkLoc)

        return tile
    # this function returns all of the tiles near the player 
    # that need collision physics
    def physicsRectAround(self, pos):
        rect = []
        
        #this checks the coordinates of every single tile that is
        # near to the player. tTiles then stores the tile type of
        # each of the tiles at the coordinates stored in tTilekey
        # if the type stored in tTiles is one that needs collision
        # add a rectangle object at that coordinate for collision
        for tTilekey in self.tilesAround(pos):
            tTiles = self.tilemap[tTilekey]
            if tTiles['type'] in physicTiles:
                rect.append(pygame.Rect(tTiles['pos'][0]*self.tileSize, tTiles['pos'][1]*self.tileSize,self.tileSize,self.tileSize))
        return rect
    
    def render(self,surf, offset=(0,0)):

        for tile in self.offGridT:
            # self.offGridT is a list so will be interpeted as a 
            # pixals not in the grid litterally in the name
            # so no need to multiply by tileSize
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]- offset[0], tile['pos'][1]- offset[1]))

        # this will check the screen starting from the top left (offset[0]//self.tileSize)
        # to the top right (offset[0] + surf.get_width)//self.tileSize + 1)
        # the plus one is there because this will be 1 tile off if not aded

        # the nested for loop will check from top to bottom of the screen
        for x in range(offset[0] // self.tileSize, (offset[0] + surf.get_width()) // self.tileSize +1):
            for y in range(offset[1] // self.tileSize, (offset[1] + surf.get_height()) // self.tileSize + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    # .blit([thing want to render], [location of render])
                    # self.game.assets[] refers to the dictionary in main 
                    # that contains all of the different types of tiles and
                    # player assets
                    # tile varible refers to the object created in this current for loop
                    # use ['pos'] in tile['pos'] to navagate the dictionary created in the 
                    # constructor in this tilemap Class
                    # the postion contained two values which is why ther is an addition (())
                    # tile['pos'] is multiplied by self.tileSize because the postion value is in
                    # terms of the grid but we want the tile to be the size of the asset
                    # to make pixal art
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))           