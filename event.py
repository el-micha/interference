import pygame

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

        if pygame.mouse.get_pressed()[0]:
            self.game.set_mouse_tile(0)


