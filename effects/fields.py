from entities.entities import Entity
import pygame

class Field(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for a circle: radius, for other forms: max distance from origin
        self.reach = 256
        self.color = (50, 50, 200, 100)

    def draw(self, surface):
        circle = pygame.Surface((self.reach*2+1, self.reach*2+1), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.color, (self.reach, self.reach), self.reach)
        circle.set_alpha(100)
        circle.convert()
        surface.blit(circle, (self.x - self.reach, self.y - self.reach))
        # above does not work, quick hack:
        #pygame.draw.circle(surface, self.color, (self.x, self.y), self.reach)