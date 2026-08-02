from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE = Path(__file__).with_name("verify_negative_initial_chambers.py")
SPEC = importlib.util.spec_from_file_location("verify_negative_initial", MODULE)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def test_asymmetric_chamber() -> None:
    counts = VERIFY.check_asymmetric_chamber()
    assert all(counts.values())


def test_dimensionless_chart() -> None:
    VERIFY.check_dimensionless_chart()


def test_finite_low_block_guard() -> None:
    result = VERIFY.finite_low_block_guard()
    assert result["minimum_x_one"] > 0
    assert result["minimum_y_one"] > 0


def test_finite_no_borrow_falsifier() -> None:
    result = VERIFY.finite_no_borrow_falsifier()
    assert result["negative_rank_five"] == 0
