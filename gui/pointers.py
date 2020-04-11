import pygame

import default
import settings
from gui.components import GUI
from helpers import dist


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
        if not self.game.paused and not self.game.construction_mode:
            mx, my = pygame.mouse.get_pos()
            surface.blit(
                self.icon,
                (int(mx / default.TILE_SIZE) * default.TILE_SIZE, int(my / default.TILE_SIZE) * default.TILE_SIZE),
            )


class BuildingPlacer(GUI):
    def __init__(self, building, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.building = building
        self.hidden = False

    def draw(self, surface):
        if not self.hidden:
            mx, my = pygame.mouse.get_pos()
            x = int(mx / default.TILE_SIZE) * default.TILE_SIZE
            y = int(my / default.TILE_SIZE) * default.TILE_SIZE
            self.building.set_position(x, y)

            if not self.game.character.can_construct(self.building):
                width, height = self.building.get_sprite_size()
                rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                rect_surface.fill((255, 0, 0, 60))
                surface.blit(rect_surface, (self.building.x, self.building.y))

            self.building.draw(surface)
