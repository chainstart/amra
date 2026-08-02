from verify_third_active_independent_audit import audit, symbolic_certificate


def test_symbolic_page_constant_and_endpoint_ledger() -> None:
    result = symbolic_certificate()
    assert "(s - 7)" in result["K6_at_minus_1_over_s"]
    assert "(s - 8)" in result["K7_at_minus_1_over_s"]


def test_independent_rows_bases_and_transports() -> None:
    result = audit(maximum_q=20, maximum_s=20)
    assert result["status"].endswith("PASS")
    assert result["six_exact_bases_checked"]
