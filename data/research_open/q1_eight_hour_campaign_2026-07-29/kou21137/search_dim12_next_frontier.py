#!/usr/bin/env python3
"""Necessary profile frontier for 12-dimensional F_3 algebras.

This applies only the already proved profile filters.  The output cases
are inputs to future closure-branch analysis, not realizability claims.
"""

from __future__ import annotations

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


def enumerate_profiles() -> list[tuple[int, ...]]:
    profiles: list[tuple[int, ...]] = []

    def extend(
        length: int, prefix: tuple[int, ...], remaining: int
    ) -> None:
        if len(prefix) == length:
            if remaining == 0:
                profiles.append(prefix)
            return
        minimum = 2 if not prefix else 1
        later_minimum = length - len(prefix) - 1
        for value in range(minimum, remaining - later_minimum + 1):
            extend(length, prefix + (value,), remaining - value)

    for length in range(6, 9):
        extend(length, (), 12)
    return profiles


def main() -> int:
    all_profiles = enumerate_profiles()
    stages: list[tuple[str, list[tuple[int, ...]]]] = []

    def append_stage(name: str, predicate) -> None:
        source = all_profiles if not stages else stages[-1][1]
        stages.append((
            name,
            [profile for profile in source if predicate(profile)],
        ))

    append_stage("layer_rank", layer_rank_valid)
    append_stage("quadratic_relation", quadratic_relation_valid)
    append_stage("one_layer", one_dimensional_layer_valid)
    append_stage("degree", not_degree_forced_commuting)
    append_stage("tail_tensor", not_tail_tensor_forced_commuting)
    append_stage("length7_power", not_seven_layer_power_forced_commuting)
    append_stage("cyclic_j3_tail", not_cyclic_j3_tail_forced_commuting)
    append_stage(
        "length8_cyclic_basis",
        not_eight_layer_cyclic_basis_forced_commuting,
    )
    append_stage(
        "length6_closure",
        not_length_six_closure_forced_commuting,
    )

    frontier = stages[-1][1]
    expected_frontier = [
        (2, 2, 2, 2, 2, 2),
        (3, 2, 2, 2, 2, 1),
        (2, 2, 2, 2, 2, 1, 1),
        (2, 2, 2, 3, 1, 1, 1),
        (2, 3, 2, 2, 1, 1, 1),
        (2, 3, 3, 1, 1, 1, 1),
        (3, 2, 2, 2, 1, 1, 1),
        (2, 2, 2, 2, 1, 1, 1, 1),
    ]
    assert frontier == expected_frontier

    length_counts = {
        length: sum(len(profile) == length for profile in all_profiles)
        for length in range(6, 9)
    }
    stage_counts = "".join(
        f"|after_{name}={len(profiles)}"
        for name, profiles in stages
    )
    print(
        "DIM12_PROFILE_FRONTIER"
        f"|total={len(all_profiles)}"
        f"|length6={length_counts[6]}"
        f"|length7={length_counts[7]}"
        f"|length8={length_counts[8]}"
        "|length9=0"
        f"{stage_counts}"
        f"|profile_candidates={len(frontier)}"
        "|status=necessary_profiles_only"
    )
    for profile in frontier:
        print(
            "DIM12_BRANCH_INPUT"
            f"|profile={','.join(map(str, profile))}"
            "|status=requires_new_closure_branch_analysis"
        )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
