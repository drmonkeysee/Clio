import numpy as np

from clio.world.grid import WorldMap
from clio.world.terrain import TerrainType

# TerrainType integer values in enum order.
_TERRAIN_VALUES: list[int] = [t.value for t in TerrainType]

# Weighted distribution. No spatial structure — each tile is drawn independently.
# Weights chosen to produce a visually varied map: roughly 30% water, 70% land.
_WEIGHTS: list[float] = [
    0.20,  # OCEAN
    0.08,  # COAST
    0.04,  # RIVER  (placeholder; proper rivers are edge features, §1.3 Step 4)
    0.22,  # PLAIN
    0.18,  # FOREST
    0.12,  # HILL
    0.05,  # MOUNTAIN
    0.07,  # DESERT
    0.04,  # TUNDRA
]

assert len(_TERRAIN_VALUES) == len(_WEIGHTS), "terrain/weight mismatch"
assert abs(sum(_WEIGHTS) - 1.0) < 1e-9, "weights must sum to 1"


def generate(
    rows: int,
    cols: int,
    seed: int | None = None,
) -> WorldMap:
    """Return a fully random (spatially unstructured) world map.

    Each tile is independently sampled — no noise, no clustering. Intended
    as a visual proof-of-concept for the rendering pipeline; use
    `generate_simplex` for structured, noise-driven terrain instead.
    """
    rng = np.random.default_rng(seed)

    terrain = rng.choice(
        np.array(_TERRAIN_VALUES, dtype=np.uint8),
        size=(rows, cols),
        p=_WEIGHTS,
    ).astype(np.uint8)

    elevation = rng.random((rows, cols)).astype(np.float32)
    temperature = rng.random((rows, cols)).astype(np.float32)
    moisture = rng.random((rows, cols)).astype(np.float32)
    biome = terrain.copy()

    return WorldMap(
        terrain=terrain,
        elevation=elevation,
        temperature=temperature,
        moisture=moisture,
        biome=biome,
    )
