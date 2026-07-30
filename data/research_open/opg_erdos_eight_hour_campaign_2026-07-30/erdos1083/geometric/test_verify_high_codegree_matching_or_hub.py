from fractions import Fraction

from verify_high_codegree_matching_or_hub import (
    audit,
    critical_exponent_ledger,
    exhaustive_weighted_extraction_check,
    finite_field_tensor,
)


def test_exhaustive_small_weighted_extraction_lemma():
    assert exhaustive_weighted_extraction_check() == 4**6 - 1


def test_critical_split_exponents():
    ledger = critical_exponent_ledger(Fraction(11, 2))
    assert ledger["label_count"] == 2
    assert ledger["rich_cell"] == Fraction(7, 2)
    assert ledger["automatic_matching"] == Fraction(1, 2)
    assert ledger["hub_mass"] == 5
    assert ledger["hub_label_count"] == 1


def test_one_third_tradeoff_exponents():
    split = critical_exponent_ledger(
        Fraction(16, 3), Fraction(1, 3)
    )
    assert split["automatic_matching"] == Fraction(1, 3)
    assert split["hub_mass"] == 5
    assert split["hub_label_count"] == Fraction(4, 3)


def test_quadratic_tensor_exact_ledger_and_no_k42():
    model = finite_field_tensor(5)
    assert model["total_mass"] == 5**8
    assert model["aggregate_energy"] == 5**13
    assert model["diagonal_energy"] == 5**12
    assert model["good_matching_labels"] == 5**3 - 5
    assert model["maximum_pair_row_common_labels"] == 5
    assert model["maximum_triple_row_common_labels"] == 1
    assert model["maximum_four_row_common_labels"] == 1


def test_full_audit():
    result = audit(7)
    assert result["status"] == "PASS"
    model = result["finite_field_model"]
    assert model["support_cells"] == 7**4
    assert model["triple_row_checks"] > 10_000
    assert model["four_row_checks"] > 100_000
