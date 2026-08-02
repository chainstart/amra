from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name("verify_negative_precap.py")
SPEC = importlib.util.spec_from_file_location("verify_negative_precap", MODULE)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def test_symbolic_recurrence_guards() -> None:
    VERIFY.check_pre_cap_words()
    VERIFY.check_offset_monotonicity()


def test_first_wall_atlas() -> None:
    VERIFY.check_first_wall_atlas()


def test_finite_first_cap_falsifier() -> None:
    result = VERIFY.first_cap_falsifier()
    assert result["negative_without_next_seed"] == 0
