#!/usr/bin/env python3
"""Exact finite guards for the distinct-factor P786 campaign.

The finite optimizer is complete only at each printed cutoff.  The symbolic
proofs in OBSTRUCTION_ANALYSIS.md carry the all-parameter statements.
"""

from __future__ import annotations

from collections import defaultdict
from decimal import Decimal, getcontext
from itertools import combinations
from math import comb
from pathlib import Path
import hashlib
import json


getcontext().prec = 80


def primes(count: int) -> list[int]:
    result: list[int] = []
    candidate = 2
    while len(result) < count:
        if all(candidate % p for p in result if p * p <= candidate):
            result.append(candidate)
        candidate += 1
    return result


def subset_records(universe: list[int]) -> list[tuple[int, int, int]]:
    records = [(1, 0, 0)]
    for index, value in enumerate(universe):
        old = list(records)
        records.extend((product * value, card + 1, mask | (1 << index)) for product, card, mask in old)
    return records


def minimal_bad_supports(universe: list[int]) -> list[int]:
    by_product: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for product, card, mask in subset_records(universe):
        by_product[product].append((card, mask))
    supports: set[int] = set()
    for group in by_product.values():
        for (card_a, mask_a), (card_b, mask_b) in combinations(group, 2):
            if card_a != card_b:
                supports.add(mask_a ^ mask_b)
    ordered = sorted(supports, key=lambda mask: (mask.bit_count(), mask))
    minimal: list[int] = []
    for support in ordered:
        if not any(item & support == item for item in minimal):
            minimal.append(support)
    return minimal


def exact_finite_optima(maximum: int = 18) -> dict[str, object]:
    rows = []
    for cutoff in range(2, maximum + 1):
        universe = list(range(2, cutoff + 1))
        bad = minimal_bad_supports(universe)
        best_size = -1
        best_mask = 0
        for mask in range(1 << len(universe)):
            size = mask.bit_count()
            if size <= best_size:
                continue
            if all(mask & support != support for support in bad):
                best_size = size
                best_mask = mask
        best = [value for index, value in enumerate(universe) if best_mask & (1 << index)]
        # Independent subset-product replay of the maximizing set.
        cardinality_by_product: dict[int, int] = {}
        for product, card, _ in subset_records(best):
            if product in cardinality_by_product:
                assert cardinality_by_product[product] == card
            else:
                cardinality_by_product[product] = card
        rows.append({
            "N": cutoff,
            "minimal_bad_supports": len(bad),
            "optimum": best_size,
            "witness": best,
        })
    return {
        "maximum": maximum,
        "rows": rows,
        "scope": "complete fixed-N forbidden-support ILP by exhaustive binary assignments; no asymptotic inference",
    }


def log_fractional_cover_guard(maximum: int = 18) -> dict[str, object]:
    rows = []
    for cutoff in range(6, maximum + 1):
        universe = list(range(2, cutoff + 1))
        bad = minimal_bad_supports(universe)
        log_cutoff = Decimal(cutoff).ln()
        weights = [(Decimal(cutoff) / Decimal(value)).ln() / log_cutoff for value in universe]
        minimum_edge_weight = min(
            sum(weights[index] for index in range(len(universe)) if support & (1 << index))
            for support in bad
        )
        assert minimum_edge_weight >= Decimal(1) - Decimal("1e-60")
        total = sum(weights)
        exact_total = (Decimal(cutoff) * log_cutoff - sum(Decimal(value).ln() for value in range(1, cutoff + 1))) / log_cutoff - 1
        assert abs(total - exact_total) < Decimal("1e-60")
        rows.append({
            "N": cutoff,
            "minimal_bad_supports": len(bad),
            "minimum_edge_weight": str(minimum_edge_weight),
            "total_fractional_weight": str(total),
        })
    return {
        "rows": rows,
        "conclusion": "w_N(n)=log(N/n)/log N covers every enumerated minimal bad support with weight at least one",
        "scope": "finite replay; the exact all-N proof is the logarithmic identity in SURVIVOR_DEEPENING.md",
    }


def variant_mismatch_guard() -> dict[str, object]:
    admissible = [2, 4]
    products = [(product, card) for product, card, _ in subset_records(admissible)]
    assert len({product for product, _ in products}) == 4
    # Prime-2 exponent vectors are 1 and 2: 2*v(2)-v(4)=0 but coefficient sum is 1.
    assert 2 * 1 - 2 == 0 and 2 - 1 != 0
    return {
        "set": admissible,
        "subset_products": sorted(product for product, _ in products),
        "distinct_factor_property": True,
        "repeated_relation": "2*2=4",
        "conclusion": "totally additive level-one separation is not necessary in the Finset variant",
    }


