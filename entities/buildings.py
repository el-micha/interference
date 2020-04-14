import pygame

import default
from effects.fields import EnergyField
from .entities import Entity
from .items import Coal
from .resources import Stone
from .tiles import RockFloor, CoalFloor
from helpers import dist

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

    def get_size(self):
        return self.sprite.get_size()

    def set_position(self, x, y):
        self.x = x
        self.y = y

        xsprite, ysprite = self.get_size()
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
        width, height = self.get_size()
        tiles = []
        for x in range(self.x, self.x + width, default.TILE_SIZE):
            for y in range(self.y, self.y + height, default.TILE_SIZE):
                tile = self.game.tile_grid.get_tile(x, y)
                tiles.append(tile)
        return tiles

    def is_constructable(self):
        return self.is_floor_suitable() and not self.is_floor_blocked()

    def is_floor_suitable(self):
        for tile in self.get_tiles_below():
            if type(tile) not in self.suitable_floors:
                return False

        return True

    def is_floor_blocked(self):
        for tile in self.get_tiles_below():
            if tile.is_blocking:
                return True

        return False

    def make_floor_blocking(self):
        for tile in self.get_tiles_below():
            tile.is_blocking = True


class CoalDrill(Building):
    """
    A basic dissipator should burn 1 coal item per tick, that is about 60 per second.
    A single coalDrill should power up to 3 dissipators, so it should produce at least 3/tick.
    A simple mining field buff should enable a drill to serve 4 dissipators, so the buff should tip the
    output just over 4 items/tick.

    """
    name = 'Coal Drill'
    keyboard_shortcut = 'c'
    construction_costs = [(1, Stone)]
    suitable_floors = [CoalFloor, RockFloor]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = pygame.image.load("art/81_coal_drill.png")

        # resources per tick
        self.base_mining_rate = 3
        self.stored_res = 0
        self.capacity = self.base_mining_rate * 60 * 3 # 3 seconds until storage full
        #self.distribution_rate = 9999999 # should probably be limited or deleted

    def tick(self, tick):
        # these two could be generalized if we need more kinds of drills, hence res instead of coal
        self.mine_resources()
        self.distribute_resources()

    def mine_resources(self):
        self.stored_res = min(self.stored_res + self.get_mining_rate(), self.capacity)

    def distribute_resources(self):
        # calculate fair share for each consumer
        # give to fullest consumer first, and if they cannot take their whole fair share, split the rest for the other consumers
        consumers = list(sorted(self.get_consumers(), key=lambda c: -c.stored_coal))
        remaining_consumers = len(consumers)
        fair_share = self.stored_res / remaining_consumers
        for consumer in consumers:
            actual_share = int(min(fair_share, consumer.coal_capacity - consumer.stored_coal))
            consumer.stored_coal += actual_share
            self.stored_res -= actual_share
            remaining_consumers -= 1
            fair_share += (fair_share - actual_share) / max(1, remaining_consumers) # lazy way to prevent /0

    def get_consumers(self):
        cons = [x for x in self.get_neighbours() if hasattr(x, "stored_coal")]
        print(f"found {len(cons)} consumers")
        return cons

    def get_neighbours(self):
        neigh = []
        for building in set(self.game.buildings) - set(self):
            # TODO: implement real neighbourhood
            if dist(self.x, self.y, building.x, building.x) < 32 * 3:
                neigh.append(building)
        print(f"found {len(neigh)} neighbours")
        return neigh

    def get_mining_rate(self):
        return self.base_mining_rate

    def is_floor_suitable(self):
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

        xsprite, ysprite = self.get_size()
        self.fields = [
            EnergyField(self.game, x=self.x + int(xsprite / 2), y=self.y + int(ysprite / 2)),
        ]

        self.stored_coal = 0
        self.coal_capacity = 60
        self.coal_consumption = 1

    def tick(self, tick):
        available_energy = self.stored_coal / self.coal_consumption
        if available_energy > 1:
            self.stored_coal -= self.coal_consumption
            self.set_fields(True)
        else:
            print("not enough fuel to dissipate")
            self.set_fields(False)

    def set_fields(self, active):
        for field in self.fields:
            field.is_active = active

    def draw(self, surface):
        super().draw(surface)

        for field in self.fields:
            if not field.active:
                continue
            field.draw(surface)
