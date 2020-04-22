from entities.entities import Entity
from effects.visuals import Sprite, ExplosionSprite

class Explosion(Entity):

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = ExplosionSprite(self.game, self.pos)
        self.radius = 0
        self.max_radius = 200
        self.growth = 1
        self.active = True

    def draw(self, surface):
        if self.active:
            self.sprite.draw(surface)

    def tick(self, tick):
        if not self.active:
            return
        self.radius += 1
        tiles = self.game.tile_grid.get_tiles_within_radius(self.pos, self.radius)
        for tile in tiles:
            if hasattr(tile, "durability"):
                tile.durability = 1
        if self.radius >= self.max_radius:
            self.active = False
