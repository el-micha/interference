import settings
from gui import layouts
from gui.components import GUI, Window, Rows, TextLabel
from entities.coordinates import Vector


class MainMenu(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = layouts.WINDOW_WIDTH_MD
        self.height = layouts.WINDOW_HEIGHT_LG
        self.size = Vector(self.width, self.height)

        self.pos = Vector(layouts.X_6 - self.width * 0.5, layouts.Y_1)

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

        text_rows.add_child(TextLabel('(esc) Main Menu', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('===============', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('(1) Save game', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('(2) Load game', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('(q) Quit game', layouts.TEXT_COLOR))


class FPSMenu(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = layouts.WINDOW_WIDTH_XS
        self.height = layouts.WINDOW_HEIGHT_XS
        self.size = Vector(self.width, self.height)

        self.pos = Vector(layouts.X_11, layouts.Y_11)

    def draw(self, surface):
        if not settings.DEBUG_MODE:
            return

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

        fps = f'FPS: {int(self.game.clock.get_fps())}'
        text_rows.add_child(TextLabel(fps, layouts.TEXT_COLOR))

        super().draw(surface)
