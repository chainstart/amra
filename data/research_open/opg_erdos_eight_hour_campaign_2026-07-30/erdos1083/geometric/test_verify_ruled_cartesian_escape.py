from verify_ruled_cartesian_escape import audit


def test_ruled_cartesian_escape():
    result = audit(maximum_t=7)
    assert result["status"] == "finite_checks_passed"
    assert len(result["rows"]) == 12
    assert all(
        row["distinct_labels"] >= row["theorem_integer_floor"]
        for row in result["rows"]
    )
