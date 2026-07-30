from verify_saddle_pole_orders import audit


def test_exact_saddle_poles_through_rank_three():
    result = audit(maximum_rank=3)
    assert result["status"] == "finite_exact_pole_audit_passed"
    assert result["kernel_records"][-1] == {
        "rank": 3,
        "determinant_pole_at_half": 4,
        "central_kernel_pole": 4,
        "expected_3r_minus_5": 4,
    }
