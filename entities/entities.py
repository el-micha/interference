import pygame

import default

"""
Design outline

need components:
- position, movement
- area of effect
- tile properties like hardness etc
- tile transformations: empty to water / sand
- tile movement: sand is moved
- tile descruction and dropping of minerals etc
- UI, inventory, goals
- controllers: characters by players and AI, robots by scripts
- entity guis for robots, machines, factories, vehicles
- physics, maybe (flying bullets)
-





"""


class ID:
    """Hands out unique ids and stores all id-d entities sorted by type"""
    id_counter = -1
    type_dict = {}

    @staticmethod
    def request_id(thing):
        if type(thing) not in ID.type_dict.keys():
            ID.type_dict[type(thing)] = []
        if not thing in ID.type_dict[type(thing)]:
            ID.type_dict[type(thing)].append(thing)
        else:
            print("ID Error: Thing is already in ID list.")
            return None
        ID.id_counter += 1
        return ID.id_counter


class Entity:
    def __init__(self, x=None, y=None):
        self.id = ID.request_id(self)
        self.x = x
        self.y = y
        self.is_blocking = True
        self.color = (0, 0, 0)
        self.art_id = 0
        self.size = default.TILE_SIZE

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, surface):
        # print("entity default draw. overwrite")
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, 32, 32))
