from .entities import Entity
import random

class Tile(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_minable = False
        self.art_id = 0
        self.is_blocking = False


class RockFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([31, 32, 33])


class CoalFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([34, 35])

class SilverFloor(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = random.choice([36])