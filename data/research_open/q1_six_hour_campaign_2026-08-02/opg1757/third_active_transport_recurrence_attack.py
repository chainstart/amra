#!/usr/bin/env python3
"""Search a fixed-layer recurrence for the odd transport bulk kernel."""

from __future__ import annotations

import math
from functools import cache

import sympy as sp

from third_active_comparison_attack import (
    B,
    S,
    choose_fixed,
    initial_kernel,
    kernel,
    lam,
    shifted_nonnegative,
    u,
)


def full_page_kernel(page: int, base: int, parameter: sp.Expr) -> sp.Expr:
    value = lam(parameter) ** (2 * (page - base))
    if base > 2:
        value *= kernel(base, parameter)
    return sp.expand(value)


def page_multiplier(page: int, base: int) -> int:
    return (-1) ** (page - base) * math.comb(page - 2, base - 2)


@cache
def odd_w_components() -> dict[int, sp.Expr]:
    """W_s=sum_(a=2)^6 u_a^(2s-15) C_a(s), W_s=12s beta^8 L_s."""

    components = {base: sp.S.Zero for base in range(2, 7)}

    def add(base: int, offset: int, value: sp.Expr) -> None:
        if offset < 0:
            raise AssertionError((base, offset))
        components[base] += u(base) ** offset * value

    # s F6_(s+1) +(s-4)u6^2 F6_s-E(u6^2 F6_s).
    for base in range(2, 7):
        multiplier = page_multiplier(6, base)
        add(
            base,
            15 - 2 * base,
            S * multiplier * full_page_kernel(6, base, S + 1),
        )
        transported_kernel = u(6) ** 2 * full_page_kernel(6, base, S)
        add(
            base,
            13 - 2 * base,
            multiplier
            * (
                (S - 4) * transported_kernel
                - B * sp.diff(transported_kernel, B)
            ),
        )
        exponent = 2 * S - 2 * base - 2
        add(
            base,
            12 - 2 * base,
            -multiplier * exponent * base * B * transported_kernel,
        )

    # -12 s^3(s-3) beta^4 lambda_s^2 F4_s.
    for base in range(2, 5):
        add(
            base,
            13 - 2 * base,
            -12
            * S**3
            * (S - 3)
            * B**4
            * lam(S) ** 2
            * page_multiplier(4, base)
            * full_page_kernel(4, base, S),
        )

    # -12 s^5(s-4)(s-5) beta^8 u6^2 lambda_s^4 u2^(2s-10).
    add(
        2,
        5,
        -12
        * S**5
        * (S - 4)
        * (S - 5)
        * B**8
        * u(6) ** 2
        * lam(S) ** 4,
    )
    return {base: sp.expand(value) for base, value in components.items()}


@cache
def even_w_components() -> dict[int, sp.Expr]:
    """W_s=sum_(a=2)^7 u_a^(2s-17) C_a(s), W_s=60s beta^10 L_s."""

    components = {base: sp.S.Zero for base in range(2, 8)}

    def add(base: int, offset: int, value: sp.Expr) -> None:
        if offset < 0:
            raise AssertionError((base, offset))
        components[base] += u(base) ** offset * value

    # s F7_(s+1) +(s-4)u7^2 F7_s-E(u7^2 F7_s).
    for base in range(2, 8):
        multiplier = page_multiplier(7, base)
        add(
            base,
            17 - 2 * base,
            S * multiplier * full_page_kernel(7, base, S + 1),
        )
        transported_kernel = u(7) ** 2 * full_page_kernel(7, base, S)
        add(
            base,
            15 - 2 * base,
            multiplier
            * (
                (S - 4) * transported_kernel
                - B * sp.diff(transported_kernel, B)
            ),
        )
        exponent = 2 * S - 2 * base - 2
        add(
            base,
            14 - 2 * base,
            -multiplier * exponent * base * B * transported_kernel,
        )

    # -20 s^3(s-3) beta^4 lambda_s^2 F5_s.
    for base in range(2, 6):
        add(
            base,
            15 - 2 * base,
            -20
            * S**3
            * (S - 3)
            * B**4
            * lam(S) ** 2
            * page_multiplier(5, base)
            * full_page_kernel(5, base, S),
        )

    # -60 s^5(s-4)(s-5) beta^8 u7^2 lambda_(s-2)^4 F3_(s-2).
    for base in range(2, 4):
        add(
            base,
            11 - 2 * base,
            -60
            * S**5
            * (S - 4)
            * (S - 5)
            * B**8
            * u(7) ** 2
            * lam(S - 2) ** 4
            * page_multiplier(3, base)
            * full_page_kernel(3, base, S - 2),
        )
    return {base: sp.expand(value) for base, value in components.items()}


