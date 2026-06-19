import numpy as np
from opensimplex import OpenSimplex

from clio.world.grid import WorldMap
from clio.world.terrain import TerrainType

# --- Elevation thresholds (0–1 after border fade) ---
_OCEAN_THRESHOLD: float = 0.38  # below → deep ocean
_COAST_THRESHOLD: float = 0.45  # below → shallow coast
_HILL_THRESHOLD: float = 0.73  # above → hill (top ~15% of land tiles)
_MOUNTAIN_THRESHOLD: float = 0.83  # above → mountain (top ~8% of land)

# --- Climate thresholds ---
_COLD_THRESHOLD: float = 0.30  # temperature below → tundra eligible
_HOT_THRESHOLD: float = 0.68  # temperature above → desert eligible if dry
_DRY_THRESHOLD: float = 0.35  # moisture below → dry (desert)
_WET_THRESHOLD: float = 0.55  # moisture above → wet (forest)

# --- Noise parameters ---
# NOTE (map sizes): frequency is relative — linspace maps [0, frequency] across
# the tile count, so continent size scales proportionally with the map. On larger
# maps (128×128, 256×256) the continent-to-world ratio stays the same, but you
# will likely want more octaves to add tile-level detail, and possibly a higher
# frequency to produce more distinct landmasses. The elevation/climate thresholds
# are approximately size-stable (min-max normalisation keeps noise in [0, 1]
# regardless of sample count), but revisit them if biome distribution looks wrong.
_ELEV_FREQUENCY: float = 2.0  # ~2 noise cycles across the map → continent scale
_ELEV_OCTAVES: int = 5  # detail octaves for elevation
_MOIST_FREQUENCY: float = 3.0  # moisture varies at finer scale than elevation
_MOIST_OCTAVES: int = 3

# --- Border fade: land clusters centrally, ocean frames the edges ---
# Multiplicative fade that is 1.0 in the inner circle and drops to 0 at the
# corners. Only the outer ring is affected; interior tiles are untouched.
_INNER_FRACTION: float = 0.65  # normalised radius below which fade = 1.0

# --- Elevation cooling: highlands are colder than lowlands ---
_ELEVATION_COOLING: float = 0.35

# Seed offsets for independent noise passes (prime gaps, avoids correlation).
_MOISTURE_SEED_OFFSET: int = 1_000_003


def _fractal_noise(
    seed: int,
    rows: int,
    cols: int,
    *,
    octaves: int,
    frequency: float,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
) -> np.ndarray:
    """Multi-octave (fractal / fBm) simplex noise, normalized to 0–1.

    Returns a float32 array of shape (rows, cols).
    `noise2array(xs, ys)` returns shape (len(ys), len(xs)), so we pass
    xs of length cols and ys of length rows.
    """
    xs = np.linspace(0.0, frequency, cols, dtype=np.float64)
    ys = np.linspace(0.0, frequency, rows, dtype=np.float64)

    result = np.zeros((rows, cols), dtype=np.float64)
    amplitude = 1.0
    total_amplitude = 0.0
    freq_scale = 1.0

    for i in range(octaves):
        gen = OpenSimplex(seed + i)
        result += gen.noise2array(xs * freq_scale, ys * freq_scale) * amplitude
        total_amplitude += amplitude
        amplitude *= persistence
        freq_scale *= lacunarity

    # noise2array returns values in [-1, 1]; sum is in [-total_amplitude, total_amplitude].
    # Map to [0, 1] via the theoretical range, then stretch to use the full
    # [0, 1] range (min-max normalise) so thresholds are seed-independent.
    result = (result / total_amplitude + 1.0) / 2.0
    lo, hi = result.min(), result.max()
    if hi > lo:
        result = (result - lo) / (hi - lo)
    return result.astype(np.float32)


