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

    def remove_items(self, item, amount=1):
        stack = self.get_stack(item)

        if not stack:
            raise RuntimeError('Tried to remove non-existent item from inventory.')

        if stack.amount > amount:
            stack.modify(-1 * amount)
        elif stack.amount == amount:
            self.stacks.remove(stack)
        else:
            raise RuntimeError('Tried to remove more items from inventory than available.')

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
