from gui import layouts
from gui.components import GUI, Window, Rows, TextLabel


class MainMenu(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = layouts.WINDOW_WIDTH_MD
        self.height = layouts.WINDOW_HEIGHT_LG

        self.x = layouts.X_6 - self.width / 2
        self.y = layouts.Y_1

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
            x=10,
            y=10,
            background_alpha=1,
        )
        window.add_child(text_rows)

        text_rows.add_child(TextLabel('(esc) Main Menu', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('===============', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('(q) Quit game', layouts.TEXT_COLOR))

