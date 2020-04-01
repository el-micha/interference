import pygame

import default
from .entities import Entity


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = (255, 255, 0)
        self.size = int(default.TILE_SIZE / 2)
        self.reach = 64

    def draw(self, surface):
        r = int(self.size / 2)
        pygame.draw.circle(surface, self.color, (self.x, self.y), r)
