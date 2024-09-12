class titlemap:
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
    
    def render(self,banan):
        for loc in self.tilemap: