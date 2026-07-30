from independent_verify_growing_depth import (
    audit,
    component_formula_audit,
    determinant_audit,
    explicit_constant_audit,
    majorant_audit,
    support_and_newton_audit,
)


def test_finite_products_heat_normalization_and_majorants():
    component_formula_audit(12)
    component_ratio, tail_ratio = majorant_audit(12)
    assert component_ratio < 1
    assert tail_ratio < 1


def test_determinant_tail_support_and_newton_stress():
    assert determinant_audit(12) < 1
    assert support_and_newton_audit() > 200
    assert explicit_constant_audit(30) < 1


def test_full_independent_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["imports_existing_opg_verifier"] is False
    assert result["C15_denominator"] == 119750400
    assert result["C16_denominator"] == 1556755200
    assert result["seventh_boundary_values_checked"] == 24
