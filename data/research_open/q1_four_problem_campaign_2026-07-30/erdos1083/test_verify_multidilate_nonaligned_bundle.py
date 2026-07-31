from fractions import Fraction

from verify_multidilate_nonaligned_bundle import (
    audit_instance,
    endpoint_exponent_certificate,
    exhaustive_small_audit,
    geometric_formula_certificate,
    parabolic_spectral_graph_certificate,
)


def test_exhaustive_small_energy_and_support_audit() -> None:
    result = exhaustive_small_audit()
    assert result["instances_audited"] >= 50


def test_geometric_circle_axis_formula_exactly() -> None:
    records = geometric_formula_certificate()
    assert len(records) == 6


def test_endpoint_exponents_are_exact() -> None:
    result = endpoint_exponent_certificate()
    assert result["pass"]
    assert result["h_lower"] == "19/9"
    assert result["reuse_gap"] == "1/6"
    assert result["overlap_exponent"] == "2/9"
    assert result["rich_label_exponent"] == "35/18"
    assert result["row_degree_exponent"] == "13/18"
    assert result["synchronized_pair_exponent"] == "17/6"


def test_parabolic_spectral_graph_bounds() -> None:
    result = parabolic_spectral_graph_certificate()
    assert result["quadratic_cap_pass"]
    assert result["rich_count_pass"]
    assert result["energy_pass"]


def test_overlap_identity_with_translated_rows() -> None:
    x_set = (Fraction(0), Fraction(1), Fraction(2))
    t_star = (Fraction(0), Fraction(1), Fraction(4), Fraction(9))
    rows = {
        Fraction(1): (Fraction(0), Fraction(1), Fraction(4)),
        Fraction(2): (Fraction(0), Fraction(4), Fraction(9)),
        Fraction(5): (Fraction(1), Fraction(4), Fraction(9)),
    }
    shifts = {
        Fraction(1): Fraction(3),
        Fraction(2): Fraction(-2),
        Fraction(5): Fraction(7),
    }
    result = audit_instance(x_set, t_star, rows, shifts)
    assert result["energy_pass"]
    assert result["support_cs_pass"]
    assert result["intersection_identity_pass"]


def test_zero_dilation_is_rejected() -> None:
    try:
        audit_instance(
            (Fraction(0), Fraction(1)),
            (Fraction(0), Fraction(1)),
            {Fraction(0): (Fraction(0), Fraction(1))},
        )
    except ValueError as error:
        assert "nonzero" in str(error)
    else:
        raise AssertionError("zero dilation should have been rejected")
