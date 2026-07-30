from independent_verify_newton import run_audit


def test_independent_newton_audit() -> None:
    result = run_audit()
    assert result["schema"].endswith(".v1")
    assert result["formula_checks"] == 36
    assert result["edge_pair_orbit_checks"] == 12
    assert result["determinant_checks"] == 16
    assert len(result["coefficient_checks"]) == 6
