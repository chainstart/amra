from verify_opposite_star_colour_support import run_exhaustive


def test_leaf_independence_colour_support_guards():
    result = run_exhaustive(max_leaves=6)
    assert result["status"] == "PASS"
    assert result["aggregate_support_systems"] > 0
    assert result["union_rectangle_systems"] == result["aggregate_support_systems"]
