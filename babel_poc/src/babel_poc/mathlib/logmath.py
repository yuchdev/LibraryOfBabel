import math


def log10_pow(base: float, exponent: int) -> float:
    """log10(base^exponent) = exponent * log10(base)"""
    return exponent * math.log10(base)


def log10_ratio(log10_a: float, log10_b: float) -> float:
    """log10(a/b) = log10(a) - log10(b)"""
    return log10_a - log10_b


def scientific_from_log10(log10_value: float) -> tuple[float, int]:
    """
    Convert log10(x) to mantissa/exponent form.
    Example: 3.30103 -> (2.0, 3)
    """
    exponent = int(math.floor(log10_value))
    mantissa = 10 ** (log10_value - exponent)
    return mantissa, exponent


def log10_sum_exp(log10_terms: list[float]) -> float:
    """Stable log10(sum(10^x_i))."""
    if not log10_terms:
        return float("-inf")
    max_val = max(log10_terms)
    if math.isinf(max_val):
        return max_val
    total = sum(10 ** (x - max_val) for x in log10_terms)
    return max_val + math.log10(total)


def log10_factorial(n: int) -> float:
    """log10(n!) = lgamma(n+1) / ln(10)"""
    return math.lgamma(n + 1) / math.log(10)


def log10_combination(n: int, k: int) -> float:
    """log10(C(n,k))"""
    if k < 0 or k > n:
        return float("-inf")
    return log10_factorial(n) - log10_factorial(k) - log10_factorial(n - k)
