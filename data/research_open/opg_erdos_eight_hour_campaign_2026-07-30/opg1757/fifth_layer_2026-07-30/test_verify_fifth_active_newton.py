from verify_fifth_active_newton import audit, fifth_coefficient


def test_symbolic_fifth_layer_audit():
    result = audit()
    assert result["schema"].endswith(".v1")
    assert result["symbolic_layers"] == [11, 12]
    assert len(result["component_pattern_checks"]) == 10
    assert result["direct_values"][5] == 5040
    assert result["direct_values"][6] == 1095840


def test_initial_fifth_layer_values():
    assert [fifth_coefficient(k) for k in range(5, 10)] == [
        5040,
        1095840,
        388668240,
        102879564480,
        21371783388480,
    ]
