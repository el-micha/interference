import os
from timeit import default_timer as timer

import pygame

import default
import noise
import settings
from effects.fields import LightField

from entities.resources import Rock, CoalVein, SilverVein, IronVein
from entities.tiles import Tile
from entities.coordinates import Vector
import math

from events.events import MiningEvent
from events.observers import Observer


class TileGrid(Observer):
    def __init__(self, game, num_cols, num_rows):
        self.game = game
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid = None
        self.tile_mapping = None
        self.tile_size = default.TILE_SIZE

        self.load_static()
        self.generate_tiles()

    def load_static(self):
        self.tile_mapping = TileMapping(settings.ART_DIR)

    def generate_tiles(self):
        tile_types = [Rock, IronVein, IronVein, Rock, Rock, Rock, CoalVein, CoalVein, CoalVein, CoalVein, SilverVein]
        grid_noise = noise.smooth_noise(self.num_cols, self.num_rows, 3)
        grid_mapping = noise.map_noise_to_ids(grid_noise, tile_types)
        self.grid = [[None for _ in line] for line in grid_mapping]
        for i, line in enumerate(grid_mapping):
            print(f"creating row {i} of {len(grid_mapping)}")
            for j, tile_type in enumerate(line):
                pos = self.__grid_to_coords__(i, j)  # row, column
                self.grid[i][j] = tile_type(self.game, pos, Vector(default.TILE_SIZE, default.TILE_SIZE))

    # def draw(self, surface):
    #     for i, line in enumerate(self.grid):
    #         for j, tile in enumerate(line):
    #             tile.draw_raw(surface, self.tile_mapping)

    def draw(self, surface):
        s = timer()
        visible_tiles = set()
        for light_field in self.game.get_fields(LightField):
            visible_tiles.update(self.get_tiles_within_radius(light_field.pos, light_field.get_radius()))
        e0 = timer()
        tiles_on_screen = []
        for row in self.get_grid_view():
            tiles_on_screen.extend(row)
        drawable_tiles = visible_tiles.intersection(set(tiles_on_screen))
        surface.blits([(self.tile_mapping.get(art_id), self.game.camera.apply(pos)) for art_id, pos in
                       map(lambda x: x.get_draw_info(), drawable_tiles)])
        e = timer()
        # print(f"gathering tiles took {e0-s} seconds")
        # print(f"blits method took {e-e0} seconds")
        # print(f"drawing tiles took {e-s} seconds")

    def get_grid_view(self):
        margin = 2 * default.TILE_SIZE
        top_left = self.get_tile(self.game.camera.inverse_apply(Vector(-margin, -margin)))
        bottom_left = self.get_tile(self.game.camera.inverse_apply(Vector(-margin, settings.SCREEN_HEIGHT + margin)))
        top_right = self.get_tile(self.game.camera.inverse_apply(Vector(settings.SCREEN_WIDTH + margin, -margin)))
        bottom_right = self.get_tile(
            self.game.camera.inverse_apply(Vector(settings.SCREEN_WIDTH + margin, settings.SCREEN_HEIGHT + margin)))

        top = top_left or top_right
        bottom = bottom_left or bottom_right
        left = top_left or bottom_left
        right = top_right or bottom_right

        if top is not None:
            i, j = self.__coords_to_grid__(top.pos)
            start_row = i
            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(top.pos), 200)
        else:
            start_row = 0

        if bottom is not None:
            i, j = self.__coords_to_grid__(bottom.pos)
            end_row = i
            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(bottom.pos), 200)
        else:
            end_row = len(self.grid)

        if left is not None:
            i, j = self.__coords_to_grid__(left.pos)
            start_col = j
            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(left.pos), 200)
        else:
            start_col = 0

        if right is not None:
            i, j = self.__coords_to_grid__(right.pos)
            end_col = j
            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(right.pos), 200)
        else:
            end_col = len(self.grid[0])

        rows = self.grid[start_row:end_row]
        return [row[start_col:end_col] for row in rows]

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

    def get_tiles_within_radius(self, point, radius):
        """
        Sample circle from 2d-list:
        Start tile_size/2 away from top and get left and right offsets, which are list slice indices.
        Continue for top - tilesize/2 - tilesize * i for line i from top, etc
        """
        ts = default.TILE_SIZE
        tiles = set()
        num_rows = int(2 * radius / ts)
        for row_num in range(num_rows):
            # find y
            y = ts * (num_rows / 2 - row_num)
            x = math.sqrt(radius ** 2 - y ** 2)

            y = y - ts / 2

            left_offset = Vector(-x, y)
            right_offset = Vector(x, y)

            i, j_left = self.__coords_to_grid__(point + left_offset)
            i, j_right = self.__coords_to_grid__(point + right_offset)

            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(point + left_offset), 2)
            # pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(point + right_offset), 2)

            if i < 0 or i >= self.num_rows:
                continue
            row = self.grid[i]
            slice_start = max(0, j_left)
            slice_stop = min(j_right, self.num_cols)
            tiles.update(row[slice_start:slice_stop])
        return tiles

    def old_get_tiles_within_radius(self, point, r_max, r_min=1):
        """Return list of all tiles with distance greater than r_min and smaller than r_max around point.
        Create circles with increasing radii. Sample each circle with a max distance smaller than tilesize.
        Radius increase also small, so no tiles can slip through
        At least consider circles with r_min and r_max, even if distance is too small.
        This method could be massively improved by sampling an outer circle and considering rows of tiles at a time.
        """
        oversampling_factor = 1.50  # at least sqrt(2) due to diagonal
        sample_distance = self.tile_size / oversampling_factor
        num_circles = int((r_max - r_min) / sample_distance)
        radii = [r_min] + [r_min + sample_distance * (i + 0.5) for i in range(num_circles)] + [r_max]
        tiles = set()
        for r in radii:
            tiles.update(self.get_tiles_on_circle(point, r, oversampling_factor))
        return tiles

    def get_tiles_on_circle(self, point, radius, oversampling_factor=1.5):
        num_samples = int(2 * math.pi * radius / self.tile_size * oversampling_factor)  # factor 1.5 for small corners
        tiles = []  # dont forget to check for None
        for i in range(num_samples):
            x = point.x + math.sin(i * (2 * math.pi) / num_samples) * radius
            y = point.y + math.cos(i * (2 * math.pi) / num_samples) * radius
            tile = self.get_tile(Vector(int(x), int(y)))

            pygame.draw.circle(self.game.surface, (255, 255, 255), self.game.camera.apply(Vector(x, y)), 2)

            if tile is not None:
                tiles.append(tile)
        return set(tiles)

    @staticmethod
    def __coords_to_grid__(point):
        x, y = point
        return math.floor(y / default.TILE_SIZE), math.floor(x / default.TILE_SIZE)

    @staticmethod
    def __grid_to_coords__(i, j):
        off = default.TILE_SIZE / 2
        return Vector(j * default.TILE_SIZE + off, i * default.TILE_SIZE + off)

    def __str__(self):
        s = ""
        for line in self.grid:
            s += " ".join(map(str, line)) + "\n"
        return s

    def __getstate__(self):
        """
        Returns the state when saving the game.
        """

        state = self.__dict__.copy()
        del state['tile_mapping']

        return state

    def __setstate__(self, state):
        """
        Restores the game state when loading the game.
        """

        self.__dict__.update(state)
        self.load_static()

    def notify(self, observable, event, *args, **kwargs):
        if isinstance(event, MiningEvent):
            event.resource.durability -= event.mining_power
            if event.resource.durability < 0:
                drops = event.resource.drops()

                if event.inventory is not None:
                    event.inventory.add_items(drops)
                    for drop in drops:
                        print(f'{observable} picked up {drop}')

                self.replace_tile(event.resource.pos, event.resource.reveals())


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
                self.tilemap[prefix] = pygame.image.load(os.path.join(art_directory, file)).convert()
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
