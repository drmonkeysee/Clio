import numpy as np
import pytest

from clio.world import generate_random, generate_simplex
from clio.world.terrain import TerrainType

# Non-square dimensions to catch row/col swaps in shape assertions.
ROWS, COLS = 16, 24
SEED = 42

_GENERATORS = [generate_random, generate_simplex]
_GENERATOR_IDS = ["generate_random", "generate_simplex"]


@pytest.fixture(params=_GENERATORS, ids=_GENERATOR_IDS)
def generator(request):
    return request.param


def test_output_shapes(generator) -> None:
    world = generator(ROWS, COLS, seed=SEED)
    for field in (
        world.terrain,
        world.elevation,
        world.temperature,
        world.moisture,
        world.biome,
    ):
        assert field.shape == (ROWS, COLS)
    assert world.rows == ROWS
    assert world.cols == COLS


def test_output_dtypes(generator) -> None:
    world = generator(ROWS, COLS, seed=SEED)
    assert world.terrain.dtype == np.uint8
    assert world.biome.dtype == np.uint8
    assert world.elevation.dtype == np.float32
    assert world.temperature.dtype == np.float32
    assert world.moisture.dtype == np.float32


def test_float_fields_in_unit_range(generator) -> None:
    world = generator(ROWS, COLS, seed=SEED)
    for field in (world.elevation, world.temperature, world.moisture):
        assert float(field.min()) >= 0.0
        assert float(field.max()) <= 1.0


def test_terrain_values_are_valid_terrain_types(generator) -> None:
    world = generator(ROWS, COLS, seed=SEED)
    valid = {t.value for t in TerrainType}
    actual = set(np.unique(world.terrain).tolist())
    assert actual.issubset(valid)


def test_biome_equals_terrain_but_is_distinct_array(generator) -> None:
    world = generator(ROWS, COLS, seed=SEED)
    assert np.array_equal(world.biome, world.terrain)
    assert world.biome is not world.terrain


def test_determinism(generator) -> None:
    a = generator(ROWS, COLS, seed=SEED)
    b = generator(ROWS, COLS, seed=SEED)
    assert np.array_equal(a.terrain, b.terrain)
    assert np.array_equal(a.elevation, b.elevation)
    assert np.array_equal(a.temperature, b.temperature)
    assert np.array_equal(a.moisture, b.moisture)
    assert np.array_equal(a.biome, b.biome)


def test_different_seeds_produce_different_results(generator) -> None:
    a = generator(ROWS, COLS, seed=42)
    b = generator(ROWS, COLS, seed=99)
    assert not np.array_equal(a.terrain, b.terrain)
