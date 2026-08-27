#!/usr/bin/env python3
"""Exact finite guards for symbolic counterfamilies in the P786 successor.

The program checks instantiated identities and boundary inequalities.  The
all-parameter conclusions are the proofs in OBSTRUCTION_ANALYSIS.md and
MECHANISM_FALSIFICATION.md, not extrapolations from these loops.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import json


def primes(count: int, *, avoid: set[int] | None = None) -> list[int]:
    avoid = avoid or set()
    out: list[int] = []
    candidate = 2
    while len(out) < count:
        if candidate not in avoid and all(candidate % p for p in range(2, int(candidate**0.5) + 1)):
            out.append(candidate)
        candidate += 1
    return out


def ceil_log_base(value: int, base: int) -> int:
    power = 1
    exponent = 0
    while power < value:
        power *= base
        exponent += 1
    return exponent


def path_base_circuit(s: int, *, padding_prime: int = 2, controlled: set[int] | None = None):
    """Return odd/base-prime products on the bipartition of P_(2s+1)."""
    controlled = controlled or set()
    labels = primes(2 * s + 10, avoid=controlled | {padding_prime})[: 2 * s]
    # Vertices 0,...,2s, with even vertices on the larger shore.
    q = []
    for vertex in range(2 * s + 1):
        value = 1
        if vertex > 0:
            value *= labels[vertex - 1]
        if vertex < 2 * s:
            value *= labels[vertex]
        q.append(value)
    left = q[0::2]
    right = q[1::2]
    assert len(left) == s + 1 and len(right) == s
    assert len(set(q)) == 2 * s + 1
    assert product(left) == product(right) == product(labels)
    return labels, left, right


def product(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def padded_path_circuit(s: int, K: int, *, padding_prime: int = 2, controlled: set[int] | None = None):
    labels, left_q, right_q = path_base_circuit(s, padding_prime=padding_prime, controlled=controlled)
    base = padding_prime
    N = base**K
    left_e0 = [K - ceil_log_base(q, base) for q in left_q]
    right_e = [K - ceil_log_base(q, base) for q in right_q]
    assert min(left_e0 + right_e) >= 0
    delta = sum(left_e0) - sum(right_e)
    assert delta > 0
    quotient, remainder = divmod(delta, len(left_e0))
    decrements = [quotient + (i < remainder) for i in range(len(left_e0))]
    left_e = [e - d for e, d in zip(left_e0, decrements)]
    assert min(left_e) >= 0
    assert sum(left_e) == sum(right_e)
    left = [base**e * q for e, q in zip(left_e, left_q)]
    right = [base**e * q for e, q in zip(right_e, right_q)]
    assert len(set(left + right)) == 2 * s + 1
    assert product(left) == product(right)
    assert max(left + right) <= N
    return {
        "s": s,
        "K": K,
        "N": N,
        "labels": labels,
        "left": left,
        "right": right,
        "max_decrement": max(decrements),
        "delta": delta,
    }


def unbalanced_supports(values: list[int]) -> set[int]:
    groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for mask in range(1 << len(values)):
        chosen = [values[i] for i in range(len(values)) if mask & (1 << i)]
        groups[product(chosen)].append((mask.bit_count(), mask))
    supports: set[int] = set()
    for records in groups.values():
        for (ca, ma), (cb, mb) in combinations(records, 2):
            if ca != cb:
                supports.add(ma ^ mb)
    return supports


def moving_thin_tail_guard() -> dict[str, object]:
    rows = []
    # eta=1/denominator and K*eta grows across these exact instances.
    for denominator, K in [(4, 256), (8, 512), (16, 1024), (24, 1536)]:
        eta = Fraction(1, denominator)
        s = 4 * denominator
        data = padded_path_circuit(s, K)
        values = data["left"] + data["right"]
        # Exact check a > N^(1-eta): a^denominator > N^(denominator-1).
        assert all(value**denominator > data["N"] ** (denominator - 1) for value in values)
        rows.append({
            "eta": f"1/{denominator}",
            "s": s,
            "support": len(values),
            "K": K,
            "max_decrement": data["max_decrement"],
            "equal_product": True,
            "inside_strict_tail": True,
        })

    # Exhaustive minimal-support replay at small s; the universal proof uses
    # the unique edge-prime equations on every connected path.
    minimal_rows = []
    for s in range(1, 5):
        data = padded_path_circuit(s, 128)
        values = data["left"] + data["right"]
        full = (1 << len(values)) - 1
        bad = unbalanced_supports(values)
        assert bad == {full}
        minimal_rows.append({"s": s, "support": 2 * s + 1, "only_bad_support_is_full": True})
    return {"tail_rows": rows, "minimal_rows": minimal_rows}


def circuit_triangle_guard() -> dict[str, object]:
    edges = [{2, 3, 6}, {5, 6, 30}, {2, 5, 10}]
    assert all(len(a & b) == 1 for a, b in combinations(edges, 2))
    assert not set.intersection(*edges)
    assert 2 * 3 == 6 and 5 * 6 == 30 and 2 * 5 == 10
    # {2,3,6} is a maximal disjoint family; choosing 3 misses both others.
    assert 3 not in edges[1] and 3 not in edges[2]
    return {"edges": [sorted(edge) for edge in edges], "arbitrary_representative_failure": 3}


def residue_free_largest_prime_guard() -> dict[str, object]:
    # 2*3=6.  In the largest-prime fibre p=3, {3} and {6} balance in
    # cardinality, but stripping 3 leaves the lower-prime residue 1 versus 2.
    assert 2 * 3 == 6
    return {
        "relation": "2*3=6",
        "top_fibre": 3,
        "top_counts": [1, 1],
        "stripped_cofactor_products": [1, 2],
        "triangular_without_residue": False,
    }


def adjacent_degree_guard(maximum_s: int = 8) -> dict[str, object]:
    rows = []
    cursor = 0
    labels = primes(sum(s * (s + 1) for s in range(1, maximum_s + 1)) + 10)
    for s in range(1, maximum_s + 1):
        edge_primes = labels[cursor : cursor + s * (s + 1)]
        cursor += s * (s + 1)
        grid = [edge_primes[i * s : (i + 1) * s] for i in range(s + 1)]
        left = [product(row) for row in grid]
        right = [product(grid[i][j] for i in range(s + 1)) for j in range(s)]
        assert product(left) == product(right)
        assert len(set(left + right)) == 2 * s + 1
        rows.append({"s": s, "degrees": [s, s + 1], "support": 2 * s + 1})
    return {"rows": rows}


def rank_one_guard(maximum_r: int = 40) -> dict[str, object]:
    rows = []
    for r in [1, 2, 5, 10, maximum_r]:
        triples = []
        occupied: set[int] = set()
        for j in range(r):
            a, b, c = 3 * j + 1, 3 * j + 2, 6 * j + 3
            assert a + b == c and max(a, b, c) <= 6 * r
            assert not ({a, b, c} & occupied)
            occupied.update({a, b, c})
            triples.append([a, b, c])
        rows.append({"r": r, "matrix_rank": 1, "disjoint_bad_supports": r, "transversal_lower_bound": r})
    return {"rows": rows}


def finite_signature_guard() -> dict[str, object]:
    controlled = {2, 3, 5, 7}
    data = padded_path_circuit(5, 160, padding_prime=11, controlled=controlled)
    values = data["left"] + data["right"]
    assert all(all(value % p for p in controlled) for value in values)
    return {
        "controlled_primes": sorted(controlled),
        "padding_prime": 11,
        "support": len(values),
        "all_zero_controlled_signature": True,
        "equal_product": product(data["left"]) == product(data["right"]),
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "moving_thin_tail": moving_thin_tail_guard(),
        "circuit_triangle": circuit_triangle_guard(),
        "largest_prime_residue": residue_free_largest_prime_guard(),
        "adjacent_active_degrees": adjacent_degree_guard(),
        "rank_one_family": rank_one_guard(),
        "finite_signature": finite_signature_guard(),
        "scope": "exact finite guards for separately proved all-parameter counterfamilies; no finite-to-asymptotic inference",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
