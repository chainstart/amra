"""Counterexample and symmetrized-unit tests for the next audit round."""

from __future__ import annotations

from itertools import permutations
from math import factorial, prod

import mpmath as mp
import sympy as sp


R = -3069


def consecutive_unit_polynomial(degree: int) -> sp.Poly:
    x = sp.symbols("x")
    return sp.Poly(sp.prod(x + k for k in range(1, degree + 1)) - 1, x)


def coefficient_vector(poly: sp.Poly, degree: int) -> tuple[int, ...]:
    return tuple(int(poly.nth(index)) for index in range(degree))


def explicit_minor_row_indices(degree: int) -> tuple[int, ...]:
    """Rows u1,c1,u2,c2,u3,...,u_(d-2) in the interlaced row list."""
    if degree < 4:
        raise ValueError("the explicit full minor starts in degree four")
    return (0, 1, 2, 3) + tuple(
        2 * (k - 1) for k in range(3, degree - 1)
    )


def explicit_minor_closed_form(
    degree: int, multiplier: int = -R
) -> int:
    """Signed coefficient minor for the rows in explicit_minor_row_indices.

    The coefficient columns are ordered 1,x,...,x^(d-1), and the two
    doubled SAT symmetrizations are

        u_k = (x+k) - multiplier*q_k + offset,
        c_k = (x+k) + multiplier*q_k.

    The answer is independent of ``offset``.
    """
    if degree < 4:
        raise ValueError("the explicit full minor starts in degree four")
    superfactorial = prod(factorial(index) for index in range(1, degree - 2))
    return (-1) ** degree * 4 * multiplier ** (degree - 2) * superfactorial


def explicit_side_lengths_closed_form(
    degree: int, multiplier: int = -R
) -> tuple[int, ...]:
    """Exact doubled power-basis side lengths for the audited shifts."""
    if degree < 4:
        raise ValueError("the audited side formula starts in degree four")
    x = sp.symbols("x")
    largest_inverse = sp.Poly(
        sp.prod(x + k for k in range(2, degree + 1)), x
    )
    return tuple(
        2
        * (
            abs(multiplier) * int(largest_inverse.nth(index))
            + (1 if index in (0, 1) else 0)
        )
        + 1
        for index in range(degree)
    )


def consecutive_family_scaling_audit(
    first_degree: int = 5, last_degree: int = 30
) -> dict:
    """Closed-form digit sequence and honest asymptotic compatibility audit."""
    if first_degree < 5 or last_degree < first_degree:
        raise ValueError("invalid audited degree range")
    records = []
    for degree in range(first_degree, last_degree + 1):
        defining = consecutive_unit_polynomial(degree)
        determinant = abs(explicit_minor_closed_form(degree))
        side_lengths = explicit_side_lengths_closed_form(degree)
        box_size = 2 * prod(side_lengths)
        records.append(
            {
                "degree": degree,
                "irreducible": defining.is_irreducible,
                "real_root_count": len(defining.intervals()),
                "minor": determinant,
                "minor_digits": len(str(determinant)),
                "box_size": box_size,
                "box_digits": len(str(box_size)),
                "parameter_count": degree - 1,
            }
        )
    return {
        "records": tuple(records),
        "minor_recurrence": "D_(d+1)=3069*(d-2)!*D_d",
        "minor_growth": "log D_d=Theta(d^2 log d)",
        "box_growth": "log box_size=Theta(d^2 log d)",
        "small_doubling": (
            "the rectangular container has doubling at most 2^d="
            "box_size^o(1)"
        ),
        "overlap_density": (
            "doubling every coordinate gives each selected shift overlap "
            "density at least 2^-d=box_size^-o(1)"
        ),
        "target_failure": (
            "|T|=d-1=box_size^o(1), far below box_size^(2/5); "
            "the identity certifies an obstruction, not a construction"
        ),
    }


