
import pygame
from entities.coordinates import Vector

class Sprite:
    def __init__(self):
        pass

    def draw(self, surface, point):
        pass

class ExplosionSprite(Sprite):
    def __init__(self):
        self.radius = 10
        self.color = (240, 200, 20, 128)
        self.sprites = self.circles()

    def draw(self, surface, point):
        try:
            circle = next(self.sprites)
            drawx, drawy = (point - Vector(self.radius, self.radius)).round()
            surface.blit(circle, (drawx, drawy))
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
