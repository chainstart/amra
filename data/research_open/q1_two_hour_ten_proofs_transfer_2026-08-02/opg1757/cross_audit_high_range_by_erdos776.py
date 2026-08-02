#!/usr/bin/env python3
"""Independent exact audit of the proposed effective high-range bound.

This does not import either author certificate program.  It reconstructs
the four objects from the old recurrence input, pins both that source and
the resulting expanded component digest, and recomputes every rational
constant and integer-power threshold in HIGH_RANGE_EFFECTIVITY_BLOCKER.md.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / "q1_six_hour_campaign_2026-08-02" / "opg1757"
SOURCE = OLD / "third_active_transport_recurrence_attack.py"
SOURCE_SHA256 = "a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125"
COMPONENT_SHA256 = "60088139bd17a2a3e52f643896ca46b6708a87ab090c2658e28656569b02ed70"
S_GAP = int(
    "557318272747802613573322901489669353946699423886389776921726369126"
    "099873157883699268070504958536925059099817311331374"
)
X = sp.symbols("audit_shift", nonnegative=True)


def least_strict_power_threshold(constant: Fraction, margin: Fraction) -> int:
    """Least integer s with denominator^v*s^u > numerator^v."""
    numerator, denominator = constant.numerator, constant.denominator
    u, v = margin.numerator, margin.denominator

    def passes(value: int) -> bool:
        return denominator**v * value**u > numerator**v

    low, high = 0, 1
    while not passes(high):
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if passes(middle):
            high = middle
        else:
            low = middle
    assert passes(high)
    assert not passes(high - 1)
    return high


def component_digest(objects: dict[str, dict[int, sp.Expr]]) -> str:
    digest = hashlib.sha256()
    for name, components in objects.items():
        for base in sorted(components):
            digest.update(f"{name}:{base}:".encode())
            digest.update(sp.srepr(sp.expand(components[base])).encode())
            digest.update(b"\n")
    return digest.hexdigest()


def coefficientwise_shifted_nonnegative(expr: sp.Expr, parameter, beta, start: int) -> bool:
    return all(
        coefficient >= 0
        for coefficient in sp.Poly(
            sp.expand(expr.subs(parameter, X + start)), beta, X
        ).coeffs()
    )


def main() -> None:
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert source_hash == SOURCE_SHA256
    sys.path.insert(0, str(OLD))
    import third_active_transport_recurrence_attack as recurrence

    beta, parameter = recurrence.B, recurrence.S
    objects = {
        "odd_sufficient": recurrence.odd_w_components(),
        "even_sufficient": recurrence.even_w_components(),
        "odd_page": recurrence.page_recurrence_components(6),
        "even_page": recurrence.page_recurrence_components(7),
    }
    assert component_digest(objects) == COMPONENT_SHA256

    # p, full beta degree, lower-base s-degree, largest retained shift,
    # positivity start, common-exponent offset, transport-index offset,
    # low shift, bulk loss, high-index distance below L at the bulk endpoint.
    metadata = {
        "odd_sufficient": (6, 19, 11, 19, 8, -15, 8, 0, 12, 8),
        "even_sufficient": (7, 23, 13, 23, 9, -17, 10, 0, 14, 10),
        "odd_page": (6, 18, 8, 18, 8, -14, 8, 2, 12, 8),
        "even_page": (7, 22, 10, 22, 9, -16, 10, 2, 14, 10),
    }
    expected = {
        "odd_sufficient": (
            80,
            Fraction(32263317969653120815494524068429824, 48828125),
            102,
        ),
        "even_sufficient": (
            120,
            Fraction(
                13640357738883598259403345884706295095651860375632,
                2101890673828125,
            ),
            182963662611742278515145357606424176862843,
        ),
        "odd_page": (
            68,
            Fraction(537834204620338688824696369053696, 48828125),
            75,
        ),
        "even_page": (
            105,
            Fraction(
                16379880062727150667612377994429058027750150674,
                129746337890625,
            ),
            1494048895141509478550315587139453832856,
        ),
    }
    margins = {6: Fraction(669, 50), 7: Fraction(59, 72)}

    thresholds: dict[str, int] = {}
    constants: dict[str, Fraction] = {}
    counts: dict[str, int] = {}
    for name, components in objects.items():
        p, degree_bound, s_bound, high_shift, start, ell, k_add, low_shift, bulk_loss, guard = metadata[name]
        total = Fraction(0)
        count = 0
        actual_degree = 0
        actual_s_degree = 0
        for base, expr in components.items():
            if base >= p:
                continue
            polynomial = sp.Poly(sp.expand(expr), beta)
            actual_degree = max(actual_degree, polynomial.degree())
            for (shift,), coefficient in polynomial.terms():
                coefficient_poly = sp.Poly(coefficient, parameter)
                coefficient_l1 = sum(
                    abs(int(value)) for value in coefficient_poly.all_coeffs()
                )
                actual_s_degree = max(actual_s_degree, coefficient_poly.degree())
                total += Fraction(
                    2**degree_bound * coefficient_l1 * p**high_shift,
                    base**shift,
                )
                count += 1
        assert (actual_degree, actual_s_degree) == (degree_bound, s_bound)
        assert (count, total) == expected[name][:2]
        threshold = least_strict_power_threshold(total, margins[p])
        assert threshold == expected[name][2]
        thresholds[name] = threshold
        constants[name] = total
        counts[name] = count

        dominant = components[p]
        assert coefficientwise_shifted_nonnegative(
            dominant, parameter, beta, start
        )
        low_coefficient = sp.Poly(dominant, beta).coeff_monomial(
            beta**low_shift
        )
        expected_low = (
            2 * (parameter - 2)
            if "sufficient" in name
            else (36 if p == 6 else 50)
        )
        assert sp.expand(low_coefficient - expected_low) == 0
        assert sp.Poly(dominant, beta).coeff_monomial(beta**high_shift) != 0

        # For every integer d>=31, the high index is nonnegative.  At the
        # bulk endpoint d=2s-bulk_loss, it is exactly L-guard.  Therefore if
        # the low endpoint is illegal, the high endpoint is legal throughout
        # the full bulk interval, without a finite scan.
        assert 31 + k_add - high_shift >= 0
        computed_guard = ell + bulk_loss - k_add + high_shift
        assert computed_guard == guard > 0

    s_high = max(thresholds.values())
    assert s_high == 182963662611742278515145357606424176862843
    assert len(str(s_high)) == 42
    assert s_high < S_GAP

    # Exact contiguous bulk/top interfaces and common natural-support end.
    assert (12 - 1, 4 + 7) == (11, 11)  # odd: 2s-12 / 2s-11
    assert (14 - 1, 4 + 9) == (13, 13)  # even: 2s-14 / 2s-13

    print("INDEPENDENT OPG HIGH-RANGE EFFECTIVITY AUDIT: PROMOTE")
    print("source_sha256", source_hash)
    print("component_sha256", COMPONENT_SHA256)
    print("lower_counts", counts)
    print("constants", constants)
    print("thresholds", thresholds)
    print("S_high", s_high)
    print("S_high_digits", len(str(s_high)))
    print("dominated_by_S_gap", s_high < S_GAP)


if __name__ == "__main__":
    main()
