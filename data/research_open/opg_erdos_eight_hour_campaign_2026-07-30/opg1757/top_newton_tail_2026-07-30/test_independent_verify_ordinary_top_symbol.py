from independent_verify_ordinary_top_symbol import (
    abc_audit,
    audit,
    determinant_audit,
)


def test_independent_abc_and_second_difference():
    _, a, _, c = abc_audit(8)
    assert c[4] == -2
    assert c[8] == 2*6*5*a[6]


def test_independent_determinant_symbol_and_prefactor():
    records = determinant_audit(7)
    assert [loss for loss, _ in records] == [4, 5, 6, 7]


def test_full_independent_ordinary_top_symbol_audit():
    result = audit()
    assert result["verdict_as_written"] == "PASS"
    assert result["formula_verdict"] == "PASS"
    assert result["determinant_leading_numerator"] == 2
    assert result["ordinary_leading_coefficient"] == 1
