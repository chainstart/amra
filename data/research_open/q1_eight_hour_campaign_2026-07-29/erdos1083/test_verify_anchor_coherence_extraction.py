from fractions import Fraction

import verify_anchor_coherence_extraction as verifier


def test_extraction_loss_ledger() -> None:
    ledger = verifier.exponent_ledger(1, 30)
    assert ledger["overlap_exponent"] == Fraction(33, 10)
    assert ledger["one_anchor_pair_mass_exponent"] == 0
    assert ledger["required_retention_exponent"] == -Fraction(3, 10)
    assert ledger["minimum_bucket_size_exponent"] == Fraction(17, 20)
    assert ledger["missing_joint_factor_exponent"] == Fraction(2, 5)


def test_latin_assignment_is_pairwise_diffuse_and_regular() -> None:
    certificate = verifier.latin_anchor_barrier(13, 5)
    assert certificate["every_block_uses_each_anchor_once"]
    assert certificate["pair_multiplicity_minimum"] == 1
    assert certificate["pair_multiplicity_maximum"] == 1
    assert certificate["common_label_services"] == 0
    assert (
        certificate["anchor_degree_minimum"]
        == certificate["expected_anchor_degree"]
    )
    assert (
        certificate["anchor_degree_maximum"]
        == certificate["expected_anchor_degree"]
    )


def test_finite_barrier_satisfies_all_marginal_identities() -> None:
    certificate = verifier.finite_marginal_barrier(
        fibre_count=13,
        block_count_per_fibre=13,
        block_size=13,
        hub_block_count=3,
        other_group_size=2,
    )
    assert certificate["block_count"] == 13**2
    assert certificate["incidence_count"] == 13**3
    assert certificate["ordered_overlap"] == 2 * (
        certificate["unordered_hub_overlap"]
        + certificate["unordered_other_overlap"]
    )
    assert (
        certificate["triangle_degree_sum"]
        == certificate["incidence_count"]
    )
    assert certificate["joint_moment"] == certificate["ordered_overlap"]
    assert certificate["maximum_reuse_degree"] <= 13
    assert certificate["triangle_degree"] <= 13**2


def test_gram_rectangle_identity() -> None:
    assert verifier.gram_rectangle_identity(
        (Fraction(2), Fraction(5)),
        (Fraction(7), Fraction(-3)),
        (Fraction(11), Fraction(4)),
        (Fraction(-2), Fraction(9)),
    )
