from verify_all_rank_falling_triangle_corollary import audit


def test_all_rank_falling_triangle_corollary():
    result = audit()
    assert len(result["falling_records"]) == 5
    assert len(result["recurrence_records"]) == 5
    assert result["falling_records"][-1]["forced_roots"] == [
        5,
        6,
        7,
        8,
        9,
    ]
    assert all(
        record["degree"] == 3 * record["rank"]
        and record["residual_degree"] == 2 * record["rank"]
        and record["alternating_leading_sign"]
        for record in result["falling_records"]
    )
    assert result["recurrence_records"][-1][
        "forced_boundary_root"
    ] == 8
    assert result["status"] == "finite_exact_triangle_audit_passed"
