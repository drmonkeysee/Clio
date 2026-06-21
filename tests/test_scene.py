from clio import palette
from clio.scene import Pop, Scene, ShowWorldMap
from clio.world import MapGenerator

_TM0 = palette.ThemeManager(start=0)
_TM1 = palette.ThemeManager(start=1)


def test_scene_default_state() -> None:
    scene = Scene(palette.ThemeManager())
    assert scene.theme is palette.THEMES[0]
    assert scene.take_transition() is None


def test_take_transition_returns_none_when_no_transition() -> None:
    scene = Scene(palette.ThemeManager())
    assert scene.take_transition() is None


def test_take_transition_returns_request_and_clears_it() -> None:
    scene = Scene(palette.ThemeManager())
    req = ShowWorldMap(MapGenerator.SIMPLEX)
    scene.transition_to(req)
    assert scene.take_transition() is req
    assert scene.take_transition() is None  # cleared after first take


def test_terminate_signals_pop() -> None:
    scene = Scene(palette.ThemeManager())
    scene.terminate()
    assert isinstance(scene.take_transition(), Pop)


def test_terminate_clears_after_take() -> None:
    scene = Scene(palette.ThemeManager())
    scene.terminate()
    scene.take_transition()
    assert scene.take_transition() is None


def test_cycle_theme_advances_through_themes() -> None:
    scene = Scene(palette.ThemeManager())
    for expected in list(palette.THEMES[1:]) + [palette.THEMES[0]]:
        scene.cycle_theme()
        assert scene.theme is expected


def test_shared_manager_propagates_to_all_scenes() -> None:
    """Two scenes sharing a ThemeManager both see a cycle made by either one."""
    tm = palette.ThemeManager()
    s1 = Scene(tm)
    s2 = Scene(tm)
    assert s1.theme is s2.theme is palette.THEMES[0]
    s1.cycle_theme()
    assert s1.theme is palette.THEMES[1]
    assert s2.theme is palette.THEMES[1]
