from itertools import chain

import pygame
import default
from entities.coordinates import Vector
from effects.visuals import Sprite
from effects.fields import Field, LightField, EnergyField


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


class Entity:
    """
    An entity has:
    - a position in world coordinates pos = (x, y)
    - a size = (width, height) # rougly the collision box
    - a draw function which respects sprite size and world coords

    - sprite
    self.sprite = SpriteLoader.get("character_sprite")
    """

    def __init__(self, game, pos: Vector, size: Vector):
        self.id = ID.request_id(self)
        self.game = game
        self.pos = pos  # considdle: .set or =, that is the riddle
        self.size = size
        if self.size is None:
            self.size = Vector(default.TILE_SIZE, default.TILE_SIZE)
        # default sprite
        self.sprite = pygame.Surface(self.size.round(), pygame.SRCALPHA)
        self.sprite.fill((255, 255, 0, 128))

        # properties
        self.width = property(self.size.x)
        self.height = property(self.size.y)

    def get_tiles_below(self):
        w, h = (self.size * 0.5).round()
        px, py = self.pos.round()

        x_min = px - w
        x_max = px + w
        y_min = py - h
        y_max = py + h

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
        if not require_valid_move or self.is_valid_move(delta):
            # self.pos = self.pos + delta changes self.pos object,
            # so fields and other stuff referencing character's pos object
            # are not changed unless we change pos' x,y manually
            self.pos.set(self.pos + delta)
            # self.pos = self.pos + delta

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
        light_fields = Field.get_fields_of_type(LightField)
        for field in light_fields:
            if field.get_effect(self.pos) > 0:
                return True
        return False

    def get_available_energy(self):
        energy = 0
        for field in Field.get_fields_of_type(EnergyField):
            energy += field.get_effect(self.pos)
        return energy

    def draw(self, surface):
        if isinstance(self.sprite, pygame.Surface):
            # TODO: using spritesize now, is this always correct?
            sprite_size = Vector(*self.sprite.get_size())
            draw_pos = (self.pos - (sprite_size * 0.5)).round()
            surface.blit(self.sprite, draw_pos)
        elif isinstance(self.sprite, Sprite):
            self.sprite.draw(surface, self.pos)
        else:
            print("Entity.draw expects a sprite or overwriting of draw.")
