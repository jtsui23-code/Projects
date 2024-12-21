import pygame

# Offsets to check neighboring tile positions around a given tile.
# Includes the current tile (0, 0) and its 8 surrounding tiles.
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

# Tiles that will interact with physics (e.g., collision detection).
PHYSICS_TILES = {'grass', 'stone'}

class Tilemap:
    # Initialize the tilemap class.
    def __init__(self, game, tileSize=16):

        # Reference to the main game instance, used for accessing game assets.
        self.game = game

        # Size of each tile in pixels.
        self.tileSize = tileSize

        # The tilemap is represented as a dictionary where:
        #   - Key: A string in the format 'x;y' representing tile coordinates.
        #   - Value: A dictionary containing tile properties (type, variant, position).
        #
        # Using a dictionary allows for sparse tile placement, enabling gaps 
        # and disconnected landmasses (e.g., islands).
        # A list would require filling in every position between tiles.
        # Tile positions are stored as strings because JSON does not support tuples.
        self.tilemap = {}


        # A list to store off-grid tiles that do not align with the main grid.
        self.offgridTiles = []


        # Example of using tilemap system
        for i in range(20):
            for j in range (20):
                self.tilemap[str(0 + i) + ';' + str(j)] = {'type': 'newGrass', 'variant': 1, 'pos': (0 + i, j)}
            # self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}

    

    # Get all tiles surrounding the given position.
    #
    # Args:
    #   pos (tuple): The (x, y) position in pixels.
    #
    # Returns:
    #   A list of tile dictionaries representing the neighboring tiles.
    def tilesAround(self, pos):

        tiles = []
        # Convert pixel position to grid coordinates.
        tileLoc = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))

        # Check all neighboring positions using NEIGHBOR_OFFSETS.
        for offset in NEIGHBOR_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ';' + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])

        return tiles

    # Get rectangles for tiles with physics interactions surrounding the given position.
    #
    # Args:
    #   pos (tuple): The (x, y) position in pixels.
    #
    # Returns:
    #   A list of pygame.Rect objects representing the physics-enabled tiles.
    def physicsRectsAround(self, pos):

        rects = []

        # Check neighboring tiles and include only those with physics properties.
        for tile in self.tilesAround(pos):

            if tile['type'] in PHYSICS_TILES:

                # Create a rectangle at the tile's position, scaled to the tile size.
                rects.append(pygame.Rect(tile['pos'][0] * self.tileSize, tile['pos'][1] * self.tileSize, self.tileSize, self.tileSize))

        return rects

    # Draw all tiles (off-grid and grid-aligned) to the given surface.
    #
    # Args:
    #   surface: The surface (e.g., game window) to draw tiles on.
    def render(self, surface, offset=(0,0)):

        # This only renders the tiles that are in the horizontal range of the screen
        # to optimize performance instead of rendering every single tile on the window.
        # offset[0] // self.tileSize is the farthest left side of the camera which is where the
        # Tiles will start to render and 
        # (offset[0] + surface.get_width()) // self.tileSize + 1 is the farthest right side of the camera.
        # The reason for // self.tileSize is because the offset is in the units of pixels while
        # the tiles are in the units of tile size.
        for x in range(offset[0] // self.tileSize, (offset[0] + surface.get_width()) // self.tileSize + 1):
            pass
        # # Draw off-grid tiles stored in the list.
        # for tile in self.offgridTiles:

        #     # Using the list of offset tiles to access the map assets in game class
        #     # tile['type'] represent the key in the assets dictionary while 
        #     # tile['variant'] is the paired element to the key
        #     # Ex) In the context of the map it would look like so
        #     # {tile['type'] : tile['variant'] }
        #     # tile['pos'][0] - offset[0] accounts for 'camera' movement
        #     surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            
            
        # Draw all grid-aligned tiles stored in the dictionary.
        for loc in self.tilemap:
            tile = self.tilemap[loc]

            # Convert grid coordinates to pixel coordinates for rendering.
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))