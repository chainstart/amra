from verify_fourth_active_newton import audit, fourth_coefficient


def test_symbolic_fourth_layer_audit() -> None:
    result = audit()
    assert result["schema"].endswith(".v1")
    assert result["symbolic_layers"] == [9, 10]
    assert result["direct_values"][4] == 24
    assert result["direct_values"][5] == 14088


def test_initial_fourth_layer_values() -> None:
    assert [fourth_coefficient(k) for k in range(4, 9)] == [
        24,
        14088,
        1979520,
        300069360,
        68886560880,
    ]
