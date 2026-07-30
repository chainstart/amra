from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_three_star_closure as closure
from amra.discovery.opg_coloring_search import decode_graph6
from amra.discovery.opg_uniform_forest_twin_transfer import (
    DEFAULT_FALSE_TWIN_BASE_GRAPH6,
    DEFAULT_FALSE_TWIN_EDGE_PAIR,
    FalseTwinCertificateError,
    _advance_false_twin_distribution,
    _combine_forced_distributions,
    _distribution_digest,
)


@pytest.fixture(scope="module")
def certificate() -> dict[str, object]:
    return closure.build_three_star_high_risk_certificate()


def test_fixed_high_risk_masks_are_the_inherited_edge_endpoints() -> None:
    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    assert closure._neighbourhood_from_mask(
        closure.FIXED_FIRST_STAR_MASK
    ) == graph.edges[DEFAULT_FALSE_TWIN_EDGE_PAIR[0]]
    assert closure._neighbourhood_from_mask(
        closure.FIXED_SECOND_STAR_MASK
    ) == graph.edges[DEFAULT_FALSE_TWIN_EDGE_PAIR[1]]


def test_the_two_fixed_star_transfers_commute_exactly() -> None:
    graph = decode_graph6(DEFAULT_FALSE_TWIN_BASE_GRAPH6)
    base = _combine_forced_distributions(
        graph, DEFAULT_FALSE_TWIN_EDGE_PAIR
    )
    first = closure._neighbourhood_from_mask(
        closure.FIXED_FIRST_STAR_MASK
    )
    second = closure._neighbourhood_from_mask(
        closure.FIXED_SECOND_STAR_MASK
    )
    forward = _advance_false_twin_distribution(base, first, {})
    forward = _advance_false_twin_distribution(forward, second, {})
    reverse = _advance_false_twin_distribution(base, second, {})
    reverse = _advance_false_twin_distribution(reverse, first, {})
    assert forward == reverse
    assert _distribution_digest(forward) == (
        "f7d6e18283a901db2956d8b9a789cdf8f3269a90f11317ca01751d31496f4f3c"
    )


def test_complete_three_star_certificate_summary(
    certificate: dict[str, object],
) -> None:
    assert certificate["schema"] == closure.CERTIFICATE_SCHEMA
    assert certificate["status"] == "certified"
    scope = certificate["scope"]
    assert scope["fixed_first_star_mask"] == 17
    assert scope["fixed_second_star_mask"] == 36
    assert scope["all_edge_pairs_checked"] is False
    summary = certificate["summary"]
    assert summary == {
        "third_star_neighbourhood_count": 512,
        "expected_third_star_neighbourhood_count": 512,
        "all_margin_coefficients_strictly_positive": True,
        "minimum_margin_polynomial_coefficient": 75,
        "margin_polynomial_degree_histogram": {
            "5": 120,
            "8": 192,
            "6": 200,
        },
        "all_t5_holdouts_match": True,
        "selected_inherited_pair_is_never_a_counterexample": True,
        "all_edge_pairs_checked": False,
        "whole_graph_family_counterexample_exhaustion_claimed": False,
    }
    assert len(certificate["records"]) == 512
    assert [
        record["third_star_mask"]
        for record in certificate["records"]
    ] == list(range(512))


def test_coordinate_recurrence_and_t5_holdouts_are_exact(
    certificate: dict[str, object],
) -> None:
    recurrence = certificate["krylov_recurrence"]
    assert recurrence["annihilator"] == "(T_S-6I)^5"
    assert recurrence["coordinate_count"] == 13_720
    assert recurrence["nonzero_residual_coordinates"] == 0
    assert recurrence["maximum_absolute_residual"] == 0
    assert recurrence["residual_rows_sha256"] == (
        "cbfae6618136de5177321c1f81fe35511efb96bed7b6c7190a8cf45d5e25d951"
    )
    for record in certificate["records"]:
        assert record["t5_holdout_matches"] is True
        assert all(
            coefficient > 0
            for coefficient in record["margin_closed_form"][
                "polynomial_coefficients"
            ]
        )


def test_large_t_closest_third_star_is_a_second_mask_17(
    certificate: dict[str, object],
) -> None:
    samples = {
        record["twin_count"]: record
        for record in certificate["ratio_sample_maxima"]
    }
    assert samples[10_000]["third_star_mask"] == 17
    assert samples[10_000]["third_star_neighbourhood"] == [0, 4]
    assert int(samples[10_000]["relative_gap_numerator"]) > 0
    assert (
        int(samples[10_000]["ratio_numerator"])
        < int(samples[10_000]["ratio_denominator"])
    )


def test_verifier_rejects_tampering_without_trusting_the_payload(
    certificate: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pristine = copy.deepcopy(certificate)
    monkeypatch.setattr(
        closure,
        "build_three_star_high_risk_certificate",
        lambda: pristine,
    )
    tampered = copy.deepcopy(certificate)
    tampered["records"][17]["margin_closed_form"][
        "polynomial_coefficients"
    ][0] += 1
    with pytest.raises(
        FalseTwinCertificateError,
        match="differs from exact recomputation",
    ):
        closure.verify_three_star_high_risk_certificate(tampered)


def test_atomic_write_can_be_reloaded_and_verified(
    certificate: dict[str, object],
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    pristine = copy.deepcopy(certificate)
    monkeypatch.setattr(
        closure,
        "build_three_star_high_risk_certificate",
        lambda: pristine,
    )
    output = tmp_path / "certificate.json"
    closure.write_three_star_high_risk_certificate(output, pristine)
    reloaded = json.loads(output.read_text(encoding="utf-8"))
    closure.verify_three_star_high_risk_certificate(reloaded)
    assert reloaded == pristine
