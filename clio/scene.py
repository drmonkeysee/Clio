"""Base scene class and transition contract for the Clio scene loop.

Scenes are the top-level state machine for the app. Each scene owns its
event handling, update logic, and drawing. The main loop in app.py checks
the scene transition after every frame:

  - None          → stay in the current scene
  - another Scene → switch to that scene next frame
  - quit flag     → exit the app
"""

from __future__ import annotations

import pygame


class Scene:
    def __init__(self) -> None:
        self.next_scene: Scene | None = None
        self.quit: bool = False

    def get_transition(self) -> Scene | None:
        """Get the next scene transition, or None to stay on this scene."""
        if nxt := self.next_scene:
            nxt.next_scene = None   # reset so the scene starts clean
        return nxt

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: int) -> None:
        """Called each frame with elapsed milliseconds since the last tick."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
