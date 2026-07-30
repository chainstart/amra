from verify_ordinary_first_five_long_recurrence_bands import audit


def test_first_five_long_recurrence_bands():
    result = audit()
    assert result["ordinary_to_newton_rows"] == 6
    assert result["positive_bands"] == 5
    assert [
        record["minimum_depth"] for record in result["records"]
    ] == [1, 3, 5, 7, 9]
    assert result["status"] == "all_depth_symbolic_audit_passed"
