from verify_ordinary_top_symbol import audit


def test_ordinary_top_symbol():
    result = audit(maximum_loss=12)
    assert result["record_count"] == 13
    assert result["determinant_symbol"] == "2*x**2/(1-x)"
    assert result["ordinary_leading_symbol"] == "1/(1-x)"
    assert result["records"][0] == {
        "loss": 0,
        "A": "1",
        "B": "0",
        "C": "0",
    }
