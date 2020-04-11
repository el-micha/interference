import pygame

import default
from effects.fields import MiningField, ViewField
from .entities import Entity
from .items import Coal
from .resources import Stone
from .tiles import RockFloor, CoalFloor


class Building(Entity):
    name = None
    description = None
    keyboard_shortcut = None
    construction_costs = []
    suitable_floors = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = []
        self.sprite = pygame.image.load("art/80_building.png")

    def draw(self, surface):
        surface.blit(self.sprite, (self.x, self.y))

    def get_sprite_size(self):
        return self.sprite.get_size()

    def set_position(self, x, y):
        self.x = x
        self.y = y

        xsprite, ysprite = self.get_sprite_size()
        for field in self.fields:
            field.x = self.x + int(xsprite / 2)
            field.y = self.y + int(ysprite / 2)

    @classmethod
    def is_affordable(cls, inventory):
        for amount, resource_cls in cls.construction_costs:
            stack = inventory.get_stack(resource_cls)
            if not stack or stack.amount < amount:
                return False

        return True

    def get_tiles_below(self):
        width, height = self.get_sprite_size()
        tiles = []
        for x in range(self.x, self.x + width, default.TILE_SIZE):
            for y in range(self.y, self.y + height, default.TILE_SIZE):
                tile = self.game.tile_grid.get_tile(x, y)
                tiles.append(tile)

        return tiles

    def is_constructable(self):
        for tile in self.get_tiles_below():
            if type(tile) not in self.suitable_floors:
                return False

        return True


class CoalDrill(Building):
    name = 'Coal Drill'
    keyboard_shortcut = 'c'
    construction_costs = [(1, Stone)]
    suitable_floors = [CoalFloor, RockFloor]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/81_coal_drill.png")

    def is_constructable(self):
        tiles = self.get_tiles_below()
        if CoalFloor not in [type(x) for x in tiles]:
            return False
        if not all([type(tile) in self.suitable_floors for tile in tiles]):
            return False
        return True

class EnergyDissipator(Building):
    name = 'Energy Dissipator'
    keyboard_shortcut = 'e'
    construction_costs = [(1, Stone), (1, Coal)]
    suitable_floors = [RockFloor, CoalFloor]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/82_energy_dissipator.png")

        xsprite, ysprite = self.get_sprite_size()
        self.fields = [
            MiningField(self.game, x=self.x + int(xsprite / 2), y=self.y + int(ysprite / 2)),
            ViewField(self.game, x=self.x + int(xsprite / 2), y=self.y + int(ysprite / 2)),
        ]

    def draw(self, surface):
        super().draw(surface)

        for field in self.fields:
            field.draw(surface)
