from verify_sixth_active_newton import audit, sixth_coefficient


def test_raw_fifth_audit_and_sixth_layer():
    result = audit()
    assert result["schema"].endswith(".v1")
    assert result["independent_fifth_audit"]["verdict"] == "PASS"
    assert result["sixth_denominators"] == [907200, 9979200]
    assert result["direct_values"][5] == 720
    assert result["direct_values"][6] == 322560


def test_initial_sixth_layer_values():
    assert [sixth_coefficient(k) for k in range(5, 10)] == [
        720,
        322560,
        288691200,
        94624871040,
        35530741814400,
    ]
