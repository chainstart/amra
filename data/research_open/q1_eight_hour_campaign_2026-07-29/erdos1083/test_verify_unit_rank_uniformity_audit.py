from verify_unit_rank_uniformity_audit import (
    conditional_theorem_ledger,
    coordinate_box_cost,
    degree_dependent_proxy,
    packing_rank_lower_bound,
    strong_uniformity_proxy,
)


def test_packing_bound_strengthens_with_longer_shortest_vector():
    n = 10**100
    weak = packing_rank_lower_bound(n, 1 / 1000)
    strong = packing_rank_lower_bound(n, 1)
    assert strong["required_rank"] > weak["required_rank"]


def test_degree_proxy_is_weaker_than_strong_uniformity():
    comparisons = []
    for exponent in (20, 50, 100, 200):
        n = 10**exponent
        weak = degree_dependent_proxy(n)
        strong = strong_uniformity_proxy(n)
        assert strong["required_rank"] >= weak["required_rank"]
        comparisons.append(strong["required_rank"] > weak["required_rank"])
    assert any(comparisons)


def test_binary_coordinate_volume_does_not_close_the_target():
    n = 10**200
    rank = degree_dependent_proxy(n)["required_rank"]
    cost = coordinate_box_cost(n, rank)
    assert cost["fits"]
    assert cost["power_exponent"] < 0.1


def test_ledger_marks_two_fifths_as_conditional():
    ledger = conditional_theorem_ledger()
    assert "only" in ledger["degree_dependent_height_only"]
    assert "no rank lower bound" in ledger["unconditional_warning"]
