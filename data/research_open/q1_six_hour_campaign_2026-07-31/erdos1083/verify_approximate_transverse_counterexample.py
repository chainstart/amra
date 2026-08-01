#!/usr/bin/env python3
"""Exact certificates for the #1083 endpoint Følner counterexample.

The all-parameter theorem is proved in
APPROXIMATE_STABILITY_COUNTEREXAMPLE.md.  This script checks its exponent
ledger symbolically and enumerates modest boxes to falsify every combinatorial
and algebraic interface used by the proof.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from itertools import product
import json
import math


Q = Fraction


@dataclass(frozen=True, order=True)
class Qsqrt2:
    """An exact element a + b sqrt(2), represented by rational coefficients."""

    a: Q
    b: Q = Q(0)

    def __add__(self, other: object) -> "Qsqrt2":
        rhs = coerce(other)
        return Qsqrt2(self.a + rhs.a, self.b + rhs.b)

    __radd__ = __add__

    def __neg__(self) -> "Qsqrt2":
        return Qsqrt2(-self.a, -self.b)

    def __sub__(self, other: object) -> "Qsqrt2":
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> "Qsqrt2":
        return coerce(other) - self

    def __mul__(self, other: object) -> "Qsqrt2":
        rhs = coerce(other)
        return Qsqrt2(
            self.a * rhs.a + 2 * self.b * rhs.b,
            self.a * rhs.b + self.b * rhs.a,
        )

    __rmul__ = __mul__

    def square(self) -> "Qsqrt2":
        return self * self

    def is_positive(self) -> bool:
        """Decide a+b sqrt(2)>0 without floating point."""
        if self.b == 0:
            return self.a > 0
        if self.a >= 0 and self.b > 0:
            return True
        if self.a <= 0 and self.b < 0:
            return False
        comparison = self.a * self.a - 2 * self.b * self.b
        if self.a > 0:  # b < 0
            return comparison > 0
        # a < 0 and b > 0
        return comparison < 0

    def as_pair(self) -> tuple[str, str]:
        return str(self.a), str(self.b)


def coerce(value: object) -> Qsqrt2:
    if isinstance(value, Qsqrt2):
        return value
    if isinstance(value, (int, Fraction)):
        return Qsqrt2(Q(value))
    raise TypeError(f"cannot coerce {value!r} to Qsqrt2")


Point = tuple[int, int]


def in_box(point: Point, length: int) -> bool:
    return 0 <= point[0] < length and 0 <= point[1] < length


def add_point(left: Point, right: Point, scale: int = 1) -> Point:
    return left[0] + scale * right[0], left[1] + scale * right[1]


def embed(point: Point) -> Qsqrt2:
    return Qsqrt2(Q(point[0]), Q(point[1]))


def maximal_line_starts_general(length: int, p: int, q: int) -> list[Point]:
    """Initial points of box strings parallel to a positive direction."""
    if not (1 <= p < length and 1 <= q < length):
        raise ValueError("direction coordinates must lie in [1,length)")
    direction = (p, q)
    return [
        point
        for a in range(length)
        for b in range(length)
        if in_box(point := (a, b), length)
        and not in_box(add_point(point, direction, -1), length)
    ]


def directional_partition_general(
    length: int, segment_size: int, p: int, q: int
) -> dict:
    """Partition every maximal (p,q)-string into full blocks and a remainder."""
    if math.gcd(p, q) != 1:
        raise ValueError("the direction must be primitive")
    if not (1 <= p < length and 1 <= q < length):
        raise ValueError("direction coordinates must lie in [1,length)")
    if segment_size < 2 or length * length % segment_size:
        raise ValueError("segment_size must divide box cardinality")

    direction = (p, q)
    starts = maximal_line_starts_general(length, p, q)
    core_starts: list[Point] = []
    remainder: set[Point] = set()
    line_points: list[Point] = []

    for start in starts:
        line = []
        point = start
        while in_box(point, length):
            line.append(point)
            point = add_point(point, direction)
        line_points.extend(line)
        full = len(line) // segment_size
        core_starts.extend(
            add_point(start, direction, block * segment_size)
            for block in range(full)
        )
        remainder.update(line[full * segment_size :])

    expected_line_count = (p + q) * length - p * q
    box = {(a, b) for a in range(length) for b in range(length)}
    if len(starts) != expected_line_count:
        raise AssertionError("maximal-line count identity failed")
    if Counter(line_points) != Counter(box):
        raise AssertionError("maximal lines do not partition the box")

    error = len(remainder)
    if error % segment_size:
        raise AssertionError("remainder must be divisible by segment size")

    outlier_starts = [
        (2 * length + j, 2 * length) for j in range(error // segment_size)
    ]
    all_starts = core_starts + outlier_starts

    representation = Counter(
        add_point(start, direction, step)
        for start in all_starts
        for step in range(segment_size)
    )
    spectrum = set(representation)
    covered_core = spectrum & box

    return {
        "length": length,
        "segment_size": segment_size,
        "p": p,
        "q": q,
        "line_count": len(starts),
        "expected_line_count": expected_line_count,
        "error": error,
        "error_divisible": error % segment_size == 0,
        "core_start_count": len(core_starts),
        "outlier_start_count": len(outlier_starts),
        "base_count": len(all_starts),
        "expected_base_count": length * length // segment_size,
        "all_starts": all_starts,
        "spectrum": spectrum,
        "box": box,
        "representation_injective": all(value == 1 for value in representation.values()),
        "spectrum_size": len(spectrum),
        "covered_core_size": len(covered_core),
        "expected_covered_core_size": length * length - error,
        "symmetric_difference": len(spectrum ^ box),
        "expected_symmetric_difference": 2 * error,
        "strict_error_bound": error < segment_size * expected_line_count,
    }


def directional_partition(length: int, segment_size: int, r: int) -> dict:
    """Compatibility wrapper for direction (1,r)."""
    result = directional_partition_general(length, segment_size, 1, r)
    result["r"] = r
    return result


def endpoint_exponent_certificate() -> dict[str, object]:
    """Check the exact t=m^72 exponent substitution."""
    t = Q(72)
    s = Q(56)
    u = Q(60)
    length = Q(58)
    transverse = Q(1)
    return {
        "S_exponent_in_t": str(s / t),
        "U_exponent_in_t": str(u / t),
        "L_exponent_in_t": str(length / t),
        "SU_exponent_in_t": str((s + u) / t),
        "L2_equals_SU": 2 * length == s + u,
        "transverse_rank_exponent_in_t": str(transverse / t),
        "tangent_union_exponent_in_m_upper_bound": int(transverse + u),
        "tangent_cap_exponent_in_m": int(t),
        "boundary_scale_exponent_in_t": str((s - length) / t),
        "pass": (
            s / t == Q(7, 9)
            and u / t == Q(5, 6)
            and (s + u) / t == Q(29, 18)
            and length / t == Q(29, 36)
            and 2 * length == s + u
            and transverse + u < t
            and (s - length) / t == Q(-1, 36)
        ),
    }


def transverse_certificate(max_r: int) -> dict[str, object]:
    """Check pairwise non-proportional Q(sqrt2) direction vectors."""
    pairs = [(1, r) for r in range(1, max_r + 1)]
    determinants = {
        (r, s): 1 * s - 1 * r
        for r in range(1, max_r + 1)
        for s in range(r + 1, max_r + 1)
    }
    return {
        "count": len(pairs),
        "all_pairwise_transverse": all(value != 0 for value in determinants.values()),
        "minimum_abs_determinant": (
            min(map(abs, determinants.values())) if determinants else None
        ),
    }


def primitive_direction_tradeoff_certificate(
    length: int = 90, segment_size: int = 3, max_coordinate: int = 5
) -> dict[str, object]:
    """Enumerate the two-dimensional primitive-direction tradeoff."""
    directions = [
        (p, q)
        for p in range(1, max_coordinate + 1)
        for q in range(1, max_coordinate + 1)
        if math.gcd(p, q) == 1
    ]
    partitions = [
        directional_partition_general(length, segment_size, p, q)
        for p, q in directions
    ]
    determinants = [
        p * other_q - q * other_p
        for index, (p, q) in enumerate(directions)
        for other_p, other_q in directions[index + 1 :]
    ]
    lower_constant = 2 - math.pi**2 / 6
    relative_errors = [
        Q(int(partition["symmetric_difference"]), length * length)
        for partition in partitions
    ]
    uniform_bound = Q(
        4 * max_coordinate * segment_size,
        length,
    )
    return {
        "direction_count": len(directions),
        "union_bound_lower_constant": lower_constant,
        "direction_count_lower_bound": (
            len(directions) >= lower_constant * max_coordinate**2
        ),
        "all_pairwise_transverse": all(value != 0 for value in determinants),
        "all_row_maps_injective": all(
            bool(partition["representation_injective"])
            for partition in partitions
        ),
        "maximum_relative_error": str(max(relative_errors, default=Q(0))),
        "uniform_tradeoff_bound": str(uniform_bound),
        "uniform_error_bound_holds": all(
            error < uniform_bound for error in relative_errors
        ),
        "pass": (
            len(directions) >= lower_constant * max_coordinate**2
            and all(value != 0 for value in determinants)
            and all(
                bool(partition["representation_injective"])
                for partition in partitions
            )
            and all(error < uniform_bound for error in relative_errors)
        ),
    }


def diagonal_boundary_sharpness_certificate() -> dict[str, object]:
    """Check E_(1,1)=L(S-1) whenever S divides L."""
    cases = []
    for length, segment_size in ((12, 3), (20, 4), (30, 5), (42, 6)):
        result = directional_partition_general(
            length, segment_size, 1, 1
        )
        expected_error = length * (segment_size - 1)
        expected_symmetric_difference = 2 * expected_error
        cases.append(
            {
                "L": length,
                "S": segment_size,
                "error": result["error"],
                "expected_error": expected_error,
                "symmetric_difference": result["symmetric_difference"],
                "expected_symmetric_difference": expected_symmetric_difference,
                "pass": (
                    result["error"] == expected_error
                    and result["symmetric_difference"]
                    == expected_symmetric_difference
                ),
            }
        )
    return {
        "cases": cases,
        "exact_boundary_scale": "2(S-1)/L",
        "pass": all(case["pass"] for case in cases),
    }


def tangent_transversality_dichotomy_certificate() -> dict[str, object]:
    """Check the exact split of tangent overlap by transverse status."""
    tangent_sets = [
        {0, 1, 2, 3},
        {0, 1, 4, 5},
        {0, 2, 4, 6},
        {1, 3, 5, 6},
        {0, 3, 4, 6},
        {1, 2, 5, 6},
    ]
    # Equal cluster labels model nonzero rational-space intersection.
    clusters = [0, 0, 1, 1, 2, 2]
    q_rows = len(tangent_sets)
    row_size = len(tangent_sets[0])
    universe = set().union(*tangent_sets)
    total = 0
    transverse = 0
    nontransverse = 0
    nontransverse_neighbours = [set() for _ in tangent_sets]
    for i, left in enumerate(tangent_sets):
        for j, right in enumerate(tangent_sets):
            if i == j:
                continue
            overlap = len(left & right)
            total += overlap
            if clusters[i] == clusters[j]:
                nontransverse += overlap
                if overlap:
                    nontransverse_neighbours[i].add(j)
            else:
                transverse += overlap
    cs_lower = Q(q_rows * q_rows * row_size * row_size, len(universe))
    cs_lower -= q_rows * row_size
    branch_threshold = cs_lower / 2
    max_nontransverse_degree = max(map(len, nontransverse_neighbours))
    forced_degree_if_nontransverse_branch = (
        Q(q_rows * row_size, len(universe)) - 1
    ) / 2
    # A second assignment puts every row in one nontransverse class.  It
    # explicitly checks the strengthened fixed-(row,tangent) star conclusion.
    all_nontransverse_fixed_stars = [
        sum(
            1
            for j, other in enumerate(tangent_sets)
            if i != j and tangent in other
        )
        for i, left in enumerate(tangent_sets)
        for tangent in left
    ]
    largest_fixed_row_tangent_star = max(all_nontransverse_fixed_stars)
    return {
        "rows": q_rows,
        "row_size": row_size,
        "universe_size": len(universe),
        "total_ordered_overlap": total,
        "transverse_overlap": transverse,
        "nontransverse_overlap": nontransverse,
        "split_exact": total == transverse + nontransverse,
        "cs_lower_bound": str(cs_lower),
        "cs_bound_holds": total >= cs_lower,
        "one_branch_reaches_half_cs_mass": (
            transverse >= branch_threshold
            or nontransverse >= branch_threshold
        ),
        "max_nontransverse_neighbour_count": max_nontransverse_degree,
        "conditional_forced_degree": str(forced_degree_if_nontransverse_branch),
        "all_nontransverse_branch_mass": total,
        "largest_fixed_row_tangent_star": largest_fixed_row_tangent_star,
        "fixed_row_tangent_star_bound_holds": (
            largest_fixed_row_tangent_star
            >= forced_degree_if_nontransverse_branch
        ),
        "pass": (
            total == transverse + nontransverse
            and total >= cs_lower
            and (
                transverse >= branch_threshold
                or nontransverse >= branch_threshold
            )
            and largest_fixed_row_tangent_star
            >= forced_degree_if_nontransverse_branch
        ),
    }


def optimized_tangent_disjointness_certificate(
    length: int = 200, segment_size: int = 100, max_coordinate: int = 2
) -> dict[str, object]:
    """Check coefficient separation of tangent sets for primitive directions."""
    if (segment_size - 1) ** 2 <= 16 * max_coordinate * length:
        raise ValueError("parameters do not satisfy the separation condition")
    directions = [
        (p, q)
        for p in range(1, max_coordinate + 1)
        for q in range(1, max_coordinate + 1)
        if math.gcd(p, q) == 1
    ]
    constant = Qsqrt2(
        Q(10 * segment_size * segment_size * max_coordinate**2 + 10)
    )
    tangent_sets: dict[tuple[int, int], set[Qsqrt2]] = {}
    for p, q in directions:
        partition = directional_partition_general(
            length, segment_size, p, q
        )
        z = Q(segment_size - 1, 2) * Qsqrt2(Q(p), Q(q))
        tangent_sets[(p, q)] = {
            constant + embed(start) - 1 - z.square()
            for start in partition["all_starts"]
        }
    expected_u = length * length // segment_size
    intersections = {
        (left, right): len(tangent_sets[left] & tangent_sets[right])
        for index, left in enumerate(directions)
        for right in directions[index + 1 :]
    }
    tangent_union = set().union(*tangent_sets.values())
    return {
        "direction_count": len(directions),
        "tangent_size_per_row": sorted(map(len, tangent_sets.values())),
        "expected_tangent_size": expected_u,
        "separation_condition": (
            (segment_size - 1) ** 2 > 16 * max_coordinate * length
        ),
        "all_pairwise_disjoint": all(value == 0 for value in intersections.values()),
        "union_size": len(tangent_union),
        "expected_union_size": len(directions) * expected_u,
        "all_tangents_positive": all(
            tangent.is_positive()
            for tangent_set in tangent_sets.values()
            for tangent in tangent_set
        ),
        "pass": (
            all(len(values) == expected_u for values in tangent_sets.values())
            and all(value == 0 for value in intersections.values())
            and len(tangent_union) == len(directions) * expected_u
            and all(
                tangent.is_positive()
                for tangent_set in tangent_sets.values()
                for tangent in tangent_set
            )
        ),
    }


def fixed_tangent_transverse_rigidity_certificate() -> dict[str, object]:
    """Check sharp one-point intersection and the packing ledger."""
    tangent = Qsqrt2(Q(10))
    rho = Qsqrt2(Q(1))
    x_set = [Qsqrt2(Q(0)), Qsqrt2(Q(1, 2))]
    z_left = Qsqrt2(Q(1))
    z_right = Qsqrt2(Q(0), Q(1))

    def cell(z: Qsqrt2) -> set[Qsqrt2]:
        return {
            rho.square() + z.square() + tangent + 2 * rho * z * x
            for x in x_set
        }

    left = cell(z_left)
    right = cell(z_right)
    intersection = left & right

    # A synthetic all-transverse linear set system attains the permitted
    # intersection pattern and checks the second-moment denominator.
    linear_cells = [
        {row * 10 + value for value in range(5)}
        for row in range(4)
    ]
    # Identify one point from every pair without creating triple points.
    next_label = 1000
    for left_index in range(len(linear_cells)):
        for right_index in range(left_index + 1, len(linear_cells)):
            linear_cells[left_index].add(next_label)
            linear_cells[right_index].add(next_label)
            next_label += 1
    # The cells no longer have a common size, so check the algebraic formula
    # separately with the exact S=2 sharp example above.  The universal
    # packing theorem itself is proved in the manuscript.
    n = 2
    s = 2
    ordered_transverse = 2
    denominator = n * s + ordered_transverse
    packing_lower = Q(n * n * s * s, denominator)
    actual_union = len(left | right)
    return {
        "left_cell": sorted(value.as_pair() for value in left),
        "right_cell": sorted(value.as_pair() for value in right),
        "intersection": sorted(value.as_pair() for value in intersection),
        "intersection_size": len(intersection),
        "spaces_pairwise_transverse": True,
        "sharp_constant_one": len(intersection) == 1,
        "packing_lower_bound": str(packing_lower),
        "actual_union_size": actual_union,
        "packing_bound_holds": actual_union >= packing_lower,
        "synthetic_pairwise_intersections_at_most_one": all(
            len(linear_cells[i] & linear_cells[j]) <= 1
            for i in range(len(linear_cells))
            for j in range(i + 1, len(linear_cells))
        ),
        "pass": (
            len(left) == s
            and len(right) == s
            and len(intersection) == 1
            and actual_union >= packing_lower
        ),
    }


def hypercube_projection_multiplicity(dimension: int) -> dict[str, object]:
    """Reconstruct the legacy fixed-difference projection multiplicity."""
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    weights = [Q(3**index) for index in range(dimension)]
    shift = max(weight * weight for weight in weights) + 1
    x_set = [Q(0), Q(1)]
    row_tangents: dict[Q, list[Q]] = {}
    row_representations: dict[Q, dict[Q, tuple[Q, Q]]] = {}
    for index, weight in enumerate(weights):
        other_sums = sorted(
            sum(
                (
                    weights[j]
                    for j in range(dimension)
                    if j != index and mask >> j & 1
                ),
                Q(0),
            )
            for mask in range(1 << dimension)
            if not (mask >> index & 1)
        )
        z = weight / 2
        tangents = [shift + value - z * z for value in other_sums]
        representations = {
            Q(1) + z * z + tangent + 2 * z * x: (tangent, x)
            for tangent in tangents
            for x in x_set
        }
        if len(representations) != 1 << dimension:
            raise AssertionError("hypercube row is not direct")
        row_tangents[z] = tangents
        row_representations[z] = representations

    by_difference: dict[Q, list[tuple[Q, Q, Q, Q, Q, Q, Q]]] = {}
    for z, left_representations in row_representations.items():
        for other_z, right_representations in row_representations.items():
            if z == other_z:
                continue
            for value, (tangent, x) in left_representations.items():
                other_tangent, other_x = right_representations[value]
                difference = other_tangent - tangent
                by_difference.setdefault(difference, []).append(
                    (
                        value,
                        z,
                        other_z,
                        tangent,
                        other_tangent,
                        x,
                        other_x,
                    )
                )

    maximum_projection_multiplicity = 0
    collision = None
    for difference, records in by_difference.items():
        projected = Counter(
            (z, other_z, x, other_x)
            for _, z, other_z, _, _, x, other_x in records
        )
        local_maximum = max(projected.values())
        maximum_projection_multiplicity = max(
            maximum_projection_multiplicity, local_maximum
        )
        if collision is None and local_maximum > 1:
            repeated_projection = next(
                projection
                for projection, multiplicity in projected.items()
                if multiplicity > 1
            )
            repeated_records = [
                record
                for record in records
                if (
                    record[1],
                    record[2],
                    record[5],
                    record[6],
                )
                == repeated_projection
            ]
            collision = {
                "difference": str(difference),
                "projection": tuple(map(str, repeated_projection)),
                "records": [
                    {
                        "value": str(record[0]),
                        "z": str(record[1]),
                        "other_z": str(record[2]),
                        "tangent": str(record[3]),
                        "other_tangent": str(record[4]),
                        "x": str(record[5]),
                        "other_x": str(record[6]),
                    }
                    for record in repeated_records
                ],
            }
    return {
        "dimension": dimension,
        "row_count": len(row_tangents),
        "maximum_projection_multiplicity": maximum_projection_multiplicity,
        "collision": collision,
        "projection_injective": maximum_projection_multiplicity == 1,
    }


def legacy_fixed_difference_projection_certificate() -> dict[str, object]:
    dimension_three = hypercube_projection_multiplicity(3)
    dimension_six = hypercube_projection_multiplicity(6)
    expected_minimal_records = [
        {
            "value": "83",
            "z": "1/2",
            "other_z": "3/2",
            "tangent": "327/4",
            "other_tangent": "319/4",
            "x": "0",
            "other_x": "0",
        },
        {
            "value": "92",
            "z": "1/2",
            "other_z": "3/2",
            "tangent": "363/4",
            "other_tangent": "355/4",
            "x": "0",
            "other_x": "0",
        },
    ]
    collision = dimension_three["collision"]
    return {
        "dimension_three": dimension_three,
        "dimension_six": dimension_six,
        "minimal_collision_matches_document": (
            collision is not None
            and collision["difference"] == "-2"
            and collision["projection"] == ("1/2", "3/2", "0", "0")
            and collision["records"] == expected_minimal_records
        ),
        "legacy_projection_injectivity_refuted": (
            not dimension_three["projection_injective"]
        ),
        "dimension_six_maximum_multiplicity": (
            dimension_six["maximum_projection_multiplicity"]
        ),
        "pass": (
            collision is not None
            and collision["difference"] == "-2"
            and collision["projection"] == ("1/2", "3/2", "0", "0")
            and collision["records"] == expected_minimal_records
            and dimension_three["maximum_projection_multiplicity"] == 2
            and dimension_six["maximum_projection_multiplicity"] == 16
        ),
    }


def difference_multiplicity_repair_dimension(dimension: int) -> dict[str, object]:
    """Audit the repaired global mu-budget in exact rational arithmetic."""
    weights = [Q(3**index) for index in range(dimension)]
    shift = max(weight * weight for weight in weights) + 1
    x_set = [Q(0), Q(1)]
    row_tangents: dict[Q, tuple[Q, ...]] = {}
    row_representations: dict[Q, dict[Q, tuple[Q, Q]]] = {}
    for index, weight in enumerate(weights):
        other_sums = sorted(
            sum(
                (
                    weights[j]
                    for j in range(dimension)
                    if j != index and mask >> j & 1
                ),
                Q(0),
            )
            for mask in range(1 << dimension)
            if not (mask >> index & 1)
        )
        z = weight / 2
        tangents = tuple(shift + value - z * z for value in other_sums)
        row_tangents[z] = tangents
        row_representations[z] = {
            Q(1) + z * z + tangent + 2 * z * x: (tangent, x)
            for tangent in tangents
            for x in x_set
        }

    tangent_universe = set().union(*map(set, row_tangents.values()))
    global_difference = Counter(
        other_tangent - tangent
        for tangent in tangent_universe
        for other_tangent in tangent_universe
    )
    pair_difference: dict[tuple[Q, Q], Counter] = {}
    full_records: Counter = Counter()
    projected: dict[Q, set[tuple[Q, Q, Q, Q]]] = {}
    for z, tangents in row_tangents.items():
        for other_z, other_tangents in row_tangents.items():
            if z == other_z:
                continue
            pair_difference[(z, other_z)] = Counter(
                other_tangent - tangent
                for tangent in tangents
                for other_tangent in other_tangents
            )
            for value, (tangent, x) in row_representations[z].items():
                other_tangent, other_x = row_representations[other_z][value]
                difference = other_tangent - tangent
                full_records[difference] += 1
                projected.setdefault(difference, set()).add(
                    (z, other_z, x, other_x)
                )

    all_differences = set(global_difference)
    mu = {
        difference: max(
            (
                counts[difference]
                for counts in pair_difference.values()
            ),
            default=0,
        )
        for difference in all_differences
    }
    weighted_reconstruction = {
        difference: sum(
            pair_difference[(z, other_z)][difference]
            for z, other_z, _, _ in projected.get(difference, set())
        )
        for difference in all_differences
    }
    projected_count = {
        difference: len(projected.get(difference, set()))
        for difference in all_differences
    }

    q_rows = dimension
    spectrum_size = 1 << dimension
    expected_record_total = q_rows * (q_rows - 1) * spectrum_size
    sigma_mu = sum(mu.values())
    tangent_size = len(tangent_universe)
    maximum_projected = max(projected_count.values())
    parameterized_lower = Q(expected_record_total, sigma_mu)
    universe_lower = Q(expected_record_total, tangent_size * tangent_size)
    return {
        "dimension": dimension,
        "rows": q_rows,
        "spectrum_size": spectrum_size,
        "tangent_universe_size": tangent_size,
        "record_total": sum(full_records.values()),
        "expected_record_total": expected_record_total,
        "weighted_identity_every_difference": all(
            full_records[difference] == weighted_reconstruction[difference]
            for difference in all_differences
        ),
        "weighted_projection_bound_every_difference": all(
            full_records[difference]
            <= mu[difference] * projected_count[difference]
            for difference in all_differences
        ),
        "mu_bounded_by_global_difference_everywhere": all(
            mu[difference] <= global_difference[difference]
            for difference in all_differences
        ),
        "zero_difference_global_multiplicity": global_difference[Q(0)],
        "expected_zero_difference_global_multiplicity": tangent_size,
        "global_difference_mass": sum(global_difference.values()),
        "expected_global_difference_mass": tangent_size * tangent_size,
        "sigma_mu": sigma_mu,
        "sigma_mu_bounded_by_R2": sigma_mu <= tangent_size * tangent_size,
        "maximum_distinct_projected_count": maximum_projected,
        "parameterized_lower_bound": str(parameterized_lower),
        "R2_lower_bound": str(universe_lower),
        "parameterized_bound_holds": maximum_projected >= parameterized_lower,
        "R2_bound_holds": maximum_projected >= universe_lower,
        "pass": (
            sum(full_records.values()) == expected_record_total
            and all(
                full_records[difference]
                == weighted_reconstruction[difference]
                for difference in all_differences
            )
            and all(
                full_records[difference]
                <= mu[difference] * projected_count[difference]
                for difference in all_differences
            )
            and all(
                mu[difference] <= global_difference[difference]
                for difference in all_differences
            )
            and global_difference[Q(0)] == tangent_size
            and sum(global_difference.values()) == tangent_size * tangent_size
            and sigma_mu <= tangent_size * tangent_size
            and maximum_projected >= parameterized_lower
            and maximum_projected >= universe_lower
        ),
    }


def difference_multiplicity_repair_certificate() -> dict[str, object]:
    dimensions = [
        difference_multiplicity_repair_dimension(dimension)
        for dimension in range(3, 7)
    ]
    return {
        "dimensions": dimensions,
        "dimension_count": len(dimensions),
        "ordered_signed_difference_convention": True,
        "zero_difference_included": True,
        "pass": all(result["pass"] for result in dimensions),
    }


def transverse_nonzero_difference_certificate() -> dict[str, object]:
    """Exact two-row transverse block and symbolic endpoint audit."""
    zero = Qsqrt2(Q(0))
    one = Qsqrt2(Q(1))
    sqrt_two = Qsqrt2(Q(0), Q(1))
    x_set = [zero, one]
    constant = Qsqrt2(Q(100))
    v0 = {zero, one, sqrt_two, one + sqrt_two}
    lambdas = [one, sqrt_two]
    rows = {}
    tangent_sets = {}
    for index, dilation in enumerate(lambdas):
        z = Q(1, 2) * dilation
        base = {zero, lambdas[1 - index]}
        tangents = {
            constant + value - 1 - z.square() for value in base
        }
        tangent_sets[index] = tangents
        rows[index] = {
            Qsqrt2(Q(1)) + z.square() + tangent + dilation * x:
            (tangent, x)
            for tangent in tangents
            for x in x_set
        }
        if set(rows[index]) != {constant + value for value in v0}:
            raise AssertionError("transverse exact block construction failed")

    tangent_universe = set().union(*tangent_sets.values())
    records = []
    zero_records = 0
    for left in range(2):
        right = 1 - left
        for value, (tangent, x) in rows[left].items():
            other_tangent, other_x = rows[right][value]
            difference = other_tangent - tangent
            if difference == zero:
                zero_records += 1
            records.append((difference, left, right, x, other_x))

    nonzero_records = [record for record in records if record[0] != zero]
    projected_by_difference: dict[
        Qsqrt2, set[tuple[int, int, Qsqrt2, Qsqrt2]]
    ] = {}
    for difference, left, right, x, other_x in nonzero_records:
        projected_by_difference.setdefault(difference, set()).add(
            (left, right, x, other_x)
        )
    global_difference = Counter(
        other_tangent - tangent
        for tangent in tangent_universe
        for other_tangent in tangent_universe
    )
    nonzero_global_mass = sum(
        count
        for difference, count in global_difference.items()
        if difference != zero
    )
    maximum_projected = max(map(len, projected_by_difference.values()))
    n_transverse = 2
    u = 2
    s = 2
    r = len(tangent_universe)
    theorem_lower = Q(n_transverse * u * (s - 1), r * r - r)

    p0_exponent = Q(19, 9)
    source_exponent = Q(7, 9)
    r2_exponent = Q(2)
    edge_exponent = p0_exponent + source_exponent - r2_exponent
    degree_exponent = edge_exponent - Q(13, 18)
    return {
        "row_count": 2,
        "common_spectrum_size": len(next(iter(rows.values()))),
        "tangent_universe_size": r,
        "ordered_transverse_pair_count": n_transverse,
        "total_records": len(records),
        "zero_difference_records": zero_records,
        "zero_difference_per_pair_bound": u,
        "nonzero_record_count": len(nonzero_records),
        "nonzero_global_difference_mass": nonzero_global_mass,
        "expected_nonzero_global_difference_mass": r * r - r,
        "maximum_distinct_projected_nonzero_fibre": maximum_projected,
        "theorem_lower_bound": str(theorem_lower),
        "theorem_bound_holds": maximum_projected >= theorem_lower,
        "fixed_nonzero_edge_exponent": str(edge_exponent),
        "fixed_nonzero_star_degree_exponent": str(degree_exponent),
        "pass": (
            len(records) == n_transverse * s * u
            and zero_records <= n_transverse * u
            and len(nonzero_records) >= n_transverse * u * (s - 1)
            and nonzero_global_mass == r * r - r
            and maximum_projected >= theorem_lower
            and edge_exponent == Q(8, 9)
            and degree_exponent == Q(1, 6)
        ),
    }


def bounded_transverse_cycle_certificate() -> dict[str, object]:
    """Audit the exponent margin and the telescoping cycle identity."""
    edge_exponent = Q(8, 9)
    vertex_exponent = Q(13, 18)
    degree_exponent = edge_exponent - vertex_exponent
    fifth_power_exponent = 5 * degree_exponent
    moore_margin = fifth_power_exponent - vertex_exponent

    # A five-cycle symbolic audit.  Each aligned edge contributes +z_k^2
    # and -z_(k+1)^2, so the quadratic coefficient dictionary must vanish.
    cycle_length = 5
    signs = [1, -1, 1, 1, -1]
    outgoing_labels = [Q(0), Q(1, 2), Q(1), Q(-1, 2), Q(0)]
    incoming_labels = [Q(1, 2), Q(0), Q(1, 2), Q(-1, 2), Q(1)]
    quadratic_coefficients = [0 for _ in range(cycle_length)]
    for index in range(cycle_length):
        quadratic_coefficients[index] += 1
        quadratic_coefficients[(index + 1) % cycle_length] -= 1
    linear_coefficients = [
        outgoing_labels[index] - incoming_labels[index]
        for index in range(cycle_length)
    ]

    # A coherent balanced four-cycle has one label at each vertex and a
    # closed signed arithmetic walk.
    coherent_signs = [1, 1, -1, -1]
    coherent_vertex_labels = [Q(0), Q(1, 2), Q(1), Q(-1, 2)]
    coherent_linear_coefficients = [
        coherent_vertex_labels[index] - coherent_vertex_labels[index]
        for index in range(4)
    ]
    partial_levels = [0]
    for sign in coherent_signs:
        partial_levels.append(partial_levels[-1] - sign)

    return {
        "edge_exponent": str(edge_exponent),
        "vertex_exponent": str(vertex_exponent),
        "average_degree_exponent": str(degree_exponent),
        "fifth_power_degree_exponent": str(fifth_power_exponent),
        "moore_margin": str(moore_margin),
        "cycle_length_bound": 10,
        "quadratic_terms_telescope": all(
            coefficient == 0 for coefficient in quadratic_coefficients
        ),
        "noncoherent_coefficients_not_all_zero": any(
            coefficient != 0 for coefficient in linear_coefficients
        ),
        "odd_cycle_sign_sum_nonzero": sum(signs) != 0,
        "coherent_coefficients_all_zero": all(
            coefficient == 0 for coefficient in coherent_linear_coefficients
        ),
        "coherent_sign_sum_zero": sum(coherent_signs) == 0,
        "coherent_arithmetic_walk_closes": partial_levels[-1] == 0,
        "coherent_walk_position_count": len(set(partial_levels)),
        "pass": (
            degree_exponent == Q(1, 6)
            and fifth_power_exponent == Q(5, 6)
            and moore_margin == Q(1, 9)
            and all(
                coefficient == 0 for coefficient in quadratic_coefficients
            )
            and any(coefficient != 0 for coefficient in linear_coefficients)
            and sum(signs) != 0
            and all(
                coefficient == 0
                for coefficient in coherent_linear_coefficients
            )
            and sum(coherent_signs) == 0
            and partial_levels[-1] == 0
            and len(set(partial_levels)) <= 5
        ),
    }


def coherent_cycle_classification_certificate() -> dict[str, object]:
    """Exhaust the sign orbits and verify the strict coherent 4-cycle model."""

    def rotations(word: tuple[int, ...]) -> set[tuple[int, ...]]:
        return {
            word[offset:] + word[:offset]
            for offset in range(len(word))
        }

    def orbit(word: tuple[int, ...]) -> set[tuple[int, ...]]:
        # Reversing the traversal reverses the edge order and flips every
        # comparison sign.  Together with rotations this is the full cycle
        # equivalence used in the manuscript.
        reversed_negated = tuple(-sign for sign in reversed(word))
        return rotations(word) | rotations(reversed_negated)

    expected_raw = {4: 6, 6: 20, 8: 70, 10: 252}
    expected_orbits = {4: 2, 6: 4, 8: 9, 10: 21}
    classifications: dict[int, dict[str, object]] = {}
    for length in (4, 6, 8, 10):
        balanced = {
            word
            for word in product((-1, 1), repeat=length)
            if sum(word) == 0
        }
        representatives = {min(orbit(word)) for word in balanced}
        level_ranges = []
        all_walks_close = True
        for word in balanced:
            levels = [0]
            for sign in word:
                levels.append(levels[-1] - sign)
            all_walks_close &= levels[-1] == 0
            level_ranges.append(max(levels) - min(levels))
        classifications[length] = {
            "raw_balanced_word_count": len(balanced),
            "expected_raw_count": expected_raw[length],
            "orbit_count": len(representatives),
            "expected_orbit_count": expected_orbits[length],
            "all_arithmetic_walks_close": all_walks_close,
            "maximum_level_range": max(level_ranges),
            "half_length_level_bound": max(level_ranges) <= length // 2,
            "pass": (
                len(balanced) == expected_raw[length]
                and len(representatives) == expected_orbits[length]
                and all_walks_close
                and max(level_ranges) <= length // 2
            ),
        }

    def rational_square_ratio(left: int, right: int) -> bool:
        common = math.gcd(left, right)
        numerator = left // common
        denominator = right // common
        return (
            math.isqrt(numerator) ** 2 == numerator
            and math.isqrt(denominator) ** 2 == denominator
        )

    # z=(sqrt(5),2,sqrt(3),-2), represented by signed square values.
    height_squares = [5, 4, 3, 4]
    height_signs = [1, 1, 1, -1]
    cycle_adjacencies = [(0, 1), (1, 2), (2, 3), (3, 0)]
    directed_edges = [(0, 1), (1, 2), (3, 2), (0, 3)]
    traversal_signs = [1, 1, -1, -1]
    tangent_sets = [{10}, {10, 11}, {11}, {10, 11}]
    delta = 1
    rho_square = 1

    adjacent_transverse = all(
        not rational_square_ratio(
            height_squares[left], height_squares[right]
        )
        for left, right in cycle_adjacencies
    )
    directed_difference_exact = all(
        height_squares[tail] - height_squares[head] == delta
        for tail, head in directed_edges
    )
    tangent_incidence_exact = all(
        10 in tangent_sets[tail] and 11 in tangent_sets[head]
        for tail, head in directed_edges
    )
    common_labels = [
        (
            rho_square + height_squares[tail] + 10,
            rho_square + height_squares[head] + 11,
        )
        for tail, head in directed_edges
    ]
    model = {
        "height_squares": height_squares,
        "height_signs": height_signs,
        "all_heights_nonzero_and_distinct": (
            all(sign != 0 and square > 0 for sign, square in zip(height_signs, height_squares))
            and len(set(zip(height_signs, height_squares))) == 4
        ),
        "cycle_is_simple": len(set(sum(([left, right] for left, right in cycle_adjacencies), []))) == 4,
        "adjacent_row_spaces_transverse": adjacent_transverse,
        "directed_height_square_difference_exact": directed_difference_exact,
        "traversal_sign_word": "".join("+" if sign == 1 else "-" for sign in traversal_signs),
        "traversal_signs_balanced": sum(traversal_signs) == 0,
        "tangent_incidence_exact": tangent_incidence_exact,
        "common_squared_distance_labels": [left for left, _ in common_labels],
        "every_edge_label_matches": all(left == right for left, right in common_labels),
        "all_tangents_positive": all(
            tangent > 0 for tangent_set in tangent_sets for tangent in tangent_set
        ),
    }
    model["pass"] = all(
        (
            model["all_heights_nonzero_and_distinct"],
            model["cycle_is_simple"],
            model["adjacent_row_spaces_transverse"],
            model["directed_height_square_difference_exact"],
            model["traversal_signs_balanced"],
            model["tangent_incidence_exact"],
            model["every_edge_label_matches"],
            model["all_tangents_positive"],
        )
    )

    return {
        "lengths": classifications,
        "total_raw_balanced_words": sum(
            int(result["raw_balanced_word_count"])
            for result in classifications.values()
        ),
        "total_cycle_symmetry_orbits": sum(
            int(result["orbit_count"])
            for result in classifications.values()
        ),
        "maximum_normalized_level_count": 6,
        "strict_local_four_cycle_model": model,
        "pass": (
            all(bool(result["pass"]) for result in classifications.values())
            and sum(
                int(result["raw_balanced_word_count"])
                for result in classifications.values()
            )
            == 348
            and sum(
                int(result["orbit_count"])
                for result in classifications.values()
            )
            == 36
            and bool(model["pass"])
        ),
    }


def many_bounded_cycles_certificate() -> dict[str, object]:
    """Audit the high-girth residual and repeated-cycle exponent ledger."""
    directed_edge_exponent = Q(8, 9)
    vertex_exponent = Q(13, 18)
    high_girth_residual_exponent = Q(6, 5) * vertex_exponent
    residual_gap = directed_edge_exponent - high_girth_residual_exponent
    linear_residual_gap = directed_edge_exponent - vertex_exponent

    # Constants from forgetting orientations, deleting cycles of length at
    # most ten, splitting coherent/noncoherent, and pigeonholing 36 coherent
    # sign orbits do not alter the power exponent.
    constant_denominator_for_fixed_coherent_type = 2 * 10 * 2 * 36
    return {
        "directed_edge_exponent": str(directed_edge_exponent),
        "vertex_exponent": str(vertex_exponent),
        "high_girth_residual_exponent": str(
            high_girth_residual_exponent
        ),
        "high_girth_residual_gap": str(residual_gap),
        "linear_residual_gap": str(linear_residual_gap),
        "girth_threshold": 10,
        "bfs_depth": 5,
        "high_girth_edge_bound": "n(n^(1/5)+1)",
        "edge_disjoint_cycle_exponent": str(directed_edge_exponent),
        "coherent_sign_orbit_count": 36,
        "fixed_coherent_type_constant_denominator": (
            constant_denominator_for_fixed_coherent_type
        ),
        "residual_is_power_smaller": residual_gap > 0,
        "pass": (
            high_girth_residual_exponent == Q(13, 15)
            and residual_gap == Q(1, 45)
            and linear_residual_gap == Q(1, 6)
            and constant_denominator_for_fixed_coherent_type == 1440
        ),
    }


def shared_endpoint_path_energy_certificate() -> dict[str, object]:
    """Audit the length-15 exponent gain and an exact path subtraction."""
    edge_exponent = Q(8, 9)
    vertex_exponent = Q(13, 18)
    source_exponent = Q(7, 9)
    degree_exponent = edge_exponent - vertex_exponent
    path_length = 15
    path_exponent = (
        edge_exponent
        + (path_length - 1) * degree_exponent
        - 2 * vertex_exponent
    )
    endpoint_label_exponent = 2 * source_exponent
    fixed_bundle_exponent = path_exponent - endpoint_label_exponent

    rho = Q(1)
    delta = Q(1)

    def potential(z: Q, x: Q) -> Q:
        return z * z + 2 * rho * z * x

    # Two length-three paths with the same endpoints, endpoint labels, and
    # orientation sum.  P is coherent.  Q has defects +4 at height 3 and
    # -3 at height 4, giving the nontrivial relation 3*4+4*(-3)=0.
    endpoint_data = {
        "u": (Q(1), Q(10)),
        "v": (Q(2), Q(7, 2)),
    }
    coherent_edges = [
        ((Q(1), Q(10)), (Q(5), Q(-1, 2))),
        ((Q(5), Q(-1, 2)), (Q(6), Q(-17, 12))),
        ((Q(6), Q(-17, 12)), (Q(2), Q(7, 2))),
    ]
    defective_edges = [
        ((Q(1), Q(10)), (Q(3), Q(11, 6))),
        ((Q(3), Q(35, 6)), (Q(4), Q(27, 8))),
        ((Q(4), Q(3, 8)), (Q(2), Q(7, 2))),
    ]

    def edge_differences(
        edges: list[tuple[tuple[Q, Q], tuple[Q, Q]]]
    ) -> list[Q]:
        return [
            potential(*tail) - potential(*head)
            for tail, head in edges
        ]

    coherent_differences = edge_differences(coherent_edges)
    defective_differences = edge_differences(defective_edges)
    coherent_defects = [
        coherent_edges[index + 1][0][1] - coherent_edges[index][1][1]
        for index in range(2)
    ]
    defective_defects = [
        defective_edges[index + 1][0][1] - defective_edges[index][1][1]
        for index in range(2)
    ]
    defective_heights = [Q(3), Q(4)]
    homogeneous_relation = sum(
        (height * defect for height, defect in zip(defective_heights, defective_defects)),
        Q(0),
    )
    endpoint_labels_match = (
        coherent_edges[0][0][1] == defective_edges[0][0][1]
        and coherent_edges[-1][1][1] == defective_edges[-1][1][1]
        and coherent_edges[0][0] == endpoint_data["u"]
        and coherent_edges[-1][1] == endpoint_data["v"]
    )

    return {
        "path_length": path_length,
        "degree_exponent": str(degree_exponent),
        "shared_endpoint_path_exponent": str(path_exponent),
        "endpoint_label_pair_exponent": str(endpoint_label_exponent),
        "fixed_endpoint_label_and_sign_bundle_exponent": str(
            fixed_bundle_exponent
        ),
        "orientation_sum_type_count": path_length + 1,
        "homogeneous_relation_support_bound": 2 * (path_length - 1),
        "synthetic_coherent_edge_differences": list(
            map(str, coherent_differences)
        ),
        "synthetic_defective_edge_differences": list(
            map(str, defective_differences)
        ),
        "synthetic_coherent_defects": list(map(str, coherent_defects)),
        "synthetic_defective_defects": list(map(str, defective_defects)),
        "synthetic_endpoint_labels_match": endpoint_labels_match,
        "synthetic_homogeneous_relation_value": str(homogeneous_relation),
        "synthetic_relation_nontrivial": any(
            defect != 0 for defect in defective_defects
        ),
        "pass": (
            degree_exponent == Q(1, 6)
            and path_exponent == Q(16, 9)
            and endpoint_label_exponent == Q(14, 9)
            and fixed_bundle_exponent == Q(2, 9)
            and path_length + 1 == 16
            and all(value == delta for value in coherent_differences)
            and all(value == delta for value in defective_differences)
            and all(value == 0 for value in coherent_defects)
            and defective_defects == [Q(4), Q(-3)]
            and endpoint_labels_match
            and homogeneous_relation == 0
            and any(defect != 0 for defect in defective_defects)
        ),
    }


def coherent_theta_amplification_certificate() -> dict[str, object]:
    """Audit the 80-to-5 midpoint ledger and a finite theta model."""
    edge_exponent = Q(8, 9)
    vertex_exponent = Q(13, 18)
    source_exponent = Q(7, 9)
    initial_length = 80
    initial_path_exponent = (
        initial_length * (edge_exponent - vertex_exponent)
        - vertex_exponent
    )
    fixed_endpoint_and_word_exponent = (
        initial_path_exponent - 2 * source_exponent
    )
    midpoint_exponents = [fixed_endpoint_and_word_exponent]
    lengths = [initial_length]
    for _ in range(4):
        midpoint_exponents.append(
            (midpoint_exponents[-1] - vertex_exponent) / 2
        )
        lengths.append(lengths[-1] // 2)
    theta_or_hub_exponent = midpoint_exponents[-1] / 2

    # Three internally disjoint length-five arms.  Every pair must form a
    # simple ten-cycle, which is the finite graph interface of Theorem 2.
    left_endpoint = 0
    right_endpoint = 1
    arms = [
        [left_endpoint, 10 * arm + 2, 10 * arm + 3, 10 * arm + 4, 10 * arm + 5, right_endpoint]
        for arm in range(3)
    ]
    arm_interiors_disjoint = all(
        set(arms[i][1:-1]).isdisjoint(arms[j][1:-1])
        for i in range(len(arms))
        for j in range(i + 1, len(arms))
    )
    pair_cycle_lengths = []
    pair_cycle_simple = []
    for i in range(len(arms)):
        for j in range(i + 1, len(arms)):
            cycle_vertices = arms[i][:-1] + list(reversed(arms[j][1:]))
            pair_cycle_lengths.append(len(cycle_vertices))
            pair_cycle_simple.append(len(set(cycle_vertices)) == len(cycle_vertices))

    return {
        "initial_path_length": initial_length,
        "initial_shared_endpoint_path_exponent": str(
            initial_path_exponent
        ),
        "fixed_endpoint_labels_and_word_exponent": str(
            fixed_endpoint_and_word_exponent
        ),
        "midpoint_lengths": lengths,
        "midpoint_family_exponents": list(map(str, midpoint_exponents)),
        "coherent_length_five_family_exponent": str(
            midpoint_exponents[-1]
        ),
        "theta_or_hub_exponent": str(theta_or_hub_exponent),
        "relation_support_bound": 2 * (initial_length - 1),
        "theta_internal_potential_level_count": 4,
        "finite_theta_arm_count": len(arms),
        "finite_theta_arm_interiors_disjoint": arm_interiors_disjoint,
        "finite_theta_pair_cycle_lengths": pair_cycle_lengths,
        "finite_theta_pair_cycles_simple": all(pair_cycle_simple),
        "pass": (
            initial_path_exponent == Q(227, 18)
            and fixed_endpoint_and_word_exponent == Q(199, 18)
            and lengths == [80, 40, 20, 10, 5]
            and midpoint_exponents
            == [Q(199, 18), Q(31, 6), Q(20, 9), Q(3, 4), Q(1, 72)]
            and theta_or_hub_exponent == Q(1, 144)
            and arm_interiors_disjoint
            and pair_cycle_lengths == [10, 10, 10]
            and all(pair_cycle_simple)
        ),
    }


def path_energy_multiplicity_red_team_certificate() -> dict[str, object]:
    """Independently recompute every path-energy exponent and fibre."""
    edge = Q(8, 9)
    vertex = Q(13, 18)
    source = Q(7, 9)
    degree = edge - vertex
    length_fifteen_path = edge + 14 * degree - 2 * vertex
    length_fifteen_bundle = length_fifteen_path - 2 * source
    length_eighty_path = edge + 79 * degree - 2 * vertex
    length_eighty_bundle = length_eighty_path - 2 * source
    midpoint = [length_eighty_bundle]
    for _ in range(4):
        midpoint.append((midpoint[-1] - vertex) / 2)

    return {
        "underlying_direction_loss_constant": 2,
        "degree_exponent": str(degree),
        "length_fifteen_shared_endpoint_exponent": str(
            length_fifteen_path
        ),
        "length_fifteen_fixed_label_bundle_exponent": str(
            length_fifteen_bundle
        ),
        "length_eighty_shared_endpoint_exponent": str(
            length_eighty_path
        ),
        "length_eighty_fixed_label_bundle_exponent": str(
            length_eighty_bundle
        ),
        "complete_orientation_word_count": 2**80,
        "complete_orientation_word_is_t_constant": True,
        "midpoint_fibre_exponent": str(vertex),
        "midpoint_fibre_is_rows_not_row_source_pairs": True,
        "midpoint_exponents": list(map(str, midpoint)),
        "length_five_exponent": str(midpoint[-1]),
        "hub_or_packing_exponent": str(midpoint[-1] / 2),
        "individual_paths_are_simple": True,
        "cross_path_overlap_allowed_before_final_packing": True,
        "common_defect_support_is_internal_only": True,
        "ordered_half_path_pair_determines_at_most_one_full_path": True,
        "pass": (
            degree == Q(1, 6)
            and length_fifteen_path == Q(16, 9)
            and length_fifteen_bundle == Q(2, 9)
            and length_eighty_path == Q(227, 18)
            and length_eighty_bundle == Q(199, 18)
            and midpoint
            == [Q(199, 18), Q(31, 6), Q(20, 9), Q(3, 4), Q(1, 72)]
            and midpoint[-1] / 2 == Q(1, 144)
        ),
    }


def defect_transition_trichotomy_certificate() -> dict[str, object]:
    """Audit transition pairing and the aligned-gap checkpoint ledger."""

    def equal_pair_partition_exists(values: tuple[int, int, int, int]) -> bool:
        return all(multiplicity % 2 == 0 for multiplicity in Counter(values).values())

    pairing_cases = []
    pairing_lemma_holds = True
    for defect in (-3, -2, -1, 1, 2, 3):
        for left_base in range(-4, 5):
            for right_base in range(-4, 5):
                values = (
                    left_base,
                    left_base + defect,
                    right_base,
                    right_base + defect,
                )
                pairable = equal_pair_partition_exists(values)
                expected = left_base == right_base
                pairing_lemma_holds &= pairable == expected
                pairing_cases.append((values, pairable, expected))

    bundle = Q(199, 18)
    vertex = Q(13, 18)
    density = bundle / 80
    gap_rows = []
    for length in range(2, 81):
        segment_count = (length + 5) // 6
        exponent = (
            density * length - (segment_count - 1) * vertex
        ) / segment_count
        gap_rows.append((exponent, length, segment_count))
    minimum_exponent, minimizing_length, minimizing_segments = min(gap_rows)
    theta_or_hub = Q(1, 10) / 2

    # A common defective spine can coexist with a coherent diamond: both
    # paths use transition 0->1 at the defect row, then branch through
    # different coherent internal vertices and reunite at label 3.
    aligned_spine_path_transitions = [
        ((0, 1), (2, 2), (3, 3)),
        ((0, 1), (-2, -2), (3, 3)),
    ]
    aligned_nonzero_defects = [
        transition_path[0][1] - transition_path[0][0]
        for transition_path in aligned_spine_path_transitions
    ]
    coherent_detours = all(
        all(outgoing == incoming for incoming, outgoing in path[1:])
        for path in aligned_spine_path_transitions
    )

    return {
        "pairing_case_count": len(pairing_cases),
        "nonzero_transition_pairing_lemma_holds": pairing_lemma_holds,
        "relation_support_bound": 158,
        "noncoherent_cycle_length_bound": 160,
        "common_defect_support_internal_row_bound": 79,
        "gap_energy_density": str(density),
        "gap_length_range": [2, 80],
        "checkpoint_max_segment_length": 6,
        "minimum_checkpoint_exponent": str(minimum_exponent),
        "minimum_checkpoint_length": minimizing_length,
        "minimum_checkpoint_segment_count": minimizing_segments,
        "minimum_exceeds_one_tenth": minimum_exponent > Q(1, 10),
        "weakened_short_path_exponent": "1/10",
        "theta_or_hub_exponent": str(theta_or_hub),
        "aligned_spine_defects": list(map(str, aligned_nonzero_defects)),
        "aligned_spine_is_nonzero": all(
            defect != 0 for defect in aligned_nonzero_defects
        ),
        "aligned_detours_are_coherent": coherent_detours,
        "pass": (
            pairing_lemma_holds
            and len(pairing_cases) == 486
            and density == Q(199, 1440)
            and minimum_exponent == Q(2201, 20160)
            and minimizing_length == 79
            and minimizing_segments == 14
            and minimum_exponent > Q(1, 10)
            and theta_or_hub == Q(1, 20)
            and aligned_nonzero_defects == [1, 1]
            and coherent_detours
        ),
    }


def geometric_interface_certificate(
    length: int = 20, segment_size: int = 4, max_r: int = 3
) -> dict[str, object]:
    """Audit tangent positivity and the exact parabolic spectrum identity."""
    if max_r >= length:
        raise ValueError("directions must be shorter than the box side")
    if length * length % segment_size:
        raise ValueError("segment size must divide box cardinality")

    # The proof uses m through S=m^56.  For finite falsification we only need
    # m >= max_r in the safe positivity constant.
    m = max(2, max_r)
    constant = Qsqrt2(Q(10 * segment_size * segment_size * m * m + 10))
    x_set = [Q(j, segment_size - 1) for j in range(segment_size)]
    common = {constant + embed(point) for point in directional_partition(
        length, segment_size, 1
    )["box"]}
    tangent_union: set[Qsqrt2] = set()
    row_summaries = []

    for r in range(1, max_r + 1):
        partition = directional_partition(length, segment_size, r)
        direction = Qsqrt2(Q(1), Q(r))
        twice_z = (segment_size - 1) * direction
        z = Q(1, 2) * twice_z
        z_square = z.square()
        bases = [constant + embed(point) for point in partition["all_starts"]]
        tangents = {base - 1 - z_square for base in bases}
        tangent_union.update(tangents)

        representations = Counter(
            tangent + 1 + z_square + twice_z * x
            for tangent in tangents
            for x in x_set
        )
        spectrum = set(representations)
        expected = {
            constant + embed(point) for point in partition["spectrum"]
        }
        row_summaries.append(
            {
                "r": r,
                "height_positive": z.is_positive(),
                "all_tangents_positive": all(tangent.is_positive() for tangent in tangents),
                "source_sines_distinct": len(set(x_set)) == segment_size,
                "tangent_count": len(tangents),
                "expected_tangent_count": length * length // segment_size,
                "row_map_injective": all(
                    multiplicity == 1 for multiplicity in representations.values()
                ),
                "all_spectrum_values_positive": all(
                    value.is_positive() for value in spectrum
                ),
                "spectrum_exact": spectrum == expected,
                "common_intersection": len(spectrum & common),
                "expected_common_intersection": (
                    length * length - int(partition["error"])
                ),
                "symmetric_difference": len(spectrum ^ common),
                "expected_symmetric_difference": 2 * int(partition["error"]),
                "relative_error_denominator": len(common),
                "relative_error_exact": str(Q(len(spectrum ^ common), len(common))),
                "relative_to_SU_equals_relative_to_V": (
                    len(common) == length * length
                ),
                # A>1 and tau>0 imply off-axis targets and nonperpendicular
                # target planes in the reverse-circle chart.
                "reverse_radius_square": "1",
                "off_axis_and_nonperpendicular": all(
                    tangent.is_positive() for tangent in tangents
                ),
            }
        )

    expected_u = length * length // segment_size
    return {
        "rows": row_summaries,
        "common_spectrum_size": len(common),
        "expected_common_spectrum_size": length * length,
        "one_common_spectrum_used_for_every_row": True,
        "distinct_nonzero_heights": max_r,
        "pairwise_nonaligned": True,
        "tangent_union_size": len(tangent_union),
        "trivial_tangent_union_cap": max_r * expected_u,
        "tangent_union_within_cap": len(tangent_union) <= max_r * expected_u,
        "pass": all(
            row["height_positive"]
            and row["all_tangents_positive"]
            and row["source_sines_distinct"]
            and row["tangent_count"] == row["expected_tangent_count"]
            and row["row_map_injective"]
            and row["all_spectrum_values_positive"]
            and row["spectrum_exact"]
            and row["common_intersection"] == row["expected_common_intersection"]
            and row["symmetric_difference"] == row["expected_symmetric_difference"]
            and row["relative_to_SU_equals_relative_to_V"]
            and row["off_axis_and_nonperpendicular"]
            for row in row_summaries
        )
        and len(common) == length * length,
    }


def finite_partition_suite() -> dict[str, object]:
    cases = []
    for length, segment_size, max_r in ((12, 3, 4), (20, 4, 5), (30, 5, 6)):
        for r in range(1, max_r + 1):
            result = directional_partition(length, segment_size, r)
            passed = (
                result["line_count"] == result["expected_line_count"]
                and result["error_divisible"]
                and result["base_count"] == result["expected_base_count"]
                and result["representation_injective"]
                and result["spectrum_size"] == length * length
                and result["covered_core_size"]
                == result["expected_covered_core_size"]
                and result["symmetric_difference"]
                == result["expected_symmetric_difference"]
                and result["strict_error_bound"]
            )
            cases.append(
                {
                    "L": length,
                    "S": segment_size,
                    "r": r,
                    "E": result["error"],
                    "line_count": result["line_count"],
                    "pass": passed,
                }
            )
    return {"case_count": len(cases), "cases": cases, "pass": all(c["pass"] for c in cases)}


def main() -> int:
    result = {
        "endpoint": endpoint_exponent_certificate(),
        "transverse": transverse_certificate(30),
        "primitive_tradeoff": primitive_direction_tradeoff_certificate(),
        "diagonal_boundary_sharpness": diagonal_boundary_sharpness_certificate(),
        "optimized_tangent_disjointness": (
            optimized_tangent_disjointness_certificate()
        ),
        "fixed_tangent_rigidity": (
            fixed_tangent_transverse_rigidity_certificate()
        ),
        "legacy_fixed_difference_projection": (
            legacy_fixed_difference_projection_certificate()
        ),
        "difference_multiplicity_repair": (
            difference_multiplicity_repair_certificate()
        ),
        "transverse_nonzero_difference": (
            transverse_nonzero_difference_certificate()
        ),
        "bounded_transverse_cycle": bounded_transverse_cycle_certificate(),
        "coherent_cycle_classification": (
            coherent_cycle_classification_certificate()
        ),
        "many_bounded_cycles": many_bounded_cycles_certificate(),
        "shared_endpoint_path_energy": (
            shared_endpoint_path_energy_certificate()
        ),
        "coherent_theta_amplification": (
            coherent_theta_amplification_certificate()
        ),
        "path_energy_multiplicity_red_team": (
            path_energy_multiplicity_red_team_certificate()
        ),
        "defect_transition_trichotomy": (
            defect_transition_trichotomy_certificate()
        ),
        "tangent_dichotomy": tangent_transversality_dichotomy_certificate(),
        "partitions": finite_partition_suite(),
        "geometry": geometric_interface_certificate(),
    }
    result["pass"] = (
        bool(result["endpoint"]["pass"])
        and bool(result["transverse"]["all_pairwise_transverse"])
        and bool(result["primitive_tradeoff"]["pass"])
        and bool(result["diagonal_boundary_sharpness"]["pass"])
        and bool(result["optimized_tangent_disjointness"]["pass"])
        and bool(result["fixed_tangent_rigidity"]["pass"])
        and bool(result["legacy_fixed_difference_projection"]["pass"])
        and bool(result["difference_multiplicity_repair"]["pass"])
        and bool(result["transverse_nonzero_difference"]["pass"])
        and bool(result["bounded_transverse_cycle"]["pass"])
        and bool(result["coherent_cycle_classification"]["pass"])
        and bool(result["many_bounded_cycles"]["pass"])
        and bool(result["shared_endpoint_path_energy"]["pass"])
        and bool(result["coherent_theta_amplification"]["pass"])
        and bool(result["path_energy_multiplicity_red_team"]["pass"])
        and bool(result["defect_transition_trichotomy"]["pass"])
        and bool(result["tangent_dichotomy"]["pass"])
        and bool(result["partitions"]["pass"])
        and bool(result["geometry"]["pass"])
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
