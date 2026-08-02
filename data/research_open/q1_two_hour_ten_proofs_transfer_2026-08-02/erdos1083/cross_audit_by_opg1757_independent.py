#!/usr/bin/env python3
"""Independent hostile audit for the Erdős #1083 author freeze.

This file deliberately imports no author verifier or author helper.  It
reconstructs the identities directly from finite dictionaries and the
displayed polynomials.
"""

from __future__ import annotations

import cmath
import itertools
import math
from collections import Counter

import sympy as sp


def clean(f: Counter) -> dict:
    return {x: int(v) for x, v in f.items() if v}


def conv(f: dict, g: dict) -> dict:
    out = Counter()
    for x, u in f.items():
        for y, v in g.items():
            out[x + y] += u * v
    return clean(out)


def conv2(f: dict, g: dict) -> dict:
    out = Counter()
    for (x1, x2), u in f.items():
        for (y1, y2), v in g.items():
            out[x1 + y1, x2 + y2] += u * v
    return clean(out)


def augmentation(f: dict) -> int:
    return sum(f.values())


def energy(f: dict) -> int:
    numerator = sum(v * (v - 1) for v in f.values())
    assert numerator % 2 == 0
    return numerator // 2


def norm2(f: dict) -> int:
    return sum(v * v for v in f.values())


def is_mask(f: dict) -> bool:
    return all(v == 1 for v in f.values())


def correlation(q: dict, d: int) -> int:
    return sum(q.get(g, 0) * q.get(g - d, 0) for g in q)


def off_diagonal(a: tuple[int, ...], q: dict) -> int:
    return sum(correlation(q, b - x) for x in a for b in a if x != b)


def edit_mask(q: dict) -> set[int]:
    """Reconstruct Lemma 1.2 on the infinite group Z."""

    c = augmentation(q)
    positive = [x for x, value in q.items() if value > 0]
    if len(positive) >= c:
        return set(positive[:c])
    result = set(positive)
    fresh = 10_000
    while len(result) < c:
        if fresh not in q:
            result.add(fresh)
        fresh += 1
    return result


def l1_to_mask(q: dict, r: set[int]) -> int:
    return sum(abs(q.get(x, 0) - (1 if x in r else 0)) for x in set(q) | r)


def multiplicity(a: tuple[int, ...], d: int) -> int:
    aset = set(a)
    return sum(1 for x in a if x + d in aset)


def dft(f: dict, character: int, p: int) -> complex:
    return sum(
        value * cmath.exp(-2j * math.pi * character * (x % p) / p)
        for x, value in f.items()
    )


def reduce_mod_p(f: dict, p: int) -> dict:
    out = Counter()
    for x, value in f.items():
        out[x % p] += value
    return clean(out)


def audit_factorial_edit_and_ledgers() -> dict[str, int]:
    factorial_cases = 0
    ledger_cases = 0
    mask_product_cases = 0
    supports = (-1, 0, 1, 2)
    sources = tuple(
        tuple(a)
        for size in (1, 2, 3)
        for a in itertools.combinations(range(4), size)
    )
    for coefficients in itertools.product(range(-2, 3), repeat=len(supports)):
        q = {x: value for x, value in zip(supports, coefficients) if value}
        c = augmentation(q)
        if c <= 0:
            continue
        delta = energy(q)
        positive_excess = sum(max(value - 1, 0) for value in q.values())
        negative_mass = sum(-value for value in q.values() if value < 0)
        assert delta >= positive_excess + negative_mass >= 0
        assert (delta == 0) == is_mask(q)
        r = edit_mask(q)
        assert len(r) == c
        assert l1_to_mask(q, r) <= 2 * delta
        factorial_cases += 1
        for a in sources:
            h = conv({x: 1 for x in a}, q)
            off = off_diagonal(a, q)
            assert off == 2 * energy(h) - 2 * len(a) * delta
            ledger_cases += 1
            if is_mask(h):
                assert off == -2 * len(a) * delta
                mask_product_cases += 1
    # Hostile sign/factor check: A=(0,1,2), q=1-x+x^2 has delta=1
    # and a mask product.  Ordered pairs give -6=-2*S*delta, whereas
    # retaining only unordered pairs would incorrectly give -3.
    witness_a = (0, 1, 2)
    witness_q = {0: 1, 1: -1, 2: 1}
    ordered = off_diagonal(witness_a, witness_q)
    unordered = sum(
        correlation(witness_q, witness_a[j] - witness_a[i])
        for i in range(len(witness_a)) for j in range(i + 1, len(witness_a))
    )
    assert ordered == -6 and unordered == -3
    return {
        "factorial_edit_cases": factorial_cases,
        "collision_ledger_cases": ledger_cases,
        "mask_product_cases": mask_product_cases,
        "ordered_debt_witness": ordered,
        "unordered_half_witness": unordered,
    }


