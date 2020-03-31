import pygame
import math
import random

from .entities import Entity


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = (200, 100, 200)
        self.radius = 12
        self.curr_radius = 16

    def tick(self, tick):
        self.curr_radius = 6 + int(self.radius * (1 + math.sin(tick / 30.0))/2)
        r,g,b = self.color
        r = max(0, min(int(r + (random.random() - random.random()) * 5), 255))
        g = max(0, min(int(g + (random.random() - random.random()) * 5), 255))
        b = max(0, min(int(b + (random.random() - random.random()) * 5), 255))
        self.color = (r,g,b)

    def draw(self, surface):
        pygame.draw.circle(surface, (255,255,0), (self.x, self.y), self.curr_radius+1)
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.curr_radius)
