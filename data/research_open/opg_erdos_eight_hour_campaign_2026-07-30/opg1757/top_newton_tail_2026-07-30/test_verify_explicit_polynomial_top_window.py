import json
from pathlib import Path

from verify_explicit_polynomial_top_window import (
    audit,
    ledger_checks,
    profile_norm_checks,
)


def test_explicit_constant_ledger():
    result = ledger_checks(256)
    assert result["difference_ledger_checks"] == 256
    assert result["fixed_offset_absorption_checks"] == 256
    assert profile_norm_checks(12) == 36


def test_explicit_eta_and_weighted_growth_certificate():
    result = audit(16, 16)
    assert result["proved_eta"] == "1/8"
    assert result["ordinary_symbol_power"] == 6
    assert result["exact_profile_norm_checks"] == 48
    assert result["weighted_symbol_checks"] == 136
    assert result["worst_weighted_ratio"] == "23/24"
    assert result["worst_weighted_location"] == {
        "depth": 2,
        "rank": 1,
    }
    assert result["classification"] == {
        "eta_one_eighth": "proved",
        "weighted_C_equals_3": "finite_evidence_only",
        "eta_one_third": "open",
    }
    assert result["status"] == "explicit_eta_certificate_passed"


def test_checked_in_certificate_matches_the_proved_boundary():
    path = Path(__file__).with_name(
        "EXPLICIT_POLYNOMIAL_TOP_WINDOW_CERTIFICATE.json"
    )
    certificate = json.loads(path.read_text())
    assert certificate["proved_eta"] == "1/8"
    assert certificate["weighted_C_equals_3"]["status"] == (
        "finite_evidence_only"
    )
    assert certificate["weighted_C_equals_3"]["checks"] == 820
    assert certificate["eta_one_third"] == "open"
