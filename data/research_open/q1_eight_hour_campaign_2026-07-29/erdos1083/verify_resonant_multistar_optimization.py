"""Exact subset optimization and multistar certificates for Round 28."""

from __future__ import annotations

from fractions import Fraction
from typing import Callable, Iterable


C = Fraction(12285, 4)
R = Fraction(-3069)
X = Fraction(-3, 2)
QElt = tuple[Fraction, Fraction]  # a+bY, where Y^2=C
KCoeff = QElt
Laurent = dict[int, KCoeff]


def qsub(left: QElt, right: QElt) -> QElt:
    return left[0] - right[0], left[1] - right[1]


def sat_compatibility(u: QElt, v: QElt) -> bool:
    """Exact F(u,v)=0 in Q(sqrt(12285))."""
    a, b = u
    c, d = v
    rational = a * a + b * b * C - c * c - d * d * C - 3 * a - 2 * d * C
    radical = 2 * a * b - 2 * c * d - 3 * b - 2 * c
    return rational == 0 and radical == 0


def rational_compatibility(u: int, v: int) -> bool:
    """The simplified rational model X=2,Y=1."""
    return u * u - v * v + 4 * u - 2 * v == 0


def subset_zeta_optima(
    universe: Iterable[object],
    difference: Callable[[object, object], object],
    compatible: Callable[[object, object], bool],
    max_size: int,
) -> dict[int, dict]:
    """Evaluate H exactly for every subset of a finite candidate universe.

    Each compatible ordered quadruple is first assigned to the bit mask of
    its distinct vertices.  A subset zeta transform then sums all quadruples
    supported inside every subset.
    """
    universe = tuple(universe)
    width = len(universe)
    coefficient = [0] * (1 << width)
    pairs = [
        (difference(left, right), (1 << i) | (1 << j))
        for i, left in enumerate(universe)
        for j, right in enumerate(universe)
    ]
    for u, u_mask in pairs:
        for v, v_mask in pairs:
            if compatible(u, v):
                coefficient[u_mask | v_mask] += 1

    energy = coefficient[:]
    for bit in range(width):
        flag = 1 << bit
        for mask in range(1 << width):
            if mask & flag:
                energy[mask] += energy[mask ^ flag]

    best = {size: {"H": -1, "mask": 0} for size in range(max_size + 1)}
    for mask, total in enumerate(energy):
        size = mask.bit_count()
        if size <= max_size and total > best[size]["H"]:
            best[size] = {"H": total, "mask": mask}
    for size, record in best.items():
        record["values"] = tuple(
            universe[index]
            for index in range(width)
            if record["mask"] & (1 << index)
        )
        if size:
            record["average_degree"] = Fraction(record["H"], size * size)
    return best


def rational_lattice_optima(max_size: int = 12) -> dict[int, dict]:
    """All subsets of a 12-point step-two lattice, for X=2,Y=1."""
    universe = tuple(range(-11, 12, 2))
    return subset_zeta_optima(
        universe,
        lambda left, right: left - right,
        rational_compatibility,
        max_size,
    )


def sat_star_candidate_universe() -> tuple[QElt, ...]:
    """The 17 points from the signed parameters t=+-1,...,+-4."""
    values: set[QElt] = {(Fraction(0), Fraction(0))}
    for raw_parameter in range(-4, 5):
        if raw_parameter == 0:
            continue
        parameter = Fraction(raw_parameter)
        u = (parameter + R / parameter) / 2 - X
        c = (parameter - R / parameter) / 2
        values.add((-u, Fraction(0)))
        values.add((c, Fraction(-1)))
    return tuple(sorted(values))


def sat_candidate_optima(max_size: int = 12) -> dict[int, dict]:
    """All subsets of the signed eight-parameter SAT star universe."""
    return subset_zeta_optima(
        sat_star_candidate_universe(), qsub, sat_compatibility, max_size
    )


def rational_sat_bound(values: Iterable[Fraction]) -> dict:
    """Exact H for rational translations under the actual SAT parameters.

    Irrational-part comparison forces v=0, then u is 0 or 3.
    """
    values = tuple(values)
    n = len(values)
    overlap_three = sum(left - right == 3 for left in values for right in values)
    total = n * n + n * overlap_three
    return {
        "n": n,
        "overlap_three": overlap_three,
        "H": total,
        "average_degree": Fraction(total, n * n),
        "sharp_upper_bound": 2 * n * n - n,
    }


def two_layer_reduction_certificate() -> dict:
    """Rational solution types when A=P union (Q-Y).

    If u=a+bY and v=c+dY, then b,d are in {-1,0,1}.  Comparing the
    rational and Y coefficients leaves one scalable hyperbola family and
    four exceptional rational points.
    """
    exceptional = (
        (Fraction(0), 0, Fraction(0), 0),
        (Fraction(3), 0, Fraction(0), 0),
        (Fraction(-189, 2), 0, Fraction(0), 1),
        (Fraction(195, 2), 0, Fraction(0), 1),
    )
    for a, b, c, d in exceptional:
        assert sat_compatibility((a, Fraction(b)), (c, Fraction(d)))
    return {
        "exceptional": exceptional,
        "scalable_type": {
            "b": 0,
            "d": -1,
            "equation": "(a-3/2)^2-c^2=-3069",
        },
        "excluded_nonsquares": (2729, 8193),
    }


