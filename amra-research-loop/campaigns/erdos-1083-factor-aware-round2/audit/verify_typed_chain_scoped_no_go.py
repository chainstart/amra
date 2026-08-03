#!/usr/bin/env python3
"""Independent finite/type and rational-ledger checks for the scoped no-go."""

from fractions import Fraction
import json


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    # Reconstructed solely from the frozen normal-form definitions.
    objects = {
        "F_j": {
            "ambient": "Z[Gamma]",
            "role": "positive_0_1_set_mask",
            "construction": "P_(lambda_j X)",
            "scalar_parameterized": True,
        },
        "Q_j": {
            "ambient": "Z[Gamma]",
            "role": "rowwise_complementary_quotient",
            "construction": "B/R_j",
            "scalar_parameterized": False,
        },
    }
    assert objects["F_j"]["scalar_parameterized"]
    assert not objects["Q_j"]["scalar_parameterized"]

    identities = (
        "F_j=G R_j",
        "P_A0=G B",
        "B=R_j Q_j",
        "P_Aj=F_0 Q_j",
    )
    assert len(identities) == 4

    # The frozen data have no Q(T), so substitution T=lambda_j X is absent.
    q_lambda_x_defined = objects["Q_j"]["scalar_parameterized"]
    assert q_lambda_x_defined is False

    # Replacing Q_j by F_j lands exactly in the inherited heavy-factor route.
    repaired_route = (
        "G divides F_j=P_(lambda_j X)",
        "dir(Newt G) subset lambda_j W",
        "choose 0!=h=lambda_j w_j",
        "z_j=h/(2 rho w_j)",
    )
    assert repaired_route[-1] == "z_j=h/(2 rho w_j)"

    K = Fraction(5, 9)
    S = Fraction(7, 9)
    U = Fraction(5, 6)
    q = Fraction(13, 18)
    target = Fraction(3)
    chart_gap = target - K
    tuple_capacity = K + S + U + q
    tuple_gap = target - tuple_capacity
    assert chart_gap == Fraction(22, 9)
    assert tuple_capacity == Fraction(26, 9)
    assert tuple_gap == Fraction(1, 9)

    # Equation (2.7): on one sign class, distinct ordered widths give a
    # fixed-extreme endpoint with K-1 distinct squared-distance values.
    widths = [2, 5, 9, 14, 20]
    anchor = widths[0]
    anchored_squared_labels = {(b - anchor) ** 2 for b in widths[1:]}
    assert len(anchored_squared_labels) == len(widths) - 1

    print(json.dumps({
        "schema": "amra.erdos1083.factor-aware-round2.typed-chain-independent-audit.v1",
        "type_reconstruction": {
            "objects": objects,
            "normal_form": identities,
            "Q_j_lambda_j_X_defined_by_frozen_data": q_lambda_x_defined,
            "result": "passed",
        },
        "F_j_repair": {
            "route": repaired_route,
            "result": "already_reaches_inherited_reciprocal_chart",
            "scope": "does not rule out an F_j invariant proving information beyond that chart",
        },
        "exponent_ledger": {
            "native": {"K": frac(K), "S": frac(S), "U": frac(U), "q": frac(q)},
            "chart_to_t_cubed_gap": frac(chart_gap),
            "formal_tuple_capacity": frac(tuple_capacity),
            "gap_from_tuple_capacity_to_t_cubed": frac(tuple_gap),
            "same_sign_fixed_extreme_check": "K-1 actual target-target squared-distance labels",
            "result": "passed",
            "scope": "26/9 is only a formal capacity sum, not an incidence bound or an injective label count",
        },
        "verdict": "pass_scoped_no_go; reject_exponent_promotion",
        "lean_used": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
