import sympy as sp

from verify_complete_log_layer import certify


def test_complete_log_layer_finite_certificate() -> None:
    result = certify(include_scan=False)
    assert result["source_sha256"].startswith("a4c8bbf5")
    assert result["spectrum"] == {
        "odd_sufficient": {
            "top_monomials": 25,
            "strictly_lower_monomials": 710,
        },
        "even_sufficient": {
            "top_monomials": 36,
            "strictly_lower_monomials": 1222,
        },
        "odd_page": {
            "top_monomials": 21,
            "strictly_lower_monomials": 525,
        },
        "even_page": {
            "top_monomials": 31,
            "strictly_lower_monomials": 949,
        },
    }
    assert result["complete_channel_identities"]["p6"] == {
        "first_positive_degree": 8,
        "checked_positive_sufficient_leads": 65,
        "checked_positive_page_leads": 65,
        "page_transition_constant": sp.Rational(4, 125),
    }
    assert result["complete_channel_identities"]["p7"] == {
        "first_positive_degree": 10,
        "checked_positive_sufficient_leads": 65,
        "checked_positive_page_leads": 65,
        "page_transition_constant": sp.Rational(49, 2160),
    }
