import pygame

import default
import settings
from grid import TileGrid
from gui.components import GUI
from helpers import dist, sub, times, round, add


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
            size = self.building.get_size()
            mpos = pygame.mouse.get_pos()
            mpos = add(mpos, (default.TILE_SIZE/2, default.TILE_SIZE/2))

            pos = sub(mpos, times(size, 0.5))

            (i, j) = TileGrid.__coords_to_grid__(pos)
            pos = TileGrid.__grid_to_coords__(i, j)
            pos = sub(pos, (default.TILE_SIZE/2, default.TILE_SIZE/2))

            pos = round(add(pos, times(size, 0.5)))

            self.building.set_position(pos)

            if not self.game.character.can_construct(self.building):
                rect_surface = pygame.Surface(size, pygame.SRCALPHA)
                rect_surface.fill((255, 0, 0, 60))
                surface.blit(rect_surface, sub(self.building.pos, times(size, 0.5)))

            self.building.draw(surface)
