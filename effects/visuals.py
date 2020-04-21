from entities.entities import Entity
import pygame


class Sprite(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, surface):
        pass

class ExplosionSprite(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = 10
        self.color = (240, 200, 20, 128)
        self.sprites = self.circles()

    def draw(self, surface):
        try:
            circle = next(self.sprites)
            surface.blit(circle, (self.pos[0] - self.radius, self.pos[1] - self.radius))
        except:
            #TODO: callback to destroy
            pass

    def circles(self):
        for i in range(1, 100):
            if i%5==0:
                self.radius += 5
            circle = pygame.Surface((self.radius * 2 + 1, self.radius * 2 + 1), pygame.SRCALPHA)
            pygame.draw.circle(circle, self.color, (self.radius, self.radius), self.radius)
            yield circle
