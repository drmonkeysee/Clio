"""Centralized color palette for Clio.

All color constants live here. Never scatter RGB literals elsewhere in the
codebase — always reference via this module (same discipline as codepage.py).

Usage::

    from clio import palette

    theme = palette.THEMES[0]           # or any Theme value
    theme = palette.next_theme(theme)   # advance to the next; TEMPORARY
    surf.fill(theme.background)
    font.render(text, True, theme.text)
"""

from dataclasses import dataclass

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
# UI chrome themes  (TEMPORARY — remove loser after side-by-side comparison)
#
# Each Theme bundles the five UI chrome colors. Terrain colors above are
# shared by all themes and not included here.
#
# Toggle on the title screen with the `t` key (calls Scene.cycle_theme()).
# Once a theme is chosen, delete the unused Theme, THEMES, next_theme(),
# Scene.cycle_theme(), and the K_t handler in title.py.
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

# Ordered tuple of all themes — drives next_theme().  # TEMPORARY
THEMES: tuple[Theme, ...] = (BONE_STONE, PARCHMENT, BROGUE_SLATE)


def next_theme(current: Theme) -> Theme:  # TEMPORARY (see block comment above)
    """Return the next theme after `current` in THEMES, wrapping around."""
    return THEMES[(THEMES.index(current) + 1) % len(THEMES)]
