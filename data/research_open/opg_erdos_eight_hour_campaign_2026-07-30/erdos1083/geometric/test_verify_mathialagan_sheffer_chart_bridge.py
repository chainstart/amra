import ast
import math
from pathlib import Path

import verify_mathialagan_sheffer_chart_bridge as bridge
from verify_mathialagan_sheffer_chart_bridge import (
    BALANCED_CRITICAL_INCIDENCE_EXPONENT,
    audit,
    chart_exception,
    source_distance_exponent,
    symbolic_special_case_certificates,
)


def test_aligned_parameter_translation():
    assert (
        chart_exception(
            alpha1=0.4,
            alpha2=0.4,
            A1=3.0,
            A2=3.0,
            w1=-0.2,
            w2=-0.2,
        )
        == "aligned"
    )
    assert (
        chart_exception(
            alpha1=0.4,
            alpha2=0.4 + math.pi,
            A1=3.0,
            A2=-3.0,
            w1=-0.2,
            w2=-0.2,
        )
        == "aligned"
    )


def test_perpendicular_translation_and_active_exclusion():
    assert (
        chart_exception(
            alpha1=0.0,
            alpha2=math.pi / 2,
            A1=0.0,
            A2=0.0,
            w1=1.0,
            w2=-2.0,
        )
        == "perpendicular"
    )
    assert (
        chart_exception(
            alpha1=0.0,
            alpha2=math.pi / 2,
            A1=0.1,
            A2=0.2,
            w1=1.0,
            w2=-2.0,
        )
        == "expanding"
    )


def test_critical_exponent_thresholds():
    assert str(BALANCED_CRITICAL_INCIDENCE_EXPONENT) == "9/4"
    assert source_distance_exponent(
        BALANCED_CRITICAL_INCIDENCE_EXPONENT,
        BALANCED_CRITICAL_INCIDENCE_EXPONENT,
    ) == 3
    assert source_distance_exponent(2.3, 2.3) > 3.0
    assert source_distance_exponent(1.5, 3.0) == 3.0
    assert source_distance_exponent(1.4, 3.0) < 3.0


def test_exact_symbolic_special_cases_and_ast_constant():
    assert all(symbolic_special_case_certificates().values())
    tree = ast.parse(Path(bridge.__file__).read_text())
    assignments = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name)
            and target.id == "BALANCED_CRITICAL_INCIDENCE_EXPONENT"
            for target in node.targets
        )
    ]
    assert len(assignments) == 1
    value = assignments[0].value
    assert isinstance(value, ast.Call)
    assert isinstance(value.func, ast.Name)
    assert value.func.id == "Fraction"
    assert [argument.value for argument in value.args] == [9, 4]


def test_full_bridge_audit():
    result = audit()
    assert result["status"] == "PASS"
    assert result["perpendicular_excluded_when_A_nonzero"] is True
