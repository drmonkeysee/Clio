"""Title screen scene.

Reuses the amber-on-black DF aesthetic from the original app.py hello world.
Presents a keyboard-navigable menu: arrow keys select, Enter confirms, Esc quits.
"""

from __future__ import annotations

import pygame

from clio import codepage
from clio.scene import Scene

_BACKGROUND: tuple[int, int, int] = (10, 10, 10)
_AMBER: tuple[int, int, int] = (255, 176, 0)
_DIM: tuple[int, int, int] = (130, 85, 0)
_CURSOR: tuple[int, int, int] = (200, 140, 0)

_TITLE = "C L I O"
_SUBTITLE = "Trade Network Emergence Simulator"

_MENU_ITEMS = ("Generate New Map", "Quit")


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
            case pygame.K_RETURN | pygame.K_KP_ENTER:
                self._activate()

    def _activate(self) -> None:
        match self._selected:
            case 0:  # Generate New Map
                from clio.scenes.world_map import WorldMapScene
                from clio.world.generate import generate_random

                world = generate_random(self._map_rows, self._map_cols)
                self.next_scene = WorldMapScene(
                    world, self._tile_font, self._tile, title=self
                )
            case 1:  # Quit
                self.quit = True

    def draw(self, screen: pygame.Surface) -> None:
        if self._surface is None or self._surface.get_size() != screen.get_size():
            self._surface = self._render(screen.get_size())
        screen.blit(self._surface, (0, 0))

    def _render(self, size: tuple[int, int]) -> pygame.Surface:
        font = self._ui_font
        _, char_h = font.size("M")
        selector = codepage.TRIANGLE_RIGHT

        lines: list[tuple[str, tuple[int, int, int]]] = [
            (_TITLE, _AMBER),
            (_SUBTITLE, _DIM),
            ("", _AMBER),
        ]
        for i, item in enumerate(_MENU_ITEMS):
            if i == self._selected:
                lines.append((f"{selector} {item}", _AMBER))
            else:
                lines.append((f"  {item}", _DIM))

        lines.append(("", _DIM))
        lines.append(("↑↓ / j k  move   Enter  select   Esc  quit", _DIM))

        surf = pygame.Surface(size)
        surf.fill(_BACKGROUND)

        total_h = char_h * len(lines)
        y_start = (size[1] - total_h) // 2

        for i, (text, color) in enumerate(lines):
            rendered = font.render(text, True, color)
            x = (size[0] - rendered.get_width()) // 2
            surf.blit(rendered, (x, y_start + i * char_h))

        return surf
