import pygame

from entities.resources import Resource


class Controller:
    def __init__(self, game, gui=None):
        self.game = game
        self.gui = gui

    def process(self, events):
        return


class CharacterController(Controller):
    def process(self, events):
        if self.game.paused:
            return

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.game.character.move(0, -4)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.game.character.move(0, 4)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.game.character.move(-4, 0)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.character.move(4, 0)

        # reuse this for tile selection & highlighting
        # mouse_up_events = [event for event in events if event.type == pygame.MOUSEBUTTONUP]
        # if len(mouse_up_events) > 0:
        #     last = mouse_up_events[-1]
        #     if last.button == 1:
        #         mx, my = last.pos
        #         self.game.tile_grid.remove_tile(mx, my)

        if pygame.mouse.get_pressed() == (1, 0, 0):
            mx, my = pygame.mouse.get_pos()
            tile = self.game.tile_grid.get_tile(mx, my)

            if tile and isinstance(tile, Resource):
                self.game.character.mine(tile)


class MainMenuController(Controller):
    def process(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.paused ^= True
                self.gui.hidden ^= True

            if not self.gui.hidden and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.game.quit = True


class CharacterInventoryController(Controller):
    def process(self, events):
        if self.game.paused:
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.gui.hidden ^= True


class ConstructionController(Controller):
    def process(self, events):
        if self.game.paused:
            return

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.gui.hidden ^= True
