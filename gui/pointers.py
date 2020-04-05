import pygame

import settings
from gui.components import GUI


class LinePointer(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = False

    def draw(self, surface):
        if settings.DEBUG_MODE and not self.game.paused:
            pygame.draw.line(surface, (255, 255, 0), (self.game.character.x + 16, self.game.character.y + 16),
                             pygame.mouse.get_pos(), 1)


class TileHighlighter(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = False
        self.icon = pygame.image.load("art/90_highlight.png")

    def draw(self, surface):
        if not self.game.paused:
            mx, my = pygame.mouse.get_pos()
            surface.blit(self.icon, (int(mx / 32) * 32, int(my / 32) * 32))
