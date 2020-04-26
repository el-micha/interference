from gui import layouts
from gui.components import GUI, TextLabel, Rows, Window
from entities.coordinates import Vector

class CharacterInventory(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = layouts.WINDOW_WIDTH_SM
        self.height = layouts.WINDOW_HEIGHT_XL
        self.size = Vector(self.width, self.height)

        self.pos = Vector(layouts.X_10, layouts.Y_0)

    def draw(self, surface):
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
            pos = Vector(10, 10),
            background_alpha=1,
        )
        window.add_child(text_rows)

        text_rows.add_child(TextLabel('(i) Inventory', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('=============', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('', layouts.TEXT_COLOR))

        for stack in self.game.character.inventory.stacks:
            if stack.amount == 1:
                label = f'{stack.item}'
            else:
                label = f'{stack.item}: {stack.amount}'
            text_rows.add_child(TextLabel(label, layouts.TEXT_COLOR))

        super().draw(surface)
