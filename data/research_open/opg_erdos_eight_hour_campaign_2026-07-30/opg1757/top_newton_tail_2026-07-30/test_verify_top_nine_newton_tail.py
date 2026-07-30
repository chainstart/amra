from verify_top_nine_newton_tail import audit


def test_top_nine_newton_tail():
    result = audit(maximum_k=25)
    assert result["status"] == "proved_exact_top_depths_0_through_8"
    assert result["redundant_checks"] == 13
    assert result["boundary"]["p_7_8"] == "155520"
    assert int(result["Q8_quadratic_block_discriminant"]) < 0
