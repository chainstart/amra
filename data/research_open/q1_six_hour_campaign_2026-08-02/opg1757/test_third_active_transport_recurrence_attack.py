from third_active_transport_recurrence_attack import (
    audit_logarithmic_dominance_data,
    audit_reconstruction,
    audit_recurrence_reconstruction,
    audit_interior_symbols,
    fixed_layer_obstruction,
)


def test_odd_transport_fixed_layer_obstruction() -> None:
    assert audit_reconstruction() == 150
    assert audit_recurrence_reconstruction() > 0
    symbols = audit_interior_symbols()
    assert symbols["odd_sufficient"][0] == 9
    assert symbols["even_sufficient"][0] == 11
    logarithmic = audit_logarithmic_dominance_data()
    assert logarithmic["odd_sufficient"] == (19, 11, 126)
    assert logarithmic["even_sufficient"] == (23, 13, 176)
    assert logarithmic["odd_page_recurrence"] == (18, 8, 80)
    assert logarithmic["even_page_recurrence"] == (22, 10, 120)
    assert logarithmic["page_reconstruction_coefficients"] == 96
    assert logarithmic["slope"] == 241
    result = fixed_layer_obstruction()
    assert result["first_negative_layer"] == 4
    assert result["first_negative_parameter"] == 17
    assert result["first_negative_value"] == -1152
