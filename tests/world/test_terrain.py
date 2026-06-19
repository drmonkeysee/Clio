import pytest

from clio import codepage
from clio.world.terrain import TerrainType, visual


@pytest.mark.parametrize("terrain", list(TerrainType))
def test_visual_returns_three_tuple(terrain: TerrainType) -> None:
    result = visual(terrain)
    assert len(result) == 3


@pytest.mark.parametrize("terrain", list(TerrainType))
def test_visual_glyph_is_from_codepage(terrain: TerrainType) -> None:
    glyph, _fg, _bg = visual(terrain)
    assert glyph in codepage.CP437


@pytest.mark.parametrize("terrain", list(TerrainType))
def test_visual_colors_are_valid_rgb(terrain: TerrainType) -> None:
    _glyph, fg, bg = visual(terrain)
    for channel in (*fg, *bg):
        assert isinstance(channel, int)
        assert 0 <= channel <= 255
