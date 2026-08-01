from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("verify_rank6_carry.py")
SPEC = importlib.util.spec_from_file_location("verify_rank6_carry", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


def test_two_independent_local_certificates_agree() -> None:
    inherited = VERIFY.local_orbit(
        VERIFY.ENGINE.upper_raise,
        VERIFY.ENGINE.lower_shadow,
    )
    independent = VERIFY.local_orbit(
        VERIFY.independent_upper,
        VERIFY.independent_lower,
    )
    assert inherited == independent
    assert inherited["gamma5"] == -46_063
    assert inherited["reserve_minus_increment"] == -84


def test_closed_form_infinite_family() -> None:
    VERIFY.check_closed_form_family()


def test_fixed_rank_obstruction_recurrence() -> None:
    VERIFY.check_fixed_rank_obstruction()
    VERIFY.check_adaptive_candidate()
    VERIFY.check_critical_offset_chamber()
    VERIFY.check_exceptional_offsets()
    VERIFY.check_rank2_endpoint_principle()
    VERIFY.check_moving_rank4_atlas()
    VERIFY.check_synchronized_chart()


def test_global_and_local_surplus_match() -> None:
    VERIFY.check_global_orbit(-46_063)
    VERIFY.check_extended_local_to_global()
