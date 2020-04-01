import pygame
import math

def dist(x, y, u, v):
    return math.sqrt((u-x)**2 + (v-y)**2)

class EventHandler:
    def __init__(self, game):
        self.game = game

    def process(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.quit = True
            print(event)
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            self.game.character.move(0, -4)
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            self.game.character.move(0, 4)
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            self.game.character.move(-4, 0)
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            self.game.character.move(4, 0)
        if pressed[pygame.K_ESCAPE]:
            # FIXME: Show menu instead of exiting game
            exit()

        # reuse this for tile selection & highlighting
        # mouse_up_events = [event for event in events if event.type == pygame.MOUSEBUTTONUP]
        # if len(mouse_up_events) > 0:
        #     last = mouse_up_events[-1]
        #     if last.button == 1:
        #         mx, my = last.pos
        #         self.game.world.remove_tile(mx, my)

        if pygame.mouse.get_pressed() == (1,0,0):
            # distance character to mouse
            x, y = self.game.character.x, self.game.character.y
            mx, my = pygame.mouse.get_pos()
            if dist(x, y, mx, my) < self.game.character.reach:
                tile = self.game.world.get_tile(mx, my)
                if tile.is_minable:
                    tile.durability -= 2
                    if tile.durability < 0:
                        self.game.world.remove_tile(mx, my)


