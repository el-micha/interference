from entities.coordinates import Vector
from entities.items import Coal, Stone
from .entities import Entity
from .inventories import Inventory
from effects.fields import LightField
from events.events import MiningEvent, EventAggregator


class Character(Entity):
    sprite_art = 'art/12_character.png'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inventory = Inventory()
        self.inventory.add_items([Coal(), Stone()]*10)

        self.color = (255, 255, 0)
        self.reach = 64 + 64
        self.base_mining_power = 200
        # self.base_view_distance = 200

        self.light_field = LightField(self.game, self, pos=self.pos, radius=500)
        self.game.add_field(self.light_field)

    # def get_view_distance(self):
    #     view_field_factors = 1 + self.get_available_energy()
    #     return self.base_view_distance * view_field_factors

    def get_mining_power(self):
        mining_field_factors = 1 + self.get_available_energy() * 2
        return self.base_mining_power * mining_field_factors

    def mine(self, resource):
        distance = Vector.dist(self.pos, resource.pos)

        if resource.is_mineable and distance < self.game.character.reach:
            EventAggregator.notify(MiningEvent(resource, self.get_mining_power(), self.inventory), self)

    def construct(self, building):
        if not self.can_construct(building):
            return

        for amount, resource_cls in building.construction_costs:
            self.inventory.remove_items(resource_cls, amount)

        building.make_floor_blocking()
        building.link_with_floor()
        self.game.add_building(building)

    def can_construct(self, building):
        if not building.is_affordable(self.inventory):
            return False

        if not building.is_constructable():
            return False

        if any(t in self.get_tiles_below() for t in building.get_tiles_below()):
            return False

        distance = Vector.dist(self.pos, building.pos)
        if self.reach < distance:
            return False

        return True
