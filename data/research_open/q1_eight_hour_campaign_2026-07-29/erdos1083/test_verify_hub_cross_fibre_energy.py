from fractions import Fraction

import verify_hub_cross_fibre_energy as verifier


def test_required_collective_saving_exponent() -> None:
    for numerator, denominator in ((0, 1), (1, 30), (1, 20)):
        ledger = verifier.exponent_ledger(numerator, denominator)
        assert ledger["required_c"] == ledger["required_c_formula"]
        assert ledger["closed_hub_exponent"] == ledger["required_hub"]
    assert verifier.exponent_ledger(0, 1)["required_c"] == Fraction(2, 5)


def test_real_pair_saturation_uses_exact_offsets_and_shared_sets() -> None:
    certificate = verifier.real_pair_saturation(18, 12, 0, 2)
    assert certificate["product_fibre_count"] >= 12
    assert certificate["all_product_sums_match"]
    assert certificate["all_target_counts_exact"]
    assert certificate["maximum_assigned_height_count"] <= 12
    assert certificate["cross_fibre_energy"] == (
        certificate["product_fibre_count"]
        * certificate["overlap_size"]
    )


def test_odd_prime_finite_field_saturates_translate_overlaps() -> None:
    certificate = verifier.finite_field_model(43, 16)
    assert certificate["generator_order"] == 42
    assert certificate["quadratic_residue_count"] == 22
    assert certificate["product_fibre_count"] <= 31
    assert certificate["union_size"] <= certificate["union_upper_bound"]
    assert (
        certificate["minimum_same_fibre_overlap"]
        >= certificate["intersection_lower_bound"]
    )
    assert certificate["ordered_overlap"] > 0


def test_rational_hyperbola_parameterization() -> None:
    for delta in (-101, -1, 1, 73, 1000):
        for parameter in (11, 37, 101):
            first, second = verifier.rational_hyperbola_pair(
                delta, parameter
            )
            assert first**2 - second**2 == delta
