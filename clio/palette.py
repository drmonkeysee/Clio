"""Centralized color palette for Clio.

All color constants live here. Never scatter RGB literals elsewhere in the
codebase — always reference via this module (same discipline as codepage.py).

Usage::

    from clio import palette

    themes = palette.ThemeManager()     # owns the active theme + toggle
    surf.fill(themes.current.background)
    font.render(text, True, themes.current.text)
    themes.cycle()                      # advance to the next theme
"""

from dataclasses import dataclass
from typing import final

type Color = tuple[int, int, int]


# ---------------------------------------------------------------------------
# Terrain colors
# Foreground (glyph) and background (biome fill) for each TerrainType.
# Both themes share these values — the naturalistic map palette is fixed.
# ---------------------------------------------------------------------------
# fmt: off
OCEAN_FG: Color = (60, 100, 180)        # ≈ deep blue glyph
OCEAN_BG: Color = (5, 15, 45)           # deep water
COAST_FG: Color = (100, 180, 210)       # light cyan glyph
COAST_BG: Color = (20, 50, 100)         # shallow water
RIVER_FG: Color = (80, 160, 255)        # bright blue glyph
RIVER_BG: Color = (20, 40, 90)          # river channel
PLAIN_FG: Color = (100, 170, 60)        # grass-green glyph
PLAIN_BG: Color = (20, 55, 20)          # grassland
FOREST_FG: Color = (30, 110, 30)        # dark green glyph
FOREST_BG: Color = (10, 35, 10)         # dense canopy
HILL_FG: Color = (165, 145, 80)         # tan glyph
HILL_BG: Color = (55, 50, 20)           # earthy brown
MOUNTAIN_FG: Color = (200, 205, 210)    # near-white glyph
MOUNTAIN_BG: Color = (70, 70, 75)       # grey rock
DESERT_FG: Color = (210, 190, 110)      # sand glyph
DESERT_BG: Color = (130, 110, 45)       # baked earth
TUNDRA_FG: Color = (170, 175, 180)      # grey glyph
TUNDRA_BG: Color = (55, 60, 65)         # cold ground
# fmt: on


# ---------------------------------------------------------------------------
# UI chrome themes
#
# Each Theme bundles the five UI chrome colors. Terrain colors above are
# shared by all themes and not included here.
#
# Toggle in any scene with the `t` key (calls Scene.cycle_theme()).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Theme:
    """Bundle of UI chrome colors for a single visual theme."""

    name: str
    background: Color  # screen / surface fill
    border: Color  # frame ring
    text: Color  # title + active menu item
    dim: Color  # subtitle, inactive menu items, help text
    accent: Color  # selection cursor / highlighted line


# Warm bone-white over near-black — Dwarf Fortress parchment-on-dark feel.
# Neutral chrome recedes so terrain hues lead.
BONE_STONE: Theme = Theme(
    name="Bone & Stone",
    background=(14, 14, 16),
    border=(208, 200, 182),
    text=(208, 200, 182),
    dim=(120, 116, 104),
    accent=(224, 196, 128),
)

# Warmer aged-paper tones — old cartography / sepia feel.
# Leans into the desert and hill tans.
PARCHMENT: Theme = Theme(
    name="Parchment",
    background=(20, 18, 16),
    border=(198, 180, 150),
    text=(198, 180, 150),
    dim=(110, 100, 84),
    accent=(170, 140, 90),
)

# Cool desaturated blue-gray chrome — Brogue / cavern feel.
# Harmonizes with the ocean and mountain blues in the terrain palette.
BROGUE_SLATE: Theme = Theme(
    name="Brogue Slate",
    background=(10, 12, 16),
    border=(150, 170, 190),
    text=(150, 170, 190),
    dim=(80, 95, 110),
    accent=(190, 205, 220),
)

# Ordered tuple of all available themes.
THEMES: tuple[Theme, ...] = (BONE_STONE, PARCHMENT, BROGUE_SLATE)


@final
class ThemeManager:
    """Owns the active theme and the cycle toggle.

    Scenes hold a reference to one shared instance, so a change made in any
    scene is immediately visible in all others.
    """

    def __init__(
        self,
        themes: tuple[Theme, ...] = THEMES,
        start: int = 0,
    ) -> None:
        self._themes = themes
        self._index = start

    @property
    def current(self) -> Theme:
        """The currently active theme."""
        return self._themes[self._index]

    def cycle(self) -> None:
        """Advance to the next theme, wrapping around."""
        self._index = (self._index + 1) % len(self._themes)
