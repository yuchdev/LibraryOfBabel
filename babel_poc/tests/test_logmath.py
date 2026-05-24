import math

from babel_poc.mathlib.logmath import (
    log10_combination,
    log10_factorial,
    log10_pow,
    log10_ratio,
    log10_sum_exp,
    scientific_from_log10,
)


def test_log10_pow_basic():
    assert math.isclose(log10_pow(10, 3), 3.0)
    assert math.isclose(log10_pow(100, 2), 4.0)


def test_log10_ratio():
    assert math.isclose(log10_ratio(3.0, 1.0), 2.0)
    assert math.isclose(log10_ratio(4.0, 4.0), 0.0)


def test_scientific_from_log10_basic():
    mantissa, exp = scientific_from_log10(3.30103)
    assert exp == 3
    assert math.isclose(mantissa, 2.0, rel_tol=1e-4)


def test_scientific_from_log10_integer():
    mantissa, exp = scientific_from_log10(5.0)
    assert exp == 5
    assert math.isclose(mantissa, 1.0, rel_tol=1e-9)


def test_log10_sum_exp_two_zeros():
    result = log10_sum_exp([0.0, 0.0])
    assert math.isclose(result, math.log10(2), rel_tol=1e-9)


def test_log10_sum_exp_empty():
    result = log10_sum_exp([])
    assert math.isinf(result)


def test_log10_factorial_zero():
    assert math.isclose(log10_factorial(0), 0.0, abs_tol=1e-9)


def test_log10_factorial_five():
    assert math.isclose(log10_factorial(5), math.log10(120), rel_tol=1e-9)


def test_log10_combination_basic():
    result = log10_combination(5, 2)
    assert math.isclose(result, math.log10(10), rel_tol=1e-9)


def test_log10_combination_edge():
    assert math.isclose(log10_combination(5, 0), 0.0, abs_tol=1e-9)
    assert math.isclose(log10_combination(5, 5), 0.0, abs_tol=1e-9)
    assert math.isinf(log10_combination(5, 6))
