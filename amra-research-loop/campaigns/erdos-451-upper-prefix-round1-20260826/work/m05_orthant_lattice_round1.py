#!/usr/bin/env python3
"""Exact diagnostics for the U451-M05 diagonal-plus-one CRT lattice.

Finite checks support bookkeeping only.  The proofs are in the companion
evidence note; this program deliberately makes no theorem claim from samples.
"""

from __future__ import annotations

import math
from functools import reduce
from fractions import Fraction
from itertools import product as cartesian_product
from operator import mul


def primes_between(k: int) -> list[int]:
    sieve = bytearray(b"\x01") * (2 * k)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(2 * k - 1) + 1):
        if sieve[p]:
            sieve[p * p : 2 * k : p] = b"\x00" * (
                ((2 * k - 1 - p * p) // p) + 1
            )
    return [p for p in range(k + 1, 2 * k) if sieve[p]]


def prod(values: list[int]) -> int:
    return reduce(mul, values, 1)


def actual_offsets(n: int, ps: list[int], ds: list[int]) -> list[int] | None:
    offsets = [(-n) % p for p in ps]
    return offsets if all(s < d for s, d in zip(offsets, ds)) else None


def symmetric_offsets(n: int, ps: list[int], ds: list[int]) -> list[int] | None:
    offsets: list[int] = []
    for p, d in zip(ps, ds):
        rem = n % p
        s = -rem if rem <= p // 2 else p - rem
        if abs(s) > d - 1:
            return None
        offsets.append(s)
    return offsets


def orientable(offsets: list[int], ds: list[int]) -> bool:
    lower = max(s - d + 1 for s, d in zip(offsets, ds))
    upper = min(offsets)
    return lower <= upper


def orientable_above(offsets: list[int], ds: list[int], n: int, floor: int) -> bool:
    """Whether a common integral shift gives an actual point above floor."""
    lower = max(s - d + 1 for s, d in zip(offsets, ds))
    upper = min(offsets)
    return max(lower, floor - n + 1) <= upper


def small_exact(k: int) -> None:
    ps = primes_between(k)
    ds = [p - k for p in ps]
    P = prod(ps)
    target_count = prod(ds)
    assert P <= 1_000_000

    apery_target_count = 0
    sym_count = 0
    orientable_sym_count = 0
    first_actual = None
    first_symmetric = None
    signed_rows: list[tuple[int, bool, bool]] = []
    for n in range(P):
        actual = actual_offsets(n, ps, ds)
        if actual is not None:
            apery_target_count += 1
            if n > 2 * k and first_actual is None:
                first_actual = n
        signed = symmetric_offsets(n, ps, ds)
        if signed is not None:
            sym_count += 1
            if orientable(signed, ds):
                orientable_sym_count += 1
            if n > 2 * k:
                signed_rows.append(
                    (n, orientable(signed, ds), orientable_above(signed, ds, n, 2 * k))
                )
            if n > 2 * k and first_symmetric is None:
                first_symmetric = n

    assert apery_target_count == target_count
    signed_box_count = prod([2 * d - 1 for d in ds])
    assert sym_count == signed_box_count
    orientable_count_bound = (4 * k + 1) * target_count
    assert orientable_sym_count <= orientable_count_bound
    assert all(p - d + 1 == k + 1 for p, d in zip(ps, ds))
    ray_det = P * P
    lattice_det = P
    assert ray_det // lattice_det == P
    signed_before_actual = [row for row in signed_rows if row[0] <= first_actual]

    active = [i for i, d in enumerate(ds) if d >= 2]
    mixed_bad = 0
    if len(active) >= 2:
        for signs in cartesian_product((-1, 1), repeat=len(active)):
            if min(signs) == max(signs):
                continue
            signed = [0] * len(ps)
            for i, sign in zip(active, signs):
                signed[i] = sign * (ds[i] - 1)
            # CRT guarantees the lattice point.  The common-shift criterion
            # itself is checked here without enumerating that CRT solution.
            assert not orientable(
                [signed[i] for i in active], [ds[i] for i in active]
            )
            mixed_bad += 1
        assert mixed_bad == 2 ** len(active) - 2
    print(
        "exact",
        f"k={k}",
        f"m={len(ps)}",
        f"P={P}",
        f"det={lattice_det}",
        f"ray_index={ray_det // lattice_det}",
        f"actual_apery={apery_target_count}",
        f"prod_d={target_count}",
        f"symmetric_apery={sym_count}",
        f"orientable_symmetric={orientable_sym_count}",
        f"signed_box={signed_box_count}",
        f"orientable_count_bound={orientable_count_bound}",
        f"first_actual_gt_2k={first_actual}",
        f"first_symmetric_gt_2k={first_symmetric}",
        f"signed_through_first_actual={len(signed_before_actual)}",
        f"orientable_through_first_actual={sum(row[1] for row in signed_before_actual)}",
        f"oriented_above_through_first_actual={sum(row[2] for row in signed_before_actual)}",
        f"exact_mixed_sign_bad_family={mixed_bad}",
    )

    delta = 1
    while delta < k:
        block = [(p, d) for p, d in zip(ps, ds) if delta <= d < 2 * delta]
        if block:
            bps = [p for p, _ in block]
            bds = [d for _, d in block]
            q = len(block)
            w = (delta - 1) // 2
            delta_b = prod([2 * w + 1 for _ in block])
            delta_b /= prod([2 * p for p in bps])
            # Reconstruct exactly after the compact integer products above.
            centered_density = Fraction(1, 1)
            actual_density = Fraction(1, 1)
            for p, d in block:
                centered_density *= Fraction(2 * w + 1, 2 * p)
                actual_density *= Fraction(d, p)
            assert math.isclose(delta_b, float(centered_density))
            H_fraction = Fraction(4 * k * delta, q) / centered_density
            H = (H_fraction.numerator + H_fraction.denominator - 1) // H_fraction.denominator
            block_period = prod(bps)
            first_block_actual = next(
                n
                for n in range(2 * k + 1, 2 * k + block_period + 1)
                if actual_offsets(n, bps, bds) is not None
            )
            claimed_bound = Fraction(6 * k * k * (6**q), q) / actual_density
            assert first_block_actual <= H + w
            assert Fraction(H + w, 1) <= claimed_bound
            print(
                "dyadic",
                f"k={k}",
                f"Delta={delta}",
                f"q={q}",
                f"first_actual={first_block_actual}",
                f"H_plus_w={H + w}",
                f"loss_ratio={(H + w) * float(actual_density):.6f}",
            )
        delta *= 2


def exponent_ledger(k: int) -> None:
    ps = primes_between(k)
    ds = [p - k for p in ps]
    m = len(ps)
    r = m + 1
    log_d_inv = sum(math.log(p / d) for p, d in zip(ps, ds))
    log_half_ratio = sum(math.log(d / (d - 0.5)) for d in ds)
    harmonic_bound = 1.0 + math.log(k)
    assert log_half_ratio <= harmonic_bound + 1e-12
    log_full_basis_barrier = 0.5 * r * math.log(r) + log_d_inv
    log_generic_m_to_m = m * math.log(max(m, 1)) + log_d_inv
    print(
        "ledger",
        f"k={k}",
        f"m={m}",
        f"log_Dinv={log_d_inv:.9f}",
        f"log_half_ratio={log_half_ratio:.9f}",
        f"half_ratio_bound={harmonic_bound:.9f}",
        f"log_full_basis_barrier={log_full_basis_barrier:.9f}",
        f"barrier_over_k={log_full_basis_barrier / k:.9f}",
        f"log_m_to_m_over_k={log_generic_m_to_m / k:.9f}",
    )


def main() -> None:
    for k in (7, 10, 15, 20):
        ps = primes_between(k)
        if prod(ps) <= 1_000_000:
            small_exact(k)
    for k in (100, 1_000, 10_000, 100_000):
        exponent_ledger(k)


if __name__ == "__main__":
    main()
