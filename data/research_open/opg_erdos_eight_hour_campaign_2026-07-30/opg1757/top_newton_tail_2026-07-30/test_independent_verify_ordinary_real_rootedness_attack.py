import json
from pathlib import Path

from independent_verify_ordinary_real_rootedness_attack import audit


def test_exact_real_rootedness_attack():
    result = audit(16)
    assert result["imports_root_claim_or_verifier"] is False
    assert result["exact_sturm_root_checks"] == 16
    assert result["strict_alternating_coefficient_checks"] == 152
    assert result["weighted_C3_checks"] == 152
    assert result["three_term_recurrence_obstructions"]["even"][
        "obstruction"
    ] == "2148751/12"
    assert result["hessenberg_negative_minor"] == "-125667"
    assert result["classification"]["real_rooted_all_d"] == "open"
    assert result["status"] == "finite_real_root_search_passed"


def test_checked_in_real_root_certificate():
    certificate = json.loads(
        Path(__file__).with_name(
            "ORDINARY_REAL_ROOTEDNESS_FINITE_CERTIFICATE.json"
        ).read_text()
    )
    assert certificate["maximum_depth"] == 40
    assert certificate["exact_sturm_root_checks"] == 40
    assert certificate["weighted_C3_checks"] == 860
    assert certificate["real_rooted_all_d"] == "open"
