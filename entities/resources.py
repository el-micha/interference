from entities.tiles import Tile


class Resource(Tile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_minable = True
        self.item_drops = []
        self.color = (192, 192, 192)
