from entities.entities import Entity
import pygame


class Field(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for a circle: radius, for other forms: max distance from origin
        self.reach = 256
        self.color = (50, 50, 200, 60)
        self.active = True

    def draw(self, surface):
        circle = pygame.Surface((self.reach * 2 + 1, self.reach * 2 + 1), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.color, (self.reach, self.reach), self.reach)
        surface.blit(circle, (self.x - self.reach, self.y - self.reach))

class EnergyField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mining_factor = 4
        self.view_factor = 2
