import pygame

from entities.resources import Resource


class Handler:
    def __init__(self, game):
        self.game = game


class EventHandler(Handler):
    def process(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit = True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.game.gui_inventory.hidden ^= True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # TODO: Pause the game
                self.game.gui_main_menu.hidden ^= True

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
