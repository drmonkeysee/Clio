import pygame

from clio import palette, scene as scene_mod
from clio.render import TILE_LOGICAL
from clio.scenes.title import TitleScene

_TITLE: str = "Clio"
_UI_FONT_SIZE: int = 24
_FPS: int = 60

# Window logical size derived from map dimensions × tile size.
# HiDPI surfaces are larger; scale is computed from the ratio at runtime.
_MAP_COLS: int = 64
_MAP_ROWS: int = 56
_LOGICAL_SIZE: tuple[int, int] = (
    (_MAP_COLS + 2) * TILE_LOGICAL,
    (_MAP_ROWS + 2) * TILE_LOGICAL,
)


def _make_font(size: int) -> pygame.font.Font:
    # Comma-separated list gives pygame a fallback chain; Menlo ships on macOS,
    # Consolas on Windows, DejaVu Sans Mono on Linux.
    return pygame.font.SysFont("menlo,consolas,dejavusansmono,monospace", max(1, size))


def run() -> None:
    pygame.init()
    win = pygame.Window(_TITLE, _LOGICAL_SIZE, allow_high_dpi=True)
    screen = win.get_surface()

    # On HiDPI displays (e.g. Retina) the surface is larger than _LOGICAL_SIZE.
    # Scale all pixel sizes to match physical pixel density.
    scale = screen.get_height() / _LOGICAL_SIZE[1]
    tile = max(1, round(TILE_LOGICAL * scale))

    ui_font = _make_font(round(_UI_FONT_SIZE * scale))
    tile_font = _make_font(tile)

    clock = pygame.time.Clock()
    current: scene_mod.Scene = TitleScene(
        palette.THEMES[0], ui_font, tile_font, tile, _MAP_COLS, _MAP_ROWS
    )

    running = True
    while running:
        dt = clock.tick(_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            current.handle_event(event)

        if not running:
            break

        current.update(dt)
        current.draw(screen)
        win.flip()

        # Check for scene transition after drawing this frame.
        if current.quit:
            running = False
        elif nxt := current.get_transition():
            current = nxt

    win.destroy()
    pygame.quit()
