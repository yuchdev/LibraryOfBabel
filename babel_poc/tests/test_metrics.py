import math

from babel_poc.constants import BORGES_LOG10_SIZE, UNIVERSE_ATOMS_LOG10
from babel_poc.mathlib.metrics import calculate_metrics


def test_calculate_metrics_basic():
    metrics = calculate_metrics("test", 1000.0)
    assert metrics.mode_id == "test"
    assert math.isclose(metrics.log10_size, 1000.0)
    assert metrics.exponent == 1000
    assert math.isclose(metrics.mantissa, 1.0, rel_tol=1e-9)


def test_smaller_than_borges():
    metrics = calculate_metrics("test", 1000.0)
    assert metrics.log10_smaller_than_borges > 0


def test_larger_than_borges():
    metrics = calculate_metrics("huge", BORGES_LOG10_SIZE + 100)
    assert metrics.log10_smaller_than_borges < 0


def test_larger_than_universe():
    metrics = calculate_metrics("test", UNIVERSE_ATOMS_LOG10 + 50)
    assert metrics.log10_larger_than_universe_atoms > 0


def test_scientific_notation():
    metrics = calculate_metrics("test", 3.30103)
    assert metrics.exponent == 3
    assert math.isclose(metrics.mantissa, 2.0, rel_tol=1e-4)
