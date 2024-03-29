from effects.fields import EnergyField, LightField
from .entities import Entity
from .items import Coal
from .resources import Stone
from .tiles import RockFloor, CoalFloor
from entities.coordinates import Vector


class Building(Entity):
    name = None
    description = None
    keyboard_shortcut = None
    construction_costs = []
    suitable_floors = []
    sprite_art = 'art/80_building.png'

    def __init__(self, *args, **kwargs):
        super().__init__(size=None, *args, **kwargs)

        self.fields = []

        self.adjacent_buildings = []
        self._tiles_below = None

    def tick(self, tick):
        pass

    def set_position(self, pos):
        self.pos.set(pos)

    @classmethod
    def is_affordable(cls, inventory):
        for amount, resource_cls in cls.construction_costs:
            stack = inventory.get_stack(resource_cls)
            if not stack or stack.amount < amount:
                return False
        return True

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
            tile.highlighted = True

    def link_with_floor(self):
        for tile in self.get_tiles_below():
            tile.blocked_by = self
            tile.highlighted = True

    def get_tiles_below(self):
        if self._tiles_below is None:
            self._tiles_below = super().get_tiles_below()
        return self._tiles_below

    def get_neighbours(self):
        return self.adjacent_buildings

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
    sprite_art = 'art/81_coal_drill.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # resources per tick
        self.base_mining_rate = 3
        self.stored_res = 0
        self.capacity = self.base_mining_rate * 60 * 3 # 3 seconds until storage full
        #self.distribution_rate = 9999999 # should probably be limited or deleted

        self.light_field = LightField(self.game, self, self.pos, 50)

    def tick(self, tick):
        # self.print_stats()
        # these two could be generalized if we need more kinds of drills, hence res instead of coal
        self.mine_resources()
        self.distribute_resources()

    def mine_resources(self):
        self.stored_res = min(self.stored_res + self.get_mining_rate(), self.capacity)

    def distribute_resources(self):
        # calculate fair share for each consumer
        # give to fullest consumer first, and if they cannot take their whole fair share, split the rest for the other consumers
        consumers = list(sorted(self.get_consumers(), key=lambda c: -c.stored_coal))
        if len(consumers) == 0:
            return
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
        #print(f"found {len(cons)} consumers")
        return cons

    def print_stats(self):
        print(f"- - - Coal drill {self.id}: - - -")
        print(f"stored res: {self.stored_res}")

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
    sprite_art = 'art/82_energy_dissipator.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields = [
            EnergyField(self.game, self, self.pos, 256),
            LightField(self.game, self, self.pos, 50)
        ]

        self.stored_coal = 0
        self.coal_capacity = 60
        self.coal_consumption = 1

    def tick(self, tick):
        # self.print_stats()
        available_energy = self.stored_coal / self.coal_consumption
        if available_energy > 1:
            self.stored_coal -= self.coal_consumption
            self.set_fields(True)
        else:
            print("not enough fuel to dissipate")
            self.set_fields(False)

    def set_fields(self, active):
        for field in self.fields:
            field.active = active

    def print_stats(self):
        print(f"- - - Energy dissipator {self.id}: - - -")
        print(f"stored coal: {self.stored_coal}")
        print(f"coal capacity: {self.coal_capacity}")
        print(f"coal consumption: {self.coal_consumption}")

    def draw(self, surface):
        super().draw(surface)


class Furnace(Building):
    name = 'Furnace'
    keyboard_shortcut = 'f'
    construction_costs = [(1, Stone)]
    suitable_floors = [RockFloor, CoalFloor]
    sprite_art = 'art/87_furnace.png'


class Workshop(Building):
    name = 'Workshop'
    keyboard_shortcut = 'k'
    construction_costs = [(1, Stone)]
    suitable_floors = [RockFloor, CoalFloor]
    sprite_art = 'art/83_workshop.png'


class IronDrill(Building):
    name = 'Iron Drill'
    keyboard_shortcut = 'l'
    construction_costs = [(1, Stone)]
    suitable_floors = [RockFloor, CoalFloor]
    sprite_art = 'art/85_iron_drill.png'


class PartsProcessor(Building):
    name = 'Parts Processor'
    keyboard_shortcut = 'p'
    construction_costs = [(1, Stone)]
    suitable_floors = [RockFloor, CoalFloor]
    sprite_art = 'art/84_processor.png'


class Assembly(Building):
    name = 'Assembly'
    keyboard_shortcut = 'm'
    construction_costs = [(1, Stone)]
    suitable_floors = [RockFloor, CoalFloor]
    sprite_art = 'art/86_assembly.png'