def _border_fade(rows: int, cols: int) -> np.ndarray:
    """Multiplicative weight: 1.0 in the inner circle, 0 at the corners.

    Tiles inside the inner circle (normalised radius < _INNER_FRACTION) are
    unaffected (weight = 1.0). Tiles beyond that radius fade smoothly to 0,
    so the map's outer ring is pulled toward ocean while the interior keeps
    its full noise-driven elevation (design §1.3 Step 1).
    """
    ry = np.linspace(-1.0, 1.0, rows, dtype=np.float32)
    rx = np.linspace(-1.0, 1.0, cols, dtype=np.float32)
    yy, xx = np.meshgrid(ry, rx, indexing="ij")
    dist = np.sqrt(yy**2 + xx**2) / np.sqrt(2.0)  # 0 = centre, 1 = corner
    fade = (1.0 - dist) / (1.0 - _INNER_FRACTION)
    return np.clip(fade, 0.0, 1.0).astype(np.float32)


def generate(
    rows: int,
    cols: int,
    seed: int | None = None,
) -> WorldMap:
    """Return a noise-driven world map with geographic structure.

    Implements design §1.3 Steps 1–3 (elevation, temperature, moisture;
    rivers and resource placement are deferred). The result is deterministic
    for a given seed; omit seed for a random world.
    """
    if seed is None:
        seed = int(np.random.default_rng().integers(0, 2**31))

    # --- Step 1: Elevation ---
    elevation = _fractal_noise(
        seed,
        rows,
        cols,
        octaves=_ELEV_OCTAVES,
        frequency=_ELEV_FREQUENCY,
    )
    # Border fade: multiply elevation by a weight that is 1 in the interior
    # and 0 at the corners, so the outer ring is ocean-dominant (§1.3 Step 1).
    elevation = elevation * _border_fade(rows, cols)

    # --- Step 2: Temperature ---
    # Primary driver is latitude: equator (middle row) warm, poles cold.
    mid = (rows - 1) / 2.0
    lat_warm = (1.0 - np.abs(np.arange(rows, dtype=np.float32) - mid) / mid)[
        :, np.newaxis
    ]  # (rows, 1) — broadcasts across cols
    # Elevation cools highlands.
    temperature = np.clip(lat_warm - elevation * _ELEVATION_COOLING, 0.0, 1.0).astype(
        np.float32
    )

    # --- Step 3: Moisture ---
    moisture = _fractal_noise(
        seed + _MOISTURE_SEED_OFFSET,
        rows,
        cols,
        octaves=_MOIST_OCTAVES,
        frequency=_MOIST_FREQUENCY,
    )

    # --- Terrain classification (vectorized) ---
    land = elevation >= _COAST_THRESHOLD

    # Water classification.
    water_type = np.where(
        elevation < _OCEAN_THRESHOLD,
        np.uint8(TerrainType.OCEAN),
        np.uint8(TerrainType.COAST),
    )

    # Land classification ordered by precedence (elevation first, then climate).
    cold = temperature < _COLD_THRESHOLD
    hot_dry = (temperature >= _HOT_THRESHOLD) & (moisture < _DRY_THRESHOLD)
    wet = moisture >= _WET_THRESHOLD

    land_type = np.select(
        [
            elevation >= _MOUNTAIN_THRESHOLD,
            elevation >= _HILL_THRESHOLD,
            cold,
            hot_dry,
            wet,
        ],
        [
            np.uint8(TerrainType.MOUNTAIN),
            np.uint8(TerrainType.HILL),
            np.uint8(TerrainType.TUNDRA),
            np.uint8(TerrainType.DESERT),
            np.uint8(TerrainType.FOREST),
        ],
        default=np.uint8(TerrainType.PLAIN),
    )

    terrain = np.where(land, land_type, water_type).astype(np.uint8)

    # Biome is the climate-refined terrain classification. Currently equal to
    # terrain; will diverge once cultural and resource layers are added.
    biome = terrain.copy()

    return WorldMap(
        terrain=terrain,
        elevation=elevation,
        temperature=temperature,
        moisture=moisture,
        biome=biome,
    )
