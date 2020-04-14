from entities.entities import Entity
import pygame
from helpers import dist

class Field(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for a circle: radius, for other forms: max distance from origin
        self.reach = 256
        self.color = (50, 50, 200, 60)
        self.active = True
        self.amplitude = 1

    def get_effect(self, pos):
        if not self.active:
            return 0
        distance = dist(self.x, self.y, pos[0], pos[1])
        if distance <= self.reach:
            return self.amplitude
        else:
            return 0

    def draw(self, surface):
        circle = pygame.Surface((self.reach * 2 + 1, self.reach * 2 + 1), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.color, (self.reach, self.reach), self.reach)
        surface.blit(circle, (self.x - self.reach, self.y - self.reach))

class EnergyField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amplitude = 2