@cache
def page_recurrence_components(page: int) -> dict[int, sp.Expr]:
    """Common-base kernels for F_(p,s+1)-u_p^2 F_(p,s).

    More precisely, the returned values G_(p,a,s) satisfy

        F_(p,s+1)-u_p^2 F_(p,s)
          = sum_a u_a^(2s-2p-2) G_(p,a,s).
    """

    components = {}
    for base in range(2, page + 1):
        multiplier = page_multiplier(page, base)
        following = (
            u(base) ** (2 * page - 2 * base + 2)
            * full_page_kernel(page, base, S + 1)
        )
        transported = (
            u(page) ** 2
            * u(base) ** (2 * page - 2 * base)
            * full_page_kernel(page, base, S)
        )
        components[base] = sp.expand(multiplier * (following - transported))
    return components


def odd_a_recurrence_kernels() -> tuple[sp.Expr, ...]:
    """Kernels in s W_(s+1)-(s+1)u6^2 W_s."""

    components = odd_w_components()
    result = []
    for base in range(6, 1, -1):
        value = (
            S * u(base) ** 2 * components[base].subs(S, S + 1)
            - (S + 1) * u(6) ** 2 * components[base]
        )
        result.append(sp.expand(value))
    return tuple(result)


def reconstruct_w(s: int) -> sp.Poly:
    components = odd_w_components()
    length = 2 * s - 15
    return sp.Poly(
        sp.expand(
            sum(
                u(base) ** length * value.subs(S, s)
                for base, value in components.items()
            )
        ),
        B,
    )


def reconstruct_even_w(s: int) -> sp.Poly:
    components = even_w_components()
    length = 2 * s - 17
    return sp.Poly(
        sp.expand(
            sum(
                u(base) ** length * value.subs(S, s)
                for base, value in components.items()
            )
        ),
        B,
    )


def audit_reconstruction() -> int:
    from third_active_transport_bulk_attack import (
        even_lower_kernel_numerator,
        odd_lower_kernel_numerator,
    )

    checks = 0
    for s in range(8, 11):
        expected = sp.Poly(
            sp.expand(
                B**8 * sum(
                    odd_lower_kernel_numerator(degree).subs(S, s) * B**degree
                    for degree in range(2 * s - 3)
                )
            ),
            B,
        )
        if reconstruct_w(s) != expected:
            raise AssertionError((s, "W reconstruction"))
        checks += len(expected.all_coeffs())
    for s in range(9, 12):
        expected = sp.Poly(
            sp.expand(
                B**10 * sum(
                    even_lower_kernel_numerator(degree).subs(S, s) * B**degree
                    for degree in range(2 * s - 3)
                )
            ),
            B,
        )
        if reconstruct_even_w(s) != expected:
            raise AssertionError((s, "even W reconstruction"))
        checks += len(expected.all_coeffs())
    return checks


def leading_symbol(expression: sp.Expr) -> tuple[int, sp.Expr]:
    x = sp.symbols("x")
    polynomial = sp.Poly(expression, B)
    data = []
    for degree in range(polynomial.degree() + 1):
        coefficient = sp.Poly(polynomial.coeff_monomial(B**degree), S)
        data.append((degree, coefficient.degree(), sp.LC(coefficient)))
    maximum = max(item[1] for item in data)
    symbol = sp.factor(
        sum(leading * x**degree for degree, order, leading in data if order == maximum)
    )
    return maximum, symbol


def audit_interior_symbols() -> dict[str, object]:
    x = sp.symbols("x")
    odd_components = odd_w_components()
    even_components = even_w_components()
    symbols = {
        "odd_sufficient": leading_symbol(odd_components[6]),
        "even_sufficient": leading_symbol(even_components[7]),
        "odd_page_recurrence": leading_symbol(
            u(6) ** 2 * (kernel(6, S + 1) - kernel(6, S))
        ),
        "even_page_recurrence": leading_symbol(
            u(7) ** 2 * (kernel(7, S + 1) - kernel(7, S))
        ),
    }
    expected = {
        "odd_sufficient": (9, 1119744 * x**16 * (6 * x + 1) ** 2),
        "even_sufficient": (11, 161414428 * x**20 * (7 * x + 1) ** 2),
        "odd_page_recurrence": (7, 4478976 * x**16 * (6 * x + 1) ** 2),
        "even_page_recurrence": (9, 807072140 * x**20 * (7 * x + 1) ** 2),
    }
    for name, (order, symbol) in symbols.items():
        expected_order, expected_symbol = expected[name]
        if order != expected_order or sp.expand(symbol - expected_symbol) != 0:
            raise AssertionError((name, order, symbol))
    return symbols


