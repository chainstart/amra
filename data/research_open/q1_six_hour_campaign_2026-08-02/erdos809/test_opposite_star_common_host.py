from verify_opposite_star_common_host import run_exhaustive


def test_exhaustive_common_host_guards():
    result = run_exhaustive(max_n=5)
    assert result["status"] == "PASS"
    assert result["star_systems"] > 0
    assert result["union_rectangle_witnesses"] > 0
    assert result["two_budget_parameter_cases"] > 0