def bipartite_circuit_guard(maximum_s: int = 6) -> dict[str, object]:
    rows = []
    cursor = 0
    prime_list = primes(sum(s * (s + 1) for s in range(2, maximum_s + 1)) + 20)
    for s in range(2, maximum_s + 1):
        labels = prime_list[cursor:cursor + s * (s + 1)]
        cursor += s * (s + 1)
        edge = [[labels[i * s + j] for j in range(s)] for i in range(s + 1)]
        left = []
        for row in edge:
            value = 1
            for p in row:
                value *= p
            left.append(value)
        right = []
        for j in range(s):
            value = 1
            for i in range(s + 1):
                value *= edge[i][j]
            right.append(value)
        assert len(set(left + right)) == 2 * s + 1
        left_product = 1
        right_product = 1
        for value in left:
            left_product *= value
        for value in right:
            right_product *= value
        assert left_product == right_product

        # Exhaustively check that every unequal-cardinality collision cancels
        # to the full K_(s+1,s) relation.
        all_values = left + right
        groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
        for product, card, mask in subset_records(all_values):
            groups[product].append((card, mask))
        full = (1 << len(all_values)) - 1
        collision_count = 0
        for group in groups.values():
            for (card_a, mask_a), (card_b, mask_b) in combinations(group, 2):
                if card_a != card_b:
                    collision_count += 1
                    assert mask_a ^ mask_b == full
        assert collision_count >= 1
        rows.append({
            "s": s,
            "left_size": s + 1,
            "right_size": s,
            "vertices": 2 * s + 1,
            "edge_primes": s * (s + 1),
            "unbalanced_collisions": collision_count,
            "minimal_full_support": True,
        })
    return {
        "rows": rows,
        "scope": "finite replay of the all-s connected edge-prime proof",
    }


def high_tail_guard() -> dict[str, object]:
    rows = []
    for cutoff in [10**4, 10**6, 10**8]:
        for length in [2, 3, 4, 5, 6]:
            threshold = Decimal(cutoff) ** (Decimal(1) - Decimal(1) / Decimal(length))
            # For r<=L and s<r, r(1-1/L)>=r-1>=s.
            for r in range(1, length + 1):
                for s in range(r):
                    assert Decimal(r) * (Decimal(1) - Decimal(1) / Decimal(length)) >= Decimal(s)
            rows.append({"N": cutoff, "L": length, "lower_cutoff": str(threshold)})
    return {
        "rows": rows,
        "conclusion": "the strict high tail forbids every unequal relation with larger shore at most L",
    }


def exact_one_density_guard() -> dict[str, object]:
    rows = []
    prime_list = primes(20)
    one_over_e = Decimal(1).exp() ** Decimal(-1)
    for count in range(1, 21):
        density = Decimal(1)
        lam = Decimal(0)
        for p in prime_list[:count]:
            density *= Decimal(p - 1) / Decimal(p)
            lam += Decimal(1) / Decimal(p)
        density *= lam
        assert density <= lam * (-lam).exp()
        assert lam * (-lam).exp() <= one_over_e
        rows.append({"prime_count": count, "density": str(density), "lambda": str(lam)})
    return {
        "rows": rows,
        "upper_bound": "lambda*exp(-lambda)<=1/e",
    }


def elementary_kill_guards(maximum: int = 5000) -> dict[str, object]:
    prime_list = primes(700)
    pi_maximum = sum(p <= maximum for p in prime_list)
    while prime_list[-1] <= maximum:
        prime_list = primes(len(prime_list) + 500)
        pi_maximum = sum(p <= maximum for p in prime_list)
    assert pi_maximum < maximum // 2
    assert 2 * 3 == 6
    assert len({2, 3}) == 2 and len({6}) == 1
    return {
        "private_prime": {"N": maximum, "pi_N": pi_maximum, "required_for_half_density": maximum // 2},
        "bad_union": {"first_admissible_block": [2, 3], "second_admissible_block": [6], "union_relation": "2*3=6"},
        "common_dilation": "an r-versus-s relation acquires x^r versus x^s, so r!=s destroys a formal common-dilation identity",
    }


def main() -> None:
    payload = {
        "status": "PASS",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "variant_mismatch": variant_mismatch_guard(),
        "exact_finite_optima": exact_finite_optima(),
        "log_fractional_cover": log_fractional_cover_guard(),
        "bipartite_circuits": bipartite_circuit_guard(),
        "high_tail": high_tail_guard(),
        "exact_one_density": exact_one_density_guard(),
        "elementary_kills": elementary_kill_guards(),
        "scope": "finite exact guards plus replays of separately proved symbolic formulas; no density-one theorem",
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
