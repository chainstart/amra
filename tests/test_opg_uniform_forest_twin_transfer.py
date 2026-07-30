from __future__ import annotations

import copy
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_twin_transfer as twin_transfer
from amra.discovery.opg_uniform_forest_extensions import (
    encode_simple_graph6,
)
from amra.discovery.opg_uniform_forest_twin_transfer import (
    CERTIFIED_FALSE_TWIN_CASES,
    KRYLOV_RECURRENCE_COEFFICIENTS,
    FalseTwinCertificateError,
    build_krylov_recurrence_certificate,
    closed_form_count_vector,
    closed_form_margin,
    false_twin_partition_transitions,
    forward_partition_distribution,
    scan_false_twin_family,
    write_krylov_recurrence_certificate,
)


FALSE_TWIN_BASE = "H?`bM~^"
FALSE_TWIN_PAIR = (0, 2)
FALSE_TWIN_NEIGHBOURHOOD = (1, 5, 6, 7, 8)

# Independently recorded recursive deletion-contraction results for t=0..4.
DELETION_CONTRACTION_REGRESSION = (
    (54_124, 19_726, 21_496, 7_834),
    (522_404, 190_034, 203_780, 74_126),
    (4_781_828, 1_736_768, 1_838_420, 667_700),
    (41_970_816, 15_223_968, 15_943_776, 5_783_136),
    (356_015_088, 128_992_824, 133_885_008, 48_509_064),
)


@pytest.fixture(scope="module")
def family_a_certificate() -> dict[str, object]:
    return build_krylov_recurrence_certificate()


def _canonical_component_partition(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
) -> tuple[int, ...]:
    parent = list(range(vertex_count))

    def find(vertex: int) -> int:
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            raise ValueError("cyclic edge set")
        parent[right_root] = left_root

    labels: dict[int, int] = {}
    result = []
    for vertex in range(vertex_count):
        root = find(vertex)
        if root not in labels:
            labels[root] = len(labels)
        result.append(labels[root])
    return tuple(result)


def _brute_partition_distribution(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    forced: frozenset[int],
) -> Counter[tuple[int, ...]]:
    counts: Counter[tuple[int, ...]] = Counter()
    for mask in range(1 << len(edges)):
        selected_indexes = frozenset(
            index
            for index in range(len(edges))
            if mask & (1 << index)
        )
        if not forced <= selected_indexes:
            continue
        selected_edges = tuple(edges[index] for index in selected_indexes)
        try:
            partition = _canonical_component_partition(
                vertex_count, selected_edges
            )
        except ValueError:
            continue
        counts[partition] += 1
    return counts


def _brute_family_counts(
    base_vertex_count: int,
    base_edges: tuple[tuple[int, int], ...],
    edge_pair: tuple[int, int],
    neighbourhood: tuple[int, ...],
    twin_count: int,
) -> tuple[int, int, int, int]:
    edges = list(base_edges)
    for offset in range(twin_count):
        twin = base_vertex_count + offset
        edges.extend((vertex, twin) for vertex in neighbourhood)
    edge_tuple = tuple(edges)
    counts = [0, 0, 0, 0]
    first, second = edge_pair
    for mask in range(1 << len(edge_tuple)):
        selected_indexes = tuple(
            index
            for index in range(len(edge_tuple))
            if mask & (1 << index)
        )
        selected_edges = tuple(
            edge_tuple[index] for index in selected_indexes
        )
        try:
            _canonical_component_partition(
                base_vertex_count + twin_count, selected_edges
            )
        except ValueError:
            continue
        counts[0] += 1
        if first in selected_indexes:
            counts[1] += 1
        if second in selected_indexes:
            counts[2] += 1
        if first in selected_indexes and second in selected_indexes:
            counts[3] += 1
    return tuple(counts)


