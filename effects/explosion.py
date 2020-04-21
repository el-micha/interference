from entities.entities import Entity
from effects.visuals import Sprite, ExplosionSprite

class Explosion(Entity):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.sprite = ExplosionSprite(self.game, self.pos)

    def draw(self, surface):
        self.sprite.draw(surface)

    def tick(self, tick):
        pass