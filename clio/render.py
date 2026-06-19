import pygame

from clio.world.grid import WorldMap
from clio.world.terrain import TerrainType, visual

# Default logical tile size in pixels. The atlas accepts a physical pixel size
# (tile * HiDPI scale) so callers should pass the pre-scaled value.
TILE_LOGICAL: int = 14


class GlyphAtlas:
    """Pre-rendered tile surfaces keyed by TerrainType value.

    Each entry is a tile×tile Surface with the terrain background color filled
    and the CP437 glyph centered in the foreground color. Built once per font /
    tile size; the scene blits cached surfaces every frame rather than
    re-rendering text each tick.
    """

    def __init__(self, font: pygame.font.Font, tile: int) -> None:
        self._tile = tile
        self._cache: dict[int, pygame.Surface] = {}
        for terrain_type in TerrainType:
            glyph, fg, bg = visual(terrain_type)
            surf = pygame.Surface((tile, tile))
            surf.fill(bg)
            text = font.render(glyph, True, fg)
            x = (tile - text.get_width()) // 2
            y = (tile - text.get_height()) // 2
            surf.blit(text, (x, y))
            self._cache[terrain_type.value] = surf

    @property
    def tile(self) -> int:
        return self._tile

    def cell(self, terrain_value: int) -> pygame.Surface:
        """Return the pre-rendered Surface for the given TerrainType integer value."""
        return self._cache[terrain_value]


def render_world_map(world: WorldMap, atlas: GlyphAtlas) -> pygame.Surface:
    """Composite the full world map into a single Surface.

    Called once per generated map; the resulting Surface is blitted each frame
    by WorldMapScene without re-iterating the tile array.
    """
    tile = atlas.tile
    surf = pygame.Surface((world.cols * tile, world.rows * tile))
    for row in range(world.rows):
        for col in range(world.cols):
            terrain_val = int(world.terrain[row, col])
            surf.blit(atlas.cell(terrain_val), (col * tile, row * tile))
    return surf
