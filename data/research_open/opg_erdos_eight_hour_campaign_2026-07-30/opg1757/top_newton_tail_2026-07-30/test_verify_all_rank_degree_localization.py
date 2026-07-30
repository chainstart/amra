from verify_all_rank_degree_localization import audit


def test_exact_localized_rings_through_rank_three():
    result = audit(maximum_rank=3)
    assert result["status"] == "finite_exact_localization_audit_passed"
    assert result["low_rank_marked_identities"] == {
        "delta_0": "0",
        "epsilon_0": "0",
        "epsilon_1": "0",
    }
    assert result["leading_laurent_records"][2] == {
        "rank": 2,
        "c_r": "-35/72",
        "d_r": "5/6",
        "e_r": "-1",
        "e_pattern_checked": True,
    }
    assert result["central_records"][0]["highest_laurent_layer"] == "2"
    assert all(
        record["t_valuation"] >= record["chain_rule_lower_bound"]
        for record in result["central_summand_records"]
    )
    assert result["symbol_records"][-1]["denominator_power_bound"] == 4
