import pygame

from .entities import Entity


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = (200, 100, 200)
