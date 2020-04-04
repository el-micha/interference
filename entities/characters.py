import pygame

import default
from .entities import Entity


class Character(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.inventory = Inventory()

        self.color = (255, 255, 0)
        self.size = int(default.TILE_SIZE / 2)
        self.reach = 64 + 64

    def draw(self, surface):
        r = int(self.size / 2)
        pygame.draw.circle(surface, self.color, (self.x, self.y), r)


class Inventory:
    def __init__(self):
        self.stacks = []

    def get_stack(self, item):
        for stack in self.stacks:
            if stack.item.__class__ == item.__class__:
                return stack

        return None

    def add_item(self, item):
        stack = self.get_stack(item)
        if stack and item.is_stackable:
            stack.modify(1)
        else:
            stack = ItemStack(item, amount=1)
            self.stacks.append(stack)

    def remove_item(self, item):
        stack = self.get_stack(item)

        if not stack:
            raise RuntimeError('Tried to remove non-existent item from inventory.')

        if stack.amount > 1:
            stack.modify(-1)
        else:
            self.stacks.remove(stack)

    def print(self):
        for stack in self.stacks:
            print(f'{stack.item}: {stack.amount}')


class ItemStack:
    def __init__(self, item, amount=1):
        self.item = item
        self.amount = amount

    def modify(self, amount):
        self.amount += amount
