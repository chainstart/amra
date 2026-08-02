#!/usr/bin/env python3
"""Exact finite data for the complete-channel logarithmic-layer proof.

The asymptotic theorem is proved in COMPLETE_LOG_LAYER_THEOREM.md.  This
program verifies its finite algebraic input from the frozen old-campaign
common-base decomposition.  The optional scan is corroboration only.
"""

from __future__ import annotations

import hashlib
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
OLD_LANE = (
    HERE.parents[1]
    / "q1_six_hour_campaign_2026-08-02"
    / "opg1757"
)
OLD_RECURRENCE = OLD_LANE / "third_active_transport_recurrence_attack.py"
EXPECTED_OLD_RECURRENCE_SHA256 = (
    "a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125"
)

sys.path.insert(0, str(OLD_LANE))

from third_active_transport_recurrence_attack import (  # noqa: E402
    B,
    S,
    even_w_components,
    odd_w_components,
    page_recurrence_components,
)


X, Y = sp.symbols("x y")


@dataclass(frozen=True)
class Monomial:
    beta_shift: int
    s_degree: int
    coefficient: int

    @property
    def height(self) -> int:
        """Effective logarithmic-boundary height deg_s - beta_shift."""

        return self.s_degree - self.beta_shift


def source_hash() -> str:
    return hashlib.sha256(OLD_RECURRENCE.read_bytes()).hexdigest()


def monomials(expression: sp.Expr) -> tuple[Monomial, ...]:
    result: list[Monomial] = []
    for (j,), s_coefficient in sp.Poly(sp.expand(expression), B).terms():
        for (m,), coefficient in sp.Poly(s_coefficient, S).terms():
            if not coefficient.is_Integer:
                raise AssertionError((j, m, coefficient))
            result.append(Monomial(j, m, int(coefficient)))
    return tuple(result)


def top_terms(expression: sp.Expr) -> tuple[int, dict[int, tuple[int, int]]]:
    data = monomials(expression)
    height = max(term.height for term in data)
    top = {
        term.beta_shift: (term.s_degree, term.coefficient)
        for term in data
        if term.height == height
    }
    if len(top) != sum(term.height == height for term in data):
        raise AssertionError("two top monomials share a beta shift")
    return height, top


def sufficient_template(p: int, a: int) -> dict[int, tuple[int, int]]:
    r = p - a
    scalar = 2 * (-1) ** r * math.comb(p - 2, r)
    return {
        j: (j + 1, scalar * math.comb(2 * r, j))
        for j in range(2 * r + 1)
    }


def page_lower_template(p: int, a: int) -> dict[int, tuple[int, int]]:
    r = p - 1 - a
    scalar = 2 * (p - 2) * (-1) ** r * math.comb(p - 3, r)
    return {
        j: (j - 1, scalar * math.comb(2 * r + 1, j - 2))
        for j in range(2, 2 * r + 4)
    }


def check_lower_height(
    expression: sp.Expr, top_height: int, top: dict[int, tuple[int, int]]
) -> int:
    lower = [
        term.height
        for term in monomials(expression)
        if (term.s_degree, term.coefficient)
        != top.get(term.beta_shift)
    ]
    if lower and max(lower) > top_height - 1:
        raise AssertionError((top_height, max(lower)))
    return len(lower)


def audit_spectrum() -> dict[str, object]:
    objects = {
        "odd_sufficient": (6, odd_w_components(), "sufficient"),
        "even_sufficient": (7, even_w_components(), "sufficient"),
        "odd_page": (6, page_recurrence_components(6), "page"),
        "even_page": (7, page_recurrence_components(7), "page"),
    }
    endpoint = {6: 36, 7: 50}
    result: dict[str, object] = {}
    for name, (p, components, kind) in objects.items():
        top_count = 0
        lower_count = 0
        for a, expression in components.items():
            height, actual = top_terms(expression)
            if kind == "sufficient":
                expected_height = 1
                expected = sufficient_template(p, a)
            elif a < p:
                expected_height = -1
                expected = page_lower_template(p, a)
            else:
                expected_height = -2
                expected = {2: (0, endpoint[p])}
            if height != expected_height or actual != expected:
                raise AssertionError((name, a, height, actual, expected))
            top_count += len(actual)
            lower_count += check_lower_height(
                expression, expected_height, expected
            )
        result[name] = {
            "top_monomials": top_count,
            "strictly_lower_monomials": lower_count,
        }
    return result


