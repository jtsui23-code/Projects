import pygame

# This list contains all the possible offset of coordinates
# around a pixal
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

# Tiles that will have physics applied to them
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    def __init__(self, game, tileSize=16):
        self.game = game
        self.tileSize = tileSize

        # Tiles are represented as map because this allows for having separted 
        # land masses like two islands while a list forces you to fill in every tile 
        # between the 2 islands
        
        # self.tilemap will have a key of a string like so '3;1' to represent position of 
        # tile it is a string because the tilemap will be a json and json does not support
        # tuples Ex) (1,1) 
        self.tilemap = {}

        self.offgridTiles = []


        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}
    

    def tilesAround(self, pos):
        tiles = []
        tileLoc = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))
        for offset in NEIGHBOR_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ';' + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])
        return tiles
    
    def physicsRectsAround(self, pos):
        rects = []
        for tile in self.tilesAround(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))
        return rects

    def render(self, surface):
        # Traverses through the entire offgrid tilemap in list and draws every tile on the 
        # game window
        for tile in self.offgridTiles:
            surface.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])
            
        # Traverses through the entire tilemap dictionary and draws every tile on the 
        # game window
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize))