from third_active_transport_top_attack import EXPECTED_SHIFTS, certify


def test_universal_top_transport_bands() -> None:
    result = certify()
    assert len(result["odd"]) == 8
    assert len(result["even"]) == 10
    assert tuple(item["shift"] for item in result["odd"]) == EXPECTED_SHIFTS["odd"]
    assert tuple(item["shift"] for item in result["even"]) == EXPECTED_SHIFTS["even"]
    assert result["ratio_shift_monomials"] == 330
    assert result["exceptional_values"] == 24
    assert result["direct_crosschecks"] == 72