def audit_logarithmic_dominance_data() -> dict[str, object]:
    """Exact finite data used by the logarithmic low-boundary theorem."""

    objects = {
        "odd_sufficient": (odd_w_components(), 6, 8),
        "even_sufficient": (even_w_components(), 7, 9),
        "odd_page_recurrence": (page_recurrence_components(6), 6, 8),
        "even_page_recurrence": (page_recurrence_components(7), 7, 9),
    }
    expected = {
        "odd_sufficient": (19, 11, 126),
        "even_sufficient": (23, 13, 176),
        "odd_page_recurrence": (18, 8, 80),
        "even_page_recurrence": (22, 10, 120),
    }
    result = {}
    for name, (components, dominant, start) in objects.items():
        dominant_kernel = components[dominant]
        ok, positive_monomials = shifted_nonnegative(dominant_kernel, start)
        if not ok:
            raise AssertionError((name, positive_monomials))
        beta_degree = max(sp.degree(value, B) for value in components.values())
        lower_s_degree = max(
            sp.degree(value, S)
            for base, value in components.items()
            if base < dominant
        )
        actual = (beta_degree, lower_s_degree, positive_monomials)
        if actual != expected[name]:
            raise AssertionError((name, actual, expected[name]))
        result[name] = actual

    page_reconstruction_coefficients = 0
    for page, parameters in ((6, (8, 9)), (7, (9, 10))):
        components = page_recurrence_components(page)
        for parameter in parameters:
            def page_value(value: int) -> sp.Expr:
                return sp.expand(
                    sum(
                        page_multiplier(page, base)
                        * u(base) ** (2 * value - 2 * base - 2)
                        * full_page_kernel(page, base, value)
                        for base in range(2, page + 1)
                    )
                )

            direct = sp.Poly(
                sp.expand(
                    page_value(parameter + 1)
                    - u(page) ** 2 * page_value(parameter)
                ),
                B,
            )
            rebuilt = sp.Poly(
                sp.expand(
                    sum(
                        u(base) ** (2 * parameter - 2 * page - 2)
                        * value.subs(S, parameter)
                        for base, value in components.items()
                    )
                ),
                B,
            )
            if direct != rebuilt:
                raise AssertionError((page, parameter, "page reconstruction"))
            page_reconstruction_coefficients += len(direct.all_coeffs())
    if page_reconstruction_coefficients != 96:
        raise AssertionError(page_reconstruction_coefficients)
    result["page_reconstruction_coefficients"] = page_reconstruction_coefficients

    # Endpoint coefficients used to retain one positive dominant summand in
    # the low and high halves of the support.
    odd_w = sp.Poly(objects["odd_sufficient"][0][6], B)
    even_w = sp.Poly(objects["even_sufficient"][0][7], B)
    odd_page = sp.Poly(objects["odd_page_recurrence"][0][6], B)
    even_page = sp.Poly(objects["even_page_recurrence"][0][7], B)
    endpoints = {
        "odd_sufficient_low": sp.factor(odd_w.coeff_monomial(B**0)),
        "odd_sufficient_high": sp.factor(odd_w.coeff_monomial(B**19)),
        "even_sufficient_low": sp.factor(even_w.coeff_monomial(B**0)),
        "even_sufficient_high": sp.factor(even_w.coeff_monomial(B**23)),
        "odd_page_low": sp.factor(odd_page.coeff_monomial(B**2)),
        "odd_page_high": sp.factor(odd_page.coeff_monomial(B**18)),
        "even_page_low": sp.factor(even_page.coeff_monomial(B**2)),
        "even_page_high": sp.factor(even_page.coeff_monomial(B**22)),
    }
    if sp.expand(endpoints["odd_sufficient_low"] - 2 * (S - 2)) != 0:
        raise AssertionError(endpoints["odd_sufficient_low"])
    if sp.expand(endpoints["even_sufficient_low"] - 2 * (S - 2)) != 0:
        raise AssertionError(endpoints["even_sufficient_low"])
    if endpoints["odd_page_low"] != 36:
        raise AssertionError(endpoints["odd_page_low"])
    if endpoints["even_page_low"] != 50:
        raise AssertionError(endpoints["even_page_low"])
    if any(
        value.subs(S, start) <= 0
        for value, start in (
            (endpoints["odd_sufficient_high"], 8),
            (endpoints["even_sufficient_high"], 9),
            (endpoints["odd_page_high"], 8),
            (endpoints["even_page_high"], 9),
        )
    ):
        raise AssertionError("a retained high endpoint lost positivity")

    # log(1+x) > x-x^2/2 for x>0.  These exact inequalities imply
    # 241*log(6/5)>30 and 241*log(7/6)>36, respectively.
    if not (241 * 9 > 30 * 50 and 241 * 11 > 36 * 72):
        raise AssertionError("logarithmic slope budget changed")
    result["slope"] = 241
    result["endpoint_coefficients"] = endpoints
    return result


