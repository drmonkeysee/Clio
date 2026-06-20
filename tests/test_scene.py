from clio import palette
from clio.scene import Scene

_T0 = palette.THEMES[0]
_T1 = palette.THEMES[1]


def test_scene_default_state() -> None:
    scene = Scene(_T0)
    assert scene.theme is _T0
    assert scene.next_scene is None
    assert scene.quit is False


def test_get_transition_returns_none_when_no_transition() -> None:
    scene = Scene(_T0)
    assert scene.get_transition() is None


def test_get_transition_returns_next_scene() -> None:
    a = Scene(_T0)
    b = Scene(_T0)
    a.next_scene = b
    assert a.get_transition() is b


def test_get_transition_resets_returned_scene_to_clean_state() -> None:
    # b has its own pending transition to c; after a transitions to b,
    # b must start clean (next_scene = None) so it doesn't immediately
    # re-transition on the next frame.
    a = Scene(_T0)
    b = Scene(_T0)
    c = Scene(_T0)
    a.next_scene = b
    b.next_scene = c
    result = a.get_transition()
    assert result is b
    assert result.next_scene is None


def test_get_transition_hands_theme_to_next_scene() -> None:
    # The outgoing scene's theme is forwarded to the incoming scene on
    # transition, even if the incoming scene was constructed with a
    # different theme.
    a = Scene(_T0)
    b = Scene(_T1)
    a.next_scene = b
    a.get_transition()
    assert b.theme is _T0


def test_cycle_theme_advances_through_themes() -> None:
    scene = Scene(_T0)
    for expected in list(palette.THEMES[1:]) + [palette.THEMES[0]]:
        scene.cycle_theme()
        assert scene.theme is expected
