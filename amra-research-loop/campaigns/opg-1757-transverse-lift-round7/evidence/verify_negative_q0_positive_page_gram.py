#!/usr/bin/env python3
"""Exact Gram certificates for six q0-negative chambers with P pages."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

from verify_mixed_three_negative import divide_polynomial
from verify_negative_c_direct_chambers import (
    add,
    constant,
    multiply,
    power,
    variable,
)
from verify_negative_page_direct_chambers import (
    chart_polynomial,
    digest,
    schur_substitute,
)
from verify_negative_q0_no_positive_gram import (
    build_delta,
    common_monomial,
    divide_monomial,
    gram,
    positive_bernstein,
    quadratic_certificate,
)
from verify_nonnegative_route_chambers import state_polynomial


EVIDENCE = Path(__file__).parent
TAU = 7


def route_quantity(index, state):
    """Return q for a positive page in its P/L/R chart."""
    assert index in (1, 2) and state in "PLR"
    first = variable(1 + 2 * index)
    second = variable(2 + 2 * index)
    if state == "P":
        return add(add(multiply(first, second), first), second)
    return first


def positive_route_determinant(state):
    """Return B for the positive routes c,q3,q4."""
    c = variable(0)
    q3 = route_quantity(1, state[1])
    q4 = route_quantity(2, state[2])
    return add(
        add(multiply(multiply(c, q3), q4), multiply(c, q3)),
        add(multiply(c, q4), multiply(q3, q4)),
    )


def state_schur(delta, state):
    states = tuple(state)
    cleared = chart_polynomial(delta, states, 0)
    schur, a_degree = schur_substitute(cleared, states, 0)
    assert a_degree == 2
    return schur


def monomial(degrees):
    return {tuple(degrees): Fraction(1)}


def permute_slots(poly, pairs):
    """Apply disjoint variable swaps and collect exact coefficients."""
    mapping = list(range(8))
    for left, right in pairs:
        mapping[left], mapping[right] = mapping[right], mapping[left]
    result = {}
    for powers, value in poly.items():
        transformed = [0] * 8
        for old_slot, degree in enumerate(powers):
            transformed[mapping[old_slot]] = degree
        transformed = tuple(transformed)
        result[transformed] = result.get(transformed, Fraction()) + value
    return {powers: value for powers, value in result.items() if value}


def outer_core(determinant, state):
    """Divide the outer tau-Gram determinant by all manifest squares."""
    assert state in ("LPP", "LPR")
    s0 = variable(2)
    s4 = variable(6)
    one_minus_s0 = add(constant(1), s0, -1)
    B = positive_route_determinant(state)
    q3 = route_quantity(1, state[1])
    q4 = route_quantity(2, state[2])
    common = (4, 0, 2, 2, 0, 2, 0, 0)
    if state == "LPP":
        factors = (one_minus_s0, q3, q4, B)
    else:
        one_minus_s4 = add(constant(1), s4, -1)
        factors = (
            one_minus_s0,
            q3,
            add(q4, s4),
            one_minus_s4,
            B,
        )
    positive_factor = constant(1)
    for factor in factors:
        positive_factor = multiply(positive_factor, power(factor, 2))
    quotient = divide_monomial(determinant, common)
    core = divide_polynomial(quotient, positive_factor)
    assert determinant == multiply(
        monomial(common),
        multiply(positive_factor, core),
    )
    return core, common


def lift_q0_zero(poly):
    """Restrict a seven-slot nonnegative-chart polynomial to q0=0 and lift."""
    result = {}
    for powers, value in poly.items():
        if powers[1] != 0:
            continue
        lifted = tuple(powers) + (0,)
        result[lifted] = value
    return result


def beta0_dependency(beta0, delta, state, theorem):
    """Check beta0=B^2 times the already-certified q0=0 chart exactly."""
    assert state in theorem["certified_chambers"]
    q0_zero = lift_q0_zero(state_polynomial(delta, tuple(state)))
    B = positive_route_determinant(state)
    assert beta0 == multiply(q0_zero, power(B, 2))
    return {
        "terms": len(beta0),
        "q0_zero_chart_terms": len(q0_zero),
        "exact_identity": "beta0=B^2*Delta_chart(q0=0)",
        "dependency_schema": theorem["schema"],
        "dependency_conclusion": theorem["conclusion"],
        "sha256": digest(beta0),
    }


def beta2_certificate(beta2, state):
    if state == "LPP":
        transformed = positive_bernstein(beta2, [2])
        assert len(transformed) == 4145
        assert min(transformed.values()) == Fraction(1, 6)
        return {
            "kind": "direct_tensor_bernstein",
            "terms": len(beta2),
            "bounded_slots": [2],
            "bernstein_nonzero": len(transformed),
            "minimum": str(min(transformed.values())),
            "sha256": digest(beta2),
        }

    assert state == "LPR"
    one_minus_s4 = add(constant(1), variable(6), -1)
    quotient = divide_polynomial(beta2, one_minus_s4)
    assert beta2 == multiply(one_minus_s4, quotient)
    record = quadratic_certificate(quotient, 6, [2])
    assert record["endpoint_bernstein_nonzero"] == [428, 698]
    assert record["endpoint_minimum"] == ["1/6", "1/6"]
    assert record["determinant_terms"] == 5878
    assert record["determinant_common_monomial"] == [0, 0, 2, 0, 0, 0, 0, 0]
    assert record["determinant_residual_terms"] == 5878
    assert record["determinant_bernstein_nonzero"] == 7331
    assert record["determinant_minimum"] == "1/15"
    return {
        "kind": "one_minus_s4_times_unit_interval_gram",
        "terms": len(beta2),
        "positive_factor": "1-s4",
        "quotient": record,
        "sha256": digest(beta2),
    }


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(",", ":"))


def main():
    delta, forest_count, connected_count = build_delta()
    theorem = json.loads(
        (EVIDENCE / "nonnegative_effective_route_theorem.json").read_text()
    )
    assert theorem["certified_count"] == 27

    representatives = {
        state: state_schur(delta, state)
        for state in ("LPP", "LPR")
    }
    all_states = {
        state: state_schur(delta, state)
        for state in ("LPP", "LPR", "LRP", "RLP", "RPL", "RPP")
    }
    assert permute_slots(representatives["LPR"], ((3, 5), (4, 6))) == all_states["LRP"]
    assert permute_slots(representatives["LPP"], ((3, 4), (5, 6))) == all_states["RPP"]
    assert permute_slots(representatives["LPR"], ((3, 4),)) == all_states["RPL"]
    assert permute_slots(all_states["LRP"], ((5, 6),)) == all_states["RLP"]

    records = {}
    for state, schur in representatives.items():
        beta0, _, beta2, determinant = gram(schur, TAU)
        core, common = outer_core(determinant, state)
        if state == "LPP":
            assert len(core) == 195
            transformed = positive_bernstein(core, [2])
            assert len(transformed) == 215
            assert min(transformed.values()) == 1
            core_record = {
                "kind": "direct_tensor_bernstein",
                "terms": len(core),
                "bounded_slots": [2],
                "bernstein_nonzero": len(transformed),
                "minimum": str(min(transformed.values())),
                "sha256": digest(core),
            }
        else:
            assert state == "LPR" and len(core) == 87
            core_record = {
                "kind": "nested_unit_interval_gram",
                **quadratic_certificate(core, 6, [2]),
            }
            assert core_record["endpoint_bernstein_nonzero"] == [17, 57]
            assert core_record["endpoint_minimum"] == ["1", "1"]
            assert core_record["determinant_terms"] == 222
            assert core_record["determinant_bernstein_nonzero"] == 237
            assert core_record["determinant_minimum"] == "1"
        records[state] = {
            "schur_terms": len(schur),
            "outer_gram_terms": len(determinant),
            "outer_common_monomial": list(common),
            "beta0": beta0_dependency(beta0, delta, state, theorem),
            "beta2": beta2_certificate(beta2, state),
            "outer_core": core_record,
            "schur_sha256": digest(schur),
        }

    theorem_hash = sha256(canonical(theorem).encode()).hexdigest()
    print(json.dumps({
        "schema": "amra.opg1757.round7.negative-q0-positive-page-gram.v1",
        "reconstruction": {
            "deletion_forests": forest_count,
            "endpoint_connected_forests": connected_count,
            "Delta_b_original_terms": len(delta),
        },
        "domain": "q0<0, q3>0, q4>0, c>0, K>0; the q0 page has one negative activity and at least one other page is in its nonnegative-activity P chart",
        "representatives": ["LPP", "LPR"],
        "symmetry_closure": {
            "LPP": ["LPP", "RPP"],
            "LPR": ["LPR", "LRP", "RLP", "RPL"],
        },
        "certified_chambers": ["LPP", "LPR", "LRP", "RLP", "RPL", "RPP"],
        "certified_count": 6,
        "beta0_dependency": {
            "artifact": "nonnegative_effective_route_theorem.json",
            "sha256": theorem_hash,
            "reason": "at tau=0 the negative L chart is exactly the q0=0 nonnegative L chart",
        },
        "records": records,
        "conclusion": "Delta_b>=0 in all six listed q0-negative positive-page chambers",
        "scope": "six additional q0-negative activity chambers; five q0-negative N chambers and all unresolved q3/q4-negative orientations remain open, so the generic sign and OPG-1757 are not claimed",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
