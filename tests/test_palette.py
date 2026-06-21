from clio import palette


def test_theme_manager_starts_on_first_theme() -> None:
    tm = palette.ThemeManager()
    assert tm.current is palette.THEMES[0]


def test_theme_manager_cycle_advances_in_order() -> None:
    tm = palette.ThemeManager()
    themes = list(palette.THEMES)
    for expected in themes[1:]:
        tm.cycle()
        assert tm.current is expected


def test_theme_manager_cycle_wraps_around() -> None:
    tm = palette.ThemeManager()
    for _ in palette.THEMES:
        tm.cycle()
    assert tm.current is palette.THEMES[0]


def test_theme_manager_custom_start_index() -> None:
    tm = palette.ThemeManager(start=1)
    assert tm.current is palette.THEMES[1]
