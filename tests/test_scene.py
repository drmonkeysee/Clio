from clio.scene import Scene


def test_scene_default_state() -> None:
    scene = Scene()
    assert scene.next_scene is None
    assert scene.quit is False


def test_get_transition_returns_none_when_no_transition() -> None:
    scene = Scene()
    assert scene.get_transition() is None


def test_get_transition_returns_next_scene() -> None:
    a = Scene()
    b = Scene()
    a.next_scene = b
    assert a.get_transition() is b


def test_get_transition_resets_returned_scene_to_clean_state() -> None:
    # b has its own pending transition to c; after a transitions to b,
    # b must start clean (next_scene = None) so it doesn't immediately
    # re-transition on the next frame.
    a = Scene()
    b = Scene()
    c = Scene()
    a.next_scene = b
    b.next_scene = c
    result = a.get_transition()
    assert result is b
    assert result.next_scene is None
