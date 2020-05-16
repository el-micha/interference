import pygame
from entities.coordinates import Vector


class Field:

    def __init__(self, game, parent, pos, radius):
        # for a circle: radius, for other forms: max distance from origin
        self.parent = parent
        self.game = game
        self.pos = pos
        self.base_radius = radius
        self.base_amplitude = 1
        self.color = (50, 50, 200, 30)
        self.active = True
        # lazy sprite
        self.circle = None
        self.old_radius = self.get_radius()

    def get_amplitude(self):
        return self.base_amplitude

    def get_radius(self):
        return self.base_radius

    def get_effect(self, point):
        if not self.active:
            return 0
        distance = Vector.dist(self.pos, point)
        if distance <= self.get_radius():
            return self.get_amplitude()
        else:
            return 0

    def get_circle(self):
        if self.get_radius() != self.old_radius or self.circle is None:
            circle = pygame.Surface((self.get_radius() * 2 + 1, self.get_radius() * 2 + 1), pygame.SRCALPHA)
            pygame.draw.circle(circle, self.color, (self.get_radius(), self.get_radius()), self.get_radius())
            self.circle = circle
            self.old_radius = self.get_radius()
        return self.circle

    def draw(self, surface):
        circle = self.get_circle()
        draw_pos = Vector(self.pos.x - self.get_radius(), self.pos.y - self.get_radius())
        surface.blit(circle, self.game.camera.apply(draw_pos))


class EnergyField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_amplitude(self):
        return self.base_amplitude * 2


class LightField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_radius(self):
        energy = 1
        for field in self.game.get_fields(EnergyField):
            energy += field.get_effect(self.pos) / 2
        return self.base_radius * energy


    def draw(self, surface):
        pass
        # self.color = (50, 50, 200, 200)
        # circle = pygame.Surface((self.get_radius() * 2 + 1, self.get_radius() * 2 + 1), pygame.SRCALPHA)
        # pygame.draw.circle(circle, self.color, (self.get_radius(), self.get_radius()), self.get_radius())
        # draw_pos = Vector(self.pos.x - self.get_radius(), self.pos.y - self.get_radius())
        # surface.blit(circle, self.game.camera.apply(draw_pos))


