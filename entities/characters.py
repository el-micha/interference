import pygame

import default
from effects.fields import MiningField, ViewField
from helpers import dist
from .entities import Entity


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
        view_field_factors = self.__get_field_factors__(ViewField, 'view_factor')
        return self.view_distance * view_field_factors

    def get_mining_power(self):
        mining_field_factors = self.__get_field_factors__(MiningField, 'mining_factor')
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

    def draw(self, surface):
        r = int(self.size / 2)
        pygame.draw.circle(surface, self.color, (self.x, self.y), r)


class Inventory:
    def __init__(self):
        self.stacks = []

    def get_stack(self, item):
        for stack in self.stacks:
            if stack.item.__class__ == item.__class__ or stack.item.__class__ == item:
                return stack

        return None

    def add_item(self, item):
        stack = self.get_stack(item)
        if stack and item.is_stackable:
            stack.modify(1)
        else:
            stack = ItemStack(item, amount=1)
            self.stacks.append(stack)

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    def remove_item(self, item):
        stack = self.get_stack(item)

        if not stack:
            raise RuntimeError('Tried to remove non-existent item from inventory.')

        if stack.amount > 1:
            stack.modify(-1)
        else:
            self.stacks.remove(stack)

    def print(self):
        items = ''
        for stack in self.stacks:
            items += f'{stack.amount} {stack.item}, '

        print(f'Inventory: {items}')


class ItemStack:
    def __init__(self, item, amount=1):
        self.item = item
        self.amount = amount

    def modify(self, amount):
        self.amount += amount
