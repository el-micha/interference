import pygame
from helpers import *
import default


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
    - a size = (width, height)
    - a draw function which respects sprite size and world coords
    """
    def __init__(self, game, pos=(64, 64), size=None):
        self.id = ID.request_id(self)
        self.game = game
        self.pos = pos
        self.size = size
        if self.size is None:
            self.size = default.TILE_SIZE, default.TILE_SIZE
        self.sprite = pygame.Surface(self.size, pygame.SRCALPHA)
        self.sprite.fill((255,255,0,128))

        # properties
        self.width = property(self.size[0])
        self.height = property(self.size[1])
        self.x = property(self.pos[0])
        self.y = property(self.pos[1])

    def intersects(self, point):
        """Assume a rectangular form around self.pos. Overwrite this if round or other form."""
        left = self.pos[0] - self.width / 2
        right = self.pos[0] + self.width / 2
        top = self.pos[1] - self.height / 2
        bottom = self.pos[1] + self.height / 2
        return left <= point[0] <= right and top <= point[1] <= bottom

    def move(self, delta, require_valid_move=True):
        if not require_valid_move or self.is_valid_move(delta):
            self.pos = add(self.pos, delta)

    def is_valid_move(self, delta):
        new_x, new_y = add(self.pos, delta)

        r = int(self.size[0] / 2) - 1
        above = self.game.tile_grid.get_tile((new_x, new_y - r))
        below = self.game.tile_grid.get_tile((new_x, new_y + r))
        right = self.game.tile_grid.get_tile((new_x + r, new_y))
        left = self.game.tile_grid.get_tile((new_x - r, new_y))

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
        draw_pos = round(sub(self.pos, times(self.size, 0.5)))
        surface.blit(self.sprite, draw_pos)

