#!/usr/bin/env python3
"""Regression certificate for the OPG uniform-height theorem.

The all-parameter proof is the inequality ledger in
UNIFORM_HEIGHT_AND_GROWING_WINDOW_THEOREM.md.  This executable checks:

1. exact truncated endpoint atoms through total endpoint rank six;
2. the termwise inequality epsilon_order + t_degree <= 2(e + rho);
3. master-profile conservation and all four changing shifts through q=12;
4. the explicit arithmetic envelopes.

The finite ranges are regression checks, not the source of the universal
quantifiers in the theorem.
"""

from __future__ import annotations

from fractions import Fraction
from math import factorial


Monomial = tuple[int, int, int]  # epsilon order, t degree, v degree
Series = dict[Monomial, Fraction]


def add(*series: Series) -> Series:
    out: Series = {}
    for current in series:
        for monomial, coefficient in current.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
    return {key: value for key, value in out.items() if value}


def scale(series: Series, scalar: Fraction) -> Series:
    return {
        monomial: scalar * coefficient
        for monomial, coefficient in series.items()
        if scalar * coefficient
    }


def multiply(left: Series, right: Series, max_v: int) -> Series:
    out: Series = {}
    for (j1, d1, k1), a in left.items():
        for (j2, d2, k2), b in right.items():
            if k1 + k2 > max_v:
                continue
            key = (j1 + j2, d1 + d2, k1 + k2)
            out[key] = out.get(key, Fraction(0)) + a * b
    return {key: value for key, value in out.items() if value}


def power(series: Series, exponent: int, max_v: int) -> Series:
    out: Series = {(0, 0, 0): Fraction(1)}
    for _ in range(exponent):
        out = multiply(out, series, max_v)
    return out


def endpoint_inputs(max_v: int) -> tuple[Series, Series, Series, Series]:
    """Return E, exp(epsilon*v*t), V, and J, truncated in v."""

    generator: Series = {}
    for a in range(1, max_v + 1):
        generator[(a - 1, a + 1, a)] = Fraction(1, factorial(a + 1))

    exponential: Series = {(0, 0, 0): Fraction(1)}
    generator_power: Series = {(0, 0, 0): Fraction(1)}
    for count in range(1, max_v + 1):
        generator_power = multiply(generator_power, generator, max_v)
        exponential = add(
            exponential,
            scale(generator_power, Fraction(1, factorial(count))),
        )

    marked_exponential: Series = {}
    for a in range(max_v + 1):
        marked_exponential[(a, a, a)] = Fraction(1, factorial(a))

    v_series: Series = {
        (0, 1, 0): Fraction(1),
        (0, 2, 0): Fraction(-1, 2),
    }
    for a in range(1, max_v + 1):
        v_series[(a, a + 2, a)] = Fraction(-(a + 1), factorial(a + 2))

    jacobian: Series = {(0, 0, 0): Fraction(1)}
    for a in range(max_v + 1):
        jacobian[(a, a + 1, a)] = Fraction(-1, factorial(a))

    return exponential, marked_exponential, v_series, jacobian


def endpoint_integrand(
    h: int, rho: int, max_v: int
) -> Series:
    exponential, marked_exponential, v_series, jacobian = endpoint_inputs(
        max_v
    )
    first = multiply(
        marked_exponential,
        power(v_series, rho, max_v),
        max_v,
    )
    if rho:
        second = scale(
            multiply(
                jacobian,
                power(v_series, rho - 1, max_v),
                max_v,
            ),
            Fraction(rho, 2**h),
        )
        braces = add(first, second)
    else:
        braces = first
    return multiply(exponential, braces, max_v)


def audit_atom_budget(max_rank: int = 6) -> int:
    checked = 0
    for h in range(3):
        for rho in range(max_rank + 1):
            for excess in range(max_rank - rho + 1):
                integrand = endpoint_integrand(h, rho, excess)
                scalar_slice = Fraction(0)
                for (epsilon_order, t_degree, v_degree), coefficient in (
                    integrand.items()
                ):
                    if v_degree != excess:
                        continue
                    if epsilon_order + t_degree > 2 * (excess + rho):
                        raise AssertionError(
                            "endpoint atom budget failed for "
                            f"h={h}, rho={rho}, e={excess}, "
                            f"(j,d)=({epsilon_order},{t_degree})"
                        )
                    scalar_slice += abs(coefficient)
                    checked += 1
                majorant = Fraction((6 * rho + 9) * 2**rho)
                if scalar_slice > majorant:
                    raise AssertionError(
                        f"scalar majorant failed at {(h, rho, excess)}"
                    )
    return checked


