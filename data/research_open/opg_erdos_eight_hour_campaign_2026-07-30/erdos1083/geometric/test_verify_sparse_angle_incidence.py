from verify_sparse_angle_incidence import audit


def test_sparse_angle_incidence_expansion() -> None:
    result = audit()
    assert result["schema"].endswith(".v1")
    assert len(result["random_sparse_records"]) == 120
    assert result["full_rectangle_record"]["incidence_count"] == 72
