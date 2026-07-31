from verify_general_k_beta5_beta8 import (
    audit,
    full_domain_positive_polynomials,
)


def test_general_k_beta5_beta8_exact_interpolation() -> None:
    result = audit()
    assert result["status"] == "PASS"
    assert [row["kernel_beta_rank"] for row in result["records"]] == [
        5,
        6,
        7,
        8,
    ]


def test_every_shifted_Q_coefficient_is_strictly_positive() -> None:
    for _, polynomial in full_domain_positive_polynomials().values():
        assert all(
            coefficient > 0
            for _, coefficient in polynomial.as_poly().terms()
        )
