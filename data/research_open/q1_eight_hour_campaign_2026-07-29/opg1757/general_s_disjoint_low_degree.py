#!/usr/bin/env python3
"""General-s low-degree certificate for the disjoint-core Rayleigh margin.

This is a deliberately narrow complement to ``complete_split_rayleigh.py``.
For the edge pair (01,23), it proves that the alpha^2 beta^d part of the
positive-factor-normalized margin has nonnegative coefficients for

    4 <= d <= max_beta  (default max_beta=8),

simultaneously for every clique size s>=4 and every page count r>=0.

Put u=s-4 and t=r.  The output basis is

    beta^d binomial(t,k) binomial(u,q).

Why finite interpolation in s is exact
--------------------------------------
In N^j, a beta^d term records j ordered page masks with exactly d total
spoke incidences.  Apart from the four marked core vertices, such a record
mentions at most d anonymous core vertices.  Its count is consequently a
polynomial in u=s-4 of degree at most d, naturally in the binomial basis.
The d+1 exact evaluations u=0,...,d therefore determine it identically,
not statistically.  The code uses max_beta+1 values for every chain entry,
then performs the remaining algebra symbolically.

The result is only a low-(alpha,beta)-degree slice.  It is not a proof of
the complete margin for arbitrary s.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import Counter
from collections import defaultdict
from pathlib import Path

import sympy as sp


S, T, U = sp.symbols("s t u", integer=True)
Profile = tuple[int, ...]


def profile_selections(
    profile: Profile, maximum_size: int
) -> list[tuple[int, int, Profile]]:
    """Aggregate spoke masks by how many blocks of each size they select.

    The old implementation enumerated subsets of the *positions* in
    ``profile``.  Most positions are anonymous singleton blocks, so that
    becomes wasteful as ``s`` grows.  If ``k_w`` blocks of size ``w`` are
    selected, the number of actual spoke masks is

        product_w binomial(c_w,k_w) w**k_w.

    This routine returns ``(number_selected, multiplicity, destination)``.
    It is exactly the same transfer, merely quotiented by equal block sizes.
    """

    counts = sorted(Counter(profile).items())
    result: list[tuple[int, int, Profile]] = []

    def visit(
        index: int,
        selected_count: int,
        merged_size: int,
        multiplicity: int,
        remaining: list[int],
    ) -> None:
        if selected_count > maximum_size:
            return
        if index == len(counts):
            if selected_count >= 2:
                destination = tuple(sorted((*remaining, merged_size)))
                result.append(
                    (selected_count, multiplicity, destination)
                )
            return

        block_size, count = counts[index]
        for chosen in range(min(count, maximum_size - selected_count) + 1):
            visit(
                index + 1,
                selected_count + chosen,
                merged_size + chosen * block_size,
                multiplicity
                * math.comb(count, chosen)
                * block_size**chosen,
                remaining + [block_size] * (count - chosen),
            )

    visit(0, 0, 0, 1, [])
    return result


def initial_profile(s: int, kind: str) -> Profile:
    """Block-size profile of the minimal-alpha core state."""

    if kind == "z":
        return (1,) * s
    if kind == "e":
        return tuple(sorted((2, *((1,) * (s - 2)))))
    if kind == "ef":
        return tuple(sorted((2, 2, *((1,) * (s - 4)))))
    raise ValueError(f"unknown core state {kind}")


def truncated_chain_sums(
    s: int, kind: str, max_beta: int
) -> list[list[int]]:
    """Return [beta^d] sum(N^j v_kind), truncated at max_beta."""

    return truncated_profile_chain(initial_profile(s, kind), max_beta)


def truncated_profile_chain(
    profile: Profile, max_beta: int
) -> list[list[int]]:
    """Return the N-chain sums for one arbitrary block-size profile."""

    max_order = max_beta // 2
    vector: dict[tuple[Profile, int], int] = {
        (profile, 0): 1
    }
    chain: list[list[int]] = []
    for _ in range(max_order + 1):
        total = [0] * (max_beta + 1)
        for (_, degree), coefficient in vector.items():
            total[degree] += coefficient
        chain.append(total)

        next_vector: defaultdict[tuple[Profile, int], int] = defaultdict(int)
        for (profile, old_degree), coefficient in vector.items():
            maximum_size = max_beta - old_degree
            for mask_size, multiplicity, destination in profile_selections(
                profile, maximum_size
            ):
                next_vector[
                    (destination, old_degree + mask_size)
                ] += coefficient * multiplicity
        vector = dict(next_vector)
    return chain


def interpolated_chain_data(max_beta: int) -> dict[tuple[str, int, int], sp.Expr]:
    """Interpolate every needed N-chain coefficient exactly in s."""

    sample_sizes = range(4, 4 + max_beta + 1)
    raw = {
        s: {
            kind: truncated_chain_sums(s, kind, max_beta)
            for kind in ("z", "e", "ef")
        }
        for s in sample_sizes
    }
    data: dict[tuple[str, int, int], sp.Expr] = {}
    for kind in ("z", "e", "ef"):
        data[(kind, 0, 0)] = sp.S.One
        for order in range(1, max_beta // 2 + 1):
            for degree in range(2 * order, max_beta + 1):
                values = [
                    (s, raw[s][kind][order][degree]) for s in sample_sizes
                ]
                polynomial = sp.interpolate(values, S)
                if sp.degree(polynomial, S) > degree:
                    raise AssertionError("the incidence degree bound was violated")
                data[(kind, order, degree)] = sp.expand(polynomial)
    return data


def ordinary_beta_layers(max_beta: int) -> dict[int, sp.Expr]:
    """Derive [alpha^2 beta^d] of the normalized disjoint-edge margin."""

    chain = interpolated_chain_data(max_beta)
    layers: list[sp.Expr] = [sp.S.Zero] * (max_beta + 1)
    max_order = max_beta // 2

    # At minimal alpha degree, the three core vectors have one state and
    # coefficient one.  Thus the margin is R_e^2 - R_z R_ef.  A product of
    # order-j and order-k terms has denominator lambda^(j+k); multiplication
    # by lambda^(2s-4) gives the canonical numerator used in the finite-s
    # certificates.
    for sign, left, right in ((1, "e", "e"), (-1, "z", "ef")):
        for j in range(max_order + 1):
            for k in range(max_order + 1):
                t_factor = (
                    sign
                    * sp.expand_func(sp.binomial(T, j))
                    * sp.expand_func(sp.binomial(T, k))
                )
                lambda_exponent = 2 * S - 4 - j - k
                for left_degree in range(max_beta + 1):
                    left_coefficient = chain.get(
                        (left, j, left_degree), sp.S.Zero
                    )
                    if left_coefficient == 0:
                        continue
                    for right_degree in range(
                        max_beta - left_degree + 1
                    ):
                        right_coefficient = chain.get(
                            (right, k, right_degree), sp.S.Zero
                        )
                        if right_coefficient == 0:
                            continue
                        used_degree = left_degree + right_degree
                        for lambda_degree in range(
                            max_beta - used_degree + 1
                        ):
                            layers[used_degree + lambda_degree] += (
                                t_factor
                                * left_coefficient
                                * right_coefficient
                                * sp.expand_func(
                                    sp.binomial(
                                        lambda_exponent, lambda_degree
                                    )
                                )
                                * S**lambda_degree
                            )
    return {
        degree: sp.expand_func(sp.expand(layers[degree]))
        for degree in range(4, max_beta + 1)
    }


def newton_coefficients(polynomial: sp.Expr, variable: sp.Symbol) -> list[sp.Expr]:
    univariate = sp.Poly(sp.expand(polynomial), variable)
    values = [
        univariate.eval(value) for value in range(univariate.degree() + 1)
    ]
    coefficients: list[sp.Expr] = []
    while values:
        coefficients.append(sp.factor(values[0]))
        values = [
            sp.expand(values[index + 1] - values[index])
            for index in range(len(values) - 1)
        ]
    return coefficients


def build_certificate(max_beta: int = 8) -> dict[str, object]:
    if max_beta < 4:
        raise ValueError("max_beta must be at least 4")
    layers = ordinary_beta_layers(max_beta)
    rows: list[list[object]] = []
    formulas: dict[str, str] = {}

    for beta_degree, layer in layers.items():
        formulas[str(beta_degree)] = str(sp.factor(layer))
        t_coefficients = newton_coefficients(layer, T)
        reconstructed_t = sp.S.Zero
        for t_order, s_coefficient in enumerate(t_coefficients):
            if s_coefficient == 0:
                continue
            u_polynomial = sp.expand(s_coefficient.subs(S, U + 4))
            u_coefficients = newton_coefficients(u_polynomial, U)
            reconstructed_u = sp.S.Zero
            for u_order, coefficient in enumerate(u_coefficients):
                if coefficient == 0:
                    continue
                if coefficient < 0:
                    raise AssertionError(
                        f"negative row at beta={beta_degree}, "
                        f"t-order={t_order}, u-order={u_order}"
                    )
                rows.append(
                    [
                        beta_degree,
                        t_order,
                        u_order,
                        str(coefficient),
                    ]
                )
                reconstructed_u += coefficient * sp.expand_func(
                    sp.binomial(U, u_order)
                )
            if sp.expand(reconstructed_u - u_polynomial) != 0:
                raise AssertionError("u-Newton reconstruction failed")
            reconstructed_t += s_coefficient * sp.expand_func(
                sp.binomial(T, t_order)
            )
        if sp.expand(reconstructed_t - layer) != 0:
            raise AssertionError("t-Newton reconstruction failed")

    payload = json.dumps(rows, separators=(",", ":")).encode("utf-8")
    return {
        "schema": "amra.complete_split.general_s_disjoint_alpha2.v1",
        "claim": (
            "For s>=4 and r>=0, the alpha^2 beta^d layers listed below "
            "of the normalized disjoint-core Rayleigh numerator are "
            "nonnegative."
        ),
        "scope_warning": (
            "This covers only alpha degree 2 and beta degrees 4 through "
            f"{max_beta}; it is not the full general-s margin."
        ),
        "variables": "u=s-4>=0, t=r>=0",
        "basis": "beta^d binomial(t,k) binomial(u,q)",
        "ordinary_layer_formulas": formulas,
        "rows_beta_tbin_ubin_coefficient": rows,
        "sha256_rows": hashlib.sha256(payload).hexdigest(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-beta", type=int, default=8)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
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