def audit_popular_difference() -> int:
    checked = 0
    supports = (-1, 0, 1, 2)
    sources = tuple(
        tuple(a)
        for size in (2, 3)
        for a in itertools.combinations(range(5), size)
    )
    for coefficients in itertools.product((-1, 0, 1, 2), repeat=4):
        q = {x: value for x, value in zip(supports, coefficients) if value}
        c = augmentation(q)
        negative = {x: -value for x, value in q.items() if value < 0}
        if c <= 0 or not negative:
            continue
        positive = {x: value for x, value in q.items() if value > 0}
        nminus = sum(negative.values())
        for a in sources:
            h = conv({x: 1 for x in a}, q)
            if any(value < 0 for value in h.values()):
                continue
            best = max(
                multiplicity(a, r - v) for r in positive for v in negative
            )
            assert best * (c + nminus) >= len(a)
            differences = {b - x for x in a for b in a if b != x}
            mu = max(multiplicity(a, d) for d in differences)
            lower = max(1, math.ceil(len(a) / mu) - c)
            assert energy(q) >= nminus >= lower
            checked += 1
    assert checked > 0
    return checked


def audit_prime_shadow_and_fourier() -> dict[str, float | int]:
    # A=(0,1,2), q=1-x+x^2, and A*q=(0,2,4) is an exact mask.
    p = 7
    a = {0: 1, 1: 1, 2: 1}
    q = {0: 1, 1: -1, 2: 1}
    m = conv(a, q)
    assert m == {0: 1, 2: 1, 4: 1}
    s, c, delta = 3, 1, 1
    assert all(abs(dft(a, k, p)) > 1e-9 for k in range(p))
    ratios = [abs(dft(m, k, p)) ** 2 / abs(dft(a, k, p)) ** 2 for k in range(p)]
    rowwise = sum(ratios) / p - c
    second = sum(
        (s - abs(dft(a, k, p)) ** 2) * ratios[k] for k in range(p)
    ) / p
    aggregate = sum(abs(dft(m, k, p)) ** 2 * 2 / abs(dft(a, k, p)) ** 2 for k in range(p)) / p - 2 * c
    assert abs(rowwise - 2 * delta) < 1e-9
    assert abs(second - 2 * s * delta) < 1e-9
    assert abs(aggregate - 4 * delta) < 1e-9

    # Exhaust the rank-one p=5,7 nonempty masks of size <p.
    invertible_masks = 0
    for prime in (5, 7):
        for bits in range(1, (1 << prime) - 1):
            mask = {x: 1 for x in range(prime) if bits >> x & 1}
            if len(mask) >= prime:
                continue
            assert all(abs(dft(mask, k, prime)) > 1e-8 for k in range(prime))
            invertible_masks += 1

    # Both guards are necessary: p=S permits a zero, and a support collision
    # can change an l2 norm even though reduction remains a homomorphism.
    full = {0: 1, 1: 1, 2: 1}
    assert abs(dft(full, 1, 3)) < 1e-9
    colliding = {0: 1, 7: 1}
    assert norm2(colliding) == 2
    assert reduce_mod_p(colliding, 7) == {0: 2}
    assert norm2(reduce_mod_p(colliding, 7)) == 4
    return {
        "invertible_masks": invertible_masks,
        "rowwise_rhs": round(rowwise, 12),
        "second_rhs": round(second, 12),
        "aggregate_rhs": round(aggregate, 12),
    }


def audit_transverse_minimum_debt() -> int:
    checked = 0
    for s in range(4, 13):
        px = {(i, 0): 1 for i in range(s)}
        py = {(0, i): 1 for i in range(s)}
        q = {(1, 0): 1, (0, 1): 1, (1, 1): -1, (1, s): 1, (s, 1): 1}
        assert augmentation(q) == 3
        assert norm2(q) == 5
        assert energy(q) == 1
        for product in (conv2(px, q), conv2(py, q)):
            assert is_mask(product)
            assert len(product) == 3 * s
        checked += 1
    return checked


def audit_aperiodic_signed_quotient() -> dict[str, int | bool]:
    p = {e: 1 for e in (0, 1, 3, 5, 6)}
    q = {0: 1, 5: -1, 8: 1, 10: 1, 13: -1, 18: 1}
    expected = {e: 1 for e in (0, 1, 3, 9, 11, 13, 15, 21, 23, 24)}
    assert conv(p, q) == expected
    factors = (
        {0: 1, 8: 1},
        {0: 1, 1: -1, 2: 1},
        {0: 1, 1: 1, 3: -1, 4: -1, 5: -1, 7: 1, 8: 1},
    )
    assert conv(conv(factors[0], factors[1]), factors[2]) == q
    assert tuple(augmentation(f) for f in factors) == (2, 1, 1)
    assert augmentation(q) == 2 and norm2(q) == 6 and energy(q) == 2

    x = sp.symbols("x")
    polynomial = sp.Poly(1 + x + x**3 + x**5 + x**6, x, modulus=3)
    assert polynomial.is_irreducible
    assert sp.rem(sp.Poly(x**9 - x, x, modulus=3), polynomial) == sp.Poly(x**4 - x**3 - 1, x, modulus=3)
    assert sp.rem(sp.Poly(x**27 - x, x, modulus=3), polynomial) == sp.Poly(-x**5 - x**4 - x**2 - x - 1, x, modulus=3)
    assert sp.rem(sp.Poly(x**729 - x, x, modulus=3), polynomial).is_zero
    f = lambda y: y**3 + y**2 - 3 * y - 1
    assert f(-0.5) > 0 > f(0)
    assert f(1) < 0 < f(2)
    assert f(-3) < 0 < f(-2)
    return {"product_terms": len(expected), "delta_q": energy(q), "irreducible_mod_3": True}


