from independent_verify_ordinary_subleading_symbol import audit


def test_independent_subleading_profiles_and_central_expansion():
    result = audit(maximum_loss=16, maximum_depth=12)
    assert result["imports_existing_opg_verifier"] is False
    assert result["profile_checks"] == 186
    assert result["g1_exactly_antisymmetric"] is True
    assert result["central_moment_checks"] == 192
    assert result["H2"] == "-2*t**4/(t - 1)"
    assert result["H3"] == (
        "-t**4*(43*t**4 - 129*t**3 + 108*t**2 "
        "- 6*t + 6)/(3*(t - 1)**4)"
    )
    assert result["h3_coefficient_checks"] == 12
    assert result["subleading_generating_function"] == (
        "-z*(43*z**3 - 123*z**2 + 90*z + 12)"
        "/(6*(z - 1)**4)"
    )


def test_independent_subleading_polynomials_and_verdict():
    result = audit(maximum_loss=14, maximum_depth=10)
    assert result["subleading_polynomial_checks"] == 10
    assert result["rows"][-1] == {
        "depth": 10,
        "subleading": "-1057",
    }
    assert result["formula_verdict"] == "PASS"
    assert (
        result["all_orders_proof_verdict"]
        == "PASS_WITH_SYMBOLIC_SADDLE_CERTIFICATE"
    )
