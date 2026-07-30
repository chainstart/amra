from verify_growing_top_window import audit


def test_growing_top_window():
    result = audit(maximum_stirling_n=48, maximum_page_count=10)
    assert result["maximum_stirling_n"] == 48
    assert result["recurrence_checks"] == 1225
    assert result["bound_checks"] == 325
    assert len(result["linearity_records"]) == 9
    assert sum(
        record["identity_checks"]
        for record in result["linearity_records"]
    ) == 81
