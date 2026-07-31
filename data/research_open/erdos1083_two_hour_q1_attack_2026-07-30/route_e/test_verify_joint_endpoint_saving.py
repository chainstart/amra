from fractions import Fraction

import pytest

from verify_joint_endpoint_saving import (
    branch_certificate,
    conditional_threshold,
    endpoint_certificate,
    service_saturation_model,
)


def test_endpoint_joint_equality() -> None:
    cert = endpoint_certificate()
    assert cert["kappa"] == Fraction(2, 9)
    assert cert["joint_left"] == Fraction(82, 9)
    assert cert["joint_left"] == cert["joint_right"]


def test_exact_service_saturation() -> None:
    cert = service_saturation_model(6, 8, 4)
    assert cert["circle_count"] == 48
    assert cert["target_count"] == 32
    assert cert["label_count"] == 9
    assert cert["producer_count"] == 192
    assert cert["producer_count"] == cert["service_cap"]
    assert set(cert["circle_multiplicities"].values()) == {4}
    assert set(cert["target_service_degrees"].values()) == {6}


@pytest.mark.parametrize(
    ("delta", "expected_improvement"),
    [
        (Fraction(1, 18), Fraction(1, 324)),
        (Fraction(1, 2), Fraction(1, 36)),
        (Fraction(1), Fraction(1, 18)),
    ],
)
def test_threshold_gain(
    delta: Fraction,
    expected_improvement: Fraction,
) -> None:
    cert = conditional_threshold(delta)
    assert cert["improvement"] == expected_improvement
    assert cert["threshold"] == Fraction(2, 9) + expected_improvement
    assert cert["q_branch_separation"] > 0


def test_main_branch_crosses_at_conditional_threshold() -> None:
    delta = Fraction(1, 2)
    threshold = conditional_threshold(delta)["threshold"]
    before = branch_certificate(threshold - Fraction(1, 1000), delta)
    at = branch_certificate(threshold, delta)
    after = branch_certificate(threshold + Fraction(1, 1000), delta)
    assert before["main_gap"] > 0
    assert at["main_gap"] == 0
    assert after["main_gap"] < 0


def test_q_branch_is_still_excluded_at_main_crossing() -> None:
    delta = Fraction(1, 2)
    threshold = conditional_threshold(delta)["threshold"]
    cert = branch_certificate(threshold, delta)
    assert cert["q_branch_gap"] == (13 + delta) / 16
    assert cert["q_branch_gap"] > 0


def test_audited_delta_range() -> None:
    with pytest.raises(ValueError):
        conditional_threshold(Fraction(0))
    with pytest.raises(ValueError):
        conditional_threshold(Fraction(16, 5))
