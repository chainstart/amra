from fractions import Fraction

import verify_representation_rich_cross_cell as verifier


def test_representation_rich_exponent_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["rich_cell_exponent"] == Fraction(1, 5)
    assert ledger["minimum_hub_exponent"] == Fraction(13, 20)
    assert (
        ledger["rich_cell_to_hub_ratio_exponent"]
        == -Fraction(9, 20)
    )
    assert (
        ledger["all_rich_representation_edge_exponent"]
        == Fraction(29, 10)
    )
    assert (
        ledger["c4_threshold_deficit_exponent"]
        == Fraction(1, 10)
    )
    assert (
        ledger["forced_edge_exponent_if_point_moment_fails"]
        == Fraction(29, 10)
    )
    assert (
        ledger["forced_hub_exponent_in_c4_free_branch"]
        == Fraction(9, 10)
    )
    assert ledger["maximum_hub_exponent"] == Fraction(9, 10)
    assert ledger["forced_hub_surplus_over_upper_bound"] == 0
    assert (
        ledger["required_labelled_cycle_gain_exponent"]
        == Fraction(2, 5)
    )


def test_fan_profile_satisfies_sharp_cauchy_bounds() -> None:
    certificate = verifier.fan_profile(
        ((3, 2), (1, 4), (2, 2), (5, 0), (0, 3))
    )
    assert certificate["active_block_count"] == 5
    assert certificate["signed_channel_count"] == 8
    assert certificate["representation_count"] == 22
    assert certificate["fan_energy"] == 72
    assert certificate["maximum_ruling"] == 5
    assert certificate["energy_bound_holds"]
    assert certificate["maximum_bound_holds"]


def test_one_cell_algebraic_realization_uses_a_product_matching() -> None:
    certificate = verifier.one_cell_certificate(
        product_index=9,
        signed_counts=((3, 2), (1, 4), (2, 2), (5, 0), (0, 3)),
        height_capacity=6,
    )
    assert certificate["radius_blocks_form_matching"]
    assert certificate["common_radial_product"] == 2**9
    assert certificate["representation_count"] == 22
    assert certificate["maximum_height_usage"] <= 6
    assert certificate["all_channels_hit_target_cell"]
    assert certificate["all_shift_squares_positive"]
    assert certificate["all_semialgebraic_identities"]


def test_cross_cell_cycle_cocycle_detects_consistency() -> None:
    closing = verifier.cycle_cocycle(
        (
            Fraction(7, 3),
            Fraction(-5, 2),
            Fraction(11, 6),
            Fraction(-5, 3),
        )
    )
    frustrated = verifier.cycle_cocycle(
        (
            Fraction(7, 3),
            Fraction(-5, 2),
            Fraction(11, 6),
            Fraction(-4, 3),
        )
    )
    assert closing["cycle_closes"]
    assert closing["oriented_sum"] == 0
    assert not frustrated["cycle_closes"]
    assert frustrated["oriented_sum"] != 0


def test_bipartite_c4_threshold_distinguishes_a_rectangle() -> None:
    cycle_six = verifier.bipartite_c4_certificate(
        3,
        3,
        ((0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (0, 2)),
    )
    rectangle = verifier.bipartite_c4_certificate(
        2,
        2,
        ((0, 0), (0, 1), (1, 0), (1, 1)),
    )
    assert cycle_six["is_c4_free"]
    assert cycle_six["c4_count"] == 0
    assert cycle_six["c4_free_kst_squared_holds"]
    assert not rectangle["is_c4_free"]
    assert rectangle["c4_count"] == 1
