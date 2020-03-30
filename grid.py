
import random
import os
import pygame


class Tilemap:
    """
    Loads images from a directory and creates an id:image map.
    Expects images in the directory to contain their id as a prefix of the form "01_" as in "01_background.png
    Also expects there to be at least a default image with prefix 00_"
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
        """Map an id to its tile. Default to 0"""
        return self.tilemap.get(id, self.tilemap[0])



# holds grid of tile ids.
class TileGrid:

    def __init__(self, width, height):
        # grid holds tile IDs
        tiles = [13,14,25,26]
        self.grid = [[random.choice(tiles) for x in range(width)] for y in range(height)]
        self.tilemap = Tilemap("art")
        self.tile_size = 32 # todo: get this from tilemap obj

    def draw(self, surface):
        for i, line in enumerate(self.grid):
            for j, tile_id in enumerate(line):
                surface.blit(self.tilemap.get(tile_id), (i * self.tile_size, j * self.tile_size))

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
    for k,v in tilemap.tilemap.items():
        print(k, v)