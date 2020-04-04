import settings
from gui.components import GUI, TextLabel, Rows, Window


class CharacterInventory(GUI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = 200
        self.height = 500

        self.x = (settings.SCREEN_WIDTH - self.width - 10)
        self.y = 64

    def draw(self, surface):
        self.children = []

        window = Window(
            width=self.width,
            height=self.height,
            background_color=(100, 80, 100),
            border_color=(0, 0, 0),
        )
        self.add_child(window)

        text_rows = Rows(
            width=window.width-20,
            height=window.height-20,
            x=10,
            y=10,
            background_alpha=1,
        )
        window.add_child(text_rows)

        text_rows.add_child(TextLabel('Inventory', (255, 80, 20)))
        text_rows.add_child(TextLabel('=========', (255, 80, 20)))
        text_rows.add_child(TextLabel('', (255, 80, 20)))

        for stack in self.game.character.inventory.stacks:
            if stack.amount == 1:
                label = f'{stack.item}'
            else:
                label = f'{stack.item}: {stack.amount}'
            text_rows.add_child(TextLabel(label, (0, 0, 0)))

        super().draw(surface)
