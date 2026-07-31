from fractions import Fraction

from verify_collinear_center_linearization import (
    endpoint_ledger,
    old_endpoint_linearization_gap,
    verify_finite_geometry,
)


def test_fixed_center_geometry():
    cert = verify_finite_geometry()
    assert cert["max_lift_fibre"] == 2
    assert cert["circles"] == cert["lines"]
    assert cert["checked_incidences"] > 0


def test_two_ninths_endpoint():
    cert = endpoint_ledger()
    assert cert["kappa"] == Fraction(2, 9)
    assert cert["lines_per_signed_center_j"] == cert["labels_ell"]
    assert (
        cert["circles_per_signed_line_h"] + cert["multiplicity_m"]
        == cert["targets_per_signed_center_x"]
    )


def test_old_endpoint_ledger_has_strict_linearization_gap():
    assert old_endpoint_linearization_gap() == Fraction(2, 123)
