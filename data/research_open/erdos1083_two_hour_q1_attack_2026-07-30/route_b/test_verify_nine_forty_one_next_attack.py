from verify_nine_forty_one_next_attack import (
    endpoint_aggregate_ledger,
    finite_interval_service_model,
    threshold_from_aggregate_saving,
)


def test_endpoint_aggregate_ledger():
    cert = endpoint_aggregate_ledger()
    assert cert["kappa"] == cert["signed_slopes_r"] * 9 / 41
    assert cert["target_points_per_slope_x"] == 3
    assert cert["lines_per_slope_j"] == cert["labels_ell"]


def test_finite_interval_service_model():
    cert = finite_interval_service_model()
    assert cert["triples"] == (
        cert["target_points"] * cert["lines_per_target"]
    )
    assert cert["triples"] == (
        cert["circle_classes"] * cert["multiplicity_per_circle"]
    )
    assert cert["labels"] == (
        cert["parameter_lines"] + cert["tangent_squares"] - 1
    )


def test_conditional_threshold_gain():
    from fractions import Fraction

    delta = Fraction(1, 100)
    assert threshold_from_aggregate_saving(delta) == (
        Fraction(9, 41) + Fraction(25, 41) * delta
    )
