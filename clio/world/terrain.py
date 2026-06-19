from enum import IntEnum

from clio import codepage

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
_VISUALS: dict[TerrainType, TileVisual] = {
    TerrainType.OCEAN: (codepage.WAVE, (60, 100, 180), (5, 15, 45)),
    TerrainType.COAST: (codepage.TILDE, (100, 180, 210), (20, 50, 100)),
    TerrainType.RIVER: (codepage.TILDE, (80, 160, 255), (20, 40, 90)),
    TerrainType.PLAIN: (codepage.DOT, (100, 170, 60), (20, 55, 20)),
    TerrainType.FOREST: (codepage.CLUB, (30, 110, 30), (10, 35, 10)),
    TerrainType.HILL: (codepage.LOWER_N, (165, 145, 80), (55, 50, 20)),
    TerrainType.MOUNTAIN: (codepage.CARET, (200, 205, 210), (70, 70, 75)),
    TerrainType.DESERT: (codepage.MIDDLE_DOT, (210, 190, 110), (130, 110, 45)),
    TerrainType.TUNDRA: (codepage.UNDERSCORE, (170, 175, 180), (55, 60, 65)),
}


def visual(terrain: TerrainType) -> TileVisual:
    """Return the (glyph, fg, bg) triple for the given terrain type."""
    return _VISUALS[terrain]
