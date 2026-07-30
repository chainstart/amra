import ast
from pathlib import Path

import independent_verify_ordinary_rank_eight_and_eighth_band as verifier
from independent_verify_ordinary_rank_eight_and_eighth_band import (
    DEPTH,
    EIGHTH_BAND_SHIFTED_COEFFICIENTS,
    EXPECTED_HASHES,
    PROFILE_D,
    audit,
    independently_generated_rank_eight_value,
    rank_eight_polynomial,
)


def test_rank_eight_depth_holdouts_not_used_for_interpolation():
    for depth in (8, 34, 35, 36):
        assert independently_generated_rank_eight_value(depth) == (
            rank_eight_polynomial(DEPTH).subs(DEPTH, depth)
        )


def test_rank_eight_depth_symbol_is_separate():
    assert DEPTH != PROFILE_D
    assert DEPTH.name == "rank8_depth"
    assert PROFILE_D.name == "d"
    assert PROFILE_D not in rank_eight_polynomial(DEPTH).free_symbols


def test_full_independent_rank_eight_and_eighth_band_certificate():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rank_eight"]["degree"] == 24
    assert result["rank_eight"]["interpolation_depths"] == list(
        range(9, 34)
    )
    assert result["rank_eight"]["holdout_depths"] == [8, 34, 35, 36]
    assert result["rank_eight"]["shifted_sha256"] == EXPECTED_HASHES[
        "beta8_shift"
    ]
    assert (
        result["seventh_normalized_newton"][
            "shifted_coefficient_count"
        ]
        == 44
    )
    assert result["rank_eight_c3"]["shifted_coefficient_count"] == 25
    assert result["eighth_band"]["shifted_coefficients"] == list(
        EIGHTH_BAND_SHIFTED_COEFFICIENTS
    )
    assert result["eighth_band"]["h8_forced_roots_are_simple"]


def test_no_author_rank_eight_verifier_import():
    source = Path(verifier.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
    assert not any(
        name.startswith("verify_ordinary_rank_eight")
        for name in imported_modules
    )
