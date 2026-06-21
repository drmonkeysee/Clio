from clio import palette
from clio.scene import Pop, Scene, ShowWorldMap
from clio.world import MapGenerator

_T0 = palette.THEMES[0]
_T1 = palette.THEMES[1]


def test_scene_default_state() -> None:
    scene = Scene(_T0)
    assert scene.theme is _T0
    assert scene.take_transition() is None


def test_take_transition_returns_none_when_no_transition() -> None:
    scene = Scene(_T0)
    assert scene.take_transition() is None


def test_take_transition_returns_request_and_clears_it() -> None:
    scene = Scene(_T0)
    req = ShowWorldMap(MapGenerator.SIMPLEX)
    scene.transition_to(req)
    assert scene.take_transition() is req
    assert scene.take_transition() is None  # cleared after first take


def test_terminate_signals_pop() -> None:
    scene = Scene(_T0)
    scene.terminate()
    assert isinstance(scene.take_transition(), Pop)


def test_terminate_clears_after_take() -> None:
    scene = Scene(_T0)
    scene.terminate()
    scene.take_transition()
    assert scene.take_transition() is None


def test_cycle_theme_advances_through_themes() -> None:
    scene = Scene(_T0)
    for expected in list(palette.THEMES[1:]) + [palette.THEMES[0]]:
        scene.cycle_theme()
        assert scene.theme is expected
