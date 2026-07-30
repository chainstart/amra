from fractions import Fraction

from verify_moderate_rich_aggregation_barrier import audit, ledger


def test_endpoint_one_fifth_saturates_plane_multiplicity():
    values = ledger(Fraction(1, 5))
    assert values["richness"] == Fraction(4, 5)
    assert values["circle_count"] == Fraction(23, 5)
    assert values["multiplicity"] == 1
    assert values["triple_weight"] == Fraction(28, 5)
    assert values["weighted_mass"] == Fraction(32, 5)
    assert values["hub"] == Fraction(32, 5)


def test_interior_one_fourth_exact_identities():
    kappa = Fraction(1, 4)
    values = ledger(kappa)
    assert values["richness"] == Fraction(3, 4)
    assert values["circle_count"] == Fraction(39, 8)
    assert values["multiplicity"] == Fraction(5, 8)
    assert values["triple_weight"] == Fraction(11, 2)
    assert values["weighted_mass"] == Fraction(25, 4)
    assert values["point_circle_second"] == values["unweighted_incidence"]
    assert values["weighted_second"] == values["hub"]


def test_pairwise_ms_and_high_rich_constraints_are_slack():
    for kappa in (Fraction(1, 5), Fraction(1, 4), Fraction(3, 10)):
        values = ledger(kappa)
        assert values["richness"] < Fraction(9, 4)
        assert values["ms_pair"] < 3


def test_full_moderate_rich_lp_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rational_kappa_cases"] > 20
