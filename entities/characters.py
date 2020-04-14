import pygame

import default
from effects.fields import EnergyField
from helpers import dist
from .entities import Entity
from .inventories import Inventory


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inventory = Inventory()

        self.color = (255, 255, 0)
        self.size = int(default.TILE_SIZE / 2)
        self.reach = 64 + 64
        self.mining_power = 2
        self.view_distance = 100

    def get_view_distance(self):
        view_field_factors = self.__get_field_factors__(EnergyField, 'view_factor')
        return self.view_distance * view_field_factors

    def get_mining_power(self):
        mining_field_factors = self.__get_field_factors__(EnergyField, 'mining_factor')
        return self.mining_power * mining_field_factors

    def __get_field_factors__(self, field_type, factor_attr):
        factor = 1
        for b in self.game.buildings:
            for field in b.fields:
                if isinstance(field, field_type):
                    if dist(self.x, self.y, b.x, b.y) < field.reach:
                        factor += getattr(field, factor_attr)
        return factor

    def mine(self, resource):
        distance = dist(self.x, self.y, resource.x + default.TILE_SIZE / 2, resource.y + default.TILE_SIZE / 2)

        if resource.is_minable and distance < self.game.character.reach:
            resource.durability -= self.get_mining_power()
            if resource.durability < 0:
                drops = resource.drops()
                for drop in drops:
                    print(f'Picked up {drop}')
                self.inventory.add_items(drops)

                self.game.tile_grid.replace_tile(resource.x, resource.y, resource.reveals())

    def construct(self, building):
        if not self.can_construct(building):
            return

        for amount, resource_cls in building.construction_costs:
            self.inventory.remove_items(resource_cls, amount)

        building.make_floor_blocking()
        self.game.buildings.append(building)

    def can_construct(self, building):
        if not building.is_affordable(self.inventory):
            return False

        if not building.is_constructable():
            return False

        distance = dist(self.x, self.y, building.x, building.y)
        if self.reach < distance:
            return False

        return True

    def draw(self, surface):
        r = int(self.size / 2)
        pygame.draw.circle(surface, self.color, (self.x, self.y), r)
