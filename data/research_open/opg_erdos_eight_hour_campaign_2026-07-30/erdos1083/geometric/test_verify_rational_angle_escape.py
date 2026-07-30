from verify_rational_angle_escape import audit


def test_rational_angle_escape() -> None:
    result = audit(maximum_e=5, maximum_k=14)
    assert result["schema"].endswith(".v1")
    # There are 2^(e-1) positive odd reduced numerators modulo 2^e.
    assert len(result["two_power_records"]) == 2 + 4 + 8 + 16
    assert len(result["odd_prime_records"]) == 5
    assert len(result["distance_records"]) == 3
