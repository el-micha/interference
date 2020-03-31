import random
import pygame
from grid import TileGrid
from entity import Entity
from event import EventHandler

class Game:
    def __init__(self):
        print("Starting a new game")

        # TODO: load settings from files

        # pygame stuff
        pygame.init()
        self.surface = pygame.display.set_mode((1920,1080))
        pygame.display.set_caption("inter ~~~ ference")
        self.clock = pygame.time.Clock()

        # game stuff ...
        self.world = TileGrid(int(1080 / 32), int(1920 / 32))
        self.character = Entity()

        # simulation stuff
        self.running = True
        self.quit = False
        self.event_handler = EventHandler(self)
        self.tick = 0

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
        self.character.draw(self.surface)
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
