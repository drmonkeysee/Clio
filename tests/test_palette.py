from clio import palette


def test_next_theme_advances_in_order() -> None:
    themes = list(palette.THEMES)
    for i, current in enumerate(themes):
        expected = themes[(i + 1) % len(themes)]
        assert palette.next_theme(current) is expected


def test_next_theme_wraps_around() -> None:
    last = palette.THEMES[-1]
    assert palette.next_theme(last) is palette.THEMES[0]
