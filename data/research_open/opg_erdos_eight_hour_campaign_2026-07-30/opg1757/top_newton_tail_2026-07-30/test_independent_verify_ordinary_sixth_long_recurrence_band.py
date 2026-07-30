import ast
from pathlib import Path

import sympy as sp

import independent_verify_ordinary_sixth_long_recurrence_band as independent_module
from independent_verify_ordinary_sixth_long_recurrence_band import (
    D,
    N,
    FIRST_ADMISSIBLE_VALUE,
    SHIFTED_NUMERATOR_COEFFICIENTS,
    audit,
    derive_triangles,
    signed_stirling_loss_rows,
)


def test_newton_identity_stirling_rows_against_direct_falling_factorial():
    rows = signed_stirling_loss_rows(6)
    x = sp.symbols("x")
    for depth in range(6, 13):
        falling = sp.Poly(
            sp.prod(x - value for value in range(depth)), x
        )
        for loss in range(7):
            assert rows[loss].subs(N, depth) == falling.coeff_monomial(
                x ** (depth - loss)
            )


def test_symbolic_h6_roots_and_gamma_boundary_value():
    h_rows, bands = derive_triangles()
    for root in range(6, 12):
        assert h_rows[6].subs(D, root) == 0
    assert sp.cancel(bands[5].subs(D, 11)) == FIRST_ADMISSIBLE_VALUE


def test_full_independent_sixth_band_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["reduced_denominator"] == "15359376162816000"
    assert result["positive_shift_coefficient_count"] == 18
    assert result["positive_shift_coefficients"] == list(
        SHIFTED_NUMERATOR_COEFFICIENTS
    )
    assert result["h6_forced_roots"] == [6, 7, 8, 9, 10, 11]
    assert result["h6_forced_roots_are_simple"]
    assert (
        result["h6_quotient_denominator"]
        == "2764687709306880000"
    )
    source = Path(independent_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.add(node.module)
    assert (
        "verify_ordinary_sixth_long_recurrence_band"
        not in imported_modules
    )
