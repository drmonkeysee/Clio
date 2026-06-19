"""Base scene class and transition contract for the Clio scene loop.

Scenes are the top-level state machine for the app. Each scene owns its
event handling, update logic, and drawing. The main loop in app.py reads
`next_scene` after every frame:

  - None          → stay in the current scene
  - another Scene → switch to that scene next frame
  - (sentinel)    → exit the app (set via Scene.request_quit())

The quit sentinel is a private module-level object; callers should only test
for it with `is_quit()`.
"""

from __future__ import annotations

import pygame

_QUIT: object = object()


class Scene:
    def __init__(self) -> None:
        # object covers all three states: None (stay), Scene (transition),
        # and _QUIT sentinel (exit). Callers test with is_quit() / isinstance.
        self.next_scene: object = None

    def request_quit(self) -> None:
        """Signal the main loop to exit after this frame."""
        self.next_scene = _QUIT

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: int) -> None:
        """Called each frame with elapsed milliseconds since the last tick."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass


def is_quit(scene: object) -> bool:
    """Return True if *scene* is the quit sentinel set by Scene.request_quit()."""
    return scene is _QUIT
