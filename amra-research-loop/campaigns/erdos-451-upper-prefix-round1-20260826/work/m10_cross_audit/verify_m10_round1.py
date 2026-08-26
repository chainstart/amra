#!/usr/bin/env python3
"""Independent exact checks for the M10 round-1 cross-audit.

This does not import the author scripts.  Finite searches are falsification
tools only; theorem status is determined in the audit note.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations


def primes_below(n: int) -> list[int]:
    sieve = bytearray(b"\x01") * n
    if n:
        sieve[0] = 0
    if n > 1:
        sieve[1] = 0
    for p in range(2, math.isqrt(n - 1) + 1):
        if sieve[p]:
            sieve[p * p : n : p] = b"\x00" * (((n - 1 - p * p) // p) + 1)
    return [p for p in range(2, n) if sieve[p]]


def crt2(a: int, q: int, b: int, r: int) -> int:
    assert math.gcd(q, r) == 1
    return a + q * (((b - a) * pow(q, -1, r)) % r)


def box(moduli: tuple[int, ...], k: int) -> tuple[int, list[int]]:
    period = 1
    residues = [0]
    for modulus in moduli:
        width = modulus - k
        inverse = pow(period, -1, modulus)
        residues = [
            a + period * (((b - a) * inverse) % modulus)
            for a in residues
            for b in range(width)
        ]
        period *= modulus
    residues.sort()
    assert len(residues) == math.prod(p - k for p in moduli)
    return period, residues


def gap_record(period: int, residues: list[int]) -> dict[str, int]:
    assert residues
    best = (period + residues[0] - residues[-1], residues[-1], residues[0])
    for left, right in zip(residues, residues[1:]):
        best = max(best, (right - left, left, right))
    return {"gap": best[0], "start": best[1], "end_mod_period": best[2]}


def combine(
    q: int, left: list[int], r: int, right: list[int]
) -> tuple[int, list[int]]:
    assert math.gcd(q, r) == 1
    inverse = pow(q, -1, r)
    values = [
        a + q * (((b - a) * inverse) % r) for a in left for b in right
    ]
    values.sort()
    return q * r, values


def verify_claimed_witness(k: int, left: tuple[int, ...], right: tuple[int, ...]) -> dict[str, object]:
    q, aa = box(left, k)
    r, bb = box(right, k)
    qr, both = combine(q, aa, r, bb)
    ga = gap_record(q, aa)
    gb = gap_record(r, bb)
    gi = gap_record(qr, both)
    return {
        "k": k,
        "left": left,
        "right": right,
        "periods": (q, r, qr),
        "cardinalities": (len(aa), len(bb), len(both)),
        "left_gap": ga,
        "right_gap": gb,
        "intersection_gap": gi,
        "ratio": gi["gap"] / (ga["gap"] * gb["gap"]),
    }


def direct_pair_audit(max_k: int) -> dict[str, int]:
    plist = primes_below(2 * max_k + 1)
    checked = 0
    for k in range(4, max_k + 1):
        ps = [p for p in plist if k < p < 2 * k]
        for q, p in combinations(ps, 2):
            a = q - k
            delta = p - q
            period, allowed = box((q, p), k)
            exact_gap = gap_record(period, allowed)["gap"]
            run_bound = ((k - a) // delta + 3) * q
            j0 = (a - 1) // delta
            j1 = k // delta + 1
            lower = (j1 - j0) * q - a + 1
            assert lower <= exact_gap <= run_bound
            # Check the block phase iff statement across one p-cycle.
            for j in range(p):
                phase = (j * delta) % p
                block_nonempty = any(
                    ((j * q + rem) % p) < p - k for rem in range(a)
                )
                assert block_nonempty == (not (a <= phase <= k))
            checked += 1
    return {"max_k": max_k, "prime_pairs_checked": checked}


def multiplier_pullback_gap(p: int, r: int, residues: list[int]) -> dict[str, int]:
    """Gap in t when p*t modulo r belongs to residues."""
    inv = pow(p, -1, r)
    pulled = sorted((b * inv) % r for b in residues)
    return gap_record(r, pulled)


def search_width_one_vs_dyadic(max_k: int, point_cap: int) -> dict[str, object]:
    plist = primes_below(2 * max_k + 1)
    tested = 0
    best: dict[str, object] | None = None
    violations = 0
    for k in range(4, max_k + 1):
        p0 = k + 1
        if p0 not in plist:
            continue
        ps = [p for p in plist if k < p < 2 * k and p != p0]
        for pair in combinations(ps, 2):
            widths = tuple(p - k for p in pair)
            if max(widths) >= 2 * min(widths):
                continue
            if math.prod(widths) > point_cap:
                continue
            r, bb = box(pair, k)
            gb_record = gap_record(r, bb)
            gb = gb_record["gap"]
            pulled_record = multiplier_pullback_gap(p0, r, bb)
            pulled_gap = pulled_record["gap"]
            ratio = pulled_gap / gb
            tested += 1
            if ratio > 1:
                violations += 1
            row = {
                "k": k,
                "left": (p0,),
                "right": pair,
                "right_widths": widths,
                "gap_left": p0,
                "gap_right": gb,
                "gap_intersection": p0 * pulled_gap,
                "ratio": ratio,
                "right_cardinality": len(bb),
                "right_period": r,
                "intersection_period": p0 * r,
                "right_gap_record": gb_record,
                "pullback_gap_record": pulled_record,
                "intersection_gap_record": {
                    "gap": p0 * pulled_record["gap"],
                    "start": p0 * pulled_record["start"],
                    "end_mod_period": p0 * pulled_record["end_mod_period"],
                },
            }
            if best is None or ratio > float(best["ratio"]):
                best = row
    return {"tested": tested, "violations": violations, "best": best}


def search_two_by_two(max_k: int, point_cap: int) -> dict[str, object]:
    """Actual first-two-prime block against a dyadic prime pair."""
    plist = primes_below(2 * max_k + 1)
    tested = 0
    best: dict[str, object] | None = None
    for k in range(5, max_k + 1):
        ps = [p for p in plist if k < p < 2 * k]
        if len(ps) < 4:
            continue
        left = tuple(ps[:2])
        q, aa = box(left, k)
        ga = gap_record(q, aa)["gap"]
        for right in combinations(ps[2:], 2):
            widths = tuple(p - k for p in right)
            if max(widths) >= 2 * min(widths):
                continue
            if len(aa) * math.prod(widths) > point_cap:
                continue
            r, bb = box(right, k)
            qr, both = combine(q, aa, r, bb)
            gb = gap_record(r, bb)["gap"]
            gi = gap_record(qr, both)["gap"]
            ratio = gi / (ga * gb)
            tested += 1
            row = {
                "k": k,
                "left": left,
                "right": right,
                "widths": tuple(p - k for p in left + right),
                "gaps": (ga, gb, gi),
                "ratio": ratio,
                "intersection_cardinality": len(both),
            }
            if best is None or ratio > float(best["ratio"]):
                best = row
    return {"tested": tested, "best": best}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=260)
    parser.add_argument("--point-cap", type=int, default=2_000_000)
    parser.add_argument("--skip-width-one", action="store_true")
    parser.add_argument("--skip-two-by-two", action="store_true")
    args = parser.parse_args()
    result = {
        "classification": "finite_cross_audit_only",
        "pair_theorem": direct_pair_audit(45),
        "claimed_witnesses": [
            verify_claimed_witness(22, (23, 29), (31, 43)),
            verify_claimed_witness(88, (89, 97), (131, 173)),
        ],
        "width_one_vs_dyadic": None
        if args.skip_width_one
        else search_width_one_vs_dyadic(args.max_k, args.point_cap),
        "two_by_two": None
        if args.skip_two_by_two
        else search_two_by_two(args.max_k, args.point_cap),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
