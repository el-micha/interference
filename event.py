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
        if pressed[pygame.K_UP]:
            self.game.character.move(0, -4)
        if pressed[pygame.K_DOWN]:
            self.game.character.move(0, 4)
        if pressed[pygame.K_LEFT]:
            self.game.character.move(-4, 0)
        if pressed[pygame.K_RIGHT]:
            self.game.character.move(4, 0)