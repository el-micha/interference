import pygame

from effects.fields import Field
from .entities import Entity
from .items import Coal
from .resources import Stone


class Building(Entity):
    name = None
    description = None
    keyboard_shortcut = None
    construction_costs = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/80_building.png")

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

    def __get_sprite_size__(self):
        return self.sprite.get_size()

    @classmethod
    def is_affordable(cls, inventory):
        for amount, resource_cls in cls.construction_costs:
            stack = inventory.get_stack(resource_cls)
            if not stack or stack.amount < amount:
                return False

        return True


class CoalDrill(Building):
    name = 'Coal Drill'
    keyboard_shortcut = 'c'
    construction_costs = [(10, Stone)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/81_coal_drill.png")


class EnergyDissipator(Building):
    name = 'Energy Dissipator'
    keyboard_shortcut = 'e'
    construction_costs = [(5, Stone), (10, Coal)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/82_energy_dissipator.png")

        xsprite, ysprite = self.__get_sprite_size__()
        self.field = Field(self.game, x=self.x + int(xsprite / 2), y=self.y + int(ysprite / 2))

    def draw(self, surface):
        super().draw(surface)
        self.field.draw(surface)
