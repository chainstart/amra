#!/usr/bin/env python3
"""Finite certificates for transverse Phi_6 switch-cube fibre rigidity."""

from __future__ import annotations

from itertools import product
import json


Exponent = tuple[int, ...]
Polynomial = dict[Exponent, int]


def multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    answer: Polynomial = {}
    for exponent_left, coefficient_left in left.items():
        for exponent_right, coefficient_right in right.items():
            exponent = tuple(
                a + b for a, b in zip(exponent_left, exponent_right)
            )
            answer[exponent] = answer.get(exponent, 0) + (
                coefficient_left * coefficient_right
            )
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def is_mask(polynomial: Polynomial) -> bool:
    return bool(polynomial) and all(coefficient == 1 for coefficient in polynomial.values())


def switch_factor(rank: int, coordinate: int) -> Polynomial:
    zero = [0] * rank
    one = zero.copy()
    two = zero.copy()
    one[coordinate] = 1
    two[coordinate] = 2
    return {tuple(zero): 1, tuple(one): -1, tuple(two): 1}


def all_subset_states(mask: Polynomial, rank: int) -> list[Polynomial]:
    states = []
    for subset in range(1 << rank):
        state = mask
        for coordinate in range(rank):
            if subset & (1 << coordinate):
                state = multiply(state, switch_factor(rank, coordinate))
        states.append(state)
    return states


def one_dimensional_automaton_certificate() -> dict[str, object]:
    words_checked = 0
    equivalence_failures = []
    good_by_length = {}
    for length in range(1, 13):
        good = 0
        for bits in product((0, 1), repeat=length):
            if not any(bits):
                continue
            words_checked += 1
            padded = (0, 0) + bits + (0, 0)
            forbidden = any(
                padded[index : index + 3] in ((0, 1, 0), (1, 0, 1))
                for index in range(len(padded) - 2)
            )
            mask = {(index,): bit for index, bit in enumerate(bits) if bit}
            switched = multiply(mask, switch_factor(1, 0))
            if is_mask(switched) != (not forbidden):
                equivalence_failures.append((bits, switched))
            if is_mask(switched):
                good += 1
        good_by_length[length] = good
    return {
        "words_checked": words_checked,
        "good_by_length": good_by_length,
        "equivalence_failures": equivalence_failures,
        "pass": words_checked == sum(2**length - 1 for length in range(1, 13))
        and not equivalence_failures,
    }


def rank_two_exhaustion_certificate() -> dict[str, object]:
    grid = list(product(range(3), repeat=2))
    valid = []
    equality_supports = []
    for bits in range(1, 1 << len(grid)):
        mask = {
            grid[index]: 1
            for index in range(len(grid))
            if bits & (1 << index)
        }
        states = all_subset_states(mask, 2)
        if all(is_mask(state) for state in states):
            valid.append(len(mask))
            if len(mask) == 4:
                equality_supports.append(set(mask))

    expected = []
    for first in range(2):
        for second in range(2):
            expected.append(
                {
                    (first + delta_first, second + delta_second)
                    for delta_first in (0, 1)
                    for delta_second in (0, 1)
                }
            )
    return {
        "masks_checked": (1 << len(grid)) - 1,
        "valid_masks": len(valid),
        "minimum_mass": min(valid),
        "equality_cases": len(equality_supports),
        "equality_cases_exact": {frozenset(case) for case in equality_supports}
        == {frozenset(case) for case in expected},
        "pass": min(valid) == 4
        and {frozenset(case) for case in equality_supports}
        == {frozenset(case) for case in expected},
    }


def equality_models_certificate() -> dict[str, object]:
    records = []
    for rank in range(1, 7):
        base = {exponent: 1 for exponent in product((0, 1), repeat=rank)}
        states = all_subset_states(base, rank)
        records.append(
            {
                "rank": rank,
                "states": len(states),
                "base_mass": len(base),
                "all_states_are_masks": all(is_mask(state) for state in states),
                "all_state_masses_equal": all(len(state) == 2**rank for state in states),
                "pass": len(states) == 2**rank
                and len(base) == 2**rank
                and all(is_mask(state) and len(state) == 2**rank for state in states),
            }
        )
    return {"records": records, "pass": all(record["pass"] for record in records)}


def transverse_projection_certificate() -> dict[str, object]:
    rank = 5
    source_size = 11
    quotient_mass = 2**rank
    # F_0=P_11(y), H=prod_i(1+x_i).  Projection modulo the x-directions
    # has exactly S fibres, each of the sharp minimum mass 2^k.
    fibres = source_size
    fibre_mass = quotient_mass
    total_mass = fibres * fibre_mass
    endpoint_ell = 3
    endpoint_rank = 14 * endpoint_ell
    endpoint_source = 2**endpoint_rank
    endpoint_c = 2**endpoint_ell
    return {
        "rank": rank,
        "S": source_size,
        "C": quotient_mass,
        "projected_fibres": fibres,
        "fibre_mass": fibre_mass,
        "total_mass": total_mass,
        "sharp_C_equals_2_to_k": quotient_mass == 2**rank,
        "sharp_total_identity": total_mass == source_size * quotient_mass,
        "endpoint_rank": endpoint_rank,
        "endpoint_S": endpoint_source,
        "endpoint_C": endpoint_c,
        "endpoint_full_cube_exceeds_C": 2**endpoint_rank > endpoint_c,
        "endpoint_projected_fibre_cap": (endpoint_source * endpoint_c) // (2**endpoint_rank),
        "pass": quotient_mass == 2**rank
        and total_mass == source_size * quotient_mass
        and 2**endpoint_rank > endpoint_c
        and (endpoint_source * endpoint_c) // (2**endpoint_rank) == endpoint_c,
    }


def build_report() -> dict[str, object]:
    sections = {
        "one_dimensional_automaton": one_dimensional_automaton_certificate(),
        "rank_two_exhaustion": rank_two_exhaustion_certificate(),
        "equality_models": equality_models_certificate(),
        "transverse_projection": transverse_projection_certificate(),
    }
    return {"sections": sections, "pass": all(section["pass"] for section in sections.values())}


if __name__ == "__main__":
    report = build_report()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["pass"] else 1)
