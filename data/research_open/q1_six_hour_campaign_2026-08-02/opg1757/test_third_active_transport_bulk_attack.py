from third_active_transport_bulk_attack import certify


def test_universal_low_transport_columns() -> None:
    result = certify()
    assert result["odd"]["columns"] == 31
    assert result["odd"]["positive_shifted_monomials"] == 775
    assert result["odd"]["nonnegative_recurrence_monomials"] == 713
    assert result["even"]["columns"] == 31
    assert result["even"]["positive_shifted_monomials"] == 837
    assert result["even"]["nonnegative_recurrence_monomials"] == 775
    assert result["direct_crosschecks"] == 90
