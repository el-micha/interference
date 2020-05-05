import pygame
from entities.coordinates import Vector


class Field:
    fieldmap = {}

    @staticmethod
    def register_field(field):
        if type(field) not in Field.fieldmap:
            Field.fieldmap[type(field)] = []
        Field.fieldmap[type(field)].append(field)

    @staticmethod
    def unregister_field(field):
        Field.fieldmap[type(field)].remove(field)

    @staticmethod
    def get_fields_of_type(field_type):
        if field_type not in Field.fieldmap:
            return []
        return Field.fieldmap[field_type]

    def __init__(self, game, parent, pos, radius):
        # for a circle: radius, for other forms: max distance from origin
        self.parent = parent
        self.game = game
        self.pos = pos
        self.radius = radius
        self.color = (50, 50, 200, 60)
        self.active = True
        self.amplitude = 1

        Field.register_field(self)

    def get_effect(self, point):
        if not self.active:
            return 0
        distance = Vector.dist(self.pos, point)
        if distance <= self.radius:
            return self.amplitude
        else:
            return 0

    def draw(self, surface):
        circle = pygame.Surface((self.radius * 2 + 1, self.radius * 2 + 1), pygame.SRCALPHA)
        pygame.draw.circle(circle, self.color, (self.radius, self.radius), self.radius)
        surface.blit(circle, (int(self.pos.x - self.radius), int(self.pos.y - self.radius)))


class EnergyField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amplitude = 2


class LightField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw(self, surface):
        pass


