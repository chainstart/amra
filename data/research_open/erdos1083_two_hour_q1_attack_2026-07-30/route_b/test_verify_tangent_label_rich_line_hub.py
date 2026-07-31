from verify_tangent_label_rich_line_hub import (
    endpoint_ledger_certificate,
    finite_fibre_cap_certificate,
    finite_target_fibre_certificate,
    symbolic_radius_identity,
    threshold_certificate,
)


def test_symbolic_radius_identity():
    symbolic_radius_identity()


def test_threshold_certificate():
    cert = threshold_certificate()
    assert cert["refined_crossing"] > cert["first_crossing"]
    assert cert["first_crossing"] > cert["old_threshold"]
    assert cert["strict_gain"] > 0


def test_endpoint_ledger_certificate():
    cert = endpoint_ledger_certificate()
    assert cert["kappa"].numerator == 9
    assert cert["kappa"].denominator == 41


def test_finite_fibre_cap_certificate():
    cert = finite_fibre_cap_certificate()
    assert cert["incidences"] <= cert["cap"]
    assert cert["max_centres_per_point"] <= 4


def test_finite_target_fibre_certificate():
    cert = finite_target_fibre_certificate()
    assert (
        cert["coplanar_target_points"]
        == cert["circles"] * cert["multiplicity_per_circle"]
    )
