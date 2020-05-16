import pygame

import default
import settings
from entities.coordinates import Vector


class Camera:
    def __init__(self):
        self.offset = Vector(0, 0)

    def focus(self, world_coords):
        self.offset = world_coords - Vector(settings.SCREEN_WIDTH / 2, settings.SCREEN_HEIGHT / 2)

    def scroll(self, world_coords):
        """Makes sure that `world_coords` are always visible within camera."""
        distance = world_coords - self.offset

        if distance.x < default.CAMERA_THRESHOLD:
            self.offset.x -= default.CAMERA_THRESHOLD
        elif distance.x > settings.SCREEN_WIDTH - default.CAMERA_THRESHOLD:
            self.offset.x += default.CAMERA_THRESHOLD

        if distance.y < default.CAMERA_THRESHOLD:
            self.offset.y -= default.CAMERA_THRESHOLD
        elif distance.y > settings.SCREEN_HEIGHT - default.CAMERA_THRESHOLD:
            self.offset.y += default.CAMERA_THRESHOLD

    def apply(self, world_coords):
        """Projects `world_coords` to pygame screen positions."""
        return int(world_coords.x - self.offset.x), int(world_coords.y - self.offset.y)

    def inverse_apply(self, screen_coords):
        """Projects pygame screen positions to `world_coords`."""
        return int(screen_coords.x + self.offset.x), int(screen_coords.y + self.offset.y)

    def get_mouse_coords(self):
        """Projects the pygame mouse position to world coordinates"""
        mx, my = pygame.mouse.get_pos()
        return Vector(mx + self.offset.x, my + self.offset.y)
