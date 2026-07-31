#!/usr/bin/env python3
"""Exact certificates for the #1083 block-vs-diffuse breakthrough attack.

The finite computations are falsification and bookkeeping certificates.  The
all-parameter statements are proved in BREAKTHROUGH_ATTACK.md.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
import math


Q = Fraction


def endpoint_certificate() -> dict[str, str | bool]:
    """Return the exact exponent identities of the spectral block model."""
    s = Q(7, 9)
    u = Q(5, 6)
    h = Q(19, 9)
    d = Q(3)
    row_spectrum = s + u
    block_size = h + row_spectrum - d
    number_blocks = h - block_size
    pair_count = number_blocks + 2 * block_size
    intersection_mass = pair_count + row_spectrum
    forced_pair_overlap = 2 * s + 2 * u - d

    expected = {
        "row_spectrum": Q(29, 18),
        "block_size": Q(13, 18),
        "number_blocks": Q(25, 18),
        "pair_count": Q(17, 6),
        "intersection_mass": Q(40, 9),
        "forced_pair_overlap": Q(2, 9),
    }
    actual = {
        "row_spectrum": row_spectrum,
        "block_size": block_size,
        "number_blocks": number_blocks,
        "pair_count": pair_count,
        "intersection_mass": intersection_mass,
        "forced_pair_overlap": forced_pair_overlap,
    }
    return {
        **{key: str(value) for key, value in actual.items()},
        "source_exponent": str(s),
        "target_row_exponent": str(u),
        "partner_to_source_gap": str(s - block_size),
        "overlap_to_target_gap": str(u - forced_pair_overlap),
        "pass": actual == expected
        and s - block_size == Q(1, 18)
        and u - forced_pair_overlap == Q(11, 18),
    }


def direct_tiling_rank_certificate() -> dict[str, str | int | bool]:
    """Check the endpoint value in the exact group-algebra rank theorem."""
    # log_S(SU) tends (s+u)/s at exponent scale.
    s_exponent = Q(7, 9)
    u_exponent = Q(5, 6)
    logarithmic_ratio = (s_exponent + u_exponent) / s_exponent
    independent_class_bound = math.floor(logarithmic_ratio)
    return {
        "log_S_SU_exponent_limit": str(logarithmic_ratio),
        "independent_dilation_space_bound": independent_class_bound,
        "strictly_below_three": logarithmic_ratio < 3,
        "pass": logarithmic_ratio == Q(29, 14)
        and independent_class_bound == 2,
    }


def parabolic_resolution_endpoint_certificate() -> dict[str, str | bool]:
    """Check the new exact-block tangent and difference-fibre ledgers."""
    q = Q(13, 18)
    s = Q(7, 9)
    u = Q(5, 6)
    r = Q(1)
    spectrum = s + u
    fixed_difference = 2 * q + spectrum - 2 * r
    rich_tangent = q + u - r
    tangent_pair_mass = 2 * q + 2 * u - r
    one_fibre_capacity = rich_tangent + s
    return {
        "fixed_difference_energy": str(fixed_difference),
        "rich_tangent_row_degree": str(rich_tangent),
        "tangent_pair_mass": str(tangent_pair_mass),
        "one_fibre_value_capacity": str(one_fibre_capacity),
        "common_spectrum": str(spectrum),
        "one_fibre_cannot_fill_spectrum": one_fibre_capacity < spectrum,
        "pass": fixed_difference == Q(19, 18)
        and rich_tangent == Q(5, 9)
        and tangent_pair_mass == Q(19, 9)
        and one_fibre_capacity == Q(4, 3),
    }


def build_exact_block_model(
    group_count: int = 4, group_size: int = 3, spectrum_size: int = 6
) -> dict[str, int | bool]:
    """Build the exact equality case of the abstract spectral ledger."""
    if min(group_count, group_size, spectrum_size) <= 0:
        raise ValueError("block parameters must be positive")

    rows: list[frozenset[int]] = []
    for group in range(group_count):
        spectrum = frozenset(
            range(group * spectrum_size, (group + 1) * spectrum_size)
        )
        rows.extend([spectrum] * group_size)

    multiplicity = Counter(value for row in rows for value in row)
    h = len(rows)
    b = spectrum_size
    d = len(multiplicity)
    total_membership = sum(map(len, rows))
    ordered_off_diagonal = sum(
        len(rows[i] & rows[j])
        for i in range(h)
        for j in range(h)
        if i != j
    )
    positive_ordered_pairs = sum(
        bool(rows[i] & rows[j])
        for i in range(h)
        for j in range(h)
        if i != j
    )
    cs_off_diagonal = total_membership * total_membership // d - total_membership
    average_label_degree = Fraction(total_membership, d)
    label_variance = sum(
        (Fraction(degree) - average_label_degree) ** 2
        for degree in multiplicity.values()
    )
    fractional_defect = sum(
        len(rows[i] & rows[j]) * (b - len(rows[i] & rows[j]))
        for i in range(h)
        for j in range(h)
        if i != j
    )

    return {
        "rows": h,
        "row_size": b,
        "union_size": d,
        "label_degree": min(multiplicity.values()),
        "label_regular": len(set(multiplicity.values())) == 1,
        "total_membership": total_membership,
        "ordered_off_diagonal": ordered_off_diagonal,
        "cs_off_diagonal": cs_off_diagonal,
        "cs_equality": ordered_off_diagonal == cs_off_diagonal,
        "label_variance": str(label_variance),
        "fractional_defect": fractional_defect,
        "positive_ordered_pairs": positive_ordered_pairs,
        "expected_positive_ordered_pairs": (
            group_count * group_size * (group_size - 1)
        ),
        "zero_or_full_intersections": all(
            len(rows[i] & rows[j]) in (0, b)
            for i in range(h)
            for j in range(h)
            if i != j
        ),
    }


def row_spectrum(
    x_set: tuple[Q, ...], t_set: tuple[Q, ...], z: Q, rho: Q = Q(1)
) -> frozenset[Q]:
    """The spectrum with the harmless common rho^2 translation included."""
    return frozenset(
        rho * rho + z * z + tau + 2 * rho * z * x
        for tau in t_set
        for x in x_set
    )


def reverse_circle_interface_certificate(
    rows: dict[Q, tuple[Q, ...]],
) -> dict[str, object]:
    """Audit the full Euclidean interface for the X={0,1}, rho=1 models.

    A target's positive transverse coordinate is represented by its exact
    square tau, so no floating-point square root enters the certificate.
    """
    anchor_radial_coordinate = Q(2)
    x_set = (Q(0), Q(1))
    cosine = {Q(0): Q(1), Q(1): Q(0)}
    anchor_sources = {
        (anchor_radial_coordinate + cosine[x], Q(0), x) for x in x_set
    }
    row_sources = {
        (anchor_radial_coordinate + cosine[x], Q(0), -z + x)
        for z in rows
        for x in x_set
    }
    targets = {
        (anchor_radial_coordinate, tau, -z)
        for z, t_set in rows.items()
        for tau in t_set
    }
    tangent_universe = {tau for t_set in rows.values() for tau in t_set}
    selected_labels = {Q(1) + tau for tau in tangent_universe}

    reverse_circle_checks = []
    producer_checks = []
    anchor_distance_checks = []
    for z, t_set in rows.items():
        for tau in t_set:
            target_radial_square = anchor_radial_coordinate**2 + tau
            cosine_plane_square = (
                anchor_radial_coordinate**2 / target_radial_square
            )
            selected_label = Q(1) + tau
            # In the normalized reverse-circle equation, cv=A and
            # radius^2=d-(1-c^2)v^2=d-tau.
            reverse_radius_square = selected_label - tau
            reverse_circle_checks.append(
                target_radial_square > 0
                and cosine_plane_square > 0
                and reverse_radius_square == 1
            )
            for x in x_set:
                producer_distance = cosine[x] ** 2 + tau + x**2
                producer_checks.append(producer_distance == selected_label)
                anchor_distance = (
                    cosine[x] ** 2 + tau + (z + x) ** 2
                )
                anchor_formula = Q(1) + tau + z**2 + 2 * z * x
                anchor_distance_checks.append(anchor_distance == anchor_formula)

    z_values = tuple(rows)
    return {
        "all_tangent_squares_positive": all(tau > 0 for tau in tangent_universe),
        "positive_radius_one": all(reverse_circle_checks),
        "all_target_planes_nonperpendicular": all(reverse_circle_checks),
        "all_targets_off_axis": anchor_radial_coordinate > 0,
        "distinct_height_rows": len(set(z_values)) == len(z_values),
        "nonaligned_parallel_axes": (
            len(set(z_values)) == len(z_values) and all(z != 0 for z in z_values)
        ),
        "producer_distances_exact": all(producer_checks),
        "anchor_distances_exact": all(anchor_distance_checks),
        "anchor_source_count": len(anchor_sources),
        "translated_source_count": len(row_sources),
        "expected_translated_source_count": len(rows) * len(x_set),
        "all_translated_sources_distinct": (
            len(row_sources) == len(rows) * len(x_set)
        ),
        "target_point_count": len(targets),
        "expected_target_point_count": sum(map(len, rows.values())),
        "all_targets_distinct": len(targets) == sum(map(len, rows.values())),
        "target_plane_count": len(tangent_universe),
        "selected_label_count": len(selected_labels),
        "selected_labels_match_tangent_count": (
            len(selected_labels) == len(tangent_universe)
        ),
        "anchor_circle_distinct_from_rows": all(z != 0 for z in z_values),
    }


def squared_distance(
    first: tuple[Q, Q, Q], second: tuple[Q, Q, Q]
) -> Q:
    return sum((left - right) ** 2 for left, right in zip(first, second))


def affine_quadratic_three_row_model() -> dict[str, object]:
    """A genuine rational-data reverse-circle model with three equal spectra.

    Square roots occur only as Euclidean coordinates; all certified squared
    distances are computed from the exact circle-axis formula.
    """
    x_set = (Q(0), Q(1))
    rows = {
        Q(-3, 2): (Q(11), Q(12)),
        Q(-1, 2): (Q(11), Q(14)),
        Q(1, 2): (Q(10), Q(13)),
    }
    spectra = {z: row_spectrum(x_set, t_set, z) for z, t_set in rows.items()}
    common = next(iter(spectra.values()))
    interface = reverse_circle_interface_certificate(rows)

    # Verify the Cartesian formula without introducing irrational y.  The
    # horizontal contribution is (u-A)^2 + y^2, so y is represented by y^2.
    rho = Q(1)
    formula_records: list[dict[str, str]] = []
    for z, t_set in rows.items():
        for x in x_set:
            # Choose the nonnegative cosine compatible with x=sin(phi).
            cosine_squared = Q(1) - x * x
            for tau in t_set:
                direct_from_squares = (
                    rho * rho * cosine_squared
                    + tau
                    + (z + rho * x) ** 2
                )
                formula = rho * rho + tau + z * z + 2 * rho * z * x
                if direct_from_squares != formula:
                    raise AssertionError("Euclidean circle-axis identity failed")
                formula_records.append(
                    {"z": str(z), "x": str(x), "tau": str(tau), "d": str(formula)}
                )

    # A two-label sub-overlap is carried by one fixed source sine on each
    # side.  This witnesses the sharp vertical-source no-go.
    left_z, right_z = Q(-1, 2), Q(1, 2)
    left_x, right_x = Q(0), Q(1)
    left_fixed = {
        rho * rho + left_z * left_z + tau + 2 * rho * left_z * left_x
        for tau in rows[left_z]
    }
    right_fixed = {
        rho * rho + right_z * right_z + tau + 2 * rho * right_z * right_x
        for tau in rows[right_z]
    }

    return {
        "row_count": len(rows),
        "source_size": len(x_set),
        "target_row_size": min(map(len, rows.values())),
        "tangent_universe": sorted({tau for values in rows.values() for tau in values}),
        "spectra_equal": len(set(spectra.values())) == 1,
        "common_spectrum": sorted(common),
        "each_row_injective": all(len(values) == len(x_set) * len(rows[z]) for z, values in spectra.items()),
        "fixed_source_overlap": sorted(left_fixed & right_fixed),
        "fixed_source_overlap_size": len(left_fixed & right_fixed),
        "formula_record_count": len(formula_records),
        "euclidean_interface": interface,
    }


def hypercube_identical_spectrum_model(dimension: int = 5) -> dict[str, object]:
    """Construct arbitrarily many identical injective nonaligned rows.

    The source tile is X={0,1}.  Base-three subset sums give a direct
    hypercube, and each coordinate direction becomes one parabolic row.
    """
    if dimension < 1:
        raise ValueError("dimension must be positive")
    weights = tuple(Q(3**index) for index in range(dimension))
    subset_sums = {
        sum((weights[index] for index in range(dimension) if mask >> index & 1), Q(0))
        for mask in range(1 << dimension)
    }
    shift = max(weight * weight for weight in weights) + 1
    x_set = (Q(0), Q(1))
    rows: dict[Q, tuple[Q, ...]] = {}
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
        rows[z] = tuple(shift + value - z * z for value in other_sums)

    spectra = {z: row_spectrum(x_set, values, z) for z, values in rows.items()}
    expected = frozenset(Q(1) + shift + value for value in subset_sums)
    tangent_universe = {tau for values in rows.values() for tau in values}
    interface = reverse_circle_interface_certificate(rows)
    return {
        "dimension": dimension,
        "row_count": len(rows),
        "source_size": len(x_set),
        "target_row_size": len(next(iter(rows.values()))),
        "spectrum_size": len(expected),
        "tangent_universe_size": len(tangent_universe),
        "tangent_universe_upper_bound": dimension * (1 << (dimension - 1)),
        "all_tangent_squares_positive": all(tau > 0 for tau in tangent_universe),
        "spectra_equal": all(values == expected for values in spectra.values()),
        "each_row_injective": all(
            len(values) == len(x_set) * len(rows[z])
            for z, values in spectra.items()
        ),
        "euclidean_interface": interface,
    }


def parabolic_lift_certificate() -> dict[str, int | bool]:
    """Check the exact point-line reformulation on the three-row model."""
    x_set = (Q(0), Q(1))
    rows = {
        Q(-3, 2): (Q(11), Q(12)),
        Q(-1, 2): (Q(11), Q(14)),
        Q(1, 2): (Q(10), Q(13)),
    }
    rho = Q(1)
    incidences = 0
    values: set[Q] = set()
    for z, t_set in rows.items():
        for tau in t_set:
            point_y = rho * rho + z * z + tau
            for x in x_set:
                d = point_y + 2 * rho * z * x
                # The parameter point (z, point_y) lies on
                # y = d - 2 rho x z.
                if point_y != d - 2 * rho * x * z:
                    raise AssertionError("parabolic lift incidence failed")
                incidences += 1
                values.add(d)
    return {
        "parameter_points": sum(map(len, rows.values())),
        "complete_incidences": incidences,
        "distance_values": len(values),
        "pass": incidences == 12 and len(values) == 4,
    }


def main() -> None:
    result = {
        "schema": "amra.erdos1083.spectral-block-breakthrough.v1",
        "endpoint": endpoint_certificate(),
        "direct_tiling_rank": direct_tiling_rank_certificate(),
        "parabolic_resolution_endpoint": (
            parabolic_resolution_endpoint_certificate()
        ),
        "block_model": build_exact_block_model(),
        "affine_quadratic_model": affine_quadratic_three_row_model(),
        "hypercube_model": hypercube_identical_spectrum_model(),
        "parabolic_lift": parabolic_lift_certificate(),
    }
    checks = [
        bool(result["endpoint"]["pass"]),
        bool(result["direct_tiling_rank"]["pass"]),
        bool(result["parabolic_resolution_endpoint"]["pass"]),
        bool(result["block_model"]["cs_equality"]),
        bool(result["block_model"]["zero_or_full_intersections"]),
        bool(result["affine_quadratic_model"]["spectra_equal"]),
        bool(result["affine_quadratic_model"]["each_row_injective"]),
        bool(
            result["affine_quadratic_model"]["euclidean_interface"][
                "positive_radius_one"
            ]
        ),
        bool(result["hypercube_model"]["spectra_equal"]),
        bool(result["hypercube_model"]["each_row_injective"]),
        bool(
            result["hypercube_model"]["euclidean_interface"][
                "positive_radius_one"
            ]
        ),
        bool(result["parabolic_lift"]["pass"]),
    ]
    result["status"] = "PASS" if all(checks) else "FAIL"
    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
