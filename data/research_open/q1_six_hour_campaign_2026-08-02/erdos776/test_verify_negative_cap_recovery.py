from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name("verify_negative_cap_recovery.py")
SPEC = importlib.util.spec_from_file_location("verify_negative_cap_recovery", MODULE)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def test_gap_invariant() -> None:
    VERIFY.check_gap_invariant()


def test_initial_recovery_identities() -> None:
    counts = VERIFY.check_initial_recovery_identities()
    assert all(counts.values())


def test_later_first_cap_falsifier() -> None:
    result = VERIFY.later_first_cap_falsifier()
    assert result["minimum_gamma"] > 0
