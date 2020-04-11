import random

from entities.items import Stone, Coal, Silver, Crystal
from entities.tiles import Tile, RockFloor, CoalFloor, SilverFloor


class Resource(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.durability = 100
        self.is_minable = True
        self.item_drops = []
        self.color = (192, 192, 192)
        self.is_blocking = True

    def drops(self):
        result = []
        for drop in self.item_drops:
            if random.uniform(0, 1) < drop.rate:
                result.append(drop.item_cls(self.game))

        return result

    def reveals(self):
        """When mined, this new Tile type is exposed"""
        return RockFloor(self.game, self.x, self.y)


class DropRate:
    def __init__(self, item_cls, rate):
        self.item_cls = item_cls
        self.rate = rate


class Rock(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_drops = [DropRate(Stone, 1.0), DropRate(Crystal, 0.1)]
        self.art_id = 15


class CoalOre(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_drops = [DropRate(Coal, 1.0)]
        self.art_id = 2

    def reveals(self):
        return CoalFloor(self.game, self.x, self.y)


class SilverOre(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.item_drops = [DropRate(Silver, 1.0)]
        self.art_id = 25

    def reveals(self):
        new = random.choice([RockFloor, RockFloor, RockFloor, SilverFloor])
        return new(self.game, self.x, self.y)
