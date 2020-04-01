from .entities import Entity


class Tile(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_minable = False
        self.art_id = 0
        self.is_blocking = False
