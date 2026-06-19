from dataclasses import dataclass

import numpy as np


@dataclass
class WorldMap:
    """Tile-based world map stored as parallel numpy arrays.

    Each array is shaped (rows, cols). Static geographic properties only —
    dynamic simulation state (settlements, trade traffic, etc.) is deferred
    until the simulation layer exists.
    """

    terrain: np.ndarray  # uint8: TerrainType values
    elevation: np.ndarray  # float32, 0–1 (raw heightmap, placeholder until noise)
    temperature: np.ndarray  # float32, 0–1
    moisture: np.ndarray  # float32, 0–1
    biome: np.ndarray  # uint8: placeholder equal to terrain; derived from
    # temperature + moisture once noise generation lands

    @property
    def rows(self) -> int:
        return int(self.terrain.shape[0])

    @property
    def cols(self) -> int:
        return int(self.terrain.shape[1])
