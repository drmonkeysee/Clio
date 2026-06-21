from __future__ import annotations

from enum import Enum

from clio.world.grid import WorldMap
from clio.world.random import generate_random as generate_random
from clio.world.simplex import generate_simplex as generate_simplex


class MapGenerator(Enum):
    """Enumeration of available map-generation algorithms.

    Callable: ``generator(rows, cols)`` returns a ``WorldMap``.
    """

    SIMPLEX = "simplex"
    RANDOM = "random"

    def __call__(self, rows: int, cols: int, seed: int | None = None) -> WorldMap:
        match self:
            case MapGenerator.SIMPLEX:
                return generate_simplex(rows, cols, seed)
            case MapGenerator.RANDOM:
                return generate_random(rows, cols, seed)
