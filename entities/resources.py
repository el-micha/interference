from entities.tiles import Tile


class Resource(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.durability = 100
        self.is_minable = True
        self.item_drops = []
        self.color = (192, 192, 192)
        self.is_blocking = True


class Stone(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 2


class Cole(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 15


class Silver(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.art_id = 25
