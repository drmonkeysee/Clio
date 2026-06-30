"""World map scene — generates and displays a WorldMap as a full-screen tile grid."""

from __future__ import annotations

from typing import final, override

import pygame

from clio.palette import ThemeManager
from clio.render import GlyphAtlas, render_border, render_world_map
from clio.scene import Scene
from clio.world import MapGenerator


@final
class WorldMapScene(Scene):
    def __init__(
        self,
        themes: ThemeManager,
        generator: MapGenerator,
        tile_font: pygame.font.Font,
        tile: int,
        map_cols: int,
        map_rows: int,
    ) -> None:
        super().__init__(themes)
        world = generator(map_rows, map_cols)
        atlas = GlyphAtlas(tile_font, tile)
        self._map_surf = render_world_map(world, atlas)
        self._tile = tile
        self._border: pygame.Surface | None = None
        self._border_size: tuple[int, int] | None = None
        self._border_theme = self.theme

    @override
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        match event.key:
            case pygame.K_ESCAPE:
                self.terminate()
            case pygame.K_t:
                self.cycle_theme()
            case _:
                pass

    @override
    def draw(self, screen: pygame.Surface) -> None:
        size = screen.get_size()
        if (
            self._border is None
            or size != self._border_size
            or self.theme is not self._border_theme
        ):
            self._border = render_border(size, self._tile, self.theme.border)
            self._border_size = size
            self._border_theme = self.theme
        w, h = size
        mw, mh = self._map_surf.get_size()
        screen.fill(self.theme.background)
        screen.blit(self._map_surf, ((w - mw) // 2, (h - mh) // 2))
        screen.blit(self._border, (0, 0))
