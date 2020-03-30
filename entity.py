
import pygame

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
    def __init__(self, x=16, y=16):
        self.id = ID.request_id(self)
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, surface):
        print("entity default draw. overwrite")
        pygame.draw.rect(surface, (200, 100, 200), pygame.Rect(self.x, self.y, 16, 16))
