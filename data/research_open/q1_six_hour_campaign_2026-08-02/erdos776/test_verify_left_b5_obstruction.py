from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name("verify_left_b5_obstruction.py")
SPEC = importlib.util.spec_from_file_location("verify_left_b5", MODULE)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def test_exact_certificate_and_global_orbit() -> None:
    VERIFY.check_certificate()


def test_stable_words_and_first_failure() -> None:
    VERIFY.check_stable_recurrence()
    VERIFY.check_first_rank_five_failure()


def test_adaptive_growth_inequalities() -> None:
    VERIFY.check_growth_inequalities()
