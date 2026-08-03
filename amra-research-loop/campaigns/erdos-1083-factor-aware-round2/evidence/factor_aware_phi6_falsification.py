#!/usr/bin/env python3
"""Exact Phi6 and exponent ledgers shared by round-two kill tests."""

from itertools import combinations
from math import comb, log2
import json


def degree_one_fingerprint(d, chosen):
    # (augmentation, y moment, labelled x moments)
    return (2, 1, *(2 if index in chosen else 0 for index in range(d)))


def main():
    rows = []
    for d in range(4, 17):
        k = d // 2
        subsets = tuple(frozenset(item) for item in combinations(range(d), k))
        K = len(subsets)
        fingerprints = {degree_one_fingerprint(d, item) for item in subsets}
        assert len(fingerprints) == K
        factor_degrees = [sum(index in item for item in subsets) for index in range(d)]
        assert set(factor_degrees) == {comb(d - 1, k - 1)}
        # Distinct equal-size subsets have nonzero even symmetric difference,
        # hence distance at least two; replacing one element attains two.
        witness_left = frozenset(range(k))
        witness_right = frozenset((*range(k - 1), k))
        assert len(witness_left ^ witness_right) == 2
        union_atoms = 2 * sum(comb(d, s) * 2**s for s in range(k + 1))
        B_support = 2 * 3**d
        one_row_support = 2 * 3**k
        displayed_circuit_factors = d + 1
        rows.append({
            "d": d,
            "k": k,
            "K": K,
            "degree_one_fingerprints": len(fingerprints),
            "each_factor_row_degree": factor_degrees[0],
            "minimum_omission_code_distance": 2,
            "one_row_support": one_row_support,
            "union_support": union_atoms,
            "B_support": B_support,
            "displayed_product_circuit_factors": displayed_circuit_factors,
        })

    asymptotic = []
    for d in (32, 64, 128, 256):
        k = d // 2
        K = comb(d, k)
        log_t = (9 / 5) * log2(K)  # K=t^(5/9)
        asymptotic.append({
            "d": d,
            "row_hub_exponent": log2(K) / log_t,
            "one_row_expanded_support_exponent": log2(2 * 3**k) / log_t,
            "common_B_expanded_support_exponent": log2(2 * 3**d) / log_t,
            "factor_count_exponent": log2(d + 1) / log_t,
            "warning": "none of these algebraic exponents is an actual Euclidean distance-label exponent",
        })

    print(json.dumps({
        "schema": "amra.erdos1083.factor-aware-phi6-falsification.v1",
        "finite_exact": rows,
        "normalized_exponent_ledgers": asymptotic,
        "exact_facts": {
            "actual_Q_A_separated_at_degree_one": True,
            "middle_layer_has_exponentially_many_rows": True,
            "factor_row_incidence_is_regular_and_expanding": True,
            "expanded_support_is_exponential_but_product_circuit_has_d_plus_1_factors": True,
            "phi6_supplies_common_X_scalar_copy": False,
            "phi6_supplies_paired_actual_euclidean_masks": False,
            "phi6_supplies_distance_labels_or_R3_realization": False,
        },
        "result": "pass",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
