from __future__ import annotations

import copy
import json
from itertools import combinations, product
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_twin_defect as twin_defect
from amra.discovery.opg_coloring_search import EdgeGraph, decode_graph6
from amra.discovery.opg_uniform_forest_search import (
    brute_force_forest_statistics,
)
from amra.discovery.opg_uniform_forest_twin_defect import (
    build_terminal_defect_survey,
    terminal_defect_count_vector,
    terminal_star_subset_multiplier,
    write_terminal_defect_survey,
)
from amra.discovery.opg_uniform_forest_twin_transfer import (
    DEFAULT_FALSE_TWIN_BASE_GRAPH6,
    DEFAULT_FALSE_TWIN_EDGE_PAIR,
    DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
    FalseTwinCertificateError,
    _advance_false_twin_distribution,
    _combine_forced_distributions,
    false_twin_partition_transitions,
)


@pytest.fixture(scope="module")
def terminal_defect_survey() -> dict[str, object]:
    return build_terminal_defect_survey()


def _restricted_growth_partitions(
    vertex_count: int,
) -> tuple[tuple[int, ...], ...]:
    partitions = []
    for labels in product(range(vertex_count), repeat=vertex_count):
        canonical: dict[int, int] = {}
        normalized = []
        for label in labels:
            if label not in canonical:
                canonical[label] = len(canonical)
            normalized.append(canonical[label])
        if tuple(normalized) == labels:
            partitions.append(labels)
    return tuple(partitions)


def _explicit_terminal_subset_count(
    partition: tuple[int, ...],
    neighbourhood: tuple[int, ...],
) -> int:
    valid = 0
    for subset_size in range(len(neighbourhood) + 1):
        for selected in combinations(neighbourhood, subset_size):
            labels = [partition[vertex] for vertex in selected]
            if len(labels) == len(set(labels)):
                valid += 1
    return valid


def test_terminal_multiplier_matches_subsets_and_transfer_multiplicity() -> None:
    for vertex_count in range(1, 5):
        for partition in _restricted_growth_partitions(vertex_count):
            for mask in range(1 << vertex_count):
                neighbourhood = tuple(
                    vertex
                    for vertex in range(vertex_count)
                    if mask & (1 << vertex)
                )
                expected = _explicit_terminal_subset_count(
                    partition, neighbourhood
                )
                actual = terminal_star_subset_multiplier(
                    partition, neighbourhood
                )
                transition_total = sum(
                    multiplicity
                    for _, multiplicity in false_twin_partition_transitions(
                        partition, neighbourhood
                    )
                )
                assert actual == expected
                assert transition_total == expected


def _brute_count_vector(
    vertex_count: int,
    edges: tuple[tuple[int, int], ...],
    edge_pair: tuple[int, int],
) -> tuple[int, int, int, int]:
    statistics = brute_force_forest_statistics(vertex_count, edges)
    first, second = edge_pair
    return (
        statistics.forest_count,
        statistics.edge_forest_counts[first],
        statistics.edge_forest_counts[second],
        statistics.pair_forest_counts[first][second],
    )


def test_terminal_projection_matches_independent_full_graph_bruteforce() -> None:
    base_edges = ((0, 1), (0, 2), (1, 2))
    base_graph = EdgeGraph(3, base_edges, "small-triangle")
    edge_pair = (0, 1)
    twin_neighbourhood = (0, 2)
    defect_neighbourhood = (0, 1, 2)
    distribution = _combine_forced_distributions(base_graph, edge_pair)
    transition_cache = {}

    for twin_count in range(3):
        terminal_vertex = base_graph.vertex_count + twin_count
        edges = list(base_edges)
        for offset in range(twin_count):
            twin_vertex = base_graph.vertex_count + offset
            edges.extend(
                (base_vertex, twin_vertex)
                for base_vertex in twin_neighbourhood
            )
        edges.extend(
            (base_vertex, terminal_vertex)
            for base_vertex in defect_neighbourhood
        )
        expected = _brute_count_vector(
            terminal_vertex + 1, tuple(edges), edge_pair
        )
        assert terminal_defect_count_vector(
            distribution, defect_neighbourhood
        ) == expected

        distribution = _advance_false_twin_distribution(
            distribution,
            twin_neighbourhood,
            transition_cache,
        )


