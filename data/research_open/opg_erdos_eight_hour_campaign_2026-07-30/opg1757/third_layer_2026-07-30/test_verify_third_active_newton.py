from verify_third_active_newton import symbolic_audit, third_coefficient


def test_symbolic_third_layer_audit() -> None:
    result = symbolic_audit()
    assert result["schema"].endswith(".v1")
    assert result["symbolic_layers"] == [7, 8]
    assert result["small_complete_graph_checks"] == {
        3: {"c_values": [2, 12, 24], "third_coefficient": 2},
        4: {"c_values": [0, 84, 462, 1278], "third_coefficient": 144},
    }


def test_first_exact_third_layer_values() -> None:
    assert [third_coefficient(k) for k in range(3, 9)] == [
        2,
        144,
        17832,
        1864344,
        107241840,
        24547158720,
    ]