def master_profiles(q: int, r: int):
    for overlap in range(r // 2 + 1):
        remaining = r - 2 * overlap
        for left_excess in range(remaining + 1):
            for right_excess in range(remaining - left_excess + 1):
                lambda_degree = (
                    remaining - left_excess - right_excess
                )
                if lambda_degree > q + 1 - overlap:
                    continue
                component_sum = (
                    q
                    + 3
                    - overlap
                    - left_excess
                    - right_excess
                )
                for left_components in range(1, component_sum):
                    right_components = (
                        component_sum - left_components
                    )
                    yield (
                        overlap,
                        left_excess,
                        right_excess,
                        left_components,
                        right_components,
                    )


def audit_master_ledger(max_q: int = 12) -> int:
    checked = 0
    for q in range(1, max_q + 1):
        tuple_cap = 4 * (q + 2) ** 4
        for r in range(2 * q + 1):
            profiles = list(master_profiles(q, r))
            if len(profiles) > tuple_cap:
                raise AssertionError(f"tuple cap failed at {(q, r)}")
            for overlap, e, f, c, d in profiles:
                m1 = e + c - 1
                m2 = f + d - 1
                lambda_degree = r - 2 * overlap - e - f
                if m1 + m2 + overlap != q + 1:
                    raise AssertionError(
                        f"conservation failed at {(q, r, overlap, e, f, c, d)}"
                    )
                shifts = (1 + c + e, 1 + d + f, c + e, 2 + d + f)
                if max(shifts) > q + 4:
                    raise AssertionError(
                        f"shift cap failed at {(q, r, shifts)}"
                    )
                if max(shifts) + overlap > 2 * q + 4:
                    raise AssertionError(
                        f"falling norm cap failed at {(q, r, shifts)}"
                    )
                # Remove the common 2*s from the endpoint-normalization
                # exponent.  This is identity (18b) in the theorem.
                normalized_power = (
                    -2
                    - 2 * (c + d)
                    - (e + f)
                    + lambda_degree
                )
                expected_power = -8 - 2 * q + r
                if normalized_power != expected_power:
                    raise AssertionError(
                        "master s-normalization failed at "
                        f"{(q, r, overlap, e, f, c, d)}"
                    )
                checked += 1
    return checked


def q_zero_endpoint(h: int, s: int) -> Fraction:
    """Exact Q_(h,0,2) from the unified endpoint functional."""

    alpha = h + 2
    marked_weight = Fraction(1, 2**h)
    return (
        marked_weight * s**2
        + (1 - marked_weight) * s * (s - alpha)
        - Fraction(1, 2) * (s - alpha) * (s - alpha - 1)
    )


def audit_q_zero() -> int:
    for s in range(4, 41):
        q0 = q_zero_endpoint(0, s)
        q1 = q_zero_endpoint(1, s)
        q2 = q_zero_endpoint(2, s)
        if 4 * (2 * q1 - q0 - q2) != 4:
            raise AssertionError(f"q=0 normalization failed at s={s}")
    # Both beta-support boundaries must be represented for every q.
    for q in range(1, 13):
        if not list(master_profiles(q, 0)):
            raise AssertionError(f"empty r=0 profile set at q={q}")
        if not list(master_profiles(q, 2 * q)):
            raise AssertionError(f"empty r=2q profile set at q={q}")
    return 37


def endpoint_envelope(rank: int) -> int:
    return 15 * (rank + 1) * 2**rank * (2 * rank + 4) ** (2 * rank)


def master_envelope(q: int) -> int:
    if q < 1:
        raise ValueError("q must be positive")
    return (
        7200
        * (q + 2) ** 6
        * 2 ** (2 * q + 2)
        * (2 * q + 6) ** (2 * q + 2)
    )


def audit_arithmetic(max_q: int = 200) -> int:
    for rank in range(max_q + 1):
        if endpoint_envelope(rank) < 1:
            raise AssertionError(f"invalid endpoint envelope at {rank}")
    for q in range(1, max_q + 1):
        envelope = master_envelope(q)
        if envelope > (32 * q) ** (12 * q):
            raise AssertionError(f"coarse envelope failed at q={q}")
        if envelope > (32 * q) ** (32 * q):
            raise AssertionError(f"K=32 height lemma failed at q={q}")
    # The proof for all q>=2 uses 7200<32^3, q+2<=2q,
    # 2q+6<=5q, and 4q+13<=12q.  q=1 is checked above.
    if not (
        7200 < 32**3
        and 4 + 13 <= 12 * 2
        and 2 + 2 <= 2 * 2
        and 2 * 2 + 6 <= 5 * 2
    ):
        raise AssertionError("universal coarse-inequality anchors failed")
    return max_q


def run_certificate() -> dict[str, int]:
    return {
        "endpoint_atom_monomials": audit_atom_budget(),
        "master_profiles": audit_master_ledger(),
        "q_zero_values": audit_q_zero(),
        "arithmetic_q_values": audit_arithmetic(),
    }


if __name__ == "__main__":
    result = run_certificate()
    print("OPG UNIFORM HEIGHT ENVELOPE CERTIFICATE: PASS")
    for name, value in result.items():
        print(f"{name}: {value}")
