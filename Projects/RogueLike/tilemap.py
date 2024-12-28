import pygame
import json
import tkinter as tk
from tkinter import filedialog # Needed for browsing files to load for level editor.


# Offsets to check neighboring tile positions around a given tile.
# Includes the current tile (0, 0) and its 8 surrounding tiles.
NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

# Tiles that will interact with physics (e.g., collision detection).
PHYSICS_TILES = {'grass', 'stone'}


"""
Tilemap

Description:
    This class represents the tilemap for a game, handling the storage, rendering, 
    and interaction of tiles in a grid-based system. It allows for sparse tile placement 
    and includes features for physics interaction and off-grid tile rendering.

Public Methods:
    - __init__(game, tileSize=16)                Initializes the tilemap with a reference to the game instance, 
                                                 tile size, and an empty tile dictionary.
    - tilesAround(pos)                           Retrieves a list of neighboring tiles around a given position.
    - physicsRectsAround(pos)                    Retrieves physics-enabled tiles as rectangles around a given position.
    - render(surface, offset=(0, 0))             Renders both grid-aligned and off-grid tiles onto a surface, 
                                                 with support for camera offset.

Usage:
    - Instantiate the Tilemap class: tilemap = Tilemap(game_instance, tileSize=16)
    - Access nearby tiles: tiles = tilemap.tilesAround(player_position)
    - Retrieve physics rectangles for collision: rects = tilemap.physicsRectsAround(player_position)
    - Render tiles on a surface: tilemap.render(surface, offset=(camera_x, camera_y))
"""

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
        # for i in range(20):
        #     for j in range (20):
        #         self.tilemap[str(0 + i) + ';' + str(j)] = {'type': 'newGrass', 'variant': 1, 'pos': (0 + i, j)}
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

        # Draw off-grid tiles stored in the list.
        for tile in self.offgridTiles:

            # Using the list of offset tiles to access the map assets in game class
            # tile['type'] represent the key in the assets dictionary while 
            # tile['variant'] is the paired element to the key
            # Ex) In the context of the map it would look like so
            # {tile['type'] : tile['variant'] }
            # tile['pos'][0] - offset[0] accounts for 'camera' movement
            surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))
            

        # This only renders the tiles that are in the horizontal range of the screen
        # to optimize performance instead of rendering every single tile on the window.
        # offset[0] // self.tileSize is the farthest left side of the camera which is where the
        # Tiles will start to render and 
        # (offset[0] + surface.get_width()) // self.tileSize + 1 is the farthest right side of the camera.
        # The reason for // self.tileSize is because the offset is in the units of pixels while
        # the tiles are in the units of tile size.
        # Then the same process is repeated for the y - axis to cover both the horizontal and vertical 
        # tiles on the camera.
        for x in range(offset[0] // self.tileSize, (offset[0] + surface.get_width()) // self.tileSize + 1):
            for y in range(offset[1] // self.tileSize, (offset[1] + surface.get_height()) // self.tileSize + 1):
                # This checks if the tile on the screen belongs in the tilemap dictionary.
                # If the tile does exist then it is saved in a temporary variable tile 
                # to be rendered on the window.
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    # Need to do tile['pos'][0] * self.tileSize - offset[0] 
                    # or the tiles will be really small since they are in pixel units 
                    # instead of tile size.
                    surface.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tileSize - offset[0], tile['pos'][1] * self.tileSize - offset[1]))
    
    def save(self, path):
        # Goes to the folder/path that is given and writes a json file there with all of the 
        # information regarding the tilemap, tile size, and off grid tiles in that json.
        # 'w' - write to file
        file = open(path, 'w')
        json.dump( {'tilemap': self.tilemap, 'tileSize': self.tileSize, 'offgrid': self.offgridTiles}, file)


    def load(self, path=None):
        
        # This allows the user of the level editor to select the level they want to 
        # continue to work on using a UI instead of coding in the path of the level for convience.
        if path is None:
            
            # root is a window from the tkinter library 
            # It is used to explicitly close the window UI for loading maps 
            # because this saves memory.
            root = tk.Tk()
            root.withdraw()
            # Opens the file selected in UI.
            path = filedialog.askopenfilename( 
                # filetypes adds a filter for json files to only appear.
                # The format is ( "[Text displayed]", "*[Filtered file]")
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],

                # This is the text that will appear on the UI of the level loader.
                title="Load Map"
            )

            root.destroy()
            
        # If the user picked a file in the level loader UI, load all of the contents from the json
        if path:
            try:
                # Goes to the folder/path that is given and reads a json file there with all of the 
                # information regarding the tilemap, tile size, and off grid tiles in that json.
                # 'r' - read to file
                with open(path, 'r') as file:
                    mapData = json.load(file)
                    file.close()
                    self.tilemap = mapData['tilemap']
                    self.tileSize = mapData['tileSize']
                    self.offgridTiles = mapData['offgrid']
                return True
            except FileNotFoundError:
                return False
            
        return False
