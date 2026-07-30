from verify_near_logarithmic_top_window import audit


def test_near_logarithmic_top_window():
    result = audit(maximum_loss=32, maximum_n=64)
    assert result["status"] == "finite_checks_passed"
    assert result["partition_checks"] > 10_000
    assert result["stirling_ratio_checks"] > 1_000
    assert all(
        row["new_clean_depth"] > row["old_clean_depth"]
        for row in result["scale_rows"]
    )
