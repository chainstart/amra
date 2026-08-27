#!/usr/bin/env python3
"""Exact finite falsification tests for the Erdős 451 upper-bound campaign.

The output is evidence about named bridges only.  It contains no extrapolation
from finite k to the all-parameter conjecture.
"""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import product
from math import comb, prod


def primes_below(n: int) -> list[int]:
    sieve = [True] * n
    if n:
        sieve[0] = False
    if n > 1:
        sieve[1] = False
    for q in range(2, int(n**0.5) + 1):
        if sieve[q]:
            sieve[q * q : n : q] = [False] * (((n - 1) - q * q) // q + 1)
    return [q for q, is_prime in enumerate(sieve) if is_prime]


def interval_primes(k: int) -> list[int]:
    return [p for p in primes_below(2 * k) if k < p < 2 * k]


def is_451_allowed(n: int, k: int, ps: list[int] | None = None) -> bool:
    ps = interval_primes(k) if ps is None else ps
    return all(n % p == 0 or n % p > k for p in ps)


def first_451(k: int, cap: int) -> int | None:
    ps = interval_primes(k)
    for n in range(2 * k + 1, cap + 1):
        if is_451_allowed(n, k, ps):
            return n
    return None


def allowed_with_shift(n: int, ps: list[int], widths: list[int], shifts: tuple[int, ...]) -> bool:
    # At shift zero this is the anchored interval {0,-1,...,-(d-1)}.
    return all(((s - n) % p) < d for p, d, s in zip(ps, widths, shifts))


def first_shifted(ps: list[int], widths: list[int], shifts: tuple[int, ...]) -> int:
    period = prod(ps)
    for n in range(1, period + 1):
        if allowed_with_shift(n, ps, widths, shifts):
            return n
    raise AssertionError("CRT box must be nonempty")


def density_translation_test() -> dict[str, object]:
    ps = [5, 7, 11]
    widths = [2, 3, 5]
    period = prod(ps)
    box_size = prod(widths)
    anchored = first_shifted(ps, widths, (0, 0, 0))
    maximum = (-1, ())
    for shifts in product(*[range(p) for p in ps]):
        first = first_shifted(ps, widths, shifts)
        if first > maximum[0]:
            maximum = (first, shifts)
    return {
        "moduli": ps,
        "widths": widths,
        "period": period,
        "box_size_for_every_translation": box_size,
        "density_for_every_translation": f"{box_size}/{period}",
        "anchored_first_positive": anchored,
        "max_first_positive_over_local_translations": maximum[0],
        "maximizing_local_shifts": list(maximum[1]),
        "conclusion": "Equal exact CRT density does not determine the first representative.",
    }


def translation_window_test() -> dict[str, object]:
    k = 20
    ps = interval_primes(k)
    period = prod(ps)
    allowed = [is_451_allowed(n, k, ps) for n in range(period)]
    window_length = 100
    nonempty = 0
    for start in range(period):
        if any(allowed[(start + j) % period] for j in range(1, window_length + 1)):
            nonempty += 1
    fixed_start = 2 * k
    fixed_count = sum(allowed[fixed_start + j] for j in range(1, window_length + 1))
    return {
        "k": k,
        "primes": ps,
        "period": period,
        "window_length": window_length,
        "nonempty_translated_windows": nonempty,
        "total_translated_windows": period,
        "fixed_initial_start": fixed_start,
        "fixed_initial_survivor_count": fixed_count,
        "exact_first_survivor_after_2k": first_451(k, period),
        "conclusion": "A positive translation average is compatible with an empty initial window.",
    }


def bonferroni_test() -> dict[str, object]:
    rows = []
    for m in [8, 12, 20, 30]:
        for r in [1, 3, 5]:
            if r >= m:
                continue
            value = sum(((-1) ** j) * Fraction(comb(m, j), 2**j) for j in range(r + 1))
            rows.append({"m": m, "odd_degree": r, "lower_polynomial": str(value)})
        last_odd = m - 1
        value = sum(((-1) ** j) * Fraction(comb(m, j), 2**j) for j in range(last_odd + 1))
        rows.append({"m": m, "odd_degree": last_odd, "lower_polynomial": str(value)})
    return {
        "comparator": "m independent forbidden events, each of probability 1/2",
        "true_all_allowed_probability": "2^(-m)",
        "rows": rows,
        "exact_sign_statement": "For every m and every odd r<m, sum_{j=0}^r (-1)^j binom(m,j)2^(-j)<=0.",
        "conclusion": "No proper odd Bonferroni truncation certifies the positive rare-event mass even in the ideal independent comparator.",
    }


def symmetric_sign_test() -> dict[str, object]:
    k = 7
    ps = interval_primes(k)
    n = 12
    coordinates = []
    for p in ps:
        residue = n % p
        centered = residue if residue <= p // 2 else residue - p
        coordinates.append({"p": p, "width": p - k, "residue": residue, "centered_residue": centered})
        assert abs(centered) < p - k
    n_allowed = is_451_allowed(n, k, ps)
    minus_n_allowed = all((-n) % p == 0 or (-n) % p > k for p in ps)
    assert not n_allowed and not minus_n_allowed
    return {
        "k": k,
        "n": n,
        "coordinates": coordinates,
        "n_is_one_sided_allowed": n_allowed,
        "minus_n_is_one_sided_allowed": minus_n_allowed,
        "conclusion": "The symmetric recurrence has mixed signs, and neither global orientation lies in the one-sided box.",
    }


def quotient_vectors() -> list[dict[str, object]]:
    rows = []
    for k in [10, 15, 20, 25, 30]:
        n = first_451(k, 2_000_000)
        if n is None:
            continue
        ps = interval_primes(k)
        entries = []
        for p in ps:
            s = (-n) % p
            assert s < p - k
            entries.append({"p": p, "offset": s, "quotient": (n + s) // p})
        rows.append({
            "k": k,
            "n": n,
            "prime_count": len(ps),
            "distinct_quotients": len({entry["quotient"] for entry in entries}),
            "entries": entries,
        })
    return rows


def absorption_phase_test() -> dict[str, object]:
    k = 20
    cutoff = 10
    ps = interval_primes(k)
    absorbed = [p for p in ps if p - k < cutoff]
    remaining = [p for p in ps if p not in absorbed]
    q = prod(absorbed)
    phases = []
    for p in remaining:
        inv = pow(q, -1, p)
        original = [(-s) % p for s in range(p - k)]
        transformed = sorted((inv * a) % p for a in original)
        is_cyclic_unit_interval = any(
            set(transformed) == {(start + j) % p for j in range(len(transformed))}
            for start in range(p)
        )
        phases.append({
            "p": p,
            "width": p - k,
            "inverse_absorber_mod_p": inv,
            "transformed_allowed_residues_for_multiplier": transformed,
            "is_cyclic_unit_interval": is_cyclic_unit_interval,
        })
    return {
        "k": k,
        "gap_cutoff": cutoff,
        "absorbed_primes": absorbed,
        "absorber_Q": q,
        "remaining_coordinates": phases,
        "conclusion": "Prime absorption widens the minimum cardinality but dilates every remaining interval by Q^{-1}; aligned unit-step interval structure is not preserved.",
    }


def main() -> None:
    payload = {
        "schema_version": "erdos451.upper_finite_kill_tests.v1",
        "interpretation_boundary": [
            "Every computation is exact and finite.",
            "The tests refute only the named bridge; they do not prove an asymptotic upper bound.",
            "No network data is used.",
        ],
        "density_translation": density_translation_test(),
        "translation_windows": translation_window_test(),
        "bonferroni": bonferroni_test(),
        "symmetric_sign": symmetric_sign_test(),
        "quotient_vectors": quotient_vectors(),
        "absorption_phase": absorption_phase_test(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
