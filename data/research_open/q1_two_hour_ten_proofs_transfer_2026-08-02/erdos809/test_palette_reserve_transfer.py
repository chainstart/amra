"""Regression tests for the ten-proofs palette/reserve transfer test."""

from verify_palette_reserve_transfer import (
    certificate,
    matching_outer_label_words,
    sharp_palette_row,
)


def test_first_even_and_odd_rows() -> None:
    even = sharp_palette_row(4, "even")
    assert (even["n"], even["delta"], even["maximum"]) == (18, 6, 10)
    odd = sharp_palette_row(4, "odd")
    assert (odd["n"], odd["delta"], odd["maximum"]) == (21, 7, 11)


def test_every_colour_graph_is_two_labelled() -> None:
    for g in (4, 5, 8, 13):
        for parity in ("even", "odd"):
            row = sharp_palette_row(g, parity)
            assert row["largest_colour_class"] == 2
            assert row["maximum_colour_degree"] == 1
            assert row["maximum_colour_chromatic_number"] == 2
            assert row["maximum_colour_degeneracy"] == 1
            assert row["defect"] == g


def test_repeated_palettes_have_distinct_reserve_tokens() -> None:
    for g in (4, 7, 12):
        for parity in ("even", "odd"):
            row = sharp_palette_row(g, parity)
            assert row["reserve"] >= row["defect"]
            assert row["injected_reserve_tokens"] == row["defect"]


def test_matching_labels_have_full_edge_flip_gauge() -> None:
    for edge_count in range(11):
        words = matching_outer_label_words(edge_count)
        assert len(words) == 2**edge_count
        assert (0,) * edge_count in words
        assert (1,) * edge_count in words


def test_full_parameter_certificate() -> None:
    result = certificate(max_g=20)
    assert result["parameter_rows"] == 34
    assert result["repeated_classes_checked"] == 408
    assert result["reserve_injections_checked"] == 408
    assert result["matching_gauge_words_checked"] == 2047
    assert result["pass"]
