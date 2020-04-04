import pygame

class UI:
    def __init__(self, x, y, parent=None, sprite=None, draw_func=None):
        """parent: the parent UI element, or None if this is a top level UI
        draw_func: optional draw function, taking at least a surface and a position argument"""
        self.parent = parent
        self.x = x
        self.y = y
        self.children = []
        self.sprite = sprite
        self.draw_func = draw_func

    def draw(self, surface):
        pos = self.get_abs_coords()
        if self.draw_func is not None:
            self.draw_func(surface, pos)
        elif self.sprite is not None:
            surface.blit(self.sprite, pos)
        else:
            placeholder = pygame.Surface((64, 64))
            placeholder.fill((50,200,100))
            pygame.draw.rect(placeholder, (0,0,0), pygame.Rect(0,0,63,63), 4)
            placeholder.set_alpha(128+64)
            surface.blit(placeholder, pos)
        for child in self.children:
            child.draw(surface)

    def get_abs_coords(self):
        """Calculate absolute coordinates for drawing"""
        p = (0,0)
        if self.parent is not None:
            p = (self.parent.x, self.parent.y)
        return (p[0] + self.x, p[1] + self.y)
