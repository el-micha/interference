import pygame

from cameras import Camera
from entities.coordinates import Vector
import default
import settings
from entities.trains import Train, Engine, BoringHead, Cart
from grid import TileGrid
from entities.characters import Character
from controls.controllers import CharacterController, MainMenuController, CharacterInventoryController, \
    ConstructionController
from gui.inventories import CharacterInventory
from gui.constructions import BuildingMenu
from gui.menus import MainMenu, FPSMenu
from gui.pointers import TileHighlighter, LinePointer, HoverDescription
from entities.tiles import Tile, RockFloor, CoalFloor
from effects.explosion import Explosion
from effects.fields import Field
import random


class Game:
    def __init__(self):
        # pygame stuff
        pygame.init()
        self.surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("interference")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # Entities
        self._buildings = set()
        self._fields = set()

        # game stuff ...
        start_position = Vector(
            settings.WORLD_WIDTH / 2 * default.TILE_SIZE,
            settings.WORLD_HEIGHT / 2 * default.TILE_SIZE,
        )
        self.camera = Camera()
        self.camera.focus(start_position)
        self.tile_grid = TileGrid(self, settings.WORLD_WIDTH, settings.WORLD_HEIGHT)
        self.character = Character(self, start_position + Vector(16, 16), Vector(8, 8))
        self.tile_grid.replace_tile(self.character.pos, Tile)

        start_square = start_position - Vector(5 * default.TILE_SIZE, 5 * default.TILE_SIZE, )
        for i in range(10):
            for j in range(10):
                self.tile_grid.replace_tile(Vector(start_square.x + 32 * i, start_square.y + 32 * j), random.choice([RockFloor, CoalFloor]))

        # more entities...
        self.trains = []
        #self.exp = Explosion(self, pos=Vector(32, 32), size=Vector(32, 32))

        # FIXME: Remove hardcoded trains
        east_train = Train(game=self, pos=start_square + Vector(5 * default.TILE_SIZE + default.TILE_SIZE / 2, 3 * default.TILE_SIZE / 2),
                           direction=Vector(1, 0))
        east_train.add_wagon(BoringHead(self, None, None))
        east_train.add_wagon(Engine(self, None, None))
        east_train.add_wagon(Cart(self, None, None))
        self.trains.append(east_train)

        # runtime management
        self.running = True
        self.paused = False
        self.construction_mode = False
        self.quit = False
        self.tick = 0

        # interfaces
        self.interfaces = []
        self.controllers = []

        self.register_interface(MainMenu(game=self), MainMenuController)
        self.register_controller(CharacterController(self))
        self.register_interface(LinePointer(game=self))
        self.register_interface(TileHighlighter(game=self))
        self.register_interface(HoverDescription(game=self))
        self.register_interface(CharacterInventory(game=self, hidden=False), CharacterInventoryController)
        self.register_interface(BuildingMenu(game=self, hidden=False), ConstructionController)
        self.register_interface(FPSMenu(game=self, hidden=False))

    def register_interface(self, interface, controller_cls=None):
        self.interfaces.append(interface)

        if controller_cls:
            controller = controller_cls(self, interface)
            self.register_controller(controller)

    def register_controller(self, controller):
        self.controllers.append(controller)

    def run(self):
        while self.running:
            self.process_controllers()

            if not self.paused:
                self.game_loop()

            self.draw()

            if self.quit:
                print('Quitting game')
                break
            self.clock.tick(60)

    def game_loop(self):
        self.tick += 1
        for train in self.trains:
            train.ride()
        self.tick += 1
        for building in self._buildings:
            building.tick(self.tick)

        # for k,v in Field.fieldmap.items():
        #     print(k, len(v))

    def process_controllers(self):
        events = pygame.event.get()

        for controller in self.controllers:
            controller.process(events)

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.tile_grid.draw(self.surface)
        # self.surface.blit(self.building, (256, 256))
        self.character.draw(self.surface)
        # map(lambda x:x.draw(self.surface), self.buildings)
        for building in self._buildings:
            building.draw(self.surface)
        for train in self.trains:
            train.draw(self.surface)
        self.draw_interfaces()
        #debug temp TODO
        for field in self._fields:
            field.draw(self.surface)

        pygame.display.update()

    def draw_interfaces(self):
        for interface in self.interfaces:
            if not interface.hidden:
                interface.draw(self.surface)

    def get_fields(self, field_type=None):
        if field_type is None:
            predicate = lambda _: True
        else:
            predicate = lambda field: type(field) == field_type
        return list(filter(predicate, self._fields))

    def add_field(self, field):
        self._fields.add(field)

    def get_buildings(self, b_type=None):
        if b_type is None:
            predicate = lambda _: True
        else:
            predicate = lambda field: type(field) == b_type
        return list(filter(predicate, self._buildings))

    def add_building(self, b):
        # add building AND fields you asshole
        self._buildings.add(b)
        if hasattr(b, "fields"):
            self._fields.update(b.fields)

