from entities.entities import Entity
import pygame

class Field(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for a circle: radius, for other forms: max distance from origin
        self.reach = 128
        self.color = (50, 50, 200)

    def draw(self, surface):
        circle = pygame.Surface((self.reach*2+1, self.reach*2+1))
        pygame.draw.circle(circle, self.color, (self.reach, self.reach), self.reach, 2)
        circle.set_alpha(0.8)
        surface.blit(circle, (self.x, self.y))
        # above does not work, quick hack:
        pygame.draw.circle(surface, self.color, (self.reach, self.reach), self.reach, 2)