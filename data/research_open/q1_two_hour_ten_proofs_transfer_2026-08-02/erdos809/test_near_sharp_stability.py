"""Regression tests for the parity-sharp stability cost."""

from verify_near_sharp_stability import certificate, stability_cost


def test_baseline_profiles_have_zero_cost() -> None:
    for g in (4, 5, 20):
        assert stability_cost(g, "even", 2, 0) == 0
        assert stability_cost(g, "odd", 1, 0) == 0


def test_first_parameter_and_residual_deviations() -> None:
    for g in (4, 7, 30):
        assert stability_cost(g, "even", 4, 0) == 8
        assert stability_cost(g, "odd", 3, 0) == 6
        assert stability_cost(g, "even", 2, 1) == 2 * g - 2
        assert stability_cost(g, "odd", 1, 1) == 2 * g - 2


def test_centre_offset_concavity_charge() -> None:
    assert stability_cost(10, "even", 2, 5, 0) == 70
    assert stability_cost(10, "even", 2, 5, 5) == 70
    assert stability_cost(10, "even", 2, 5, 2) == 82


def test_full_scalar_certificate() -> None:
    result = certificate(max_g=250)
    assert result["parameter_rows"] > 1_000_000
    assert result["positive_h_rows"] > 0
    assert result["nonbaseline_a_rows"] > 0
    assert result["near_band_rows"] == 2 * (250 - 3)
    assert result["centre_offset_samples"] > result["parameter_rows"]
    assert result["pass"]
