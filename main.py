import pygame

import default
import settings
from grid import TileGrid
from entities.characters import Character
from event import EventHandler
from ui import UI

class Game:
    def __init__(self):
        print("Starting a new game")

        # TODO: load settings from files

        # pygame stuff
        pygame.init()
        self.surface = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("inter B=====D ference")
        self.clock = pygame.time.Clock()

        # game stuff ...
        self.world = TileGrid(self, int(1080 / default.TILE_SIZE), int(1920 / default.TILE_SIZE))
        self.character = Character(self, x=default.TILE_SIZE + int(default.TILE_SIZE / 2),
                                   y=default.TILE_SIZE + int(default.TILE_SIZE / 2))
        self.world.remove_tile(self.character.x, self.character.y)
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
        self.testui = UI(512, 64)
        childui = UI(16, 16, parent=self.testui, sprite=None, draw_func=lambda surf,pos:pygame.draw.circle(surf, (255, 80, 20), pos, 12, 2))
        childui2 = UI(16+32, 16+32, parent=self.testui, sprite=None, draw_func=lambda surf, pos: pygame.draw.circle(surf, (20, 80, 255), pos, 12, 2))
        self.testui.children.append(childui)
        self.testui.children.append(childui2)


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
        self.world.draw(self.surface)
        self.surface.blit(self.building, (256, 256))
        self.character.draw(self.surface)
        mx, my = pygame.mouse.get_pos()
        if self.do_highlight:
            self.surface.blit(self.highlight, (int(mx / 32) * 32, int(my / 32) * 32))
        if self.do_point:
            pygame.draw.line(self.surface, (255, 255, 0), (self.character.x + 16, self.character.y + 16),
                             pygame.mouse.get_pos(), 1)
        self.testui.draw(self.surface)
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
