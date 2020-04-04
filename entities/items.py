
from .entities import Entity


class Item(Entity):
    name = None
    description = None

    is_stackable = False
    is_consumable = False

    def __str__(self):
        return self.name


class Cole(Item):
    name = 'Cole'
    description = 'Cole is mined from cole ore.'

    is_stackable = True
    is_consumable = False


class Stone(Item):
    name = 'Stone'
    description = 'Stones are mined from rocks.'

    is_stackable = True
    is_consumable = False