def audit_second_scalar_fixed_m() -> dict[str, int | bool]:
    """Exact fixed-M addendum plus a deliberately small finite gcd guard."""

    x = sp.symbols("x")
    p = 1 + x + x**3 + x**5 + x**6
    factors = (
        p,
        1 + x**8,
        1 - x + x**2,
        x**8 + x**7 - x**5 - x**4 - x**3 + x + 1,
    )
    m = sp.expand(sp.prod(factors))
    assert all(sp.Poly(f, x, domain=sp.QQ).is_irreducible for f in factors)
    assert len({sp.Poly(f, x, domain=sp.QQ).monic().as_expr() for f in factors}) == 4
    assert tuple(int(f.subs(x, 1)) for f in factors) == (5, 2, 1, 1)

    augmentation_five = []
    mask_divisors = []
    for bits in itertools.product((0, 1), repeat=4):
        divisor = sp.expand(sp.prod(f for bit, f in zip(bits, factors) if bit))
        if int(divisor.subs(x, 1)) != 5:
            continue
        augmentation_five.append(divisor)
        coefficients = sp.Poly(divisor, x, domain=sp.ZZ).as_dict().values()
        if all(value == 1 for value in coefficients):
            mask_divisors.append(divisor)
    assert len(augmentation_five) == 4
    assert mask_divisors == [p]
    assert sp.expand(x**6 * p.subs(x, x**-1)) == p

    # Conditional augmentation obstruction for coprime scalar masks.
    assert all((5 * c) % 25 != 0 for c in range(1, 5))

    # This is intentionally only a finite corroboration, not an all-ratio proof.
    pairs = 0
    nonconstant_gcds = 0
    for r in range(1, 21):
        for s in range(r + 1, 21):
            if math.gcd(r, s) != 1:
                continue
            pairs += 1
            pr = sp.Poly(p.subs(x, x**r), x, domain=sp.QQ)
            ps = sp.Poly(p.subs(x, x**s), x, domain=sp.QQ)
            nonconstant_gcds += int(sp.gcd(pr, ps).degree() > 0)
    assert nonconstant_gcds == 0
    # The displayed factorization is really the current common mask P*Q.
    q = 1 - x**5 + x**8 + x**10 - x**13 + x**18
    assert sp.expand(p * q) == m
    return {
        "fixed_M_distinct_irreducible_factors": 4,
        "augmentation_five_divisors": len(augmentation_five),
        "augmentation_five_mask_divisors": len(mask_divisors),
        "primitive_gcd_pairs_le_20_corroboration_only": pairs,
        "nonconstant_gcds_le_20": nonconstant_gcds,
        "unbounded_ratio_classification_claimed": False,
    }


def audit_hostile_quantifiers() -> dict[str, bool]:
    # Gamma={0}, A0=Aj=empty, q=2[0], and M=N=empty satisfy exactly
    # (0.1)-(0.2) with S=0,C=2.  No two-element subset of Gamma exists.
    q = {0: 2}
    assert augmentation(q) == 2 and energy(q) == 1
    assert conv({}, q) == {}
    s_zero_counterexample = True

    # The unqualified sentence "delta(q)=1 forces P_R-[v]" also needs the
    # surrounding signed hypothesis: 2[0] has delta one but no negative term.
    unsigned_delta_one_counterexample = energy(q) == 1 and all(v >= 0 for v in q.values())
    assert unsigned_delta_one_counterexample
    return {
        "S_zero_breaks_trivial_case_sentence_and_edit_conclusion": s_zero_counterexample,
        "delta_one_normal_form_requires_signed": unsigned_delta_one_counterexample,
        "application_S_ge_2_unaffected": True,
    }


def main() -> None:
    result = {
        "factorial_edit_ledgers": audit_factorial_edit_and_ledgers(),
        "popular_difference_cases": audit_popular_difference(),
        "prime_shadow_fourier": audit_prime_shadow_and_fourier(),
        "full_transverse_delta_one_parameters": audit_transverse_minimum_debt(),
        "aperiodic_signed_quotient": audit_aperiodic_signed_quotient(),
        "second_scalar_fixed_M_addendum": audit_second_scalar_fixed_m(),
        "hostile_quantifiers": audit_hostile_quantifiers(),
        "imports_author_verifier": False,
        "public_problem_proved": False,
        "verdict": "PASS_AFTER_REPAIR",
    }
    print("ERDOS1083 INDEPENDENT CROSS-AUDIT: PASS_AFTER_REPAIR")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
