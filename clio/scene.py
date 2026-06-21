"""Base scene class and transition contract for the Clio scene loop.

Scenes are the top-level state machine for the app. Each scene owns its
event handling, update logic, and drawing.

The app manages a stack of scenes:

  - stack[-1]        → the active (current) scene
  - scenes beneath   → idle, preserved on the stack

At the end of each tick the active scene's transition is consumed:

  - None             → stay on the current scene
  - ShowWorldMap(…)  → app constructs a WorldMapScene and pushes it; the
                        previous scene stays on the stack (goes idle)
  - Pop              → discard the current scene; the one beneath becomes
                        active; if the stack is empty the app exits

Each scene carries the active UI theme. The app passes the current theme into
newly constructed scenes so the chosen theme follows the session.
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from clio import palette
from clio.world import MapGenerator


# ---------------------------------------------------------------------------
# Transition request types
# ---------------------------------------------------------------------------


class SceneRequest:
    """A description of a scene to transition into; the app builds it."""


@dataclass(frozen=True)
class ShowWorldMap(SceneRequest):
    """Request a transition to the world map scene using the given generator."""

    generator: MapGenerator


class Pop:
    """Terminate the current scene; return to the one beneath it on the stack."""


type Transition = SceneRequest | Pop | None


# ---------------------------------------------------------------------------
# Base scene
# ---------------------------------------------------------------------------


class Scene:
    def __init__(self, theme: palette.Theme) -> None:
        self.theme = theme
        self._transition: Transition = None

    def cycle_theme(self) -> None:  # TEMPORARY (see palette.py)
        """Advance this scene's theme to the next in palette.THEMES."""
        self.theme = palette.next_theme(self.theme)

    # ------------------------------------------------------------------
    # Transition API
    # ------------------------------------------------------------------

    def take_transition(self) -> Transition:
        """Consume and return the pending transition, clearing it.

        Called by the app after each tick. A second call within the same
        tick returns None so a returned-to idle scene never auto-fires
        a stale signal.
        """
        t = self._transition
        self._transition = None
        return t

    def transition_to(self, request: SceneRequest) -> None:
        """Signal a transition to the described scene."""
        self._transition = request

    def terminate(self) -> None:
        """Signal that this scene should be popped from the stack."""
        self._transition = Pop()

    # ------------------------------------------------------------------
    # Overridable scene hooks
    # ------------------------------------------------------------------

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: int) -> None:
        """Called each frame with elapsed milliseconds since the last tick."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass
