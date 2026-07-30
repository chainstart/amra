from verify_ordinary_subleading_saddle_certificate import audit


def test_all_orders_subleading_saddle_certificate():
    result = audit()
    assert result["finite_loss_interpolation"] is False
    assert result["primary_shifts"] == [0, 2, 4]
    assert result["exceptional_profile_included"] is True
    assert result["maximum_inverse_s_rank"] == 3
    assert result["symbolic_identity_checks"] == 12
    assert (
        result["status"]
        == "all_orders_symbolic_certificate_passed"
    )
