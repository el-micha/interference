import pygame

import default
import settings
from grid import TileGrid
from entities.characters import Character
from event import EventHandler
from gui.inventories import CharacterInventory


class Game:
    def __init__(self):
        print("Starting a new game")

        # TODO: load settings from files

        # pygame stuff
        pygame.init()
        self.surface = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption("inter B=====D ference")
        self.clock = pygame.time.Clock()

        # game stuff ...
        self.tile_grid = TileGrid(self, int(settings.SCREEN_HEIGHT / default.TILE_SIZE),
                                  int(settings.SCREEN_WIDTH / default.TILE_SIZE))
        self.character = Character(self, x=default.TILE_SIZE + int(default.TILE_SIZE / 2),
                                   y=default.TILE_SIZE + int(default.TILE_SIZE / 2))
        self.tile_grid.remove_tile(self.character.x, self.character.y)
        self.building = pygame.image.load("art/80_building.png")

        # simulation stuff
        self.running = True
        self.quit = False
        self.event_handler = EventHandler(self)
        self.tick = 0

        # visual stuff
        self.do_highlight = True
        self.highlight = pygame.image.load("art/90_highlight.png")
        self.do_point = settings.DEBUG_MODE

        # Graphical Interfaces
        self.font = pygame.font.SysFont(None, 24)
        self.graphical_interfaces = []
        self.gui_inventory = CharacterInventory(game=self)
        self.graphical_interfaces.append(self.gui_inventory)

    def run(self):
        while self.running:
            events = pygame.event.get()
            self.event_handler.process(events)
            # if a pause was triggered: wait for pause to end
            self.await_continue()
            self.gameloop()
            self.tick += 1
            self.draw()
            if self.quit:
                break
            self.clock.tick(60)

    def await_continue(self):
        while not self.running:
            # TODO: should only handle allowed pause events, not all
            events = pygame.event.get()
            self.event_handler.process(events)
            self.clock.tick(30)

    def gameloop(self):
        pass

    def draw(self):
        self.surface.fill((0, 0, 0))
        # pygame.draw.rect(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), pygame.Rect(random.randint(0,1920), random.randint(0,1080), random.randint(2,1000), random.randint(2,1000)))
        self.tile_grid.draw(self.surface)
        self.surface.blit(self.building, (256, 256))
        self.character.draw(self.surface)
        mx, my = pygame.mouse.get_pos()
        if self.do_highlight:
            self.surface.blit(self.highlight, (int(mx / 32) * 32, int(my / 32) * 32))
        if self.do_point:
            pygame.draw.line(self.surface, (255, 255, 0), (self.character.x + 16, self.character.y + 16),
                             pygame.mouse.get_pos(), 1)

        self.draw_graphical_interfaces()

        pygame.display.update()

    def draw_graphical_interfaces(self):
        for graphical_interface in self.graphical_interfaces:
            if not graphical_interface.hidden:
                graphical_interface.draw(self.surface)


if __name__ == "__main__":
    game = Game()
    game.run()
