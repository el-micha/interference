import os
import pygame

import default
import noise

from entities.resources import Stone, Cole, Silver


class TileMapping:
    """
    Loads images from a directory and creates an id:image map.
    Expects images in the directory to contain their id as a prefix of the form "01_" as in "01_background.png
    Also expects there to be at least a default image with prefix 0_"
    """

    def __init__(self, art_directory):
        if not pygame.get_init():
            pygame.init()
        self.tilemap = {}
        files = []
        try:
            files = list(filter(lambda x: ".png" in x.lower() or ".bmp" in x.lower(), os.listdir(art_directory)))
        except IOError:
            print(f"Failed to load tilemap from directory {art_directory}")
            return
        print(f"Loading art: {files}")
        for file in files:
            try:
                prefix = int(file.split("_")[0])
                if prefix in self.tilemap:
                    print(f"Id {prefix} already exists in tilemap. Overwriting entry with {file}")
                self.tilemap[prefix] = pygame.image.load(os.path.join(art_directory, file))
            except ValueError:
                print(f"Failed to extract integer prefix from {file}. "
                      "Please add a unique id to the start of the filename and separate it with an underscore.")

    def get(self, id):
        """Map an id to its tile. Default to 0-id tile"""
        return self.tilemap.get(id, self.tilemap[0])

    def get_valid_ids(self):
        return self.tilemap.keys()

    def get_tile_size(self):
        sizes = set()
        for tile in self.tilemap.values():
            size = tile.getsize()
            sizes.add(size)
        if len(sizes) == 1:
            return sizes.pop()
        else:
            print("Tile size not uniform. Returning set")
            return sizes


class TileGrid:
    """
    Holds grid of tiles.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = None
        self.tile_mapping = TileMapping("art")
        self.tile_size = default.TILE_SIZE

        self.generate_tiles()

    def generate_tiles(self):
        tile_types = [Stone, Cole, Silver]
        grid_noise = noise.smooth_noise(self.width, self.height, 3)
        grid_mapping = noise.map_noise_to_ids(grid_noise, tile_types)
        self.grid = [[tile_type() for tile_type in line] for line in grid_mapping]

    def draw(self, surface):
        for i, line in enumerate(self.grid):
            for j, tile in enumerate(line):
                if tile:
                    art_id = tile.art_id
                else:
                    art_id = 0
                surface.blit(self.tile_mapping.get(art_id), (i * self.tile_size, j * self.tile_size))

    def set_tile(self, tile, x, y):
        i, j = self.__coords_to_grid__(x, y)
        self.grid[i][j] = tile

    def remove_tile(self, x, y):
        self.set_tile(None, x, y)

    @staticmethod
    def __coords_to_grid__(x, y):
        return int(x / default.TILE_SIZE), int(y / default.TILE_SIZE)

    def __str__(self):
        s = ""
        for line in self.grid:
            s += " ".join(map(str, line)) + "\n"
        return s


# tests
if False:
    w = World(10, 10)

    w.grid[3][3] = 1

    print(w)

    tilemap = Tilemap("art")
    for k, v in tilemap.tilemap.items():
        print(k, v)
