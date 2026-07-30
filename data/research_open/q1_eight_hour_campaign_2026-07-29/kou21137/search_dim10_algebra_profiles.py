#!/usr/bin/env python3
"""Human-checkable filtration reduction for 10-dimensional F_3 algebras."""

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

    # Exponent nine requires J^9=0, so A_9 cannot be nonzero.
    for length in range(6, 9):
        extend(length, (), 10)
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


def third_layer_valid(profile: tuple[int, ...]) -> bool:
    return not (profile[1] == 1 and profile[2] > 1)


def not_degree_forced_commuting(profile: tuple[int, ...]) -> bool:
    return not (len(profile) == 6 and profile[2] == 1)


def not_tail_tensor_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    """Apply the A5,A6 one-dimensional sixfold-tensor lemma."""

    return not (
        len(profile) == 6
        and profile[4] == profile[5] == 1
    )


def one_dimensional_layer_valid(
    profile: tuple[int, ...]
) -> bool:
    """For i>=2, a one-dimensional A_i forces A_{i+1} to be a line."""

    return all(
        not (
            profile[index] == 1 and profile[index + 1] > 1
        )
        for index in range(1, len(profile) - 1)
    )


def not_seven_layer_power_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    """Apply Lemma 1: J^8=0 and A3,A4,A6 one-dimensional."""

    return not (
        len(profile) == 7
        and profile[2] == profile[3] == profile[5] == 1
    )


def not_seven_layer_cyclic_j3_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    """Apply the cyclic J3 lemma when A4,...,A7 are lines."""

    return not (
        len(profile) == 7
        and all(dimension == 1 for dimension in profile[3:])
    )


def not_eight_layer_cyclic_cube_forced_commuting(
    profile: tuple[int, ...]
) -> bool:
    """Apply the cyclic-basis lemma when A3,...,A8 are lines."""

    return not (
        len(profile) == 8
        and all(dimension == 1 for dimension in profile[2:])
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
    rank_profiles = [
        profile for profile in all_profiles if layer_rank_valid(profile)
    ]
    third_profiles = [
        profile for profile in rank_profiles if third_layer_valid(profile)
    ]
    degree_profiles = [
        profile
        for profile in third_profiles
        if not_degree_forced_commuting(profile)
    ]
    one_layer_excluded = [
        profile
        for profile in degree_profiles
        if not one_dimensional_layer_valid(profile)
    ]
    one_layer_profiles = [
        profile
        for profile in degree_profiles
        if one_dimensional_layer_valid(profile)
    ]
    tail_tensor_excluded = [
        profile
        for profile in one_layer_profiles
        if not not_tail_tensor_forced_commuting(profile)
    ]
    tail_profiles = [
        profile
        for profile in one_layer_profiles
        if not_tail_tensor_forced_commuting(profile)
    ]
    seven_layer_excluded = [
        profile
        for profile in tail_profiles
        if not not_seven_layer_power_forced_commuting(profile)
    ]
    seven_layer_profiles = [
        profile
        for profile in tail_profiles
        if not_seven_layer_power_forced_commuting(profile)
    ]
    cyclic_j3_excluded = [
        profile
        for profile in seven_layer_profiles
        if not not_seven_layer_cyclic_j3_forced_commuting(profile)
    ]
    cyclic_j3_profiles = [
        profile
        for profile in seven_layer_profiles
        if not_seven_layer_cyclic_j3_forced_commuting(profile)
    ]
    eight_layer_excluded = [
        profile
        for profile in cyclic_j3_profiles
        if not not_eight_layer_cyclic_cube_forced_commuting(profile)
    ]
    survivors = [
        profile
        for profile in cyclic_j3_profiles
        if not_eight_layer_cyclic_cube_forced_commuting(profile)
    ]
    print(
        "DIM10_PROFILES"
        f"|total={len(all_profiles)}"
        "|length6=56|length7=28|length8=8|length9=0"
        f"|after_layer_rank={len(rank_profiles)}"
        f"|after_d2_d3={len(third_profiles)}"
        f"|after_degree={len(degree_profiles)}"
        f"|after_one_layer={len(one_layer_profiles)}"
        f"|after_tail_tensor={len(tail_profiles)}"
        f"|after_length7_power={len(seven_layer_profiles)}"
        f"|after_length7_cyclic_j3={len(cyclic_j3_profiles)}"
        f"|after_length8_cyclic_tail={len(survivors)}"
        f"|survivors={len(survivors)}"
    )
    for profile in one_layer_excluded:
        print(
            "DIM10_ONE_LAYER_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=di_one_forces_di1_at_most_one"
        )
    for profile in tail_tensor_excluded:
        print(
            "DIM10_TAIL_TENSOR_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=J7_zero_and_d5_d6_one"
        )
    for profile in seven_layer_excluded:
        print(
            "DIM10_LENGTH7_POWER_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=J8_zero_and_d3_d4_d6_one"
        )
    for profile in cyclic_j3_excluded:
        print(
            "DIM10_LENGTH7_CYCLIC_J3_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=J8_zero_and_d4_through_d7_one"
        )
    for profile in eight_layer_excluded:
        print(
            "DIM10_LENGTH8_CYCLIC_TAIL_EXCLUDED"
            f"|profile={','.join(str(value) for value in profile)}"
            "|reason=J9_zero_and_d3_through_d8_one"
        )
    for profile in survivors:
        structure, associativity, relevant, surjections = model_complexity(
            profile
        )
        print(
            "DIM10_SURVIVOR"
            f"|profile={','.join(str(value) for value in profile)}"
            f"|structure_variables={structure}"
            f"|associativity={associativity}"
            f"|surjectivity={surjections}"
            f"|cube_relevant_dimension={relevant}"
            f"|cube_inputs={3**relevant}"
        )
    print("DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
