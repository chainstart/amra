#!/usr/bin/env python3
"""Exact aggregate and occurrence-refined unit-incidence comparison."""

from fractions import Fraction
from itertools import combinations
import json


def rank(matrix):
    work = [[Fraction(x) for x in row] for row in matrix]
    pivot = 0
    for column in range(len(work[0])):
        selected = next((i for i in range(pivot, len(work)) if work[i][column]), None)
        if selected is None:
            continue
        work[pivot], work[selected] = work[selected], work[pivot]
        scale = work[pivot][column]
        work[pivot] = [x / scale for x in work[pivot]]
        for i in range(len(work)):
            if i != pivot and work[i][column]:
                scale = work[i][column]
                work[i] = [x - scale*y for x, y in zip(work[i], work[pivot])]
        pivot += 1
    return pivot


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1)**j * value * determinant([
            row[:j] + row[j + 1:] for row in matrix[1:]
        ])
        for j, value in enumerate(matrix[0])
    )


def unit_minor(matrix, target_rank):
    for rows in combinations(range(len(matrix)), target_rank):
        for columns in combinations(range(len(matrix[0])), target_rank):
            square = [[matrix[i][j] for j in columns] for i in rows]
            value = determinant(square)
            if abs(value) == 1:
                return {"rows": rows, "columns": columns, "determinant": value}
    raise AssertionError("no unit maximal minor")


def apply(matrix, vector):
    return tuple(sum(a*b for a, b in zip(row, vector)) for row in matrix)


# Minimal actual centre-leaf block, with columns (g,f,b,r,q).  Rows are read
# directly from Fj=G Rj, F0, PAj=F0 Qj, PA0=G B, and B=Rj Qj.
aggregate_variables = ("g", "f", "b", "r", "q")
actual_rows = {
    "unit(Fj)=unit(G)+unit(Rj)": [1, 0, 0, 1, 0],
    "unit(F0)": [0, 1, 0, 0, 0],
    "unit(PAj)=unit(F0)+unit(Qj)": [0, 1, 0, 0, 1],
    "unit(PA0)=unit(G)+unit(B)": [1, 0, 1, 0, 0],
    "unit(B)-unit(Rj)-unit(Qj)=0": [0, 0, 1, -1, -1],
}
aggregate = list(actual_rows.values())
formal_m1 = [
    [1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [1, 0, 1, 0, 0],
    [0, 0, 1, -1, -1],
]
assert aggregate == formal_m1
assert rank(aggregate) == 4
minor = unit_minor(aggregate, 4)
gauge = (1, 0, -1, -1, 0)
assert apply(aggregate, gauge) == (0,)*5

# The identity row equals PA0+F0-Fj-PAj, including its right side.  The right
# side equality is the common-spectrum identity PA0*F0=PAj*Fj.
dependency = tuple(
    aggregate[3][i] + aggregate[1][i] - aggregate[0][i] - aggregate[2][i]
    for i in range(5)
)
assert dependency == tuple(aggregate[4])

source_identity = [aggregate[i] for i in (0, 1, 4)]
assert rank(source_identity) == 3
spectrum_shift = (0, 0, 1, 0, 1)
assert apply(source_identity, spectrum_shift) == (0,)*3
assert apply(aggregate, spectrum_shift) != (0,)*5

# Actual right sides are arbitrary exponent vectors phi_j,phi_0,alpha_j,
# alpha_0 subject only to alpha_0+phi_0=phi_j+alpha_j.  The special scalar
# multiples in the old finite example are one choice, not an algebraic
# consequence of common X.
generic_rhs_symbols = ("phi_j", "phi_0", "alpha_j", "alpha_0", "0")
generic_rhs_relation = "alpha_0+phi_0-phi_j-alpha_j=0"

# Occurrence-refined one-leaf model.  Let B have k normalized irreducible
# occurrences h_i, with R using the first split of them and Q the remainder.
# Columns are (g,f,h_1,...,h_k); product rows are Fj,F0,PAj,PA0.
refinement_rows = []
for k in range(2, 9):
    split = max(1, k // 2)
    source = [1, 0] + [1 if i < split else 0 for i in range(k)]
    fixed_f = [0, 1] + [0]*k
    complement = [0, 1] + [0 if i < split else 1 for i in range(k)]
    common = [1, 0] + [1]*k
    matrix = [source, fixed_f, complement, common]
    matrix_rank = rank(matrix)
    assert matrix_rank == 3

    # Aggregate projection h -> (b=sum_all, r=sum_R, q=sum_Q) has kernel
    # dimension (split-1)+(k-split-1)=k-2.  Every such direction annihilates
    # all product rows: it is internal associate-normalization gauge.
    internal_kernel_dimension = k - 2
    total_kernel_dimension = (k + 2) - matrix_rank
    assert total_kernel_dimension == k - 1
    assert total_kernel_dimension == internal_kernel_dimension + 1
    refinement_rows.append({
        "factor_occurrences": k,
        "R_occurrences": split,
        "Q_occurrences": k - split,
        "variables": k + 2,
        "product_row_rank": matrix_rank,
        "total_kernel_dimension": total_kernel_dimension,
        "aggregate_projection_internal_kernel_dimension": internal_kernel_dimension,
        "remaining_aggregate_gauge_dimension": 1,
    })

print(json.dumps({
    "schema": "amra.erdos1083.unit-matrix-round7.actual-realization.v1",
    "minimal_actual_block": {
        "source": "POWER_LARGE_SIMULTANEOUS_SWITCH_CORE.md equations (0.3), restricted to centre row 0 and one leaf j",
        "ambient_ring": "Z[Gamma], Gamma finitely generated torsion-free",
        "paired_positive_products": ["PA0=G*Rj*Qj", "PAj=F0*Qj"],
        "aggregate_variables": aggregate_variables,
        "actual_rows": actual_rows,
        "formal_m1_rows_match_exactly": True,
        "rank": 4,
        "primitive_minor": minor,
        "kernel": [gauge],
    },
    "row_typing": {
        "absolute_product_observables": ["unit(Fj)", "unit(F0)", "unit(PAj)", "unit(PA0)"],
        "algebraic_identity": "unit(B)-unit(Rj)-unit(Qj)=0",
        "identity_dependency": "row(PA0)+row(F0)-row(Fj)-row(PAj)",
        "generic_actual_right_sides": generic_rhs_symbols,
        "only_automatic_rhs_relation": generic_rhs_relation,
        "special_scalar_multiple_rhs_forced_by_common_X": False,
    },
    "source_identity_subsystem": {
        "rank": 3,
        "kernel_dimension": 2,
        "gauge": gauge,
        "spectrum_shift": spectrum_shift,
    },
    "ambient_lattice": {
        "Gamma": "Z^r because it is finitely generated torsion-free",
        "full_exponent_kernel": "Gamma times the primitive aggregate gauge, coordinatewise",
        "extra_observable_kernel_from_tensoring": False,
        "signs": "fixed after choosing all aggregate representatives with positive nonzero augmentation",
    },
    "factor_occurrence_refinement": refinement_rows,
    "interpretation": {
        "aggregate_realization": "proved for the actual normal-form identities once their four absolute product units are treated as observed right sides",
        "raw_occurrence_completeness": "false without canonical associate normalization; k occurrences add k-2 internal projection-kernel directions in the one-leaf refinement",
        "extra_raw_directions_are_geometric": False,
        "power_large_joint_absolute_profile_fixed_at_subpower_cost": False,
    },
    "public_exponent_changed": False,
    "lean_used": False,
}, indent=2, sort_keys=True))
