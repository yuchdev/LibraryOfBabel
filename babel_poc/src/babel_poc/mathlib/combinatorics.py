import math

from babel_poc.mathlib.logmath import log10_combination, log10_sum_exp


def log10_no_adjacent_punct(n: int, w: int, p: int) -> float:
    """
    log10 of the number of sequences of length N from (W words + P punctuation)
    where no two punctuation tokens are adjacent.

    Formula: sum over k=0..floor(N/2): C(N-k+1, k) * P^k * W^(N-k)

    Uses log-space summation.
    """
    if w == 0:
        return float("-inf")
    log10_w = math.log10(w) if w > 0 else float("-inf")
    log10_p = math.log10(p) if p > 0 else float("-inf")
    max_k = n // 2
    log10_terms: list[float] = []
    for k in range(0, max_k + 1):
        log10_c = log10_combination(n - k + 1, k)
        log10_pk = k * log10_p if p > 0 else (0.0 if k == 0 else float("-inf"))
        log10_wn_k = (n - k) * log10_w
        term = log10_c + log10_pk + log10_wn_k
        if not math.isinf(term):
            log10_terms.append(term)
    return log10_sum_exp(log10_terms)
