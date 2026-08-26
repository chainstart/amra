#!/usr/bin/env python3
"""Structured falsification of anchored-block gap submultiplicativity.

This is finite evidence only.  It searches boxes whose every local set is an
initial interval and splits the coprime coordinates into two nonempty blocks.
"""

from __future__ import annotations

from itertools import combinations, product
import json
import math
import random


def crt_pair(a, q, b, r):
    return a + q * (((b - a) * pow(q, -1, r)) % r)


def box_residues(moduli, widths):
    modulus = 1
    residues = [0]
    for q, d in zip(moduli, widths):
        residues = [crt_pair(a, modulus, b, q) for a in residues for b in range(d)]
        modulus *= q
    return modulus, sorted(residues)


def max_gap(modulus, residues):
    return max(
        [residues[i + 1] - residues[i] for i in range(len(residues) - 1)]
        + [modulus + residues[0] - residues[-1]]
    )


def max_gap_record(modulus, residues):
    candidates = [
        (residues[i + 1] - residues[i], residues[i], residues[i + 1])
        for i in range(len(residues) - 1)
    ]
    candidates.append((modulus + residues[0] - residues[-1], residues[-1], residues[0]))
    gap, start, end = max(candidates)
    return {"gap": gap, "start": start, "end_mod_period": end}


def combine_boxes(q, aa, r, bb):
    return sorted(crt_pair(a, q, b, r) for a in aa for b in bb)


tested = 0
generic_witness = None

# Exhaustive width tests on several genuinely multi-coordinate block splits.
families = [
    ((2, 3), (5, 7)),
    ((3, 4), (5, 7)),
    ((2, 5), (3, 7, 11)),
    ((3, 5), (4, 7, 11)),
    ((4, 5), (3, 7, 11)),
]

for left, right in families:
    for widths in product(*(range(1, q) for q in left + right)):
        wl = widths[: len(left)]
        wr = widths[len(left) :]
        q, aa = box_residues(left, wl)
        r, bb = box_residues(right, wr)
        assert math.gcd(q, r) == 1
        ga = max_gap(q, aa)
        gb = max_gap(r, bb)
        inter = combine_boxes(q, aa, r, bb)
        gi = max_gap(q * r, inter)
        tested += 1
        if gi > ga * gb:
            generic_witness = {
                "kind": "exhaustive_box",
                "left_moduli": left,
                "right_moduli": right,
                "left_widths": wl,
                "right_widths": wr,
                "gap_left": ga,
                "gap_right": gb,
                "gap_intersection": gi,
            }
            break
    if generic_witness:
        break

# Reproducible randomized tests on larger coprime-coordinate boxes.
if generic_witness is None:
    rng = random.Random(45110)
    pools = [
        ((5, 7, 11), (13, 17)),
        ((7, 11), (13, 17, 19)),
        ((11, 13, 17), (19, 23)),
    ]
    for left, right in pools:
        for _ in range(1000):
            wl = tuple(rng.randrange(1, q) for q in left)
            wr = tuple(rng.randrange(1, q) for q in right)
            q, aa = box_residues(left, wl)
            r, bb = box_residues(right, wr)
            ga = max_gap(q, aa)
            gb = max_gap(r, bb)
            inter = combine_boxes(q, aa, r, bb)
            gi = max_gap(q * r, inter)
            tested += 1
            if gi > ga * gb:
                generic_witness = {
                    "kind": "seeded_random_box",
                    "left_moduli": left,
                    "right_moduli": right,
                    "left_widths": wl,
                    "right_widths": wr,
                    "gap_left": ga,
                    "gap_right": gb,
                    "gap_intersection": gi,
                }
                break
        if generic_witness:
            break

# Stronger fixed-k search: every local width is exactly q-k, as in 451,
# though the moduli in this branch need not be prime.
same_k_witness = None
for k in range(3, 18):
    ambient = range(k + 1, 2 * k)
    for moduli in combinations(ambient, 4):
        if any(math.gcd(a, b) != 1 for a, b in combinations(moduli, 2)):
            continue
        if math.prod(moduli) > 2_000_000:
            continue
        for left_indices in combinations(range(4), 2):
            if 0 not in left_indices:  # avoid counting a split and its swap
                continue
            left = tuple(moduli[i] for i in left_indices)
            right = tuple(q for i, q in enumerate(moduli) if i not in left_indices)
            wl = tuple(q - k for q in left)
            wr = tuple(q - k for q in right)
            q, aa = box_residues(left, wl)
            r, bb = box_residues(right, wr)
            ga = max_gap(q, aa)
            gb = max_gap(r, bb)
            gi = max_gap(q * r, combine_boxes(q, aa, r, bb))
            tested += 1
            if gi > ga * gb:
                same_k_witness = {
                    "kind": "fixed_k_451_widths_composite_moduli",
                    "k": k,
                    "left_moduli": left,
                    "right_moduli": right,
                    "left_widths": wl,
                    "right_widths": wr,
                    "gap_left": ga,
                    "gap_right": gb,
                    "gap_intersection": gi,
                }
                break
        if same_k_witness:
            break
    if same_k_witness:
        break

