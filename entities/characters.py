import pygame

import default
from .entities import Entity


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = (200, 100, 200)
        self.size = int(default.TILE_SIZE / 2)

    def draw(self, surface):
        r = int(self.size / 2)
        pygame.draw.circle(surface, self.color, (self.x + r, self.y + r), r)
