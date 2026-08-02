#!/usr/bin/env python3
"""Independent cross-audit for the frozen OPG-1757 logarithmic layer.

This file does not import either author verifier.  It reads only the pinned
old recurrence source and independently reconstructs its four certificate
sums, complete-channel identities, and effective majorants.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import math
from pathlib import Path
import sys

import sympy as sp


HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / "q1_six_hour_campaign_2026-08-02" / "opg1757"
SOURCE = OLD / "third_active_transport_recurrence_attack.py"
EXPECTED_SOURCE_HASH = (
    "a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125"
)
K0 = 1000
X, Y = sp.symbols("audit_x audit_y")


def load_old_recurrence():
    actual = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert actual == EXPECTED_SOURCE_HASH
    sys.path.insert(0, str(OLD))
    import third_active_transport_recurrence_attack as recurrence

    return recurrence, actual


def raw_terms(expr: sp.Expr, beta: sp.Symbol, parameter: sp.Symbol):
    """Return (beta shift, s degree, integer coefficient) without helpers."""
    result: list[tuple[int, int, int]] = []
    for (j,), coefficient in sp.Poly(sp.expand(expr), beta).terms():
        for (m,), scalar in sp.Poly(coefficient, parameter).terms():
            assert scalar.is_Integer
            result.append((j, m, int(scalar)))
    return tuple(result)


def expected_sufficient(p: int, a: int):
    r = p - a
    scalar = 2 * (-1) ** r * math.comb(p - 2, r)
    return {
        j: (j + 1, scalar * math.comb(2 * r, j))
        for j in range(2 * r + 1)
    }


def expected_page(p: int, a: int):
    r = p - 1 - a
    scalar = 2 * (p - 2) * (-1) ** r * math.comb(p - 3, r)
    return {
        j: (j - 1, scalar * math.comb(2 * r + 1, j - 2))
        for j in range(2, 2 * r + 4)
    }


def top_signature(expr, beta, parameter):
    terms = raw_terms(expr, beta, parameter)
    height = max(m - j for j, m, _ in terms)
    signature = {j: (m, c) for j, m, c in terms if m - j == height}
    assert len(signature) == sum(m - j == height for j, m, _ in terms)
    return height, signature


def egf_coefficient(poly: sp.Expr, degree: int) -> Fraction:
    """Coefficient after Y=e^(2X), reconstructed term by term."""
    total = Fraction(0)
    for (j, a), coefficient in sp.Poly(sp.expand(poly), X, Y).terms():
        residual = degree - j
        if residual >= 0:
            total += Fraction(
                int(coefficient) * (2 * a) ** residual,
                math.factorial(residual),
            )
    return total


def coefficient_data(components, beta, parameter):
    result = []
    for base, expr in components.items():
        for (shift,), coefficient in sp.Poly(expr, beta).terms():
            values = [int(x) for x in sp.Poly(coefficient, parameter).all_coeffs()]
            result.append(
                (
                    base,
                    shift,
                    len(values) - 1,
                    values[0],
                    sum(abs(x) for x in values[1:]),
                    sum(abs(x) for x in values),
                )
            )
    return tuple(result)


def falling(k: int, j: int) -> int:
    result = 1
    for value in range(k - j + 1, k + 1):
        result *= value
    return result


def independent_fixed_bound(data, exponent_offset, top_height, first):
    best = (1, first)
    max_q = 0
    for k in range(first, K0):
        lead = 0
        error = 0
        for base, shift, degree, lc, lower_l1, total_l1 in data:
            if shift > k:
                continue
            residual = k - shift
            scaled = (2 * base) ** residual * falling(k, shift)
            q_error = residual * (abs(exponent_offset) + residual)
            max_q = max(max_q, q_error)
            height = degree + residual - k
            if height == top_height:
                lead += lc * scaled
                error += (abs(lc) * q_error + 2 * lower_l1) * scaled
            else:
                assert height <= top_height - 1
                error += 2 * total_l1 * scaled
        assert lead > 0
        candidate = error // lead + 1
        if candidate > best[0]:
            best = (candidate, k)
    return {"threshold": best[0], "k": best[1], "max_Q": max_q}


def shifted_coefficients_nonnegative(expr, parameter, beta, start):
    shifted = sp.Poly(sp.expand(expr.subs(parameter, X + start)), beta, X)
    return all(value >= 0 for value in shifted.coeffs())


def independent_sufficient_tail(data, p: int):
    total = Fraction(0)
    ratios = []
    count = 0
    for base, shift, degree, _lc, _lower, l1 in data:
        if base == p:
            continue
        count += 1
        assert degree - shift <= 1
        rho = Fraction(base, p)
        consecutive = rho * Fraction(K0 + 1, K0) ** shift
        assert consecutive < 1
        ratios.append(consecutive)
        total += Fraction(l1, base**shift) * K0**shift * rho**K0
    assert total < Fraction(1, 2)
    return total, max(ratios), count


def independent_page_tail(data, p: int):
    q = p - 1
    base_shift = 2 * p - 4
    total = Fraction(0)
    ratios = []
    count = 0
    for base, shift, degree, _lc, _lower, l1 in data:
        if base >= q:
            continue
        count += 1
        assert shift >= 2
        delta = shift - degree - 1
        assert delta >= 0
        rho = Fraction(base, q) * Fraction(241, 242) ** delta
        constant = (
            Fraction(l1 * q**3, (p - 2) * base**shift)
            * Fraction(242, 241) ** (delta * base_shift)
        )
        if shift == 2:
            value = constant * rho**K0 / (K0 - 2)
            consecutive = rho * Fraction(K0 - 2, K0 - 1)
        else:
            power = shift - 3
            value = constant * K0**power * rho**K0
            consecutive = rho * Fraction(K0 + 1, K0) ** power
        assert consecutive < 1
        ratios.append(consecutive)
        total += value
    assert total < Fraction(1, 2)
    return total, max(ratios), count


def main() -> None:
    recurrence, source_hash = load_old_recurrence()
    beta, parameter = recurrence.B, recurrence.S
    objects = {
        "odd_sufficient": (6, recurrence.odd_w_components(), "sufficient"),
        "even_sufficient": (7, recurrence.even_w_components(), "sufficient"),
        "odd_page": (6, recurrence.page_recurrence_components(6), "page"),
        "even_page": (7, recurrence.page_recurrence_components(7), "page"),
    }

    spectra = {}
    channel = {}
    for name, (p, components, kind) in objects.items():
        top_count = 0
        lower_count = 0
        assembled = sp.S.Zero
        for a, expr in components.items():
            height, signature = top_signature(expr, beta, parameter)
            if kind == "sufficient":
                expected_height = 1
                expected = expected_sufficient(p, a)
            elif a < p:
                expected_height = -1
                expected = expected_page(p, a)
            else:
                expected_height = -2
                expected = {2: (0, 36 if p == 6 else 50)}
            assert (height, signature) == (expected_height, expected)
            top_count += len(signature)
            lower_count += sum(
                m - j < expected_height for j, m, _ in raw_terms(expr, beta, parameter)
            )
            if kind == "sufficient" or a < p:
                for j, (_m, scalar) in signature.items():
                    assembled += scalar * X**j * Y**a
        if kind == "sufficient":
            expected_poly = 2 * Y**2 * (Y - (1 + X) ** 2) ** (p - 2)
        else:
            expected_poly = (
                2 * (p - 2) * X**2 * (1 + X) * Y**2
                * (Y - (1 + X) ** 2) ** (p - 3)
            )
        assert sp.expand(assembled - expected_poly) == 0
        first = 2 * p - 4
        before = [egf_coefficient(assembled, k) for k in range(first)]
        after = [egf_coefficient(assembled, k) for k in range(first, first + 80)]
        assert all(value == 0 for value in before)
        assert all(value > 0 for value in after)
        spectra[name] = (top_count, lower_count)
        channel[name] = {"first": first, "first_value": str(after[0])}

    data = {
        name: coefficient_data(components, beta, parameter)
        for name, (_p, components, _kind) in objects.items()
    }
    fixed = {
        "odd_sufficient": independent_fixed_bound(data["odd_sufficient"], -15, 1, 8),
        "even_sufficient": independent_fixed_bound(data["even_sufficient"], -17, 1, 10),
        "odd_page": independent_fixed_bound(data["odd_page"], -14, -1, 8),
        "even_page": independent_fixed_bound(data["even_page"], -16, -1, 10),
    }
    expected_fixed = {
        "odd_sufficient": (84084178721600836612491482881224005603079639962, 999, 1012986),
        "even_sufficient": (103990364851545016369295143433465885138144397960117967018, 999, 1014984),
        "odd_page": (557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374, 999, 1007967),
        "even_page": (559330005252417606463492302337154032928086116534685423818097225862646092302799175753733844066084675514273958813224, 999, 1009961),
    }
    for name, expected in expected_fixed.items():
        actual = fixed[name]
        assert (actual["threshold"], actual["k"], actual["max_Q"]) == expected

    # Dominant kernels are kept whole, so coefficientwise shifted positivity
    # removes them from every absolute-error sum.
    dominant = (
        (objects["odd_sufficient"][1][6], 8),
        (objects["even_sufficient"][1][7], 9),
        (objects["odd_page"][1][5], 50),
        (objects["odd_page"][1][6], 8),
        (objects["even_page"][1][6], 100),
        (objects["even_page"][1][7], 9),
    )
    assert all(
        shifted_coefficients_nonnegative(expr, parameter, beta, start)
        for expr, start in dominant
    )
    # In each page branch the q=p-1 top template has only shifts 2 and 3;
    # shift 3 supplies A_q, while the p base has the unique height -2 shift
    # 2 term supplying A_p.  Every a<q base is exponentially smaller than
    # A_q, and every remaining p term has at least one extra height loss.
    for name, p in (("odd_page", 6), ("even_page", 7)):
        components = objects[name][1]
        q = p - 1
        q_height, q_signature = top_signature(components[q], beta, parameter)
        p_height, p_signature = top_signature(components[p], beta, parameter)
        assert q_height == -1 and set(q_signature) == {2, 3}
        assert q_signature[3][1] == 2 * (p - 2)
        assert p_height == -2 and p_signature == {
            2: (0, 36 if p == 6 else 50)
        }
        assert all(
            top_signature(components[a], beta, parameter)[0] == -1
            for a in range(2, q)
        )
    odd_q_beta3 = sp.Poly(objects["odd_page"][1][5], beta).coeff_monomial(beta**3)
    even_q_beta3 = sp.Poly(objects["even_page"][1][6], beta).coeff_monomial(beta**3)
    assert sp.expand(
        odd_q_beta3 - 8 * (parameter**2 + 35 * parameter - 1074)
    ) == 0
    assert sp.expand(
        even_q_beta3 - 10 * (parameter**2 + 49 * parameter - 2178)
    ) == 0

    growing = {}
    for name, p in (("odd_sufficient", 6), ("even_sufficient", 7)):
        growing[name] = independent_sufficient_tail(data[name], p)
    for name, p in (("odd_page", 6), ("even_page", 7)):
        growing[name] = independent_page_tail(data[name], p)

    s_gap = max(value[0] for value in expected_fixed.values())
    assert s_gap == expected_fixed["odd_page"][0]
    assert len(str(s_gap)) == 117
    assert 242**2 == 58564
    assert 242**2 - 241 * 242 == 242

    print("INDEPENDENT OPG1757 CROSS-AUDIT: PASS")
    print("source_sha256", source_hash)
    print("spectra", spectra)
    print("complete_channels", channel)
    print("fixed_thresholds", fixed)
    print(
        "growing_exact",
        {
            name: {
                "sum_below_half": value[0] < Fraction(1, 2),
                "bounded_summands": value[2],
                "max_consecutive_ratio_below_one": value[1] < 1,
            }
            for name, value in growing.items()
        },
    )
    print("S_gap_digits", len(str(s_gap)))
    print("S_gap", s_gap)


if __name__ == "__main__":
    main()
