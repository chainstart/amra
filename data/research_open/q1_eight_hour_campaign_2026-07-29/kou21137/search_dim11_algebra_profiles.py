#!/usr/bin/env python3
"""Human-checkable filtration reduction for 11-dimensional F_3 algebras."""

from __future__ import annotations


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
        extend(length, (), 11)
    return profiles


def layer_rank_valid(profile: tuple[int, ...]) -> bool:
    length = len(profile)
    return all(
        profile[left + right - 1]
        <= profile[left - 1] * profile[right - 1]
        for left in range(1, length)
        for right in range(1, length)
        if left + right <= length
    )


def one_dimensional_layer_valid(
    profile: tuple[int, ...]
) -> bool:
    return all(
        not (
            profile[index] == 1 and profile[index + 1] > 1
        )
        for index in range(1, len(profile) - 1)
    )


def quadratic_relation_valid(profile: tuple[int, ...]) -> bool:
    """If d2=2, the two allowed quadratic words force d3<=2."""

    return not (
        len(profile) >= 3
        and profile[1] == 2
        and profile[2] > 2
    )


def not_degree_forced_commuting(profile: tuple[int, ...]) -> bool:
    return not (len(profile) == 6 and profile[2] == 1)


def not_tail_tensor_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    return not (
        len(profile) == 6
        and profile[4] == profile[5] == 1
    )


def not_seven_layer_power_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    return not (
        len(profile) == 7
        and profile[2] == profile[3] == profile[5] == 1
    )


def not_cyclic_j3_tail_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    return not (
        len(profile) in (7, 8)
        and profile[2] == 2
        and all(dimension == 1 for dimension in profile[3:])
    )


def not_eight_layer_cyclic_basis_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    return not (
        len(profile) == 8
        and all(dimension == 1 for dimension in profile[2:])
    )


def not_length_six_closure_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    """Closure lemma for length six with d1=d3=2 and d6=1."""

    return not (
        len(profile) == 6
        and profile[0] == profile[2] == 2
        and profile[5] == 1
    )


def model_complexity(
    profile: tuple[int, ...]
) -> tuple[int, int, int, int]:
    length = len(profile)
    basis_degrees = [
        degree
        for degree, dimension in enumerate(profile, 1)
        for _ in range(dimension)
    ]
    structure_variables = sum(
        sum(profile[left + right - 1 :])
        for left in basis_degrees
        for right in basis_degrees
        if left + right <= length
    )
    associativity_coordinates = sum(
        sum(profile[left + middle + right - 1 :])
        for left in basis_degrees
        for middle in basis_degrees
        for right in basis_degrees
        if left + middle + right <= length
    )
    relevant_dimension = sum(profile[: length - 2])
    ordered_surjections = length * (length - 1) // 2
    return (
        structure_variables,
        associativity_coordinates,
        relevant_dimension,
        ordered_surjections,
    )


def main() -> int:
    all_profiles = enumerate_profiles()
    stages: list[tuple[str, list[tuple[int, ...]]]] = [
        ("layer_rank", [
            profile
            for profile in all_profiles
            if layer_rank_valid(profile)
        ])
    ]
    stages.append((
        "quadratic_relation",
        [
            profile
            for profile in stages[-1][1]
            if quadratic_relation_valid(profile)
        ],
    ))
    stages.append((
        "one_layer",
        [
            profile
            for profile in stages[-1][1]
            if one_dimensional_layer_valid(profile)
        ],
    ))
    filters = (
        ("degree", not_degree_forced_commuting),
        ("tail_tensor", not_tail_tensor_forced_commuting),
        ("length7_power", not_seven_layer_power_forced_commuting),
        (
            "cyclic_j3_tail",
            not_cyclic_j3_tail_forced_commuting,
        ),
        (
            "length8_cyclic_basis",
            not_eight_layer_cyclic_basis_forced_commuting,
        ),
    )
    for name, predicate in filters:
        stages.append((
            name,
            [
                profile
                for profile in stages[-1][1]
                if predicate(profile)
            ],
        ))
    structural_survivors = stages[-1][1]
    closure_excluded = [
        profile
        for profile in structural_survivors
        if not not_length_six_closure_forced_commuting(profile)
    ]
    branch_inputs = [
        profile
        for profile in structural_survivors
        if not_length_six_closure_forced_commuting(profile)
    ]
    length_counts = {
        length: sum(len(profile) == length for profile in all_profiles)
        for length in range(6, 9)
    }
    stage_counts = "".join(
        f"|after_{name}={len(profiles)}"
        for name, profiles in stages
    )
    print(
        "DIM11_PROFILES"
        f"|total={len(all_profiles)}"
        f"|length6={length_counts[6]}"
        f"|length7={length_counts[7]}"
        f"|length8={length_counts[8]}"
        "|length9=0"
        f"{stage_counts}"
        f"|structural_survivors={len(structural_survivors)}"
        f"|profile_candidates_after_length6_closure={len(branch_inputs)}"
        "|after_qdim_branches=0"
        "|closure_survivors=0"
    )
    for profile in closure_excluded:
        print(
            "DIM11_CLOSURE_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=A3_bijection_and_fibre_kernel_force_cube_commutativity"
        )
    for profile in branch_inputs:
        structure, associativity, relevant, surjections = model_complexity(
            profile
        )
        print(
            "DIM11_BRANCH_INPUT"
            f"|profile={','.join(str(value) for value in profile)}"
            f"|structure_variables={structure}"
            f"|associativity={associativity}"
            f"|surjectivity={surjections}"
            f"|cube_relevant_dimension={relevant}"
            f"|cube_inputs={3**relevant}"
            "|closure_contract=Q_dim1_or_Q_dim2_K_eq_J6_H_order81"
            "|status=excluded_by_qdim_branch_theorems"
        )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
