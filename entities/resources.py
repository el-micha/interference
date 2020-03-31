from entities.tiles import Tile


class Resource(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_minable = True
        self.item_drops = []
        self.color = (192, 192, 192)


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
