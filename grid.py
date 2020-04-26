import os
import pygame

import default
import noise
import settings

from entities.resources import Rock, CoalVein, SilverVein, IronVein
from entities.tiles import Tile
from entities.coordinates import Vector
import math

class TileGrid:
    """
    Holds grid of tiles.
    """

    def __init__(self, game, num_cols, num_rows):
        self.game = game
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid = None
        self.tile_mapping = TileMapping(settings.ART_DIR)
        self.tile_size = default.TILE_SIZE

        self.generate_tiles()

    def generate_tiles(self):
        tile_types = [Rock, IronVein, IronVein, Rock, Rock, Rock, CoalVein, CoalVein, CoalVein, CoalVein, SilverVein]
        grid_noise = noise.smooth_noise(self.num_cols, self.num_rows, 3)
        grid_mapping = noise.map_noise_to_ids(grid_noise, tile_types)
        self.grid = [[None for _ in line] for line in grid_mapping]
        for i, line in enumerate(grid_mapping):
            for j, tile_type in enumerate(line):
                pos = self.__grid_to_coords__(i, j)
                self.grid[i][j] = tile_type(self.game, pos, Vector(default.TILE_SIZE, default.TILE_SIZE))

    def draw(self, surface):
        cpos = self.game.character.pos
        for i, line in enumerate(self.grid):
            for j, tile in enumerate(line):
                if Vector.dist(cpos, tile.pos) > self.game.character.get_view_distance():
                    continue
                if tile:
                    art_id = tile.art_id
                else:
                    art_id = 0
                # could use the tile's own draw instead...
                offset = int(self.tile_size / 2)
                surface.blit(self.tile_mapping.get(art_id), (tile.pos - tile.size * 0.5).round())
                # health bar /mining progress TODO: restore and improve
                # if hasattr(tile, "durability") and tile.durability < 100:
                #     pygame.draw.line(surface, (200, 0, 0), (tile.pos[0] - offset + 2, tile.pos[1]- offset + 24), (tile.pos[0]- offset + 30, tile.pos[1]- offset + 24), 3)
                #     pygame.draw.line(surface, (200, 200, 100), (tile.pos[0]- offset + 2, tile.pos[1]- offset + 24), (tile.pos[0]- offset + int(30*tile.durability*0.01), tile.pos[1]- offset + 24), 3)

    def get_tile(self, point):
        i, j = self.__coords_to_grid__(point)
        if not self.__is_in_grid__(i, j):
            return None

        return self.grid[i][j]

    def set_tile(self, tile, point):
        i, j = self.__coords_to_grid__(point)

        if not self.__is_in_grid__(i, j):
            return

        self.grid[i][j] = tile

    def remove_tile(self, point):
        self.set_tile(Tile(self.game, point), point)

    def replace_tile(self, point, new_tile_type):
        exact_pos = self.get_tile(point).pos
        self.set_tile(new_tile_type(self.game, pos=exact_pos), exact_pos)

    def __is_in_grid__(self, i, j):
        if i < 0 or i >= self.num_rows:
            return False

        if j < 0 or j >= self.num_cols:
            return False

        return True

    def get_tiles_within_radius(self, point, r_max, r_min=1):
        """Return list of all tiles with distance greater than r_min and smaller than r_max around point.
        Create circles with increasing radii. Sample each circle with a max distance smaller than tilesize.
        Radius increase also small, so no tiles can slip through
        At least consider circles with r_min and r_max, even if distance is too small.
        This method could be massively improved by sampling an outer circle and considering rows of tiles at a time.
        """
        oversampling_factor = 1.42 # at least sqrt(2) due to diagonal
        sample_distance = self.tile_size / oversampling_factor
        num_circles = int((r_max - r_min) / sample_distance)
        radii = [r_min] + [r_min + sample_distance * (i + 0.5) for i in range(num_circles)] + [r_max]
        tiles = set()
        for r in radii:
            tiles.update(self.get_tiles_on_circle(point, r, oversampling_factor))
        return tiles

    def get_tiles_on_circle(self, point, radius, oversampling_factor=1.5):
        num_samples = int(2 * math.pi * radius / self.tile_size * oversampling_factor) # factor 1.5 for small corners
        tiles = [] # dont forget to check for None
        for i in range(num_samples):
            x = point[0] + math.sin(i * (2 * math.pi) / num_samples) * radius
            y = point[1] + math.cos(i * (2 * math.pi) / num_samples) * radius
            tile = self.get_tile(Vector(int(x), int(y)))

            pygame.draw.circle(self.game.surface, (255, 255, 255), (int(x), int(y)), 2)

            if tile is not None:
                tiles.append(tile)
        return set(tiles)

    @staticmethod
    def __coords_to_grid__(point):
        x, y = point
        return int(x / default.TILE_SIZE), int(y / default.TILE_SIZE)

    @staticmethod
    def __grid_to_coords__(i, j):
        return Vector(i * default.TILE_SIZE + int(default.TILE_SIZE/2), j * default.TILE_SIZE + int(default.TILE_SIZE/2))

    def __str__(self):
        s = ""
        for line in self.grid:
            s += " ".join(map(str, line)) + "\n"
        return s




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

