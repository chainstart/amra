from verify_arbitrary_height_energy import audit


def test_arbitrary_height_energy_dichotomy() -> None:
    result = audit()
    assert result["schema"].endswith(".v1")
    assert len(result["slice_records"]) == 10
    assert len(result["lattice_records"]) == 4
    assert result["artificial_high_lambda"] >= 6
