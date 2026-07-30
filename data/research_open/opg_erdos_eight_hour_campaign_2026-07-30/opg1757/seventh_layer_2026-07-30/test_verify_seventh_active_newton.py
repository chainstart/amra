from verify_seventh_active_newton import audit, seventh_coefficient


def test_raw_layers_certificates_and_diagonal_cross_check():
    result = audit()
    assert result["schema"].endswith(".v1")
    assert result["denominators"] == [119750400, 1556755200]
    assert result["diagonal_cross_check"]["corrected_equation_14"] == "PASS"
    assert result["diagonal_cross_check"]["A6_monic_second"] == 87
    assert result["diagonal_cross_check"]["B6_monic_second"] == 91


def test_initial_seventh_layer_values():
    assert all(seventh_coefficient(k) > 0 for k in range(6, 12))
