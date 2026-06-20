from enum import IntEnum

from clio import codepage, palette

type Color = tuple[int, int, int]
type TileVisual = tuple[str, Color, Color]


class TerrainType(IntEnum):
    OCEAN = 0
    COAST = 1
    RIVER = 2
    PLAIN = 3
    FOREST = 4
    HILL = 5
    MOUNTAIN = 6
    DESERT = 7
    TUNDRA = 8


# (glyph, fg_color, bg_color) — background encodes biome, foreground encodes
# the feature character (design §7.3).
# fmt: off
_VISUALS: dict[TerrainType, TileVisual] = {
    TerrainType.OCEAN:    (codepage.WAVE,         palette.OCEAN_FG,    palette.OCEAN_BG),
    TerrainType.COAST:    (codepage.TILDE,        palette.COAST_FG,    palette.COAST_BG),
    TerrainType.RIVER:    (codepage.TILDE,        palette.RIVER_FG,    palette.RIVER_BG),
    TerrainType.PLAIN:    (codepage.DOT,          palette.PLAIN_FG,    palette.PLAIN_BG),
    TerrainType.FOREST:   (codepage.CLUB,         palette.FOREST_FG,   palette.FOREST_BG),
    TerrainType.HILL:     (codepage.LOWER_N,      palette.HILL_FG,     palette.HILL_BG),
    TerrainType.MOUNTAIN: (codepage.CARET,        palette.MOUNTAIN_FG, palette.MOUNTAIN_BG),
    TerrainType.DESERT:   (codepage.MIDDLE_DOT,   palette.DESERT_FG,   palette.DESERT_BG),
    TerrainType.TUNDRA:   (codepage.UNDERSCORE,   palette.TUNDRA_FG,   palette.TUNDRA_BG),
}
# fmt: on


def visual(terrain: TerrainType) -> TileVisual:
    """Return the (glyph, fg, bg) triple for the given terrain type."""
    return _VISUALS[terrain]
