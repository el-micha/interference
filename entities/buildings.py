from entities.entities import Entity
import pygame
from effects.fields import Field

class Building(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/80_building.png")

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

    def __get_sprite_size__(self):
        return self.sprite.get_size()

class CoalDrill(Building):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/81_coal_drill.png")


class EnergyDissipator(Building):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/82_energy_dissipator.png")

        xsprite, ysprite = self.__get_sprite_size__()
        self.field = Field(self.game, x=self.x + int(xsprite/2), y=self.y + int(ysprite/2))

    def draw(self, surface):
        super().draw(surface)
        self.field.draw(surface)

