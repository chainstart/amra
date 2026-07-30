from verify_partial_cyclotomic_fibre_escape import audit


def test_partial_cyclotomic_fibre_escape_audit():
    result = audit()
    assert result["exact_quotient_arithmetic"] is True
    assert result["total_distinct_label_checks"] > 0
    assert result["quadratic_base_field"] == "Q(sqrt(2))"
    assert result["quadratic_base_distinct_label_checks"] > 0
    for case in result["cases"]:
        assert (
            case["exact_audited_labels"]
            >= case["cauchy_davenport_lower_bound"]
        )
    assert result["status"] == "finite_audit_passed"