def kadd(left: KCoeff, right: KCoeff) -> KCoeff:
    return left[0] + right[0], left[1] + right[1]


def kmul(left: KCoeff, right: KCoeff) -> KCoeff:
    a, b = left
    c, d = right
    return a * c + b * d * C, a * d + b * c


def lclean(poly: Laurent) -> Laurent:
    return {power: coefficient for power, coefficient in poly.items() if coefficient != (0, 0)}


def ladd(left: Laurent, right: Laurent) -> Laurent:
    result = dict(left)
    for power, coefficient in right.items():
        result[power] = kadd(result.get(power, (Fraction(0), Fraction(0))), coefficient)
    return lclean(result)


def lscale(poly: Laurent, coefficient: KCoeff) -> Laurent:
    return lclean({power: kmul(value, coefficient) for power, value in poly.items()})


def lmul(left: Laurent, right: Laurent) -> Laurent:
    result: Laurent = {}
    for left_power, left_coefficient in left.items():
        for right_power, right_coefficient in right.items():
            power = left_power + right_power
            product = kmul(left_coefficient, right_coefficient)
            result[power] = kadd(
                result.get(power, (Fraction(0), Fraction(0))), product
            )
    return lclean(result)


def formal_resonant_pair(index: int) -> tuple[Laurent, Laurent]:
    """u(T^j),v(T^j) over the exact Laurent function field."""
    u = {
        index: (Fraction(1, 2), Fraction(0)),
        -index: (R / 2, Fraction(0)),
        0: (-X, Fraction(0)),
    }
    v = {
        index: (Fraction(1, 2), Fraction(0)),
        -index: (-R / 2, Fraction(0)),
        0: (Fraction(0), Fraction(-1)),
    }
    return lclean(u), lclean(v)


def formal_compatibility(u: Laurent, v: Laurent) -> Laurent:
    result = ladd(lmul(u, u), lscale(lmul(v, v), (Fraction(-1), Fraction(0))))
    result = ladd(result, lscale(u, (2 * X, Fraction(0))))
    result = ladd(result, lscale(v, (Fraction(0), Fraction(-2))))
    return lclean(result)


def reflect_hyperbola_v(v: Laurent) -> Laurent:
    """Send c-Y to -c-Y, the second point above the same rational u."""
    result = {}
    for power, coefficient in v.items():
        if power == 0:
            result[power] = coefficient
        else:
            result[power] = (-coefficient[0], -coefficient[1])
    return lclean(result)


def multistar_cube_certificate(k: int, side_length: int = 2) -> dict:
    """An explicit infinite family with logarithmically growing average.

    Take T transcendental (for example T=e), t_j=T^j, and put
    P={sum alpha_j u_j + sum beta_j c_j: 0<=alpha_j,beta_j<L},
    where v_j=c_j-Y.  Then A=P union (P-Y).
    """
    if k < 1 or side_length < 2:
        raise ValueError("need k>=1 and side_length>=2")
    for index in range(1, k + 1):
        u, v = formal_resonant_pair(index)
        assert formal_compatibility(u, v) == {}
        assert formal_compatibility(u, reflect_hyperbola_v(v)) == {}

    length = side_length
    p_size = length ** (2 * k)
    n = 2 * p_size
    overlap_u = n * (length - 1) // length
    overlap_v = p_size * (length - 1) // length
    certified_H = n * n + 2 * k * overlap_u * overlap_v
    difference_palette = 3 * (2 * length - 1) ** (2 * k)
    return {
        "k": k,
        "side_length": length,
        "n": n,
        "overlap_u": overlap_u,
        "overlap_v": overlap_v,
        "certified_H": certified_H,
        "certified_average_degree": Fraction(certified_H, n * n),
        "exact_H": certified_H,
        "exact_average_degree": Fraction(certified_H, n * n),
        "difference_palette": difference_palette,
        "point_exponent_service": Fraction(2),
        "growth_type": "logarithmic average degree; polynomial exponent zero",
    }


if __name__ == "__main__":
    rational = rational_lattice_optima()
    sat = sat_candidate_optima()
    print("n rational-H rational-average SAT-H SAT-average")
    for size in range(1, 13):
        print(
            size,
            rational[size]["H"],
            rational[size]["average_degree"],
            sat[size]["H"],
            sat[size]["average_degree"],
        )
    for k in (1, 2, 3, 4):
        cube = multistar_cube_certificate(k)
        print(
            "cube",
            k,
            "n=", cube["n"],
            "average=", cube["exact_average_degree"],
            "|A-A|=", cube["difference_palette"],
        )
