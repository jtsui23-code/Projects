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
    
    def render(self,surf):
        for tile in self.offGridT:
            
            # self.offGridT is a list so will be interpeted as a 
            # pixals not a grid litterally in the name
            # so no need to multiply by tileSize
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0], tile['pos'][1]))

        for loc in self.tilemap:
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
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize))

        