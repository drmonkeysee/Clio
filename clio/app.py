import pygame

WINDOW_SIZE: tuple[int, int] = (640, 400)
TITLE: str = "Clio"
MESSAGE: str = "Hello from clio!"
BACKGROUND: tuple[int, int, int] = (10, 10, 10)
AMBER: tuple[int, int, int] = (255, 176, 0)
FONT_SIZE: int = 24
FPS: int = 30

_CURSOR_BLINK_MS = 530
_H_PAD = 3
_V_PAD = 1


def _load_font():
    # Comma-separated list gives pygame a fallback chain; Menlo ships on macOS,
    # Consolas on Windows, DejaVu Sans Mono on Linux.
    return pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", FONT_SIZE)


def _panel_rows(show_cursor):
    cursor = "█" if show_cursor else " "
    msg = f"{MESSAGE}{cursor}"
    inner = len(msg) + _H_PAD * 2
    top = "╔" + "═" * inner + "╗"
    empty = "║" + " " * inner + "║"
    middle = "║" + " " * _H_PAD + msg + " " * _H_PAD + "║"
    bottom = "╚" + "═" * inner + "╝"
    return [top] + [empty] * _V_PAD + [middle] + [empty] * _V_PAD + [bottom]


def _build_panel(font, show_cursor):
    rows = _panel_rows(show_cursor)
    _, char_h = font.size("M")
    # Measure panel width from the rendered top row (handles glyph metrics correctly).
    sample = font.render(rows[0], True, AMBER)
    surf = pygame.Surface((sample.get_width(), char_h * len(rows)), pygame.SRCALPHA)
    for i, row in enumerate(rows):
        surf.blit(font.render(row, True, AMBER), (0, i * char_h))
    return surf


def run() -> None:
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    font = _load_font()
    clock = pygame.time.Clock()

    # Pre-build both cursor states so the loop never allocates during rendering.
    panels = {True: _build_panel(font, True), False: _build_panel(font, False)}
    center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

    cursor_on = True
    last_blink = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        now = pygame.time.get_ticks()
        if now - last_blink >= _CURSOR_BLINK_MS:
            cursor_on = not cursor_on
            last_blink = now

        screen.fill(BACKGROUND)
        panel = panels[cursor_on]
        screen.blit(panel, panel.get_rect(center=center))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
