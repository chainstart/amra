import ast
from fractions import Fraction
from pathlib import Path

import pytest

import verify_high_rich_circle_concentration as concentration
from verify_high_rich_circle_concentration import (
    HIGH_RICH_EXPONENT,
    audit,
    exponent_ledger,
    finite_weighted_partition,
    ms_mixed_exponent,
)


def test_ms_high_pair_and_critical_threshold():
    assert HIGH_RICH_EXPONENT == Fraction(9, 4)
    assert ms_mixed_exponent(HIGH_RICH_EXPONENT, HIGH_RICH_EXPONENT) == 3
    assert ms_mixed_exponent(
        HIGH_RICH_EXPONENT + Fraction(1, 20),
        HIGH_RICH_EXPONENT + Fraction(1, 20),
    ) == Fraction(46, 15)


def test_hub_mass_gaps_for_kappa_below_one():
    ledger = exponent_ledger(Fraction(2, 5), Fraction(1, 100))
    assert ledger["high_to_hub_gap"] == Fraction(9, 5)
    assert ledger["zero_to_hub_gap"] == Fraction(3, 5)
    assert ledger["hub_mass"] > ledger["high_weighted_mass"]
    assert ledger["hub_mass"] > ledger["zero_radius_mass"]


def test_finite_multiplicity_and_disjoint_incidence_cap():
    weighted = finite_weighted_partition(
        source_size=30,
        plane_count=5,
        incidence_sizes=(7, 11, 12),
        multiplicities=(5, 3, 4),
    )
    assert weighted == 116
    assert weighted <= 150
    with pytest.raises(ValueError):
        finite_weighted_partition(
            source_size=30,
            plane_count=5,
            incidence_sizes=(16, 16),
            multiplicities=(2, 2),
        )
    with pytest.raises(ValueError):
        finite_weighted_partition(
            source_size=30,
            plane_count=5,
            incidence_sizes=(15, 15),
            multiplicities=(6, 1),
        )


def test_ast_locks_nine_four_constant():
    tree = ast.parse(Path(concentration.__file__).read_text())
    assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "HIGH_RICH_EXPONENT"
            for target in node.targets
        )
    ]
    assert len(assignments) == 1
    call = assignments[0].value
    assert isinstance(call, ast.Call)
    assert isinstance(call.func, ast.Name)
    assert call.func.id == "Fraction"
    assert [argument.value for argument in call.args] == [9, 4]


def test_full_high_rich_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["high_rich_exponent"] == "9/4"
    assert result["exponent_ledgers"] == 36
    assert result["finite_partition_cases"] == 3