def audit_recurrence_reconstruction() -> int:
    components = odd_w_components()
    kernels = odd_a_recurrence_kernels()
    checks = 0
    for s in range(8, 11):
        length = 2 * s - 15
        direct = sp.Poly(
            sp.expand(
                s * reconstruct_w(s + 1).as_expr()
                - (s + 1) * u(6) ** 2 * reconstruct_w(s).as_expr()
            ),
            B,
        )
        rebuilt = sp.Poly(
            sp.expand(
                sum(
                    u(base) ** length * value.subs(S, s)
                    for base, value in zip(range(6, 1, -1), kernels)
                )
            ),
            B,
        )
        if direct != rebuilt:
            raise AssertionError((s, "recurrence reconstruction"))
        checks += len(direct.all_coeffs())
    return checks


def fixed_layer_obstruction() -> dict[str, object]:
    """Exact obstruction to any fixed-depth termwise u2-layer proof."""

    kernels = odd_a_recurrence_kernels()
    expected_linear = {
        6: sp.Integer(408),
        5: -16 * (2 * S + 87),
        4: 96 * (S + 18),
        3: -48 * (2 * S + 19),
        2: 8 * (4 * S + 21),
    }
    for base, value in zip(range(6, 1, -1), kernels):
        actual = sp.Poly(value, B).coeff_monomial(B)
        if sp.expand(actual - expected_linear[base]) != 0:
            raise AssertionError((base, actual))

    layer4 = sum(base**4 * value for base, value in zip((4, 3, 2, 1), kernels[:4]))
    coefficient4 = sp.factor(sp.Poly(layer4, B).coeff_monomial(B))
    if sp.expand(coefficient4 + 1152 * (S - 16)) != 0:
        raise AssertionError(coefficient4)
    if coefficient4.subs(S, 17) != -1152:
        raise AssertionError("first four-layer witness changed")
    return {
        "linear_coefficients": expected_linear,
        "first_negative_layer": 4,
        "first_negative_parameter": 17,
        "first_negative_value": -1152,
    }


def search() -> None:
    kernels = odd_a_recurrence_kernels()
    e6, e5, e4, e3, _ = kernels
    length = 2 * S - 15
    for start in (8, 12, 16, 20, 24, 30, 40, 60):
        delta = shifted_nonnegative(e6, start)
        for depth in range(4, 17):
            layer = 4**depth * e6 + 3**depth * e5 + 2**depth * e4 + e3
            growth_inner = (
                3 * 2**depth * e6
                + 2 * sp.Rational(3, 2) ** depth * e5
                + e4
            )
            growth_second = 3 * sp.Rational(4, 3) ** depth * e6 + e5
            initial = initial_kernel(kernels, (4, 3, 2, 1), depth, length)
            checks = [
                delta,
                shifted_nonnegative(layer, start),
                shifted_nonnegative(growth_inner, start),
                shifted_nonnegative(growth_second, start),
                shifted_nonnegative(initial, start),
            ]
            if all(ok for ok, _ in checks):
                print("odd bulk recurrence candidate", start, depth, [x for _, x in checks])
                return
            print(
                "failed",
                start,
                depth,
                [value if ok else ("degree", value[0]) for ok, value in checks],
            )


if __name__ == "__main__":
    print("reconstruction_coefficients", audit_reconstruction())
    print("recurrence_reconstruction_coefficients", audit_recurrence_reconstruction())
    print("interior_symbols", audit_interior_symbols())
    logarithmic = audit_logarithmic_dominance_data()
    print(
        "logarithmic_dominance",
        {name: value for name, value in logarithmic.items() if name != "endpoint_coefficients"},
    )
    obstruction = fixed_layer_obstruction()
    print("OPG ODD TRANSPORT FIXED-LAYER ROUTE OBSTRUCTION: PASS")
    print("first_negative_layer", obstruction["first_negative_layer"])
    print("first_negative_parameter", obstruction["first_negative_parameter"])
    print("first_negative_value", obstruction["first_negative_value"])
    print("status_actual_transport_recurrence", "OPEN")
