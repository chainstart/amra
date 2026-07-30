from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from amra.discovery import opg_uniform_forest_two_star_defect as two_star
from amra.discovery.opg_coloring_search import decode_graph6
from amra.discovery.opg_uniform_forest_two_star_defect import (
    BASE_GRAPH6,
    CERTIFICATE_SCHEMA,
    EXPECTED_CATEGORY_COUNTS,
    KERNEL_BASE_EDGES,
    TwoStarCertificateError,
    build_two_star_certificate,
    verify_two_star_certificate,
    write_two_star_certificate,
)
from amra.discovery.opg_uniform_forest_twin_transfer import (
    DEFAULT_FALSE_TWIN_EDGE_PAIR,
    DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
    _advance_false_twin_distribution,
    _combine_forced_distributions,
    _distribution_totals,
)


@pytest.fixture(scope="module")
def two_star_certificate() -> dict[str, object]:
    return build_two_star_certificate()


def test_graph6_scope_exactly_matches_standalone_kernel() -> None:
    assert two_star._decode_compact_graph6(BASE_GRAPH6) == (
        KERNEL_BASE_EDGES
    )
    assert tuple(
        KERNEL_BASE_EDGES[index]
        for index in two_star.INHERITED_EDGE_PAIR
    ) == ((0, 4), (2, 5))
    assert two_star._mask_neighbourhood(17) == (0, 4)
    assert two_star._mask_neighbourhood(36) == (2, 5)


def test_known_closest_margin_newton_form_is_exact() -> None:
    count_newton = (
        (801_726_336, 485_029_728, 187_683_984, 42_274_800, 4_230_000),
        (260_542_656, 156_917_088, 60_447_600, 13_554_000, 1_350_000),
        (281_187_936, 162_994_032, 60_583_680, 13_139_280, 1_269_000),
        (91_375_776, 52_725_168, 19_508_688, 4_212_000, 405_000),
    )
    margin_newton = two_star._margin_binomial_coefficients(
        count_newton
    )
    assert margin_newton == (
        3_085_588_961_280,
        2_241_541_610_496,
        1_088_799_314_688,
        333_093_047_040,
        56_414_942_208,
        3_779_136_000,
        0,
        0,
        0,
    )
    margin = two_star._newton_to_closed_form(
        margin_newton,
        power_base=36,
        normalization=two_star.MARGIN_NORMALIZATION,
    )
    assert margin.denominator == 4
    assert margin.polynomial_coefficients == (
        7_348_320,
        4_274_370,
        957_684,
        101_247,
        4_848,
        75,
    )
    assert margin.evaluate(0) == 1_837_080
    assert all(margin.evaluate(twin_count) > 0 for twin_count in range(9))


def test_complete_certificate_binds_all_unordered_mask_pairs(
    two_star_certificate: dict[str, object],
) -> None:
    assert two_star_certificate["schema"] == CERTIFICATE_SCHEMA
    assert two_star_certificate["status"] == "certified"
    scope = two_star_certificate["scope"]
    assert scope["unordered_neighbourhood_pair_count"] == 131_328
    assert scope["additional_star_vertex_count"] == 2
    assert scope["edges_among_all_added_vertices"] == 0
    assert scope["all_edge_pairs_checked"] is False
    assert scope["certified_edge_pair"] == "the inherited edge pair only"

    summary = two_star_certificate["summary"]
    assert summary["category_counts"] == EXPECTED_CATEGORY_COUNTS
    assert (
        summary["all_pairs_have_strictly_positive_margin_for_all_t"]
        is True
    )
    assert (
        summary["selected_inherited_pair_is_never_a_counterexample"]
        is True
    )
    assert (
        summary["whole_graph_family_counterexample_exhaustion_claimed"]
        is False
    )

    completeness = two_star_certificate["completeness"]
    assert completeness["row_count"] == 131_328
    assert completeness["column_count"] == 22
    assert completeness["legal_selected_edge_pair_count"] == 20_823_456
    assert completeness["binary_output_sha256"] == (
        "44989aed15c994b7471ae2dbab4be840"
        "2e89bb38abcaea8510fbd9e441277efa"
    )
    assert completeness["canonical_record_sha256"] == (
        "30307520b1555b0e5af4b8a680a28b8"
        "dc8a30e6bee4a7e4780d183f6aecdead6"
    )


