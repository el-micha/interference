from entities.tiles import Tile


class Resource(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.durability = 100
        self.is_minable = True
        self.item_drops = []
        self.color = (192, 192, 192)
        self.is_blocking = True


class Rock(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 2


class ColeOre(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 15


class SilverOre(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 25
