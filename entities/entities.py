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
    def __init__(self, game, pos=None, size=None):
        self.id = ID.request_id(self)
        self.game = game
        self.pos = pos
        self.size = size
        if self.size is None:
            self.size = default.TILE_SIZE, default.TILE_SIZE
        self.width, self.height = self.size
        # is overlapping
        # tiles underneath

        self.color = (123, 234, 56)


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
        pygame.draw.rect(surface, self.color, pygame.Rect(draw_pos[0], draw_pos[1], self.width, self.height))
