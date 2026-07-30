"""Certificates for the Round 29 resonant-multistar convergence audit."""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import log

import sympy as sp


def densest_dyadic_divisor_bin(number: int) -> dict:
    """Choose a dyadic interval containing the most positive divisors."""
    if number < 1:
        raise ValueError("number must be positive")
    bins: dict[int, list[int]] = defaultdict(list)
    divisors = tuple(int(value) for value in sp.divisors(number))
    for divisor in divisors:
        bins[divisor.bit_length() - 1].append(divisor)
    index, selected = max(bins.items(), key=lambda item: (len(item[1]), -item[0]))
    return {
        "number": number,
        "divisors": divisors,
        "tau": len(divisors),
        "bin_index": index,
        "lower_endpoint": 1 << index,
        "upper_endpoint": 1 << (index + 1),
        "selected": tuple(selected),
        "count": len(selected),
        "pigeonhole_lower_bound": Fraction(
            len(divisors), number.bit_length()
        ),
    }


def divisor_multistar_certificate(number: int) -> dict:
    """Build the rank-three, same-frequency divisor multistar.

    With a transcendental T, use the proper box on

        g1=T/2, g2=R*T^-1/(2N), g3=1/2.

    For every selected divisor x|N, y=N/x and t=xT give shifts

        u=x*g1+y*g2+3*g3,  c=x*g1-y*g2.

    Both c-Y and -c-Y lie above u on the SAT hyperbola.
    """
    bin_data = densest_dyadic_divisor_bin(number)
    selected = bin_data["selected"]
    max_x = max(selected)
    max_y = max(number // value for value in selected)
    side_x = 2 * max_x + 1
    side_y = 2 * max_y + 1
    side_constant = 7
    p_size = side_x * side_y * side_constant
    n = 2 * p_size

    extra = 0
    witnesses = []
    for x in selected:
        y = number // x
        overlap_p_u = (
            (side_x - x)
            * (side_y - y)
            * (side_constant - 3)
        )
        overlap_p_c = (side_x - x) * (side_y - y) * side_constant
        overlap_a_u = 2 * overlap_p_u
        overlap_a_v = overlap_p_c
        contribution = 2 * overlap_a_u * overlap_a_v
        extra += contribution
        witnesses.append(
            {
                "x": x,
                "y": y,
                "product": x * y,
                "overlap_u": overlap_a_u,
                "overlap_v_plus": overlap_a_v,
                "overlap_v_minus": overlap_a_v,
                "contribution": contribution,
            }
        )

    certified_H = n * n + extra
    return {
        **bin_data,
        "side_lengths": (side_x, side_y, side_constant),
        "p_size": p_size,
        "n": n,
        "witnesses": tuple(witnesses),
        "certified_H": certified_H,
        "certified_average_degree": Fraction(certified_H, n * n),
        "uniform_average_lower_bound": 1 + Fraction(len(selected), 28),
        "linear_size_bound": 210 * number,
    }


def first_prime_product(count: int) -> int:
    if count < 1:
        raise ValueError("count must be positive")
    primes = list(sp.primerange(1, 10**4))
    return int(sp.prod(primes[:count]))


def primorial_multistar_certificate(prime_count: int) -> dict:
    number = first_prime_product(prime_count)
    result = divisor_multistar_certificate(number)
    result["prime_count"] = prime_count
    result["squarefree_tau"] = 2**prime_count
    return result


def independent_box_rate(side_length: int) -> float:
    """Coefficient of log(n) in the independent-frequency box."""
    if side_length < 2:
        raise ValueError("side length must be at least two")
    return (1 - 1 / side_length) ** 2 / (2 * log(side_length))


def best_integer_side_length(limit: int = 100) -> dict:
    choices = {
        side: independent_box_rate(side) for side in range(2, limit + 1)
    }
    side = max(choices, key=choices.get)
    return {"side_length": side, "rate": choices[side], "choices": choices}


def ansatz_no_go_ledger() -> dict:
    """Asymptotic exponents in the lattice-aligned ansatz."""
    return {
        "target_average_exponent": Fraction(2, 5),
        "ansatz_average_form": "exp((log(2)+o(1))*log(n)/loglog(n))",
        "ansatz_power_exponent": Fraction(0),
        "target_over_ansatz": "n^(2/5-o(1))",
        "independent_frequency_growth": "Theta(log(n))",
        "same_frequency_low_rank_growth": (
            "exp(Theta(log(n)/loglog(n)))"
        ),
        "tensor_rule": "additive gains, not multiplicative gains",
        "generic_union_rule": "quadratic-mass weighted; no larger exponent",
    }


if __name__ == "__main__":
    for prime_count in (4, 6, 8, 10):
        result = primorial_multistar_certificate(prime_count)
        print(
            "primes=", prime_count,
            "N=", result["number"],
            "tau=", result["tau"],
            "bin=", result["count"],
            "n=", result["n"],
            "average>=", result["certified_average_degree"],
        )
    print("best independent-box side", best_integer_side_length()["side_length"])
    print(ansatz_no_go_ledger())
