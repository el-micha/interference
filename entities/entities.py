import pygame
import default
from entities.coordinates import Vector
from effects.visuals import Sprite

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
        self.pos = pos
        self.size = size
        if self.size is None:
            self.size = Vector(default.TILE_SIZE, default.TILE_SIZE)
        # default sprite
        self.sprite = pygame.Surface(self.size.round(), pygame.SRCALPHA)
        self.sprite.fill((255,255,0,128))

        # properties
        self.width = property(self.size.x)
        self.height = property(self.size.y)

    def get_tiles_below(self):
        w, h = self.size * 0.5
        tiles = []
        for x in range(self.pos.x - w, self.pos.x + w, default.TILE_SIZE):
            for y in range(self.pos.y - h , self.pos.y + h, default.TILE_SIZE):
                tile = self.game.tile_grid.get_tile(Vector(x, y))
                tiles.append(tile)
        return tiles

    def intersects(self, point):
        """Assume a rectangular form around self.pos. Overwrite this if round or other form."""
        left = self.pos.x - self.width / 2
        right = self.pos.x + self.width / 2
        top = self.pos.y - self.height / 2
        bottom = self.pos.y + self.height / 2
        return left <= point[0] <= right and top <= point[1] <= bottom

    def move(self, delta, require_valid_move=True):
        if not require_valid_move or self.is_valid_move(delta):
            self.pos = self.pos + delta

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

    def draw(self, surface):
        if isinstance(self.sprite, pygame.Surface):
            draw_pos = (self.pos - (self.size * 0.5)).round()
            surface.blit(self.sprite, draw_pos)
        elif isinstance(self.sprite, Sprite):
            self.sprite.draw(surface, self.pos)
        else:
            print("Entity.draw expects a sprite or overwriting of draw.")

