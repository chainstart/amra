"""Numerical ledgers for the Round 33 unit-rank uniformity audit."""

from __future__ import annotations

from math import ceil, log


def packing_rank_lower_bound(
    n: int,
    shortest_log_vector: float,
    target_exponent: float = 0.4,
    height_radius_constant: float = 1.0,
) -> dict:
    """Rank forced by lattice packing in a logarithmic-height cube.

    A rank-r lattice with shortest sup-norm vector lambda has at most
    (1+2H/lambda)^r points in a cube of radius H.
    """
    if n <= 2 or shortest_log_vector <= 0:
        raise ValueError("need n>2 and a positive shortest vector")
    radius = height_radius_constant * log(n)
    per_rank_log_capacity = log(1 + 2 * radius / shortest_log_vector)
    required = ceil(target_exponent * log(n) / per_rank_log_capacity)
    return {
        "n": n,
        "shortest_log_vector": shortest_log_vector,
        "height_radius": radius,
        "per_rank_log_capacity": per_rank_log_capacity,
        "required_rank": required,
        "normalized_rank": required * log(log(n)) / log(n),
    }


def degree_dependent_proxy(n: int) -> dict:
    """Worst full-power-basis proxy lambda~1/d with d<=log_2 n."""
    degree = max(2, int(log(n, 2)))
    result = packing_rank_lower_bound(n, 1 / degree)
    result["degree_proxy"] = degree
    result["expected_asymptotic_constant"] = 0.2
    return result


def strong_uniformity_proxy(n: int) -> dict:
    """A slowly decaying lambda=(log n)^(-1/sqrt(loglog n))."""
    loglog = log(log(n))
    epsilon = 1 / (loglog**0.5)
    shortest = log(n) ** (-epsilon)
    result = packing_rank_lower_bound(n, shortest)
    result["epsilon"] = epsilon
    result["expected_asymptotic_constant"] = 0.4
    return result


def coordinate_box_cost(n: int, rank: int) -> dict:
    """Minimum binary full-coordinate box cost for rank r."""
    minimum_points = 2 ** (rank + 1)
    return {
        "n": n,
        "rank": rank,
        "minimum_points": minimum_points,
        "fits": minimum_points <= n,
        "power_exponent": log(minimum_points) / log(n),
    }


def conditional_theorem_ledger() -> dict:
    return {
        "exact_count": "(1+2*C*log(n)/lambda_n)^r",
        "exact_rank_bound": (
            "r >= ((2/5)*log(n)+O(1))/"
            "log(1+2*C*log(n)/lambda_n)"
        ),
        "fixed_field": "(2/5-o(1))*log(n)/loglog(n)",
        "strong_uniform_shortest_vector": (
            "lambda_n=(log n)^(-o(1)) gives the same 2/5 constant"
        ),
        "degree_dependent_height_only": (
            "with d<=O(log n), lambda_n>=d^(-1-o(1)) gives only "
            "(1/5-o(1))*log(n)/loglog(n)"
        ),
        "unconditional_warning": (
            "without uniform height/container hypotheses, no rank lower "
            "bound with coefficient 2/5 follows for varying fields"
        ),
        "volume_warning": (
            "the binary coordinate cost 2^r is n^o(1) at either threshold"
        ),
    }


if __name__ == "__main__":
    for exponent in (20, 50, 100, 200):
        n = 10**exponent
        weak = degree_dependent_proxy(n)
        strong = strong_uniformity_proxy(n)
        print(
            "10^", exponent,
            "degree-proxy rank", weak["required_rank"],
            "normalized", weak["normalized_rank"],
            "strong rank", strong["required_rank"],
            "normalized", strong["normalized_rank"],
        )
    print(conditional_theorem_ledger())
