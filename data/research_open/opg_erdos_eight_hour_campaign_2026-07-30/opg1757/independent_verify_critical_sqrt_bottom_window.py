#!/usr/bin/env python3
"""Independent red-team checks for the critical square-root window.

No AMRA verifier is imported.  The script distinguishes the direct
Corollary-4 condition from the sharper specialization of equation (39),
checks every earlier Newton parameter, audits the small-N scope of the
main-ratio inequality, and independently evaluates the main-term model.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction


WINDOW_DENOMINATOR = 2**28
WINDOW_THRESHOLD = 9 * 2**58


def endpoint_parameters(k: int, depth: int):
    if k < 2 or depth < 0:
        raise ValueError("require k >= 2 and depth >= 0")
    capacity = (k - 2) // 2
    vertex_count = capacity + 4 + depth
    base_excess = 1 if k % 2 else 2
    excess = base_excess + 2 * depth
    return capacity, vertex_count, excess


def certified_depth(k: int) -> int:
    if k < 0:
        raise ValueError("k must be nonnegative")
    return math.isqrt(k) // WINDOW_DENOMINATOR


def rational_power(base: int, exponent: int) -> Fraction:
    if base <= 0:
        raise ValueError("base must be positive")
    if exponent >= 0:
        return Fraction(base**exponent)
    return Fraction(1, base ** (-exponent))


def main_value(excess: int, vertex_count: int) -> Fraction:
    if excess < 1 or vertex_count < 1:
        raise ValueError("positive parameters required")
    return (
        Fraction(4 * excess, math.factorial(excess))
        * rational_power(vertex_count, 2 * vertex_count - 8)
    )


def exact_main_ratio(vertex_count: int, excess: int, ell: int) -> Fraction:
    if ell < 0 or 2 * ell >= excess:
        raise ValueError("ell is outside the positive-excess support")
    if vertex_count - ell < 1:
        raise ValueError("earlier vertex count must be positive")
    return (
        main_value(excess - 2 * ell, vertex_count - ell)
        / main_value(excess, vertex_count)
    )


def equation_35_bound(vertex_count: int, excess: int, ell: int) -> Fraction:
    return Fraction(excess * excess, vertex_count * vertex_count) ** ell


def actual_newton_scope(k: int, depth: int, ell: int):
    _, vertex_count, excess = endpoint_parameters(k, depth)
    if ell < 0 or ell > depth:
        raise ValueError("ell must index an actual Newton prefix term")
    earlier_vertex_count = vertex_count - ell
    earlier_excess = excess - 2 * ell
    exponent = 2 * earlier_vertex_count - 8
    # This identity is the reason equation (35) has no negative-exponent
    # problem on the actual Newton support.
    assert earlier_vertex_count >= (k - 2) // 2 + 4
    assert earlier_vertex_count >= 4
    assert exponent >= 0
    assert earlier_excess >= 1
    return earlier_vertex_count, earlier_excess, exponent


def equation_35_factor_audit(k: int, depth: int, ell: int):
    vertex_count, excess = endpoint_parameters(k, depth)[1:]
    earlier_vertex_count, earlier_excess, exponent = actual_newton_scope(
        k, depth, ell
    )
    factorial_ratio = math.prod(
        range(earlier_excess + 1, excess + 1)
    )
    assert factorial_ratio <= excess ** (2 * ell)
    assert earlier_vertex_count <= vertex_count
    assert exponent >= 0
    # (N-l)^exponent <= N^exponent is now directionally valid.
    return {
        "earlier_N": earlier_vertex_count,
        "earlier_R": earlier_excess,
        "power_exponent": exponent,
        "factorial_ratio_bounded": True,
        "base_power_bounded": True,
    }


def earlier_term_conditions(k: int, depth: int):
    _, vertex_count, excess = endpoint_parameters(k, depth)
    global_condition = (
        vertex_count >= 2**52 * (excess + 1) ** 2
    )
    rows = []
    for ell in range(depth + 1):
        earlier_n, earlier_r, exponent = actual_newton_scope(
            k, depth, ell
        )
        determinant_range = (
            earlier_n >= 4096 * (earlier_r + 1) ** 2
        )
        relative_remainder = Fraction(
            2**48 * (earlier_r + 1) ** 3,
            earlier_r * earlier_n,
        )
        binomial_bound = (
            math.comb(vertex_count - 4, ell)
            <= Fraction(vertex_count**ell, math.factorial(ell))
        )
        factor_check = equation_35_factor_audit(k, depth, ell)
        if global_condition:
            assert determinant_range
            assert relative_remainder <= 1
        assert binomial_bound
        rows.append(
            {
                "ell": ell,
                "N_ell": earlier_n,
                "R_ell": earlier_r,
                "power_exponent": exponent,
                "determinant_range": determinant_range,
                "relative_remainder_at_most_one": (
                    relative_remainder <= 1
                ),
                **factor_check,
            }
        )
    return global_condition, rows


def window_boundary_audit(k: int):
    if k < WINDOW_THRESHOLD:
        raise ValueError("below explicit theorem threshold")
    depth = certified_depth(k)
    _, vertex_count, excess = endpoint_parameters(k, depth)
    x = Fraction((excess + 1) ** 2, vertex_count)
    y = Fraction(excess**2, vertex_count)
    heat_52 = vertex_count >= 2**52 * (excess + 1) ** 2
    corollary_4_54 = vertex_count >= 2**54 * (excess + 1) ** 2
    geometric_exp_upper = y / (1 - y)
    equation_39_upper = 2**51 * x + 2 * geometric_exp_upper
    conditions, rows = earlier_term_conditions(k, depth)
    assert heat_52 and conditions
    assert x <= Fraction(1, 2**52)
    assert y <= x < 1
    assert equation_39_upper < 1
    assert all(row["determinant_range"] for row in rows)
    assert all(row["relative_remainder_at_most_one"] for row in rows)
    return {
        "k": k,
        "depth": depth,
        "N": vertex_count,
        "R": excess,
        "equation_39_condition_2^52": heat_52,
        "corollary_4_condition_2^54": corollary_4_54,
        "x": str(x),
        "equation_39_geometric_upper": str(equation_39_upper),
        "earlier_terms_checked": len(rows),
        "positive": equation_39_upper < 1,
    }


def main_model_component_float(vertex_count: int, excess: int, ell: int):
    if vertex_count - ell < 4:
        raise ValueError("need nonnegative power exponent")
    earlier_excess = excess - 2 * ell
    if earlier_excess < 1:
        raise ValueError("outside positive-excess support")
    logarithm = (
        math.lgamma(vertex_count - 3)
        - math.lgamma(ell + 1)
        - math.lgamma(vertex_count - 3 - ell)
        + math.log(Fraction(earlier_excess, excess))
        + math.lgamma(excess + 1)
        - math.lgamma(earlier_excess + 1)
        - 2 * ell * math.log(vertex_count)
        + (2 * vertex_count - 2 * ell - 8)
        * math.log1p(-Fraction(ell, vertex_count))
    )
    return math.exp(logarithm)


def main_model_sum_float(vertex_count: int, excess: int):
    support = (excess - 1) // 2
    if vertex_count - support < 4:
        raise ValueError("equation (35) scope is not satisfied")
    return math.fsum(
        (-1) ** ell
        * main_model_component_float(vertex_count, excess, ell)
        for ell in range(support + 1)
    )


def dominated_convergence_audit():
    samples = []
    for target in (Fraction(0), Fraction(1, 4), Fraction(1), Fraction(4)):
        sequence = []
        for vertex_count in (2000, 8000, 32000):
            if target == 0:
                excess = max(1, round(vertex_count ** Fraction(1, 3)))
            else:
                excess = max(
                    1, round(math.sqrt(float(target) * vertex_count))
                )
            value = main_model_sum_float(vertex_count, excess)
            actual_lambda = Fraction(excess**2, vertex_count)
            prediction = math.exp(-float(actual_lambda) / math.e**2)
            envelope_parameter = actual_lambda
            # Every nonnegative component is bounded by
            # (R^2/N)^ell/ell! once N-ell >= 4.
            envelope = 1.0
            for ell in range((excess - 1) // 2 + 1):
                if ell:
                    envelope *= float(envelope_parameter) / ell
                component = main_model_component_float(
                    vertex_count, excess, ell
                )
                assert component <= envelope * (1 + 1e-10)
            sequence.append(
                {
                    "N": vertex_count,
                    "R": excess,
                    "lambda": float(actual_lambda),
                    "model": value,
                    "prediction": prediction,
                    "absolute_error": abs(value - prediction),
                }
            )
        assert sequence[-1]["absolute_error"] < sequence[0]["absolute_error"]
        samples.append(
            {
                "target_lambda": str(target),
                "sequence": sequence,
            }
        )
    return samples


def small_n_scope_counterexample():
    """Exhibit why equation (35) needs a nonnegative power exponent."""
    vertex_count, excess, ell = 3, 3, 1
    actual = exact_main_ratio(vertex_count, excess, ell)
    claimed_bound = equation_35_bound(vertex_count, excess, ell)
    assert 2 * (vertex_count - ell) - 8 < 0
    assert actual > claimed_bound
    return {
        "N": vertex_count,
        "R": excess,
        "ell": ell,
        "earlier_power_exponent": 2 * (vertex_count - ell) - 8,
        "actual_ratio": str(actual),
        "equation_35_rhs": str(claimed_bound),
        "inequality_fails_outside_scope": True,
    }


def audit():
    boundary = [
        window_boundary_audit(k)
        for k in (
            WINDOW_THRESHOLD,
            WINDOW_THRESHOLD + 1,
            4 * WINDOW_THRESHOLD,
            100 * WINDOW_THRESHOLD + 1,
        )
    ]
    # At the exact first boundary the new constant does not satisfy the
    # older Corollary-4 threshold, so it cannot be described as its literal
    # substitution.
    assert not boundary[0]["corollary_4_condition_2^54"]

    exact_ratio_checks = 0
    for k in range(2, 81):
        for depth in range(9):
            _, vertex_count, excess = endpoint_parameters(k, depth)
            for ell in range(depth + 1):
                actual_newton_scope(k, depth, ell)
                if vertex_count < 100:
                    ratio = exact_main_ratio(vertex_count, excess, ell)
                    assert ratio <= equation_35_bound(
                        vertex_count, excess, ell
                    )
                    exact_ratio_checks += 1

    return {
        "schema": (
            "amra.opg1757.critical-sqrt-bottom-window-independent.v1"
        ),
        "verdict": "PASS_WITH_SCOPE_CLARIFICATION",
        "classification": {
            "fixed_window": (
                "explicit reparameterization and sharper error-budget "
                "specialization of Growing Depth equation (39); not a "
                "literal consequence of Corollary 4 and not a new heat "
                "or Newton estimate"
            ),
            "main_model_scaling": (
                "new explicit resummation of the already available "
                "leading-term model; not an exact-coefficient limit"
            ),
        },
        "boundary_cases": boundary,
        "exact_equation_35_checks_on_actual_support": exact_ratio_checks,
        "small_N_out_of_scope_counterexample": (
            small_n_scope_counterexample()
        ),
        "dominated_convergence_samples": dominated_convergence_audit(),
        "status": "all_independent_checks_passed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