def test_complete_survey_has_expected_exact_shape_and_strict_scope(
    terminal_defect_survey: dict[str, object],
) -> None:
    summary = terminal_defect_survey["summary"]
    assert summary == {
        "neighbourhood_count": 512,
        "expected_neighbourhood_count": 512,
        "all_margin_coefficients_strictly_positive": True,
        "minimum_margin_polynomial_coefficient": 25,
        "margin_polynomial_degree_histogram": {
            "5": 120,
            "6": 200,
            "8": 192,
        },
        "selected_inherited_pair_is_never_a_counterexample": True,
        "all_edge_pairs_checked": False,
        "defects_joining_repeated_twins_checked": False,
        "whole_graph_family_counterexample_exhaustion_claimed": False,
    }

    construction = terminal_defect_survey["construction"]
    assert construction["terminal_defect_may_join_repeated_twins"] is False
    assert construction["repeated_false_twin_count"] == (
        "arbitrary integer t >= 0"
    )
    records = terminal_defect_survey["records"]
    assert [row["mask"] for row in records] == list(range(512))
    for row in records:
        expected_neighbourhood = [
            vertex
            for vertex in range(9)
            if row["mask"] & (1 << vertex)
        ]
        assert row["neighbourhood"] == expected_neighbourhood
        margin = row["margin"]
        assert margin["power_base"] == 36
        assert margin["denominator"] > 0
        assert min(margin["polynomial_coefficients"]) > 0
        assert not any(
            margin["symbolic_annihilator_residual_coefficients"]
        )


def _evaluate_recorded_form(
    form: dict[str, object],
    twin_count: int,
) -> int:
    polynomial = sum(
        coefficient * twin_count**degree
        for degree, coefficient in enumerate(
            form["polynomial_coefficients"]
        )
    )
    numerator = form["power_base"] ** twin_count * polynomial
    quotient, remainder = divmod(numerator, form["denominator"])
    assert remainder == 0
    return quotient


def test_representative_closed_forms_predict_unfitted_t5_projection(
    terminal_defect_survey: dict[str, object],
) -> None:
    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    distribution = _combine_forced_distributions(
        graph, DEFAULT_FALSE_TWIN_EDGE_PAIR
    )
    transition_cache = {}
    for _ in range(5):
        distribution = _advance_false_twin_distribution(
            distribution,
            DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
            transition_cache,
        )

    representatives = {}
    for record in terminal_defect_survey["records"]:
        degree = record["margin"]["polynomial_degree"]
        representatives.setdefault(degree, record)
    assert set(representatives) == {5, 6, 8}

    for record in representatives.values():
        direct = terminal_defect_count_vector(
            distribution, tuple(record["neighbourhood"])
        )
        forms = record["count_closed_forms"]
        projected = tuple(
            _evaluate_recorded_form(forms[name], 5)
            for name in (
                "forest_count",
                "forest_count_e",
                "forest_count_f",
                "forest_count_ef",
            )
        )
        assert projected == direct
        margin = direct[1] * direct[2] - direct[0] * direct[3]
        assert _evaluate_recorded_form(record["margin"], 5) == margin
        assert margin > 0


def test_tampered_survey_is_rejected_before_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    terminal_defect_survey: dict[str, object],
) -> None:
    pristine = copy.deepcopy(terminal_defect_survey)
    monkeypatch.setattr(
        twin_defect,
        "build_terminal_defect_survey",
        lambda: copy.deepcopy(pristine),
    )
    tampered = copy.deepcopy(pristine)
    tampered["summary"]["all_edge_pairs_checked"] = True
    output = tmp_path / "certificate.json"
    output.write_text("sentinel\n", encoding="utf-8")

    with pytest.raises(
        FalseTwinCertificateError,
        match="differs from exact recomputation",
    ):
        write_terminal_defect_survey(output, tampered)

    assert output.read_text(encoding="utf-8") == "sentinel\n"
    assert not list(tmp_path.glob(".certificate.json.*.tmp"))


def test_certificate_cli_writes_and_verifies_atomically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    terminal_defect_survey: dict[str, object],
) -> None:
    pristine = copy.deepcopy(terminal_defect_survey)
    monkeypatch.setattr(
        twin_defect,
        "build_terminal_defect_survey",
        lambda: copy.deepcopy(pristine),
    )
    output = tmp_path / "nested" / "certificate.json"

    assert twin_defect.main(
        ["certify", "--output", str(output)]
    ) == 0
    certify_summary = json.loads(capsys.readouterr().out)
    assert certify_summary == {
        "neighbourhood_count": 512,
        "output": str(output),
        "status": "certified",
    }
    assert json.loads(output.read_text(encoding="utf-8")) == pristine
    assert output.stat().st_mode & 0o777 == 0o644
    assert not list(output.parent.glob(".certificate.json.*.tmp"))

    assert twin_defect.main(["verify", str(output)]) == 0
    verify_summary = json.loads(capsys.readouterr().out)
    assert verify_summary == {
        "certificate": str(output),
        "neighbourhood_count": 512,
        "status": "verified",
    }
