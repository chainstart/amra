from verify_md2_laurent_identity import audit


def test_symbolic_all_rank_md2_identity():
    result = audit()
    assert result["status"] == "symbolic_all_rank_md2_identity_passed"
    assert result["total_top_five_laurent_jets"][:4] == [
        "0",
        "0",
        "0",
        "0",
    ]
    assert result["total_top_five_laurent_jets"][4] == (
        "-36*r*(r - 1)/((6*r - 7)*(6*r - 5)*(6*r - 1))"
    )
    assert result["epsilon_leading_identity"] == (
        "e_r = -6*(r-1)*c_(r-1)"
    )