def consecutive_unit_certificate(degree: int) -> dict:
    """Exact additive and doubled inverse-symmetrized data for theta+k."""
    if degree < 5:
        raise ValueError("the audited totally real family starts at degree five")
    x = sp.symbols("x")
    defining = consecutive_unit_polynomial(degree)
    product_poly = sp.Poly(
        sp.prod(x + k for k in range(1, degree + 1)), x
    )
    units = [
        coefficient_vector(sp.Poly(x + k, x), degree)
        for k in range(1, degree + 1)
    ]
    raw_rank = sp.Matrix(units).rank()

    # Use the first degree-1 units; their product relation with the final
    # unit is explicit.  The inverse of theta+k is product_poly/(x+k).
    symmetrized_rows = []
    maxima = [0] * degree
    for k in range(1, degree):
        parameter = sp.Poly(x + k, x)
        inverse, remainder = sp.div(product_poly, parameter)
        assert remainder.is_zero
        u = parameter + R * inverse + sp.Poly(3, x)
        c = parameter - R * inverse
        u_vector = coefficient_vector(u, degree)
        c_vector = coefficient_vector(c, degree)
        symmetrized_rows.extend((u_vector, c_vector))
        for index in range(degree):
            maxima[index] = max(
                maxima[index],
                abs(u_vector[index]),
                abs(c_vector[index]),
            )

    matrix = sp.Matrix(symmetrized_rows)
    symmetrized_rank = matrix.rank()
    _, pivot_rows = matrix.T.rref()
    selected = matrix[list(pivot_rows[:degree]), :]
    determinant = abs(int(selected.det()))
    explicit_rows = explicit_minor_row_indices(degree)
    explicit_determinant = int(matrix[list(explicit_rows), :].det())
    explicit_formula = explicit_minor_closed_form(degree)
    side_lengths = tuple(2 * maximum + 1 for maximum in maxima)
    box_size = 2 * prod(side_lengths)

    product_remainder = sp.rem(product_poly, defining)
    return {
        "degree": degree,
        "polynomial": defining,
        "irreducible": defining.is_irreducible,
        "mod_two_irreducible": sp.Poly(
            defining.as_expr(), defining.gens[0], modulus=2
        ).is_irreducible,
        "real_root_count": len(defining.intervals()),
        "unit_norms": tuple(
            int((-1) ** degree * defining.eval(-k))
            for k in range(1, degree + 1)
        ),
        "product_remainder": product_remainder,
        "raw_additive_rank": raw_rank,
        "symmetrized_rank": symmetrized_rank,
        "symmetrized_rows": tuple(symmetrized_rows),
        "independent_minor_determinant": determinant,
        "explicit_minor_rows": explicit_rows,
        "explicit_minor_determinant": explicit_determinant,
        "explicit_minor_closed_form": explicit_formula,
        "explicit_minor_identity_holds": explicit_determinant == explicit_formula,
        "side_lengths": side_lengths,
        "side_lengths_closed_form": explicit_side_lengths_closed_form(degree),
        "box_size": box_size,
        "determinant_volume_lower_bound": determinant / factorial(degree),
    }


