import pygame

import default




class ID:
    """Hands out unique ids and stores all id-d entities sorted by type"""
    id_counter = -1
    type_dict = {}

    @staticmethod
    def request_id(thing):
        if type(thing) not in ID.type_dict.keys():
            ID.type_dict[type(thing)] = []
        if not thing in ID.type_dict[type(thing)]:
            ID.type_dict[type(thing)].append(thing)
        else:
            print("ID Error: Thing is already in ID list.")
            return None
        ID.id_counter += 1
        return ID.id_counter


class Entity:
    def __init__(self, game, x=None, y=None):
        self.id = ID.request_id(self)
        self.game = game
        self.x = x
        self.y = y
        self.is_blocking = True
        self.color = (0, 0, 0)
        self.art_id = 0
        self.size = default.TILE_SIZE

    def move(self, dx, dy, require_valid_move=True):
        if not require_valid_move or self.is_valid_move(dx, dy):
            self.x += dx
            self.y += dy

    def is_valid_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        r = int(self.size / 2) - 1
        above = self.game.tile_grid.get_tile(new_x, new_y - r)
        below = self.game.tile_grid.get_tile(new_x, new_y + r)
        right = self.game.tile_grid.get_tile(new_x + r, new_y)
        left = self.game.tile_grid.get_tile(new_x - r, new_y)

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
        # print("entity default draw. overwrite")
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, 32, 32))
