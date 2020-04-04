import pygame


class GUI:
    def __init__(self, x=0, y=0, hidden=True, game=None):
        self.x = x
        self.y = y
        self.parent = None
        self.children = []
        self.hidden = hidden
        self.game = game

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def add_child(self, child):
        child.parent = self
        child.game = self.game
        self.children.append(child)

    def get_abs_coords(self):
        """Calculate absolute coordinates for drawing"""
        p = (0, 0)
        if self.parent is not None:
            p = self.parent.get_abs_coords()
        return p[0] + self.x, p[1] + self.y


class GenericComponent(GUI):
    def __init__(self, draw_func, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.draw_func = draw_func

    def draw(self, surface):
        self.draw_func(surface, self.get_abs_coords())

        super().draw(surface)


class Window(GUI):
    def __init__(self, width=None, height=None, background_color=None, background_alpha=None, border_color=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = width
        self.height = height
        self.background_color = background_color
        self.background_alpha = background_alpha
        self.border_color = border_color

    def draw(self, surface):
        window = pygame.Surface((self.width, self.height))
        if self.background_color:
            window.fill(self.background_color)

        if self.background_alpha:
            window.set_alpha(self.background_alpha)

        if self.border_color:
            pygame.draw.rect(window, self.border_color, pygame.Rect(0, 0, self.width, self.height), 4)

        surface.blit(window, self.get_abs_coords())

        super().draw(surface)


class Rows(Window):
    def __init__(self, row_height=25, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.row_height = row_height

    def add_child(self, child):
        child.y = self.y + self.row_height * len(self.children)
        super().add_child(child)


class TextLabel(GUI):
    def __init__(self, text, text_color, background_color=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text
        self.text_color = text_color
        self.background_color = background_color

    def draw(self, surface):
        rendered_text = self.game.font.render(self.text, True, self.text_color, self.background_color)
        surface.blit(rendered_text, self.get_abs_coords())