def rigorous_degree_five_log_determinant(decimal_digits: int = 30) -> dict:
    """Interval certificate that theta+1,...,theta+4 are independent."""
    defining = consecutive_unit_polynomial(5)
    epsilon = sp.Rational(1, 10**decimal_digits)
    root_intervals = defining.intervals(eps=epsilon)
    interval_digits = max(50, decimal_digits + 30)
    previous_interval_digits = mp.iv.dps
    try:
        mp.iv.dps = interval_digits
        rows = []
        shift_intervals_exclude_zero = []
        for (lower, upper), multiplicity in root_intervals[:4]:
            assert multiplicity == 1

            # Construct both rational endpoints by interval division of
            # degenerate integer intervals.  No ordinary mp.mpf rounding is
            # allowed between the exact SymPy rationals and interval context.
            low_endpoint = mp.iv.mpf(
                [int(lower.p), int(lower.p)]
            ) / mp.iv.mpf([int(lower.q), int(lower.q)])
            high_endpoint = mp.iv.mpf(
                [int(upper.p), int(upper.p)]
            ) / mp.iv.mpf([int(upper.q), int(upper.q)])
            root_box = mp.iv.mpf([low_endpoint.a, high_endpoint.b])

            row = []
            for k in range(1, 5):
                shifted = root_box + mp.iv.mpf([k, k])
                same_sign = bool(shifted.b < 0) or bool(shifted.a > 0)
                assert same_sign
                assert 0 not in shifted
                shift_intervals_exclude_zero.append(True)
                row.append(mp.iv.log(abs(shifted)))
            rows.append(row)

        determinant = mp.iv.mpf([0, 0])
        for permutation in permutations(range(4)):
            inversions = sum(
                permutation[i] > permutation[j]
                for i in range(4)
                for j in range(i + 1, 4)
            )
            term = mp.iv.mpf([1, 1])
            for row, column in enumerate(permutation):
                term *= rows[row][column]
            determinant += -term if inversions % 2 else term
        lower = float(determinant.a)
        upper = float(determinant.b)
        width = float(determinant.b - determinant.a)
        lower_interval_text = mp.iv.nstr(
            determinant.a, interval_digits + 5
        )
        upper_interval_text = mp.iv.nstr(
            determinant.b, interval_digits + 5
        )
        excludes_zero = bool(determinant.a > 0) or bool(determinant.b < 0)
    finally:
        mp.iv.dps = previous_interval_digits
    return {
        "lower": lower,
        "upper": upper,
        "width": width,
        "lower_interval_text": lower_interval_text,
        "upper_interval_text": upper_interval_text,
        "excludes_zero": excludes_zero,
        "interval_decimal_digits": interval_digits,
        "all_shift_intervals_exclude_zero": all(
            shift_intervals_exclude_zero
        ),
        "endpoint_construction": (
            "degenerate integer intervals divided entirely in mp.iv"
        ),
        "meaning": (
            "nonzero log minor proves multiplicative independence of "
            "theta+1,...,theta+4"
        ),
    }


def determinant_container_lemma_ledger() -> dict:
    return {
        "proved_lemma": (
            "if s shift coordinate vectors lie in a proper integral box "
            "with side lengths M_j, every s-minor Delta satisfies "
            "|Delta| <= s!*product(M_j)"
        ),
        "raw_unit_claim": "false: independent units may lie in additive rank two",
        "credible_condition": (
            "apply determinant growth to t+R/t and t-R/t in a bounded-index "
            "integral/fractional-ideal coordinate lattice"
        ),
        "threshold_condition": (
            "if |Delta|/s! >= |T|^(5/2+eta), then every containing "
            "proper box has |P| >= |T|^(5/2+eta), so "
            "|T| <= |P|^(2/5-delta)"
        ),
        "conjecture": (
            "for growing-rank unit words of controlled height, some "
            "linear-size family of inverse-symmetrized shifts has "
            "determinant large enough to force super-subpolynomial "
            "additive box volume"
        ),
        "status": "CONJECTURE; not proved universally",
    }


if __name__ == "__main__":
    print(rigorous_degree_five_log_determinant())
    for degree in range(5, 13):
        result = consecutive_unit_certificate(degree)
        print(
            degree,
            "irreducible=", result["irreducible"],
            "real=", result["real_root_count"],
            "raw rank=", result["raw_additive_rank"],
            "sym rank=", result["symmetrized_rank"],
            "minor digits=", len(str(result["independent_minor_determinant"])),
            "box digits=", len(str(result["box_size"])),
        )
    scaling = consecutive_family_scaling_audit()
    print(
        "closed-form degrees 5..30:",
        tuple(
            (record["degree"], record["minor_digits"], record["box_digits"])
            for record in scaling["records"]
        ),
    )
    print(scaling["target_failure"])
    print(determinant_container_lemma_ledger())
