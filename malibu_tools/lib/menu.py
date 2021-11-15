from pygame import font, Surface
from math import ceil
from typing import List
from malibu.typing import IGraphicsService


class Menu:

    def render(self, gfx: IGraphicsService):
        srfs = []
        height = 0
        width = 0
        for index, item in enumerate(self._items):
            if index == self._selected_item:
                srf = self._font.render(f"  {item}  ", True, (255, 0, 0), (100, 0, 0))
            else:
                srf = self._font.render(f"  {item}  ", True, (255, 0, 0))
            height += srf.get_rect().height + 10
            width = max(width, srf.get_rect().width + 10)
            srfs.append(srf)

        y_offset = 5
        menu_surface = Surface((width, height))
        menu_surface.set_colorkey((0, 0, 0))
        for srf in srfs:
            menu_surface.blit(srf, (5, y_offset))
            y_offset += srf.get_rect().height + 10

        rect = menu_surface.get_rect()
        rect.center = gfx.get_viewport().center
        gfx.blit(menu_surface, rect)

    def get_selected(self):
        return self._items[self._selected_item]

    def move_down(self):
        self._selected_item = (self._selected_item + 1) % len(self._items)

    def move_up(self):
        self._selected_item = (self._selected_item - 1) % len(self._items)

    def __init__(self, items: List[str]):
        fn = font.get_default_font()
        self._font = font.SysFont(fn, 50)
        self._items = items.copy()
        self._selected_item = 0
