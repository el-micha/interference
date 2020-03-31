
import random
import os
import pygame
import matplotlib.pyplot as plt

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
        tiles = [2, 3, 15, 25, 26]

        grid = smooth_noise(width, height, 5)
        self.grid = map_noise_to_ids(grid, tiles)

        #self.grid = [[random.choice(tiles) for x in range(width)] for y in range(height)]
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


def smooth(inp):
    newgrid = [[0 for x in inp[0]] for y in inp]
    for i in range(len(inp)):
        for j in range(len(inp[0])):
            neighbours = [inp[i][j]]
            factor = 0.5
            try:
                neighbours.append(factor * inp[i-1][j])
            except:
                pass
            try:
                neighbours.append(factor * inp[i+1][j])
            except:
                pass
            try:
                neighbours.append(factor * inp[i][j-1])
            except:
                pass
            try:
                neighbours.append(factor * inp[i][j+1])
            except:
                pass
            newgrid[i][j] = sum(neighbours) / (1 + (len(neighbours)-1)*factor)
    return newgrid

def disp(inp):
    s = ""
    for line in inp:
        s += " ".join(map(str, line)) + "\n"
    print(s)


def grid_max(grid):
    maximum = 0
    for line in grid:
        for x in line:
            maximum = max(maximum, x)
    return maximum

def map_noise_to_ids(grid, ids):
    # partition [0,max] into equally sized intervals, one interval for each id in ids.
    maxm = grid_max(grid)
    disp(grid)
    print(maxm)
    num_intervals = len(ids)
    interval_size = maxm / num_intervals
    interval_borders = [interval_size * (1+x) for x in range(num_intervals)]
    def get_index(x, borders):
        for i,b in enumerate(borders):
            if x <= b:
                return i
        return len(borders)-1
    newgrid = [[0 for x in grid[0]] for y in grid]
    for i, line in enumerate(grid):
        for j, elem in enumerate(line):
            newgrid[i][j] = ids[get_index(elem, interval_borders)]
    return newgrid

def smooth_noise(width, height, iterations):
    grid = [[random.expovariate(0.1) for x in range(width)] for y in range(height)]
    #plt.imshow(grid)
    #plt.show()
    for i in range(iterations):
        grid = smooth(grid)
        #plt.imshow(grid)
        #plt.show()
    return grid




# tests
if False:
    w = World(10, 10)

    w.grid[3][3] = 1

    print(w)

    tilemap = Tilemap("art")
    for k,v in tilemap.tilemap.items():
        print(k, v)