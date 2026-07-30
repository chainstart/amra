from verify_cyclotomic_tensor_escape import audit


def test_cyclotomic_tensor_escape_audit():
    result = audit()
    assert result["exact_quotient_arithmetic"] is True
    assert result["total_distinct_label_checks"] == 104
    assert [
        case["radius_dependent_height_counts"] for case in result["cases"]
    ] == [[3, 2, 4], [2, 3, 2], [3, 4]]
    assert result["status"] == "finite_audit_passed"
