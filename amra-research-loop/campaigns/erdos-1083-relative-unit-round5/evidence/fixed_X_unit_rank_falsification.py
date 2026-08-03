#!/usr/bin/env python3
"""Exact fixed-common-X Laurent-unit rank and gauge falsification."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
import hashlib
import json
from pathlib import Path


VARIABLES = ("g", "f", "b", "r1", "r3", "q1", "q3")


def rank(matrix: list[list[Fraction]]) -> int:
    rows = [row[:] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((r for r in range(pivot_row, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for r in range(len(rows)):
            if r != pivot_row and rows[r][column]:
                factor = rows[r][column]
                rows[r] = [x - factor * y for x, y in zip(rows[r], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    total = 0
    if n == 1:
        return matrix[0][0]
    for column, value in enumerate(matrix[0]):
        minor = [row[:column] + row[column + 1 :] for row in matrix[1:]]
        total += (-1) ** column * value * determinant(minor)
    return total


def primitive_rank_minor(matrix: list[list[int]], target_rank: int) -> dict[str, object]:
    for selected_rows in combinations(range(len(matrix)), target_rank):
        for selected_columns in combinations(range(len(matrix[0])), target_rank):
            square = [[matrix[r][c] for c in selected_columns] for r in selected_rows]
            det = determinant(square)
            if abs(det) == 1:
                return {"rows": selected_rows, "columns": selected_columns, "determinant": det}
    raise AssertionError("no primitive full-rank minor")


def apply(matrix: list[list[int]], vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(sum(Fraction(a) * b for a, b in zip(row, vector)) for row in matrix)


def squarefree(value: Fraction) -> tuple[Fraction, int]:
    combined = value.numerator * value.denominator
    square = 1
    free = 1
    divisor = 2
    while divisor * divisor <= combined:
        exponent = 0
        while combined % divisor == 0:
            combined //= divisor
            exponent += 1
        square *= divisor ** (exponent // 2)
        if exponent % 2:
            free *= divisor
        divisor += 1
    if combined > 1:
        free *= combined
    return Fraction(square, value.denominator), free


def label(first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]) -> tuple[str, str, int]:
    tau, z = first
    sigma, w = second
    rational = tau + sigma + (z - w) ** 2
    coefficient, radicand = squarefree(tau * sigma)
    radical = -2 * coefficient
    if radicand == 1:
        rational += radical
        radical = Fraction()
    return str(rational), str(radical), radicand


def fixed_geometry(
    common_start: Fraction = Fraction(), common_spectrum_shift: Fraction = Fraction()
) -> dict[str, object]:
    starts = {
        1: (0, 2, 4, 6, 8, 10),
        2: (0, 1, 4, 5, 8, 9),
        3: (0, 1, 2, 6, 7, 8),
    }
    source = (common_start, common_start + 1)
    targets = []
    row_spectra = {}
    for scalar, positions in starts.items():
        z = Fraction(scalar, 2)
        distances = []
        for position in positions:
            tau = Fraction(100 + position) + common_spectrum_shift - scalar * common_start - (1 + z * z)
            assert tau > 0
            targets.append((tau, z))
            distances.extend(tau + 1 + z * z + scalar * x for x in source)
        assert sorted(distances) == [Fraction(i) + common_spectrum_shift for i in range(100, 112)]
        row_spectra[str(scalar)] = [str(item) for item in sorted(distances)]
    labels = {label(left, right) for left, right in combinations(targets, 2)}
    return {
        "common_X": [str(item) for item in source],
        "common_spectrum_shift": str(common_spectrum_shift),
        "target_count": len(targets),
        "row_spectra": row_spectra,
        "distinct_target_target_labels": len(labels),
        "collision_profile_hash": hashlib.sha256(repr(sorted(labels)).encode()).hexdigest(),
    }


def additive_quadruples(values: tuple[int, ...]) -> int:
    sums: dict[int, int] = {}
    for left in values:
        for right in values:
            sums[left + right] = sums.get(left + right, 0) + 1
    return sum(count * count for count in sums.values())


def main() -> None:
    # Rows encode, in order:
    # g+r1=a, f=2a, g+r3=3a,
    # f+q1=-a, g+b=-2a, f+q3=-3a,
    # b-r1-q1=0, b-r3-q3=0.
    matrix = [
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, -1, 0, -1, 0],
        [0, 0, 1, 0, -1, 0, -1],
    ]
    matrix_q = [[Fraction(item) for item in row] for row in matrix]
    matrix_rank = rank(matrix_q)
    assert matrix_rank == 6
    primitive_minor = primitive_rank_minor(matrix, matrix_rank)

    gauge = (Fraction(1), Fraction(0), Fraction(-1), Fraction(-1), Fraction(-1), Fraction(0), Fraction(0))
    assert apply(matrix, gauge) == (Fraction(0),) * 8

    # If only common X and factor identities are fixed, but the absolute
    # complement spectrum is not fixed, the relevant subsystem has rank five.
    # Its second kernel direction is a genuine common spectrum translation.
    source_identity_rows = (0, 1, 2, 6, 7)
    source_identity_matrix = [matrix[index] for index in source_identity_rows]
    assert rank([[Fraction(item) for item in row] for row in source_identity_matrix]) == 5
    spectrum_shift = (Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(1), Fraction(1))
    assert apply(source_identity_matrix, spectrum_shift) == (Fraction(0),) * 5
    assert apply(observable_matrix := matrix[3:6], spectrum_shift) == (Fraction(1),) * 3

    def particular(a: Fraction) -> tuple[Fraction, ...]:
        return (a, 2 * a, -3 * a, Fraction(), 2 * a, -3 * a, -5 * a)

    def right_side(a: Fraction) -> tuple[Fraction, ...]:
        return (a, 2 * a, 3 * a, -a, -2 * a, -3 * a, Fraction(), Fraction())

    for a in (Fraction(), Fraction(-1, 4), Fraction(2, 3)):
        assert apply(matrix, particular(a)) == right_side(a)
        for delta in (Fraction(-7, 3), Fraction(), Fraction(11, 5)):
            candidate = tuple(x + delta * y for x, y in zip(particular(a), gauge))
            assert apply(matrix, candidate) == right_side(a)

    # All six geometry-bearing products annihilate gauge.
    all_product_matrix = matrix[:6]
    assert apply(all_product_matrix, gauge) == (Fraction(0),) * 6

    # At fixed X={0,1}, arbitrarily many integer gauge representatives are
    # exact solutions. The actual target construction depends only on the six
    # observables and is therefore literally identical for every delta.
    geometry = fixed_geometry(Fraction(), Fraction())
    assert geometry["distinct_target_target_labels"] == 127
    shifted_geometry = fixed_geometry(Fraction(), Fraction(1, 4))
    assert shifted_geometry["distinct_target_target_labels"] == 127
    assert shifted_geometry["collision_profile_hash"] != geometry["collision_profile_hash"]
    gauge_samples = []
    for delta in range(-32, 33):
        units = tuple(Fraction(delta) * value for value in gauge)
        assert apply(matrix, units) == right_side(Fraction())
        gauge_samples.append({name: str(value) for name, value in zip(VARIABLES, units)})

    progression = tuple(range(-32, 33))
    additive_energy = additive_quadruples(progression)
    assert additive_energy > len(progression) ** 3 // 2

    payload = {
        "schema": "amra.erdos1083.relative_unit_round5.fixed_X_rank.v1",
        "unit_variables": VARIABLES,
        "constraint_matrix": matrix,
        "matrix_rank": matrix_rank,
        "raw_kernel_rank": len(VARIABLES) - matrix_rank,
        "primitive_full_rank_minor": primitive_minor,
        "torsion_in_observable_quotient_for_exact_block": "none (primitive rank minor)",
        "gauge_generator": [str(item) for item in gauge],
        "fixed_X_normalized_only_system": {
            "matrix_rank": 5,
            "kernel_rank": 2,
            "kernel_basis": [[str(item) for item in gauge], [str(item) for item in spectrum_shift]],
            "observable_spectrum_shift_generator": [str(item) for item in spectrum_shift],
            "complement_product_shift": ["1", "1", "1"],
            "meaning": "At fixed X, this direction preserves normalized quotients and factor identities but translates every absolute row spectrum together."
        },
        "general_solution": "(a,2a,-3a,0,2a,-3a,-5a)+delta*(1,0,-1,-1,-1,0,0)",
        "gauge_fixed_slice": "u(G)=a forces delta=0 and gives one representative",
        "observable_product_units": ["u(GR1)", "u(F0)", "u(GR3)", "u(F0Q1)", "u(GB)", "u(F0Q3)"],
        "observable_quotient_rank_for_exact_block": 0,
        "observable_quotient_rank_before_fixing_absolute_spectrum": 1,
        "fixed_X_adversary_search": {
            "common_X": ["0", "1"],
            "gauge_representatives_checked": len(gauge_samples),
            "delta_interval": [-32, 32],
            "all_normalized_data_equal": True,
            "all_source_complement_units_equal": True,
            "different_distance_label_profiles_found": False,
            "different_absolute_distance_label_sets_found_before_spectrum_fixing": True,
            "collision_label_counts_for_shifts_0_and_1_4": [127, 127],
            "completeness_scope": "With fixed X and normalized data alone there is one observable common-spectrum translation plus gauge. Fixing the absolute 12-label row spectrum removes that observable direction, leaving only gauge.",
        },
        "fixed_geometry": geometry,
        "shifted_fixed_X_geometry": shifted_geometry,
        "raw_unit_progression": {
            "size": len(progression),
            "ordered_additive_quadruples": additive_energy,
            "observable_profiles": 1,
            "target_collision_profiles": 1,
        },
        "tests": {
            "M1083U5-01": {"outcome": "killed", "reason": "the raw character selecting u(G) is nonconstant on gauge while all geometry is constant"},
            "M1083U5-02": {"outcome": "killed", "reason": "fixed X and normalized data admit infinitely many rational and integer gauge representatives"},
            "M1083U5-03": {"outcome": "killed", "reason": "individual factor valuations are unbounded along gauge while every product support is fixed"},
            "M1083U5-04": {"outcome": "killed", "reason": "nonzero gauge displacement crosses no observable Newton or target wall"},
            "M1083U5-05": {"outcome": "killed", "reason": "unboundedly many unit representatives give one exact target collision profile"},
            "M1083U5-06": {"outcome": "killed", "reason": "a long gauge arithmetic progression has high raw additive energy with constant collision geometry"},
            "M1083U5-07": {"outcome": "survived", "reason": "exact block has kernel rank one, primitive quotient and a unique u(G)=a gauge slice"},
            "M1083U5-08": {"outcome": "killed", "reason": "before fixing the absolute row spectrum, the exact fixed-X normalized-data quotient has one genuine observable translation direction"},
            "M1083U5-09": {"outcome": "killed", "reason": "raw conditional entropy grows on bounded gauge samples while observable entropy and labels remain zero/constant"},
            "M1083U5-10": {"outcome": "killed", "reason": "arbitrarily many gauge representatives occupy one target-order and collision chamber"}
        },
        "public_exponent_changed": False,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    output = Path(__file__).with_suffix(".json")
    output.write_bytes(encoded)
    print(json.dumps(payload, indent=2, sort_keys=True))
    print("output_sha256", hashlib.sha256(encoded).hexdigest())


if __name__ == "__main__":
    main()
