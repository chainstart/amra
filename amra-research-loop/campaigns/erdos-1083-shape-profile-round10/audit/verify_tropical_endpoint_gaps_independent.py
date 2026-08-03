#!/usr/bin/env python3
"""Independent reconstruction of the tropical endpoint-gap theorem.

No campaign evidence module is imported.
"""

from fractions import Fraction
from itertools import combinations


def shape(support):
    x = sorted(support)
    assert len(x) >= 2
    return x[-1] - x[0], x[1] - x[0], x[-1] - x[-2]


def sums(a, b):
    return {x + y for x in a for y in b}


def main() -> None:
    checks = 0

    # Independent exhaustive product-law reconstruction.
    grid = tuple(Fraction(k, 2) for k in range(-6, 9))
    sets = [set(c) for size in (2, 3) for c in combinations(grid, size)]
    for a in sets:
        wa, la, ra = shape(a)
        for b in sets:
            wb, lb, rb = shape(b)
            assert shape(sums(a, b)) == (wa + wb, min(la, lb), min(ra, rb))
            checks += 1

    # Sign reflection and all four zero/nonzero natural-anchor branches.
    anchors = [
        {Fraction(0), Fraction(1), Fraction(4)},
        {Fraction(2), Fraction(3), Fraction(6)},
        {Fraction(-4), Fraction(-1), Fraction(0)},
        {Fraction(-6), Fraction(-3), Fraction(-2)},
    ]
    magnitudes = [Fraction(k) for k in (1, 2, 5, 9)]
    for x in anchors:
        width, left, right = shape(x)
        for sign in (-1, 1):
            profiles = []
            raw = []
            for u in magnitudes:
                w, l, r = shape({sign * u * z for z in x})
                expected = (left / width, right / width) if sign > 0 else (right / width, left / width)
                assert (l / w, r / w) == expected
                profiles.append((l / w, r / w))
                raw.append((l, r))
                checks += 1
            assert len(set(profiles)) == 1
            assert len(set(raw)) == len(magnitudes)

    # Exhaust the simultaneous-feasibility/equality-wall logic over small
    # rational constants.  Rows are retained only when both f endpoints are
    # feasible.  Same-sign magnitudes are distinct.
    equality_cases = 0
    retained_cases = 0
    for c_left in map(Fraction, (1, 2, 4)):
        for c_right in map(Fraction, (1, 3, 5)):
            for L in map(Fraction, range(1, 8)):
                for R in map(Fraction, range(1, 8)):
                    mags = list(map(Fraction, range(1, 13)))
                    feasible = [u for u in mags if c_left * u >= L and c_right * u >= R]
                    eq = [u for u in feasible if c_left * u == L or c_right * u == R]
                    assert len(eq) <= 1
                    equality_cases += len(eq)
                    core = [u for u in feasible if u not in eq]
                    assert len(core) >= max(0, len(feasible) - 1)
                    for u in core:
                        fl, fr = c_left * u, c_right * u
                        assert fl > L and fr > R
                        # The min equations force the complement gaps.
                        possible_left = [a for a in map(Fraction, range(1, 15)) if min(a, fl) == L]
                        possible_right = [a for a in map(Fraction, range(1, 15)) if min(a, fr) == R]
                        assert possible_left == [L]
                        assert possible_right == [R]
                        retained_cases += 1

    # Higher-layer firewall reconstructed independently.
    a = {Fraction(0), Fraction(2), Fraction(100)}
    b = {Fraction(0), Fraction(3), Fraction(100)}
    assert sorted(sums(a, b))[:4] == [0, 2, 3, 5]

    print("PASS independent tropical endpoint-gap audit")
    print(f"product_checks={checks} equality_rows={equality_cases} retained_rows={retained_cases}")


if __name__ == "__main__":
    main()
