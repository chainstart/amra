from independent_verify_general_k_beta5_beta8 import audit


def test_independent_component_partition_audit() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert len(result["records"]) == 5