def test_forward_dp_matches_independent_subset_enumeration() -> None:
    edges = (
        (0, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (1, 3),
        (2, 3),
    )
    for forced_size in range(3):
        for forced in combinations(range(len(edges)), forced_size):
            expected = _brute_partition_distribution(
                4, edges, frozenset(forced)
            )
            actual = forward_partition_distribution(4, edges, forced)
            assert actual == expected


def test_false_twin_transfer_preserves_edge_subset_multiplicity() -> None:
    discrete = dict(
        false_twin_partition_transitions((0, 1, 2), (0, 1))
    )
    repeated_block = dict(
        false_twin_partition_transitions((0, 0, 1), (0, 1, 2))
    )

    assert discrete == {
        (0, 0, 1): 1,
        (0, 1, 2): 3,
    }
    assert repeated_block == {
        (0, 0, 0): 2,
        (0, 0, 1): 4,
    }


def test_scan_matches_independent_full_graph_bruteforce() -> None:
    base_edges = ((0, 1), (0, 2), (1, 2))
    base_graph6 = encode_simple_graph6(3, base_edges)
    scan = scan_false_twin_family(
        base_graph6,
        (0, 1),
        (0, 2),
        max_twins=2,
    )

    for record in scan.counts:
        expected = _brute_family_counts(
            3,
            base_edges,
            (0, 1),
            (0, 2),
            record.twin_count,
        )
        assert (
            record.forest_count,
            record.forest_count_e,
            record.forest_count_f,
            record.forest_count_ef,
        ) == expected


def test_false_twin_family_matches_recursive_regression_through_t4() -> None:
    scan = scan_false_twin_family(
        FALSE_TWIN_BASE,
        FALSE_TWIN_PAIR,
        FALSE_TWIN_NEIGHBOURHOOD,
        max_twins=4,
    )

    assert len(scan.counts) == 5
    assert scan.edge_pair_endpoints == ((0, 4), (2, 5))
    assert [
        (
            record.forest_count,
            record.forest_count_e,
            record.forest_count_f,
            record.forest_count_ef,
        )
        for record in scan.counts
    ] == list(DELETION_CONTRACTION_REGRESSION)
    assert [record.margin for record in scan.counts] == [
        22_680,
        1_409_616,
        82_470_960,
        4_598_664_192,
        246_584_424_960,
    ]


def test_exact_scan_to_t100_stays_below_one_and_closes_the_gap() -> None:
    scan = scan_false_twin_family(
        FALSE_TWIN_BASE,
        FALSE_TWIN_PAIR,
        FALSE_TWIN_NEIGHBOURHOOD,
        max_twins=100,
    )

    assert len(scan.counts) == 101
    assert not scan.has_violation
    assert scan.ratios_strictly_increase
    assert scan.relative_gaps_strictly_decrease
    assert scan.minimum_relative_gap.twin_count == 100
    assert scan.minimum_relative_gap.margin > 0
    assert {record.active_partitions for record in scan.counts} == {3430}
    assert scan.cached_partitions == 3430
    assert scan.cached_transition_arcs == 22_380
    for twin_count in (0, 1, 2, 3, 4, 5, 10, 25, 100):
        record = scan.counts[twin_count]
        assert closed_form_count_vector(twin_count) == (
            record.forest_count,
            record.forest_count_e,
            record.forest_count_f,
            record.forest_count_ef,
        )
        assert closed_form_margin(twin_count) == record.margin


def test_krylov_certificate_exports_exact_formula_and_vector_identity(
    family_a_certificate: dict[str, object],
) -> None:
    recurrence = family_a_certificate["krylov_recurrence"]
    assert recurrence["operator_polynomial"] == "(E-6)^5"
    assert recurrence["coefficients"] == list(
        KRYLOV_RECURRENCE_COEFFICIENTS
    )
    assert recurrence["partition_count"] == 3430
    assert recurrence["coordinate_count"] == 13_720
    assert recurrence["nonzero_residual_coordinates"] == 0
    assert [row["t"] for row in recurrence["vectors"]] == list(range(6))

    forms = family_a_certificate["closed_forms"]
    assert forms["forest_count"]["expression"] == (
        "6^t*(875*t^4+29570*t^3+366609*t^2+"
        "1974866*t+3896928)/72"
    )
    assert forms["forest_count_e"]["expression"] == (
        "6^t*(625*t^4+21250*t^3+264867*t^2+"
        "1433530*t+2840544)/144"
    )
    assert forms["forest_count_f"]["expression"] == (
        "6^t*(875*t^4+30970*t^3+401713*t^2+"
        "2259386*t+4643136)/216"
    )
    assert forms["forest_count_ef"]["expression"] == (
        "6^t*(625*t^4+22250*t^3+290147*t^2+"
        "1639762*t+3384288)/432"
    )
    assert [
        forms[name]["integrality"]["power_divisibility_from_t"]
        for name in (
            "forest_count",
            "forest_count_e",
            "forest_count_f",
            "forest_count_ef",
        )
    ] == [3, 4, 3, 4]
    for form in forms.values():
        assert not any(
            row["numerator_mod_denominator"]
            for row in form["integrality"]["prethreshold_remainders"]
        )
        assert form["symbolic_recurrence_residual_coefficients"] == [
            0,
            0,
            0,
            0,
            0,
        ]

    margin = family_a_certificate["margin"]
    assert margin["expression"] == (
        "36^t*(25*t^5+1616*t^4+33749*t^3+319228*t^2+"
        "1424790*t+2449440)/108"
    )
    assert margin["all_polynomial_coefficients_strictly_positive"]
    assert margin["integrality"]["power_divisibility_from_t"] == 2
    verification = family_a_certificate["closed_form_verification"]
    assert verification["initial_match_t"] == [0, 1, 2, 3, 4]
    assert [
        row["t"] for row in verification["direct_transfer_samples"]
    ] == [0, 1, 2, 3, 4, 5, 10, 25, 100]
    assert verification["large_t_audit"] == {
        "t": 10_000,
        "count_recurrence_residuals": [0, 0, 0, 0],
        "margin_identity_residual": 0,
        "denominator_remainders": [0, 0, 0, 0, 0],
        "margin_strictly_positive": True,
        "large_values_omitted": True,
    }


def test_closed_forms_are_integral_and_positive_at_large_t() -> None:
    for twin_count in (0, 1, 2, 3, 4, 100, 10_000):
        total, edge_e, edge_f, pair = closed_form_count_vector(
            twin_count
        )
        margin = closed_form_margin(twin_count)
        assert min(total, edge_e, edge_f, pair, margin) > 0
        assert edge_e * edge_f - total * pair == margin


@pytest.mark.parametrize(
    ("case_index", "expected_margin"),
    [
        (
            1,
            "36^t*(100*t^5+6449*t^4+127724*t^3+1126195*t^2+"
            "4644108*t+7348320)/243",
        ),
        (
            2,
            "36^t*(100*t^5+6449*t^4+127256*t^3+1118455*t^2+"
            "4602420*t+7278336)/243",
        ),
    ],
)
def test_generic_certificate_derives_other_registered_families(
    case_index: int,
    expected_margin: str,
) -> None:
    case = CERTIFIED_FALSE_TWIN_CASES[case_index]
    certificate = build_krylov_recurrence_certificate(
        case.base_graph6,
        case.edge_pair,
        case.neighbourhood,
    )

    assert certificate["instance"]["registered_case_id"] == case.case_id
    assert certificate["krylov_recurrence"][
        "nonzero_residual_coordinates"
    ] == 0
    assert certificate["krylov_recurrence"]["partition_count"] == 4035
    assert certificate["margin"]["expression"] == expected_margin
    assert certificate["margin"][
        "all_polynomial_coefficients_strictly_positive"
    ]
    assert certificate["conclusion"][
        "strict_for_every_nonnegative_integer_t"
    ]
    assert certificate["conclusion"][
        "selected_inherited_edge_pair_is_never_a_counterexample"
    ]
    assert certificate["conclusion"]["all_edge_pairs_checked"] is False
    assert certificate["conclusion"][
        "whole_graph_family_counterexample_exhaustion_claimed"
    ] is False


def test_certificate_generation_fails_closed_on_bad_transfer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def identity_transition(partition, neighbourhood):
        del neighbourhood
        return ((tuple(partition), 1),)

    monkeypatch.setattr(
        twin_transfer,
        "false_twin_partition_transitions",
        identity_transition,
    )
    with pytest.raises(
        FalseTwinCertificateError,
        match="Krylov residual is nonzero",
    ):
        build_krylov_recurrence_certificate()


def test_tampered_certificate_is_not_written(
    tmp_path: Path,
    family_a_certificate: dict[str, object],
) -> None:
    tampered = copy.deepcopy(family_a_certificate)
    tampered["krylov_recurrence"]["coefficients"][0] += 1
    output = tmp_path / "certificate.json"
    output.write_text("sentinel\n", encoding="utf-8")

    with pytest.raises(
        FalseTwinCertificateError,
        match="does not exactly match",
    ):
        write_krylov_recurrence_certificate(output, tampered)

    assert output.read_text(encoding="utf-8") == "sentinel\n"
    assert not list(tmp_path.glob(".certificate.json.*.tmp"))


def test_certificate_cli_atomically_writes_verified_json(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = tmp_path / "nested" / "certificate.json"
    assert twin_transfer.main(
        ["certify", "--output", str(output)]
    ) == 0
    summary = json.loads(capsys.readouterr().out)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert summary == {
        "coordinate_count": 13_720,
        "output": str(output),
        "partition_count": 3430,
        "status": "certified",
    }
    assert payload["status"] == "certified"
    assert payload["krylov_recurrence"][
        "nonzero_residual_coordinates"
    ] == 0
    assert output.stat().st_mode & 0o777 == 0o644
    assert not list(output.parent.glob(".certificate.json.*.tmp"))


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (
            lambda: forward_partition_distribution(
                2, ((0, 2),)
            ),
            "outside the vertex set",
        ),
        (
            lambda: forward_partition_distribution(
                2, ((0, 1),), (0, 0)
            ),
            "must be distinct",
        ),
        (
            lambda: false_twin_partition_transitions(
                (0, 2), (0,)
            ),
            "restricted-growth",
        ),
        (
            lambda: false_twin_partition_transitions(
                (0, 1), (0, 0)
            ),
            "must be distinct",
        ),
        (
            lambda: scan_false_twin_family(
                FALSE_TWIN_BASE,
                (0, 0),
                FALSE_TWIN_NEIGHBOURHOOD,
            ),
            "two distinct",
        ),
        (
            lambda: scan_false_twin_family(
                FALSE_TWIN_BASE,
                FALSE_TWIN_PAIR,
                FALSE_TWIN_NEIGHBOURHOOD,
                max_twins=-1,
            ),
            "non-negative",
        ),
    ],
)
def test_invalid_transfer_inputs_are_rejected(call, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()
