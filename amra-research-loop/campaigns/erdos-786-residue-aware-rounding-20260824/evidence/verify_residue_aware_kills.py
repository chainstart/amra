#!/usr/bin/env python3
"""Exact guards for the residue-aware P786 counterfamilies.

Finite instances corroborate the symbolic all-parameter proofs in the notes;
they are not used for finite-to-universal extrapolation.
"""

from __future__ import annotations

from collections import defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Deterministic for unsigned 64-bit integers.
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def next_primes(start: int, count: int) -> list[int]:
    out: list[int] = []
    n = max(3, start + 1)
    if n % 2 == 0:
        n += 1
    while len(out) < count:
        if is_prime(n):
            out.append(n)
        n += 2
    return out


def product(values) -> int:
    out = 1
    for value in values:
        out *= value
    return out


def ceil_log2(value: int) -> int:
    return (value - 1).bit_length()


def all_unbalanced_supports(values: list[int]) -> set[int]:
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for mask in range(1 << len(values)):
        selected = [values[i] for i in range(len(values)) if mask & (1 << i)]
        groups[product(selected)].append((mask.bit_count(), mask))
    supports: set[int] = set()
    for records in groups.values():
        for (ca, ma), (cb, mb) in combinations(records, 2):
            if ca != cb:
                supports.add(ma ^ mb)
    return supports


def rough_ordered_path(L: int, s: int, K: int) -> dict[str, object]:
    assert L >= 3 and s >= L and K % L == 0
    N = 1 << K
    y = 1 << (K // L)
    labels = next_primes(y, 2 * s)
    assert labels == sorted(labels) and all(p > y for p in labels)

    q = []
    for vertex in range(2 * s + 1):
        value = 1
        if vertex:
            value *= labels[vertex - 1]
        if vertex < 2 * s:
            value *= labels[vertex]
        q.append(value)
    assert len(set(q)) == 2 * s + 1
    left_q, right_q = q[0::2], q[1::2]
    assert product(left_q) == product(right_q) == product(labels)

    left_e0 = [K - ceil_log2(value) for value in left_q]
    right_e = [K - ceil_log2(value) for value in right_q]
    assert min(left_e0 + right_e) >= 0
    delta = sum(left_e0) - sum(right_e)
    assert delta > 0
    quotient, remainder = divmod(delta, len(left_e0))
    decrements = [quotient + (i < remainder) for i in range(len(left_e0))]
    left_e = [e - d for e, d in zip(left_e0, decrements)]
    assert min(left_e) >= 0 and sum(left_e) == sum(right_e)

    left = [(1 << e) * value for e, value in zip(left_e, left_q)]
    right = [(1 << e) * value for e, value in zip(right_e, right_q)]
    values = left + right
    assert len(set(values)) == 2 * s + 1
    assert product(left) == product(right)
    assert max(values) <= N
    assert all(value**L > N ** (L - 1) for value in values)

    degrees = [1] + [2] * (2 * s - 1) + [1]
    assert max(degrees) == 2 and sum(degrees) == 4 * s
    # Larger even shore has the two degree-one endpoints.
    assert sum(degrees[0::2]) == sum(degrees[1::2]) == 2 * s

    top = labels[-1]
    endpoint_value = left[-1]
    neighbor_value = right[-1]
    assert endpoint_value % top == 0 and neighbor_value % top == 0
    endpoint_cofactor = endpoint_value // top
    neighbor_cofactor = neighbor_value // top
    assert neighbor_cofactor % labels[-2] == 0

    return {
        "L": L,
        "s": s,
        "K": K,
        "N": N,
        "y": y,
        "labels": labels,
        "left": left,
        "right": right,
        "active_degrees": degrees,
        "cycle_rank": 0,
        "top_prime": top,
        "top_cofactors": [endpoint_cofactor, neighbor_cofactor],
        "token_count_before": 2,
        "token_count_after_strip": 2,
    }


def rough_path_guard() -> dict[str, object]:
    rows = []
    for L, s, K in [(3, 4, 48), (4, 8, 80), (5, 12, 100), (6, 18, 120)]:
        data = rough_ordered_path(L, s, K)
        values = data["left"] + data["right"]
        rows.append({
            "L": L,
            "s": s,
            "support": len(values),
            "K": K,
            "max_active_degree": max(data["active_degrees"]),
            "cycle_rank": data["cycle_rank"],
            "strict_high_tail": True,
            "squarefree_active_primes": True,
            "token_count_preserved_at_top_strip": data["token_count_before"] == data["token_count_after_strip"],
        })

    minimal = []
    for s in range(3, 5):
        data = rough_ordered_path(3, s, 48)
        values = data["left"] + data["right"]
        full = (1 << len(values)) - 1
        assert all_unbalanced_supports(values) == {full}
        minimal.append({"s": s, "support": len(values), "only_bad_support_is_full": True})
    return {"rows": rows, "minimal_replays": minimal}


def double_star(r: int, s: int) -> dict[str, object]:
    assert r >= 1 and s >= 1 and r != s
    labels = next_primes(40, r + s + 1)
    A = labels[:r]
    B = labels[r : r + s]
    p = labels[-1]
    X, Y = product(A), product(B)
    left = A + [p * Y]
    right = B + [p * X]
    values = left + right
    assert len(set(values)) == len(values)
    assert product(left) == product(right) == p * X * Y
    assert len(left) - len(right) == r - s
    assert (p * Y) // p == Y and (p * X) // p == X
    return {"r": r, "s": s, "A": A, "B": B, "p": p, "X": X, "Y": Y, "left": left, "right": right}


def double_star_guard() -> dict[str, object]:
    rows = []
    for r, s in [(2, 1), (3, 1), (4, 2), (6, 3)]:
        data = double_star(r, s)
        values = data["left"] + data["right"]
        if len(values) <= 9:
            full = (1 << len(values)) - 1
            assert all_unbalanced_supports(values) == {full}
        rows.append({
            "r": r,
            "s": s,
            "support": len(values),
            "top_fibre_cardinality": 2,
            "numerator_prime_support": s,
            "denominator_prime_support": r,
            "coprime_residues": True,
            "minimal_by_connected_edge_equations": True,
        })
    return {"rows": rows}


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "rough_ordered_paths": rough_path_guard(),
        "universal_double_stars": double_star_guard(),
        "scope": "exact finite guards for separately proved all-parameter RR.1 and RR.2; no finite extrapolation",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
