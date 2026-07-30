import math

import audit_general_f_leading_base4_newton as audit


def test_small_complete_graph_forest_rows() -> None:
    # K_3 has 1, 3, 3 forests in degrees 0, 1, 2.
    assert audit.complete_graph_forest_coefficients(0, 3, 2) == (1, 3, 3)


def test_base_four_newton_audit_through_thirty_pages() -> None:
    certificate = audit.build_audit(30)
    for row in certificate["rows"]:
        assert row["all_newton_coefficients_nonnegative"]
        assert (
            row["first_nonzero_newton_index"]
            == (row["page_count"] - 2) // 2
        )
        assert row["top_newton_coefficient"] == math.factorial(
            row["degree"]
        )
