#!/usr/bin/env python3
"""Fast exact Newton audit of the disjoint-core alpha^2 and alpha^3 layers.

The companion ``general_s_disjoint_low_degree.py`` first interpolates chain
entries symbolically.  That is convenient for displaying small formulas but
expensive beyond beta degree 12.  Here we instead evaluate the *final* layer
on the exact integer grid

    0 <= u=s-4 <= d,   0 <= t=r <= floor(d/2),

and take two-dimensional forward differences.  This directly gives the
coefficients in

    binomial(t,k) binomial(u,q).

This is a proof, not a numerical experiment.  A beta^m chain record uses at
most m anonymous core vertices.  If the remaining beta degree l comes from
the normalizing factor, its coefficient

    binomial(2s-4-j-k,l) s**l

has s-degree 2l.  Hence at total beta degree d the safe u-degree bound is
2d for alpha^2.  In the alpha^3 layer, the one additional core edge can
introduce at most two further anonymous vertices, giving 2d+2.  Every
nilpotent page uses at least two spokes, so the t-degree is at most floor(d/2).

The alpha^3 layer is included as an audit.  Its initial core vectors are
obtained by adding exactly one optional core edge to the minimal vectors:

    E_1  = 2(s-2) (3,1,...) + C(s-2,2) (2,2,1,...),
    Z_1  = C(s,2) (2,1,...),
    EF_1 = 4 (4,1,...) + 4(s-4) (3,2,1,...)
           + C(s-4,2) (2,2,2,1,...).

Thus [alpha^3] is 2 E_0 E_1 - Z_0 EF_1 - Z_1 EF_0 after the same positive
lambda^(2s-4) normalization as the alpha^2 layer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

from general_s_disjoint_low_degree import (
    Profile,
    truncated_profile_chain,
)


Chain = list[list[int]]
WeightedProfiles = dict[Profile, int]


def profile(*blocks: int, singletons: int) -> Profile:
    return tuple(sorted((*blocks, *((1,) * singletons))))


def initial_profile_combinations(
    s: int,
) -> dict[str, WeightedProfiles]:
    """Core-vector coefficients in alpha degrees 0/1 above the minimum."""

    return {
        "z0": {profile(singletons=s): 1},
        "e0": {profile(2, singletons=s - 2): 1},
        "ef0": {profile(2, 2, singletons=s - 4): 1},
        "z1": {
            profile(2, singletons=s - 2): math.comb(s, 2),
        },
        "e1": {
            profile(3, singletons=s - 3): 2 * (s - 2),
            profile(2, 2, singletons=s - 4): math.comb(s - 2, 2),
        },
        "ef1": {
            profile(4, singletons=s - 4): 4,
            profile(3, 2, singletons=s - 5): 4 * (s - 4),
            profile(2, 2, 2, singletons=s - 6): math.comb(s - 4, 2),
        },
    }


def add_scaled_chain(target: Chain, source: Chain, scale: int) -> None:
    for order, row in enumerate(source):
        for degree, value in enumerate(row):
            target[order][degree] += scale * value


def initial_chains(s: int, max_beta: int) -> dict[str, Chain]:
    max_order = max_beta // 2
    result: dict[str, Chain] = {}
    cache: dict[Profile, Chain] = {}
    for name, terms in initial_profile_combinations(s).items():
        combined = [
            [0] * (max_beta + 1) for _ in range(max_order + 1)
        ]
        for initial, coefficient in terms.items():
            if coefficient == 0:
                continue
            if initial not in cache:
                cache[initial] = truncated_profile_chain(initial, max_beta)
            add_scaled_chain(combined, cache[initial], coefficient)
        result[name] = combined
    return result


def convolve_with_lambda(
    left: list[int],
    right: list[int],
    exponent: int,
    s: int,
    max_beta: int,
) -> list[int]:
    """Coefficients of left*right*(1+s beta)^exponent."""

    if exponent < 0:
        if any(left) and any(right):
            raise AssertionError("a nonzero chain acquired a negative exponent")
        return [0] * (max_beta + 1)
    result = [0] * (max_beta + 1)
    for left_degree, left_value in enumerate(left):
        if not left_value:
            continue
        for right_degree, right_value in enumerate(right):
            used = left_degree + right_degree
            if not right_value or used > max_beta:
                continue
            for extra in range(min(exponent, max_beta - used) + 1):
                result[used + extra] += (
                    left_value
                    * right_value
                    * math.comb(exponent, extra)
                    * s**extra
                )
    return result


def layer_values_at_s(
    s: int, max_beta: int, alpha_degree: int
) -> list[list[int]]:
    """Return value[t][d] for t=0..floor(max_beta/2)."""

    chains = initial_chains(s, max_beta)
    if alpha_degree == 2:
        products = (
            (1, "e0", "e0"),
            (-1, "z0", "ef0"),
        )
    elif alpha_degree == 3:
        products = (
            (2, "e0", "e1"),
            (-1, "z0", "ef1"),
            (-1, "z1", "ef0"),
        )
    else:
        raise ValueError("only alpha degrees 2 and 3 are implemented")

    max_order = max_beta // 2
    pair_layers: list[tuple[int, int, int, list[int]]] = []
    for sign, left_name, right_name in products:
        for left_order in range(max_order + 1):
            left = chains[left_name][left_order]
            if not any(left):
                continue
            for right_order in range(max_order + 1):
                right = chains[right_name][right_order]
                if not any(right):
                    continue
                exponent = 2 * s - 4 - left_order - right_order
                coefficients = convolve_with_lambda(
                    left, right, exponent, s, max_beta
                )
                if any(coefficients):
                    pair_layers.append(
                        (
                            sign,
                            left_order,
                            right_order,
                            coefficients,
                        )
                    )

    values = [
        [0] * (max_beta + 1) for _ in range(max_order + 1)
    ]
    for t in range(max_order + 1):
        for sign, left_order, right_order, coefficients in pair_layers:
            factor = (
                sign
                * math.comb(t, left_order)
                * math.comb(t, right_order)
            )
            if not factor:
                continue
            for degree, coefficient in enumerate(coefficients):
                values[t][degree] += factor * coefficient
    return values


def forward_differences(values: list[int]) -> list[int]:
    result: list[int] = []
    current = values
    while current:
        result.append(current[0])
        current = [
            current[index + 1] - current[index]
            for index in range(len(current) - 1)
        ]
    return result


def newton_rows(
    max_beta: int, alpha_degree: int
) -> list[list[object]]:
    """Compute exact beta,t,u Newton rows by bounded-grid differences."""

    u_degree_slack = 0 if alpha_degree == 2 else 2
    maximum_u_degree = 2 * max_beta + u_degree_slack
    by_u = [
        layer_values_at_s(4 + u, max_beta, alpha_degree)
        for u in range(maximum_u_degree + 1)
    ]
    rows: list[list[object]] = []
    minimum_degree = 4 if alpha_degree == 2 else 2
    for degree in range(minimum_degree, max_beta + 1):
        max_t_order = degree // 2
        t_coefficients_by_u = [
            forward_differences(
                [by_u[u][t][degree] for t in range(max_t_order + 1)]
            )
            for u in range(2 * degree + u_degree_slack + 1)
        ]
        for t_order in range(max_t_order + 1):
            u_coefficients = forward_differences(
                [
                    t_coefficients_by_u[u][t_order]
                    for u in range(2 * degree + u_degree_slack + 1)
                ]
            )
            for u_order, coefficient in enumerate(u_coefficients):
                if coefficient:
                    rows.append(
                        [degree, t_order, u_order, str(coefficient)]
                    )
    return rows


def build_certificate(max_beta: int = 20) -> dict[str, object]:
    sections: dict[str, object] = {}
    for alpha_degree in (2, 3):
        rows = newton_rows(max_beta, alpha_degree)
        negative_rows = [
            row for row in rows if int(str(row[3])) < 0
        ]
        payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
        sections[str(alpha_degree)] = {
            "beta_degrees": [
                4 if alpha_degree == 2 else 2,
                max_beta,
            ],
            "rows_beta_tbin_ubin_coefficient": rows,
            "negative_rows": negative_rows,
            "all_newton_coefficients_nonnegative": not negative_rows,
            "sha256_rows": hashlib.sha256(payload).hexdigest(),
        }
    return {
        "schema": "amra.complete_split.general_s_disjoint_extended.v1",
        "normalization": (
            "lambda^(2s-4), lambda=1+s*beta, after removing the common "
            "positive lambda^(2t) factor"
        ),
        "variables": "u=s-4>=0, t=r>=0",
        "basis": "alpha^a beta^d binomial(t,k) binomial(u,q)",
        "exactness": (
            "For beta degree d, t-degree <= floor(d/2).  The u-degree is "
            "<=2d for alpha^2 and <=2d+2 for alpha^3.  The saved rows are "
            "exact bounded-grid forward differences."
        ),
        "beta_degrees_by_alpha": {"2": [4, max_beta], "3": [2, max_beta]},
        "alpha_degrees": sections,
        "scope_warning": (
            "This audits only the disjoint-core edge orbit and alpha "
            "degrees 2 and 3; it is not the full multivariate theorem."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-beta", type=int, default=20)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.max_beta < 4:
        raise ValueError("max_beta must be at least 4")
    certificate = build_certificate(args.max_beta)
    rendered = json.dumps(certificate, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
