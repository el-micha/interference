import pygame

import default
import settings
from grid import TileGrid
from entities.characters import Character
from controls.controllers import CharacterController, MainMenuController, CharacterInventoryController
from gui.inventories import CharacterInventory
from gui.menus import MainMenu
from gui.pointers import TileHighlighter, LinePointer
from entities.tiles import Tile
from entities.buildings import CoalDrill, EnergyDissipator

class Game:
    def __init__(self):
        # pygame stuff
        pygame.init()
        self.surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("inter B=====D ference")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # game stuff ...
        self.tile_grid = TileGrid(self, int(settings.SCREEN_HEIGHT / default.TILE_SIZE),
                                  int(settings.SCREEN_WIDTH / default.TILE_SIZE))
        self.character = Character(self, x=default.TILE_SIZE + int(default.TILE_SIZE / 2),
                                   y=default.TILE_SIZE + int(default.TILE_SIZE / 2))
        self.tile_grid.replace_tile(self.character.x, self.character.y, Tile(self, self.character.x, self.character.y))

        # buildings
        #self.building = pygame.image.load("art/81_coal_drill.png")
        self.buildings = [CoalDrill(self, x=100, y=200), EnergyDissipator(self, x=200, y=300)]

        # runtime management
        self.running = True
        self.paused = False
        self.quit = False
        self.tick = 0

        # interfaces
        self.interfaces = []
        self.controllers = []

        self.register_controller(CharacterController(self))
        self.register_interface(LinePointer(game=self))
        self.register_interface(TileHighlighter(game=self))
        self.register_interface(CharacterInventory(game=self), CharacterInventoryController)
        self.register_interface(MainMenu(game=self), MainMenuController)

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

    def process_controllers(self):
        events = pygame.event.get()

        for controller in self.controllers:
            controller.process(events)

    def draw(self):
        self.surface.fill((0, 0, 0))
        self.tile_grid.draw(self.surface)
        #self.surface.blit(self.building, (256, 256))
        self.character.draw(self.surface)
        # map(lambda x:x.draw(self.surface), self.buildings)
        for building in self.buildings:
            building.draw(self.surface)
        self.draw_interfaces()

        pygame.display.update()

    def draw_interfaces(self):
        for interface in self.interfaces:
            if not interface.hidden:
                interface.draw(self.surface)
