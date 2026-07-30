from independent_verify_all_fixed_rank_ordinary_symbol_algorithm import audit


def test_independent_rank_five_algorithm():
    result = audit(maximum_loss=10, maximum_depth=8)
    assert result["imports_existing_opg_verifier"] is False
    assert result["maximum_profile_rank"] == 5
    assert result["phase_derivative_order"] == 12
    assert result["maximum_bernoulli_index"] == 6
    assert result["profile_symbol_checks"] == 153
    assert result["exceptional_rank_five_checks"] == 6
    assert result["central_moment_checks"] == 18
    assert result["ordinary_symbol_checks_r_le_3"] == 30
    assert result["rank_three_ordinary_checks"] == 6
    assert result["rank_three_generating_identity"] is True
    assert result["verdict"] == "PASS"