def test_sample_frontier_and_closest_formula_are_stable(
    two_star_certificate: dict[str, object],
) -> None:
    samples = {
        row["twin_count"]: (row["first_mask"], row["second_mask"])
        for row in two_star_certificate["ratio_sample_maxima"]
    }
    assert samples == {
        0: (490, 490),
        1: (490, 490),
        2: (490, 490),
        4: (490, 490),
        10: (409, 409),
        25: (409, 409),
        100: (409, 409),
        187: (17, 36),
        1000: (17, 36),
        10_000: (17, 36),
    }
    closest = two_star_certificate["closest_family"]
    assert (closest["first_mask"], closest["second_mask"]) == (17, 36)
    assert closest["first_neighbourhood"] == [0, 4]
    assert closest["second_neighbourhood"] == [2, 5]
    assert closest["margin_closed_form"] == {
        "power_base": 36,
        "denominator": 4,
        "polynomial_coefficients": [
            7_348_320,
            4_274_370,
            957_684,
            101_247,
            4_848,
            75,
        ],
    }
    assert closest["ratio_increment_certificate"][
        "all_coefficients_strictly_positive"
    ] is True
    assert closest["asymptotic_relative_gap"] == {
        "coefficient_numerator": 7776,
        "coefficient_denominator": 734375,
        "power_of_t": -3,
        "statement": "1-ratio(t) ~ (7776/734375)*t^(-3)",
    }


def test_closest_count_forms_match_independent_transfer_dp(
    two_star_certificate: dict[str, object],
) -> None:
    graph = decode_graph6(BASE_GRAPH6)
    distribution = _combine_forced_distributions(
        graph,
        DEFAULT_FALSE_TWIN_EDGE_PAIR,
    )
    for neighbourhood in ((0, 4), (2, 5)):
        distribution = _advance_false_twin_distribution(
            distribution,
            neighbourhood,
            {},
        )
    closest = two_star_certificate["closest_family"]
    forms = closest["count_closed_forms"]
    transfer_cache = {}
    for twin_count in range(5):
        direct = _distribution_totals(distribution)
        formula = tuple(
            two_star.CountClosedForm(
                form["power_base"],
                form["denominator"],
                tuple(form["polynomial_coefficients"]),
            ).evaluate(twin_count)
            for form in (
                forms["forest_count"],
                forms["forest_count_e"],
                forms["forest_count_f"],
                forms["forest_count_ef"],
            )
        )
        assert formula == direct
        if twin_count < 4:
            distribution = _advance_false_twin_distribution(
                distribution,
                DEFAULT_FALSE_TWIN_NEIGHBOURHOOD,
                transfer_cache,
            )


def test_invalid_kernel_output_fails_closed(tmp_path: Path) -> None:
    path = tmp_path / "bad.bin"
    path.write_bytes(b"not-a-kernel-output")
    with pytest.raises(
        TwoStarCertificateError,
        match="magic is invalid",
    ):
        two_star._read_kernel_rows(path)


def test_tampered_certificate_is_rejected_before_write(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    two_star_certificate: dict[str, object],
) -> None:
    pristine = copy.deepcopy(two_star_certificate)
    monkeypatch.setattr(
        two_star,
        "build_two_star_certificate",
        lambda: copy.deepcopy(pristine),
    )
    tampered = copy.deepcopy(pristine)
    tampered["scope"]["all_edge_pairs_checked"] = True
    output = tmp_path / "certificate.json"
    output.write_text("sentinel\n", encoding="utf-8")

    with pytest.raises(
        TwoStarCertificateError,
        match="differs from exact recomputation",
    ):
        write_two_star_certificate(output, tampered)

    assert output.read_text(encoding="utf-8") == "sentinel\n"
    assert not list(tmp_path.glob(".certificate.json.*.tmp"))


def test_persisted_json_is_reloaded_and_verified(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    two_star_certificate: dict[str, object],
) -> None:
    pristine = copy.deepcopy(two_star_certificate)
    monkeypatch.setattr(
        two_star,
        "build_two_star_certificate",
        lambda: copy.deepcopy(pristine),
    )
    output = tmp_path / "nested" / "certificate.json"

    write_two_star_certificate(output, pristine)
    reloaded = json.loads(output.read_text(encoding="utf-8"))
    verify_two_star_certificate(reloaded)
    assert reloaded == pristine
    assert output.stat().st_mode & 0o777 == 0o644


def test_certificate_cli_round_trip_with_exact_payload(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    two_star_certificate: dict[str, object],
) -> None:
    pristine = copy.deepcopy(two_star_certificate)
    monkeypatch.setattr(
        two_star,
        "build_two_star_certificate",
        lambda: copy.deepcopy(pristine),
    )
    output = tmp_path / "certificate.json"

    assert two_star.main(
        ["certify", "--output", str(output)]
    ) == 0
    assert json.loads(capsys.readouterr().out) == {
        "output": str(output),
        "status": "certified",
        "unordered_neighbourhood_pair_count": 131_328,
    }
    assert two_star.main(["verify", str(output)]) == 0
    assert json.loads(capsys.readouterr().out) == {
        "certificate": str(output),
        "status": "verified",
        "unordered_neighbourhood_pair_count": 131_328,
    }