# Actual 451 block splits for periods small enough to enumerate exactly.
actual_rows = []
actual_witness = None
for k in (6, 8, 10, 12, 14, 18, 20):
    primes = [q for q in range(k + 1, 2 * k) if all(q % d for d in range(2, math.isqrt(q) + 1))]
    if len(primes) < 2:
        continue
    for cut in range(1, len(primes)):
        left, right = tuple(primes[:cut]), tuple(primes[cut:])
        wl = tuple(q - k for q in left)
        wr = tuple(q - k for q in right)
        q, aa = box_residues(left, wl)
        r, bb = box_residues(right, wr)
        if q * r > 2_000_000:
            continue
        ga = max_gap(q, aa)
        gb = max_gap(r, bb)
        gi = max_gap(q * r, combine_boxes(q, aa, r, bb))
        tested += 1
        row = {
            "k": k,
            "cut": cut,
            "moduli": primes,
            "gap_left": ga,
            "gap_right": gb,
            "gap_intersection": gi,
            "ratio": gi / (ga * gb),
        }
        actual_rows.append(row)
        if gi > ga * gb:
            actual_witness = {"kind": "actual_451", **row}
            break
    if actual_witness:
        break

# Target the composite fixed-k witness pattern using actual primes: the first
# two primes above k form the thin block, while the other block ranges over
# pairs farther into (k,2k).  The cap is on the number of CRT output points,
# not on the period.
actual_subset_rows = 0
actual_subset_witness = None
for k in range(5, 201):
    primes = [q for q in range(k + 1, 2 * k) if all(q % d for d in range(2, math.isqrt(q) + 1))]
    if len(primes) < 4:
        continue
    left = tuple(primes[:2])
    wl = tuple(q - k for q in left)
    q, aa = box_residues(left, wl)
    ga = max_gap(q, aa)
    for right in combinations(primes[2:], 2):
        wr = tuple(p - k for p in right)
        if math.prod(wl + wr) > 5_000_000:
            continue
        r, bb = box_residues(right, wr)
        gb = max_gap(r, bb)
        gi = max_gap(q * r, combine_boxes(q, aa, r, bb))
        actual_subset_rows += 1
        tested += 1
        if gi > ga * gb:
            actual_subset_witness = {
                "kind": "actual_451_prime_subsets",
                "k": k,
                "left_moduli": left,
                "right_moduli": right,
                "left_widths": wl,
                "right_widths": wr,
                "gap_left": ga,
                "gap_right": gb,
                "gap_intersection": gi,
                "ratio": gi / (ga * gb),
                "left_period": q,
                "right_period": r,
                "intersection_period": q * r,
                "left_cardinality": len(aa),
                "right_cardinality": len(bb),
                "intersection_cardinality": len(aa) * len(bb),
                "left_gap_record": max_gap_record(q, aa),
                "right_gap_record": max_gap_record(r, bb),
                "intersection_gap_record": max_gap_record(q * r, combine_boxes(q, aa, r, bb)),
            }
            break
    if actual_subset_witness:
        break

# Is one side already a single dyadic-width block?  This is the relevant
# restricted form for a sequential dyadic merge (the other side may be the
# accumulated earlier blocks).
actual_dyadic_side_rows = 0
actual_dyadic_side_witness = None
for k in range(5, 101):
    primes = [q for q in range(k + 1, 2 * k) if all(q % d for d in range(2, math.isqrt(q) + 1))]
    if len(primes) < 4:
        continue
    left = tuple(primes[:2])
    wl = tuple(q - k for q in left)
    q, aa = box_residues(left, wl)
    ga = max_gap(q, aa)
    for right in combinations(primes[2:], 2):
        wr = tuple(p - k for p in right)
        if max(wr) >= 2 * min(wr):
            continue
        if math.prod(wl + wr) > 5_000_000:
            continue
        r, bb = box_residues(right, wr)
        gb = max_gap(r, bb)
        inter = combine_boxes(q, aa, r, bb)
        gi = max_gap(q * r, inter)
        actual_dyadic_side_rows += 1
        tested += 1
        if gi > ga * gb:
            actual_dyadic_side_witness = {
                "kind": "actual_451_one_dyadic_side",
                "k": k,
                "left_moduli": left,
                "right_moduli": right,
                "left_widths": wl,
                "right_widths": wr,
                "gap_left": ga,
                "gap_right": gb,
                "gap_intersection": gi,
                "ratio": gi / (ga * gb),
                "left_period": q,
                "right_period": r,
                "intersection_period": q * r,
                "intersection_gap_record": max_gap_record(q * r, inter),
            }
            break
    if actual_dyadic_side_witness:
        break

print(
    json.dumps(
        {
            "classification": "finite_falsification_only",
            "claim": "G(A cap B) <= G(A) G(B) for anchored CRT interval boxes",
            "tested": tested,
            "generic_anchored_box_witness": generic_witness,
            "fixed_k_width_witness": same_k_witness,
            "actual_451_witness": actual_witness,
            "actual_451_rows": actual_rows,
            "actual_prime_subset_rows": actual_subset_rows,
            "actual_prime_subset_witness": actual_subset_witness,
            "actual_dyadic_side_rows": actual_dyadic_side_rows,
            "actual_dyadic_side_witness": actual_dyadic_side_witness,
        },
        sort_keys=True,
    )
)
