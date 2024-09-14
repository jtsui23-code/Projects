import pygame

# this list contains all the possible offset of coordinates
# around a pixal
neighborOffSet = [(-1,0), (-1,-1), (0,-1), (1,-1), (1,0),(0,0), (-1,1),(0,1),(1,1)]

# This is a set since there is no labling
# sets are faster than list and ordering doesn't matter
physicTiles = {'grass','stone'}

class tilemap:
    def __init__ (self, game, tilesize=16):
        self.game = game
        self.tileSize = tilesize
        # using a dictionary for title mapping because 
        # don't have to fill in every single tile if want 
        # two islands far apart from each other
        self.tilemap = {}
        self.offGridT = []

        for i in range(10):
            # self.tilemap[index of dictionary] = [contents that is being stored at index]
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos':(3 + i, 10)}  
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant':1,'pos':(10, 5 + i)}
    
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