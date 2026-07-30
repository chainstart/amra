from fractions import Fraction

import verify_joint_overlap_triangle_moment as verifier


def test_disjoint_marginal_supports_can_have_zero_joint_moment() -> None:
    certificate = verifier.disjoint_support_arrays(
        incidence_count=100,
        overlap_total=120,
        triangle_total=70,
        d_max=5,
        tau_max=4,
    )
    assert certificate["d_sum"] == 120
    assert certificate["tau_sum"] == 70
    assert certificate["joint_sum"] == 0
    assert certificate["d_support"] + certificate["tau_support"] <= 100


def test_random_survival_is_constant_in_balanced_regime() -> None:
    for scale in (100, 200, 500):
        lower_bound = verifier.random_survival_lower_bound(
            radius_count=scale,
            height_count=scale,
            selected_count=scale // 2,
        )
        assert lower_bound >= Fraction(1, 10)
        assert lower_bound <= Fraction(1, 8)


def test_joint_exponent_and_target_gap() -> None:
    eta = Fraction(1, 30)
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["joint_bound"] == Fraction(10, 3) - eta
    assert ledger["joint_target"] == Fraction(11, 3) + eta
    assert ledger["joint_gap"] == Fraction(1, 3) + 2 * eta
    assert (
        ledger["weighted_triangle_target"]
        == ledger["joint_gap"]
    )
    assert ledger["joint_average_per_incidence"] == (
        Fraction(1, 3) - eta
    )


def test_hub_landscape_has_enough_overlap_support_capacity() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["hub_incidence"] == Fraction(11, 3) + Fraction(1, 30)
    assert (
        ledger["hub_pair_count"]
        >= ledger["overlap_block_support"]
    )
