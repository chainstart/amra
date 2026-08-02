"""Regression tests for the leading-block deficit theorem."""

from verify_leading_block_deficit_theorem import (
    check_asymptotic_tails,
    check_double_negative_to_single_borrow_base,
    check_loss_transport,
    check_rank_three_convolution_base,
    check_rank_two_convolution_base,
)


def test_loss_transport() -> None:
    result = check_loss_transport()
    assert result["transport_pairs_checked"] > 100_000
    assert result["minimum_deficit_slack"] == 0
    assert result["minimum_vertical_slack"] == 0


def test_rank_two_convolution_base() -> None:
    result = check_rank_two_convolution_base()
    assert result["range"] == [32, 421]
    assert result["minimum_margin"] == 178


def test_rank_three_convolution_base() -> None:
    result = check_rank_three_convolution_base()
    assert result["range"] == [32, 277]
    assert result["minimum_margin"] == 258


def test_asymptotic_tails() -> None:
    result = check_asymptotic_tails()
    assert result["rank_two_tail_starts"] == 422
    assert result["rank_three_tail_starts"] == 278


def test_double_negative_to_single_borrow_base() -> None:
    result = check_double_negative_to_single_borrow_base()
    assert result["q_range"] == [2, 215]
    assert result["target_points"] == 1
    assert result["unique_witness"][:6] == [4923, 35, 13, 0, 48, 244]
    assert result["double_borrow_points"] == 3
    assert result["double_borrow_minimum"][:7] == [
        4222,
        1236,
        34,
        13,
        0,
        47,
        238,
    ]
