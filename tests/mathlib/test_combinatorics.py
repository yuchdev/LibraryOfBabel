import itertools
import math

from babel.mathlib.combinatorics import log10_no_adjacent_punct


def _bruteforce_count(n: int, w: int, p: int) -> int:
    # Exponential by design; keep n small in tests.
    symbols = [f"w{i}" for i in range(w)] + [f"p{i}" for i in range(p)]
    punct = set(symbols[w:])
    count = 0
    for sequence in itertools.product(symbols, repeat=n):
        if all(not (sequence[i] in punct and sequence[i + 1] in punct) for i in range(n - 1)):
            count += 1
    return count


def test_log10_no_adjacent_punct_matches_bruteforce_small_case():
    n, w, p = 5, 2, 1
    expected = _bruteforce_count(n, w, p)
    actual = log10_no_adjacent_punct(n, w, p)
    assert math.isclose(actual, math.log10(expected), rel_tol=1e-9)
