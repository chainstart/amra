#!/usr/bin/env python3
"""Exact finite audit of the conductor-energy law used in round 8."""

import cmath
from math import gcd, prod


def main() -> None:
    primes = (3, 5, 7)
    h_count = 2
    shift0 = 1
    t = 0.7
    q = prod(primes)

    def weight(a: int) -> float:
        exponent = sum(
            1
            for p in primes
            for j in range(h_count)
            if (a - shift0 - j) % p == 0
        )
        return t**exponent

    values = [weight(a) for a in range(q)]
    coeff = [
        sum(
            values[a] * cmath.exp(-2j * cmath.pi * h * a / q)
            for a in range(q)
        )
        / q
        for h in range(q)
    ]
    m2 = sum(v * v for v in values) / q
    assert abs(sum(abs(x) ** 2 for x in coeff) - m2) < 1e-11

    m_p = {p: 1 - h_count * (1 - t) / p for p in primes}
    v_p = {
        p: h_count * (1 - t) ** 2 / p * (1 - h_count / p)
        for p in primes
    }
    by_gcd: dict[int, float] = {}
    for h, value in enumerate(coeff):
        d = gcd(h, q) if h else q
        by_gcd[d] = by_gcd.get(d, 0.0) + abs(value) ** 2
    for d, observed in by_gcd.items():
        predicted = prod(
            m_p[p] ** 2 if d % p == 0 else v_p[p] for p in primes
        )
        assert abs(observed - predicted) < 2e-11

    # Exact ANOVA inversion: the layer indexed by S is exactly the sum of
    # Fourier frequencies whose reduced conductor is prod(S).
    max_anova_error = 0.0
    for mask in range(1 << len(primes)):
        selected = {
            p for index, p in enumerate(primes) if mask & (1 << index)
        }
        conductor = prod(selected)
        for n in range(q):
            physical = prod(
                (
                    (t if any((n - shift0 - j) % p == 0 for j in range(h_count)) else 1.0)
                    - m_p[p]
                )
                if p in selected
                else m_p[p]
                for p in primes
            )
            spectral = sum(
                coeff[h] * cmath.exp(2j * cmath.pi * h * n / q)
                for h in range(q)
                if q // (gcd(h, q) if h else q) == conductor
            )
            max_anova_error = max(max_anova_error, abs(physical - spectral))
    assert max_anova_error < 2e-11

    # Exact interval Fourier inversion.
    start, length = 17, 60
    direct = sum(weight(a % q) for a in range(start, start + length))
    fourier = sum(
        coeff[h]
        * sum(
            cmath.exp(2j * cmath.pi * h * a / q)
            for a in range(start, start + length)
        )
        for h in range(q)
    )
    assert abs(direct - fourier.real) < 2e-10
    assert abs(fourier.imag) < 2e-10
    print(
        "status=PASS "
        f"Q={q} anova_layers={1 << len(primes)} parseval_error="
        f"{abs(sum(abs(x) ** 2 for x in coeff) - m2):.3e} "
        f"anova_error={max_anova_error:.3e} "
        f"interval_error={abs(direct-fourier.real):.3e}"
    )


if __name__ == "__main__":
    main()
