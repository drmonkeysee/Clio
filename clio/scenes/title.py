"""Title screen scene.

Keyboard-navigable menu: arrow keys / j k select, Enter confirms, Esc quits.
Press t to cycle UI themes (temporary — remove once a palette is chosen).
"""

from __future__ import annotations

from enum import IntEnum
from typing import final

import pygame

import clio.world as world
from clio import codepage, palette
from clio.render import render_border
from clio.scene import Scene
from clio.scenes.world_map import WorldMapScene

_TITLE = "C L I O"
_SUBTITLE = "Trade Network Emergence Simulator"


class _MenuItem(IntEnum):
    GENERATE_SIMPLEX = 0
    GENERATE_RANDOM = 1
    QUIT = 2


_MENU_ITEMS = ("Generate Simplex Map", "Generate Random Map", "Quit")


@final
class TitleScene(Scene):
    def __init__(
        self,
        ui_font: pygame.font.Font,
        tile_font: pygame.font.Font,
        tile: int,
        map_cols: int,
        map_rows: int,
    ) -> None:
        super().__init__()
        self._ui_font = ui_font
        self._tile_font = tile_font
        self._tile = tile
        self._map_cols = map_cols
        self._map_rows = map_rows
        self._selected = 0
        self._surface: pygame.Surface | None = None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        match event.key:
            case pygame.K_ESCAPE:
                self.quit = True
            case pygame.K_UP | pygame.K_k:
                self._selected = (self._selected - 1) % len(_MENU_ITEMS)
                self._surface = None  # invalidate cached render
            case pygame.K_DOWN | pygame.K_j:
                self._selected = (self._selected + 1) % len(_MENU_ITEMS)
                self._surface = None
            case pygame.K_t:  # TEMPORARY — theme toggle
                palette.cycle()
                self._surface = None
            case pygame.K_RETURN | pygame.K_KP_ENTER:
                self._activate()

    def _activate(self) -> None:
        wgen = None
        match _MenuItem(self._selected):
            case _MenuItem.GENERATE_SIMPLEX:
                wgen = world.generate_simplex
            case _MenuItem.GENERATE_RANDOM:
                wgen = world.generate_random
            case _MenuItem.QUIT:
                self.quit = True
        if wgen:
            wmap = wgen(self._map_rows, self._map_cols)
            self.next_scene = WorldMapScene(
                wmap, self._tile_font, self._tile, title=self
            )

    def draw(self, screen: pygame.Surface) -> None:
        if self._surface is None or self._surface.get_size() != screen.get_size():
            self._surface = self._render(screen.get_size())
        screen.blit(self._surface, (0, 0))

    def _render(self, size: tuple[int, int]) -> pygame.Surface:
        font = self._ui_font
        theme = palette.active()
        _, char_h = font.size("M")
        selector = codepage.TRIANGLE_RIGHT

        lines: list[tuple[str, tuple[int, int, int]]] = [
            (_TITLE, theme.text),
            (_SUBTITLE, theme.dim),
            ("", theme.dim),
        ]
        for i, item in enumerate(_MENU_ITEMS):
            if i == self._selected:
                lines.append((f"{selector} {item}", theme.accent))
            else:
                lines.append((f"  {item}", theme.dim))

        lines.append(("", theme.dim))
        lines.append(
            ("↑↓ / j k: move   Enter: select   Esc: quit   t: theme", theme.dim)
        )
        lines.append((f"Theme: {theme.name}", theme.dim))  # TEMPORARY

        surf = pygame.Surface(size)
        surf.fill(theme.background)

        total_h = char_h * len(lines)
        y_start = (size[1] - total_h) // 2

        for i, (text, color) in enumerate(lines):
            rendered = font.render(text, True, color)
            x = (size[0] - rendered.get_width()) // 2
            surf.blit(rendered, (x, y_start + i * char_h))

        surf.blit(
            render_border(self._map_cols, self._map_rows, self._tile, theme.border),
            (0, 0),
        )

        return surf
