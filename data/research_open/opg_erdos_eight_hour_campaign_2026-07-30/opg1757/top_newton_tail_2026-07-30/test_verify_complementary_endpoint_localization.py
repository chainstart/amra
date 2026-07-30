from verify_complementary_endpoint_localization import audit


def test_exact_complementary_endpoint_identities():
    result = audit()
    assert result["status"] == "PASS"
    assert result["hypergeometric_checks"] >= 90
    assert result["main_profile_checks"] >= 90
    assert result["exceptional_profile_checks"] >= 20
    assert result["hessian_at_v_one"] == "1 - 2*x"
