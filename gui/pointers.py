import pygame

import default
import settings
from grid import TileGrid
from gui.components import GUI, TextLabel, Rows, Window
from gui import layouts
from entities.coordinates import Vector


class LinePointer(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = True

    def draw(self, surface):
        if settings.DEBUG_MODE and not self.game.paused:
            pygame.draw.line(surface, (255, 255, 0), self.game.camera.apply(self.game.character.pos),
                             pygame.mouse.get_pos(), 1)


class TileHighlighter(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = False
        self.icon = pygame.image.load("art/90_highlight.png")

    def draw(self, surface):
        if self.game.paused or self.game.construction_mode:
            return

        mx, my = pygame.mouse.get_pos()
        surface.blit(
            self.icon,
            (int(mx / default.TILE_SIZE) * default.TILE_SIZE, int(my / default.TILE_SIZE) * default.TILE_SIZE),
        )


class HoverDescription(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hidden = False
        self.width = layouts.WINDOW_WIDTH_XS
        self.height = layouts.WINDOW_HEIGHT_XS
        self.pos = Vector(layouts.X_0, layouts.Y_11)

    def draw(self, surface):
        if self.game.paused or self.game.construction_mode:
            return

        mpos = self.game.camera.get_mouse_coords()
        tile = self.game.tile_grid.get_tile((mpos.x, mpos.y))
        tile_type = tile.__class__.__name__

        self.children = []

        window = Window(
            width=self.width,
            height=self.height,
            background_color=layouts.WINDOW_BACKGROUND_COLOR,
            border_color=layouts.WINDOW_BORDER_COLOR,
        )
        self.add_child(window)

        text_rows = Rows(
            width=window.width - 20,
            height=window.height - 20,
            pos=Vector(10, 10),
            background_alpha=1,
        )
        window.add_child(text_rows)

        text_rows.add_child(TextLabel(tile_type, layouts.TEXT_COLOR))
        super().draw(surface)


class BuildingPlacer(GUI):
    def __init__(self, building, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.building = building
        self.hidden = False

    def draw(self, surface):
        if not self.hidden:
            size = self.building.size
            mpos = self.game.camera.get_mouse_coords()
            mpos = mpos + Vector(default.TILE_SIZE, default.TILE_SIZE) * 0.5

            pos = mpos - size * 0.5

            (i, j) = TileGrid.__coords_to_grid__(pos)
            pos = TileGrid.__grid_to_coords__(i, j)
            pos = pos - Vector(default.TILE_SIZE, default.TILE_SIZE) * 0.5

            pos = (pos + size * 0.5).round()

            self.building.set_position(Vector(*pos))

            if not self.game.character.can_construct(self.building):
                rect_surface = pygame.Surface(size.round(), pygame.SRCALPHA)
                rect_surface.fill((255, 0, 0, 60))
                surface.blit(rect_surface, self.game.camera.apply(self.building.pos - size * 0.5))
            self.building.draw(surface)
