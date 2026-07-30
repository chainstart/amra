import ast
from pathlib import Path

import sympy as sp

import independent_verify_ordinary_rank_seven_and_seventh_band as verifier
from independent_verify_ordinary_rank_seven_and_seventh_band import (
    DEPTH,
    PAGE,
    PROFILE_D,
    SEVENTH_BAND_SHIFTED_COEFFICIENTS,
    audit,
    exact_lagrange_polynomial,
    independently_generated_rank_seven_value,
    rank_seven_polynomial,
)


def test_defining_lagrange_products_and_disjoint_depth_holdouts():
    sample = [(1, 5), (3, 15), (6, 45)]
    polynomial = exact_lagrange_polynomial(sample, PAGE)
    assert polynomial.as_expr() == PAGE**2 + PAGE + 3

    for depth in (7, 30, 31, 32):
        assert independently_generated_rank_seven_value(depth) == (
            rank_seven_polynomial(DEPTH).subs(DEPTH, depth)
        )


def test_depth_symbols_are_genuinely_distinct():
    assert DEPTH != PROFILE_D
    assert DEPTH.name == "depth"
    assert PROFILE_D.name == "d"
    assert PROFILE_D not in rank_seven_polynomial(DEPTH).free_symbols


def test_full_independent_rank_seven_and_band_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["rank_seven"]["interpolation_depths"] == list(
        range(8, 30)
    )
    assert result["rank_seven"]["holdout_depths"] == [7, 30, 31, 32]
    assert result["rank_seven"]["p7_shifted_coefficient_count"] == 22
    assert (
        result["sixth_normalized_newton"][
            "shifted_coefficient_count"
        ]
        == 38
    )
    assert result["rank_seven_c3"]["shifted_coefficient_count"] == 22
    assert result["seventh_band"]["shifted_coefficients"] == list(
        SEVENTH_BAND_SHIFTED_COEFFICIENTS
    )
    assert result["seventh_band"]["h7_forced_roots_are_simple"]


def test_author_verifier_is_not_an_import_dependency():
    source = Path(verifier.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
    assert (
        "verify_ordinary_rank_seven_and_seventh_band"
        not in imported_modules
    )
