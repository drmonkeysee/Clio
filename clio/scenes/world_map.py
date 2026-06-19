"""World map scene — displays a generated WorldMap as a full-screen tile grid."""

from __future__ import annotations

import pygame

from clio.render import GlyphAtlas, render_world_map
from clio.scene import Scene
from clio.world.grid import WorldMap


class WorldMapScene(Scene):
    def __init__(
        self,
        world: WorldMap,
        tile_font: pygame.font.Font,
        tile: int,
        title: Scene | None = None,
    ) -> None:
        super().__init__()
        self._title = title
        atlas = GlyphAtlas(tile_font, tile)
        self._map_surf = render_world_map(world, atlas)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        match event.key:
            case pygame.K_ESCAPE:
                if self._title is not None:
                    self.next_scene = self._title
                else:
                    self.request_quit()

    def draw(self, screen: pygame.Surface) -> None:
        w, h = screen.get_size()
        mw, mh = self._map_surf.get_size()
        screen.fill((0, 0, 0))
        screen.blit(self._map_surf, ((w - mw) // 2, (h - mh) // 2))
