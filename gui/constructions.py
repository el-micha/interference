from gui import layouts
from gui.components import GUI, Window, Rows, TextLabel
from entities.buildings import CoalDrill, EnergyDissipator


class BuildingMenu(GUI):
    constructable_buildings = [CoalDrill, EnergyDissipator]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = layouts.WINDOW_WIDTH_SM
        self.height = layouts.WINDOW_HEIGHT_MD

        self.x = layouts.X_8
        self.y = layouts.Y_0

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
            x=10,
            y=10,
            background_alpha=1,
        )
        window.add_child(text_rows)

        text_rows.add_child(TextLabel('(b) Buildings', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('=============', layouts.TEXT_COLOR))
        text_rows.add_child(TextLabel('', layouts.TEXT_COLOR))

        for building in self.constructable_buildings:
            if building.is_affordable(self.game.character.inventory):
                text_rows.add_child(TextLabel(f'({building.keyboard_shortcut}) {building.name}', layouts.TEXT_COLOR))

        super().draw(surface)