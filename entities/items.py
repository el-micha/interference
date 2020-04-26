


class Item:
    name = None
    description = None

    is_stackable = False
    is_consumable = False

    def __str__(self):
        return self.name


class Coal(Item):
    name = 'Coal'
    description = 'Coal is mined from Coal ore.'

    is_stackable = True
    is_consumable = False


class Stone(Item):
    name = 'Stone'
    description = 'Stones are mined from rocks.'

    is_stackable = True
    is_consumable = False


class Silver(Item):
    name = 'Silver'
    description = 'Can be used against vampires.'

    is_stackable = True
    is_consumable = False


class Crystal(Item):
    name = 'Crystal'
    description = 'A very rare item.'

    is_stackable = False
    is_consumable = False


class IronOre(Item):
    name = 'Iron Ore'
    description = 'Smelt in a furnace to get Iron.'

    is_stackable = True
    is_consumable = False


class Iron(Item):
    name = 'Raw Iron'
    description = 'Smelt in a furnace to get Iron.'

    is_stackable = True
    is_consumable = False


class Parts(Item):
    name = 'Machine Parts'
    description = 'Needed to build machines.'

    is_stackable = True
    is_consumable = False


class Tools(Item):
    name = 'Set of tools'
    description = 'Use in a workshop to craft machine parts.'

    is_stackable = True
    is_consumable = False