def audit_complete_channel_identities() -> dict[str, object]:
    result: dict[str, object] = {}
    for p in (6, 7):
        sufficient = sp.S.Zero
        for a in range(2, p + 1):
            for j, (_, coefficient) in sufficient_template(p, a).items():
                sufficient += coefficient * X**j * Y**a
        sufficient_expected = (
            2 * Y**2 * (Y - (1 + X) ** 2) ** (p - 2)
        )
        if sp.expand(sufficient - sufficient_expected) != 0:
            raise AssertionError((p, "sufficient identity"))

        page = sp.S.Zero
        for a in range(2, p):
            for j, (_, coefficient) in page_lower_template(p, a).items():
                page += coefficient * X**j * Y**a
        page_expected = (
            2
            * (p - 2)
            * X**2
            * (1 + X)
            * Y**2
            * (Y - (1 + X) ** 2) ** (p - 3)
        )
        if sp.expand(page - page_expected) != 0:
            raise AssertionError((p, "page identity"))

        # Substitute Y=e^(2x).  The core series
        # e^(2x)-(1+x)^2 has zero coefficients below degree two and
        # strictly positive coefficients from degree two onward.
        shift = 2 * p - 4
        sufficient_positive = 0
        page_positive = 0
        for k in range(shift, shift + 65):
            suff_lead = sp.S.Zero
            page_lead = sp.S.Zero
            for a in range(2, p + 1):
                for j, (_, coefficient) in sufficient_template(p, a).items():
                    if j <= k:
                        suff_lead += (
                            sp.Rational(coefficient * 2 ** (k - j) * a ** (k - j),
                                        math.factorial(k - j))
                        )
            for a in range(2, p):
                for j, (_, coefficient) in page_lower_template(p, a).items():
                    if j <= k:
                        page_lead += (
                            sp.Rational(coefficient * 2 ** (k - j) * a ** (k - j),
                                        math.factorial(k - j))
                        )
            if suff_lead <= 0 or page_lead <= 0:
                raise AssertionError((p, k, suff_lead, page_lead))
            sufficient_positive += 1
            page_positive += 1
        result[f"p{p}"] = {
            "first_positive_degree": shift,
            "checked_positive_sufficient_leads": sufficient_positive,
            "checked_positive_page_leads": page_positive,
            "page_transition_constant": sp.Rational(
                2 * (p - 2) * p**2,
                2 * ({6: 36, 7: 50}[p]) * (p - 1) ** 3,
            ),
        }
    return result


def prepared_components(
    components: dict[int, sp.Expr], parameter: int
) -> dict[int, tuple[tuple[int, int], ...]]:
    return {
        a: tuple(
            (j, int(sp.Poly(coefficient, S).eval(parameter)))
            for (j,), coefficient in sp.Poly(expression, B).terms()
        )
        for a, expression in components.items()
    }


def exact_coefficient(
    components: dict[int, tuple[tuple[int, int], ...]],
    exponent: int,
    degree: int,
) -> int:
    value = 0
    for a, terms in components.items():
        for j, coefficient in terms:
            residual = degree - j
            if 0 <= residual <= exponent:
                value += (
                    coefficient
                    * math.comb(exponent, residual)
                    * a**residual
                )
    return value


def corroborating_scan(parameters: tuple[int, ...] = (32, 100, 250)) -> int:
    """Finite scan only; it is not used in the asymptotic proof."""

    objects = (
        ("odd_sufficient", odd_w_components(), -15, 8, 12),
        ("odd_page", page_recurrence_components(6), -14, 8, 12),
        ("even_sufficient", even_w_components(), -17, 10, 14),
        ("even_page", page_recurrence_components(7), -16, 10, 14),
    )
    checks = 0
    for name, components, exponent_offset, shift, cutoff in objects:
        for s in parameters:
            prepared = prepared_components(components, s)
            exponent = 2 * s + exponent_offset
            maximum = min(
                math.ceil(241 * math.log(s)) - 1,
                2 * s - cutoff,
            )
            for d in range(31, maximum + 1):
                value = exact_coefficient(
                    prepared, exponent, d + shift
                )
                if value <= 0:
                    raise AssertionError((name, s, d, value))
                checks += 1
    return checks


def certify(include_scan: bool = True) -> dict[str, object]:
    actual_hash = source_hash()
    if actual_hash != EXPECTED_OLD_RECURRENCE_SHA256:
        raise AssertionError((actual_hash, EXPECTED_OLD_RECURRENCE_SHA256))
    result: dict[str, object] = {
        "source_sha256": actual_hash,
        "spectrum": audit_spectrum(),
        "complete_channel_identities": audit_complete_channel_identities(),
    }
    if include_scan:
        result["corroborating_scan_coefficients"] = corroborating_scan()
    return result


def main() -> None:
    result = certify()
    print("OPG COMPLETE LOG-LAYER FINITE DATA: PASS")
    print("source_sha256:", result["source_sha256"])
    for name, data in result["spectrum"].items():
        print(name, data)
    for name, data in result["complete_channel_identities"].items():
        print(name, data)
    print(
        "corroborating_scan_coefficients:",
        result["corroborating_scan_coefficients"],
    )
    print("scan_role: CORROBORATION_ONLY")
    print("status_eventual_gap_theorem: PROVED_IN_COMPANION_NOTE")
    print("status_original_opg1757: OPEN")


if __name__ == "__main__":
    main()
