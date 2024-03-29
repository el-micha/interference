from itertools import chain

import pygame
import default
from entities.coordinates import Vector
from effects.visuals import Sprite
from effects.fields import LightField, EnergyField


class ID:
    """Hands out unique ids and stores all id-d entities sorted by type"""
    id_counter = -1
    type_dict = {}

    @staticmethod
    def request_id(thing):
        if type(thing) not in ID.type_dict.keys():
            ID.type_dict[type(thing)] = []
        if thing not in ID.type_dict[type(thing)]:
            ID.type_dict[type(thing)].append(thing)
        else:
            print("ID Error: Thing is already in ID list.")
            return None
        ID.id_counter += 1
        return ID.id_counter


class Entity(object):
    """
    An entity has:
    - a position in world coordinates pos = (x, y)
    - a size = (width, height) # rougly the collision box
    - a draw function which respects sprite size and world coords

    - sprite
    self.sprite = SpriteLoader.get("character_sprite")
    """

    def __init__(self, game, pos: Vector, size: Vector, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = ID.request_id(self)
        self.game = game
        self.pos = pos  # considdle: .set or =, that is the riddle
        self.size = size
        self.sprite = None
        self.load_static()

    def load_static(self):
        if self.size is None:
            self.size = Vector(default.TILE_SIZE, default.TILE_SIZE)

        self.load_static_sprite()

    def load_static_sprite(self):
        if hasattr(self, 'sprite_art'):
            self.sprite = pygame.image.load(self.sprite_art)
            self.size = Vector(*self.sprite.get_size())
        else:
            # Default sprite
            self.sprite = pygame.Surface(self.size.round(), pygame.SRCALPHA)
            self.sprite.fill((255, 255, 0, 128))

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    def get_tiles_below(self):
        x_min, y_min = (self.pos - self.size * 0.5).round()
        x_max, y_max = (self.pos + self.size * 0.5).round()
        tiles = set()
        for x in chain([x_max-1], range(x_min, x_max, default.TILE_SIZE)):
            for y in chain([y_max-1], range(y_min, y_max, default.TILE_SIZE)):
                tile = self.game.tile_grid.get_tile(Vector(x, y))
                tiles.add(tile)

        return list(tiles)

    def intersects(self, point):
        """Assume a rectangular form around self.pos. Overwrite this if round or other form."""
        left = self.pos.x - self.width / 2
        right = self.pos.x + self.width / 2
        top = self.pos.y - self.height / 2
        bottom = self.pos.y + self.height / 2
        return left <= point[0] <= right and top <= point[1] <= bottom

    def move(self, delta, require_valid_move=True):
        # pos assignment changes referenced object, so other references become stale. use pos.set().
        if not require_valid_move or self.is_valid_move(delta):
            self.pos.set(self.pos + delta)

    def is_valid_move(self, delta):
        new_x, new_y = self.pos + delta

        r = int(self.size.x / 2) - 1
        above = self.game.tile_grid.get_tile(Vector(new_x, new_y - r))
        below = self.game.tile_grid.get_tile(Vector(new_x, new_y + r))
        right = self.game.tile_grid.get_tile(Vector(new_x + r, new_y))
        left = self.game.tile_grid.get_tile(Vector(new_x - r, new_y))

        if above and above.is_blocking:
            return False
        elif below and below.is_blocking:
            return False
        elif right and right.is_blocking:
            return False
        elif left and left.is_blocking:
            return False

        return True

    def is_visible(self):
        light_fields = self.game.get_fields(LightField)
        for field in light_fields:
            if field.get_effect(self.pos) > 0:
                return True
        return False

    def get_available_energy(self):
        energy = 0
        for field in self.game.get_fields(EnergyField):
            energy += field.get_effect(self.pos)
        return energy

    def draw(self, surface):
        if isinstance(self.sprite, pygame.Surface):
            sprite_size = Vector(*self.sprite.get_size())
            draw_pos = self.pos - (sprite_size * 0.5)
            surface.blit(self.sprite, self.game.camera.apply(draw_pos))
        elif isinstance(self.sprite, Sprite):
            self.sprite.draw(surface, self.game.camera.apply(self.pos))
        else:
            print("Entity.draw expects a sprite or overwriting of draw.")

    def __getstate__(self):
        """
        Returns the state when saving the game.
        """

        state = self.__dict__.copy()

        if 'sprite' in state:
            del state['sprite']

        return state

    def __setstate__(self, state):
        """
        Restores the game state when loading the game.
        """

        self.__dict__.update(state)
        self.load_static()
