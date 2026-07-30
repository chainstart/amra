"""Independent tests for the first five ordinary long-recurrence bands."""

import sympy as sp

from independent_verify_ordinary_first_five_long_recurrence_bands import (
    audit,
    d,
    expected_gamma_polynomials,
    forced_factor_audit,
    index_audit,
    near_diagonal_stirling,
    ordinary_to_newton_rows,
    recurrence_bands,
    shifted_positive_rows,
)


def test_near_diagonal_stirling_antidifference():
    n, rows = near_diagonal_stirling(5)
    assert rows[0] == 1
    assert sp.factor(rows[1]) == -n * (n - 1) / 2
    for loss in range(1, 6):
        assert rows[loss].subs(n, 0) == 0
        assert sp.expand(
            rows[loss].subs(n, n + 1)
            - rows[loss]
            + n * rows[loss - 1]
        ) == 0


def test_printed_h1_h2_h3_rows():
    h_rows = ordinary_to_newton_rows(5)
    expected_h1 = -(d - 1) * (22 * d**2 + 151 * d + 258) / 36
    expected_h2 = (
        (d - 3)
        * (d - 2)
        * (
            286 * d**4
            + 3392 * d**3
            + 16445 * d**2
            + 37213 * d
            + 28668
        )
        / 5184
    )
    expected_h3 = -(
        (d - 5)
        * (d - 4)
        * (d - 3)
        * (
            158450 * d**6
            + 2236425 * d**5
            + 15204170 * d**4
            + 60657945 * d**3
            + 141977342 * d**2
            + 179753064 * d
            + 45900864
        )
        / 83980800
    )
    assert sp.cancel(h_rows[1] - expected_h1) == 0
    assert sp.cancel(h_rows[2] - expected_h2) == 0
    assert sp.cancel(h_rows[3] - expected_h3) == 0


def test_all_five_gamma_identities():
    _, gammas = recurrence_bands()
    for actual, expected in zip(gammas, expected_gamma_polynomials()):
        assert sp.cancel(actual - expected) == 0


def test_shifted_positive_coefficients_and_ranges():
    _, gammas = recurrence_bands()
    rows = shifted_positive_rows(gammas)
    assert [len(row) for row in rows] == [3, 6, 9, 12, 15]
    assert all(coefficient > 0 for row in rows for coefficient in row)
    indices = index_audit(gammas)
    assert [record["minimum_depth"] for record in indices] == [1, 3, 5, 7, 9]


def test_h4_h5_forced_factors_and_sign_normalization():
    h_rows = ordinary_to_newton_rows(5)
    result = forced_factor_audit(h_rows)
    assert result["h4_forced_roots"] == [4, 5, 6, 7]
    assert result["h5_forced_roots"] == [5, 6, 7, 8, 9]
    assert result["h4_quotient_leading_positive"]
    assert result["h5_after_minus_quotient_leading_positive"]


def test_full_independent_audit():
    result = audit()
    assert result["verdict"] == "PASS"
    assert result["gamma_identity_checks"] == 5
    assert not result["author_verifier_imported"]
