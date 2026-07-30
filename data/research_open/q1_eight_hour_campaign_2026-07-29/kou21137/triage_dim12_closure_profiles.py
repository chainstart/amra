#!/usr/bin/env python3
"""Machine-readable ledger for the proved dim-12 closure triage.

The mathematical proofs are in DIM12_CLOSURE_TRIAGE.md.  This script
only guards the exact profile/status bookkeeping.
"""

from __future__ import annotations

from search_dim12_next_frontier import enumerate_profiles
from search_dim11_algebra_profiles import (
    layer_rank_valid,
    not_cyclic_j3_tail_forced_commuting,
    not_degree_forced_commuting,
    not_eight_layer_cyclic_basis_forced_commuting,
    not_length_six_closure_forced_commuting,
    not_seven_layer_power_forced_commuting,
    not_tail_tensor_forced_commuting,
    one_dimensional_layer_valid,
    quadratic_relation_valid,
)


STATUSES = {
    (2, 2, 2, 2, 2, 2): "excluded_generalized_length6_fibre_lemma",
    (3, 2, 2, 2, 2, 1): "Q2_nonzero_projective_cube_zero_required",
    (2, 2, 2, 2, 2, 1, 1): "excluded_cross_relation_commutator",
    (2, 2, 2, 3, 1, 1, 1): "excluded_qbijective_d4_bound",
    (2, 3, 2, 2, 1, 1, 1): "Q2_KJ6_P_surjective",
    (2, 3, 3, 1, 1, 1, 1): "Q2_plane_KJ6_P_surjective",
    (3, 2, 2, 2, 1, 1, 1): "Q2_zero_set_or_KJ6_branch",
    (2, 2, 2, 2, 1, 1, 1, 1): "Q1_or_Q2_central_J8_commutator",
}


def frontier() -> list[tuple[int, ...]]:
    predicates = (
        layer_rank_valid,
        quadratic_relation_valid,
        one_dimensional_layer_valid,
        not_degree_forced_commuting,
        not_tail_tensor_forced_commuting,
        not_seven_layer_power_forced_commuting,
        not_cyclic_j3_tail_forced_commuting,
        not_eight_layer_cyclic_basis_forced_commuting,
        not_length_six_closure_forced_commuting,
    )
    profiles = enumerate_profiles()
    for predicate in predicates:
        profiles = [profile for profile in profiles if predicate(profile)]
    return profiles


def main() -> int:
    profiles = frontier()
    assert set(profiles) == set(STATUSES)
    proved_excluded = sum(
        STATUSES[profile].startswith("excluded_")
        for profile in profiles
    )
    finite_audit_excluded = sum(
        STATUSES[profile] == "excluded_qbijective_d4_bound"
        for profile in profiles
    )
    human_excluded = proved_excluded - finite_audit_excluded
    print(
        "DIM12_CLOSURE_TRIAGE"
        f"|frontier_inputs={len(profiles)}"
        f"|proved_excluded={proved_excluded}"
        f"|human_excluded={human_excluded}"
        f"|finite_audit_excluded={finite_audit_excluded}"
        f"|branch_contracts={len(profiles) - proved_excluded}"
        "|existence_certificates=0"
        "|status=necessary_conditions_only"
    )
    for profile in profiles:
        print(
            "DIM12_TRIAGE_CASE"
            f"|profile={','.join(map(str, profile))}"
            f"|result={STATUSES[profile]}"
        )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
