from .entities import Entity
import random
from entities.coordinates import Vector
import default
import pygame


class Tile(Entity):
    def __init__(self, game, pos, size=Vector(default.TILE_SIZE, default.TILE_SIZE), *args, **kwargs):
        super().__init__(game, pos, size=size, *args, **kwargs)

        self.is_mineable = False
        self.art_id = 0
        self.is_blocking = False
        self.blocked_by = None

        # debug
        self.highlighted = False

    # draw, draw_raw a temporary hack to have both options to determine visibility available...
    def draw(self, surface, tile_mapping):
        if not self.is_visible():
            return
        self.draw_raw(surface, tile_mapping)
        #if self.highlighted:
        #    a,b = self.game.camera.apply(self.pos - self.size * 0.5)
        #    c,d = self.game.camera.apply(self.pos + self.size * 0.5)
        #    pygame.draw.rect(surface, (200,200,200), pygame.Rect(a,b,c,d))

    def draw_raw(self, surface, tile_mapping):
        self.sprite = tile_mapping.get(self.art_id)
        super().draw(surface)
        # healthbar TODO: move this somewhere more appropriate...
        if hasattr(self, "durability") and self.durability < 100:
            max_bar_length = self.size.x * 0.9
            y_position = self.size.y * 0.5 * 0.7
            start = self.pos - Vector(max_bar_length * 0.5, -y_position)
            max_end = start + Vector(max_bar_length, 0)
            end = start + Vector(max_bar_length * self.durability * 0.01, 0)
            pygame.draw.line(surface, (200, 0, 0), self.game.camera.apply(start), self.game.camera.apply(max_end), 3)
            pygame.draw.line(surface, (200, 200, 100), self.game.camera.apply(start), self.game.camera.apply(end), 3)

    def get_draw_info(self):
        return self.art_id, self.pos - self.size * 0.5

    def is_adjacent_to(self, other_tile):
        return Vector.dist(self.pos, other_tile.pos) < default.TILE_SIZE * 1.42 # diagonals

class RockFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([31, 32, 33])


class CoalFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([34, 35])


class SilverFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([36])


class IronFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([37])
