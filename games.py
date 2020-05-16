import pygame

from entities.buildings import EnergyDissipator, CoalDrill
from entities.coordinates import Vector
import default
import settings
from entities.entities import ID
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
        self.tile_grid = TileGrid(self, int(settings.SCREEN_WIDTH / default.TILE_SIZE),
                                  int(settings.SCREEN_HEIGHT / default.TILE_SIZE))
        self.character = Character(self, Vector(default.TILE_SIZE + int(default.TILE_SIZE / 2),
                                   default.TILE_SIZE + int(default.TILE_SIZE / 2)), Vector(8, 8))
        self.tile_grid.replace_tile(self.character.pos, Tile)
        for i in range(5):
            for j in range(5):
                self.tile_grid.replace_tile(Vector(32 * (1+i), 32 * (1+j)), random.choice([RockFloor, CoalFloor]))


        # more entities...
        self.trains = []
        #self.exp = Explosion(self, pos=Vector(32, 32), size=Vector(32, 32))


        # FIXME: Remove hardcoded trains
        east_train = Train(game=self, pos=Vector(default.TILE_SIZE + int(default.TILE_SIZE / 2), default.TILE_SIZE * 2 + int(default.TILE_SIZE / 2)), direction=Vector(1, 0))
        east_train.add_wagon(BoringHead(self, None, None))
        east_train.add_wagon(Engine(self, None, None))
        east_train.add_wagon(Cart(self, None, None))
        self.trains.append(east_train)

        south_train = Train(game=self, pos=Vector(default.TILE_SIZE + int(default.TILE_SIZE / 2),
                            default.TILE_SIZE * 3 + int(default.TILE_SIZE / 2)), direction=Vector(0, 1))
        south_train.add_wagon(Engine(self, None, None))
        self.trains.append(south_train)

        for train in self.trains:
            for wagon in train.wagons:
                self.tile_grid.replace_tile(wagon.pos, RockFloor)
                self.tile_grid.replace_tile(wagon.pos + Vector(-1, -1), RockFloor)

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

