#!/usr/bin/env python3
"""Discovery-only three-terminal state algebra for the b/h Rayleigh gap."""

from __future__ import annotations

import sympy as sp


p1, p2, r1, r2, s1, s2, c = sp.symbols("p1 p2 r1 r2 s1 s2 c")


def main():
    # L means attached only to hub 1, so its complement weight is the edge
    # to hub 2; R is the reverse.  I means the page vertex is isolated.
    L0, R0, I0, S0 = p2, p1, p1 * p2, p1 + p2
    L3, R3, I3, S3 = r2, r1, r1 * r2, r1 + r2
    L4, R4, I4, S4 = s2, s1, s1 * s2, s1 + s2

    # No branch connects the hubs.
    t0 = c * (
        I0 * I3 * I4
        + S0 * I3 * I4 + I0 * S3 * I4 + I0 * I3 * S4
        + (L0 * R3 + R0 * L3) * I4
        + (L0 * R4 + R0 * L4) * I3
        + (L3 * R4 + R3 * L4) * I0
    )
    x0 = c * (L0 * L3 * (I4 + R4) + R0 * R3 * (I4 + L4))
    y0 = c * (L0 * L4 * (I3 + R3) + R0 * R4 * (I3 + L3))
    z0 = c * (L3 * L4 * (I0 + R0) + R3 * R4 * (I0 + L0))
    u0 = c * (L0 * L3 * L4 + R0 * R3 * R4)

    # The direct c branch is the unique hub connector.
    td = I0 * I3 * I4 + S0 * I3 * I4 + I0 * S3 * I4 + I0 * I3 * S4
    xd, yd, zd, ud = S0 * S3 * I4, S0 * S4 * I3, S3 * S4 * I0, S0 * S3 * S4

    # One marked page is the unique hub connector; the direct branch is then
    # absent and contributes its complement activity c.
    tb = c * (I3 * I4 + I0 * I4 + I0 * I3)
    xb = c * (S3 * I4 + S0 * I4)
    yb = c * (S4 * I3 + S0 * I3)
    zb = c * (S4 * I0 + S3 * I0)
    ub = c * (S3 * S4 + S0 * S4 + S0 * S3)

    states = {
        "t": sp.expand(t0 + td + tb),
        "x03": sp.expand(x0 + xd + xb),
        "y04": sp.expand(y0 + yd + yb),
        "z34": sp.expand(z0 + zd + zb),
        "u": sp.expand(u0 + ud + ub),
    }
    t, x, y, z, u = states.values()
    delta = sp.expand((t + y + z) * (t + x + z) - t * (t + x + y + z + u))
    compressed = sp.expand((x + z) * (y + z) + t * (z - u))
    assert delta == compressed

    for name, polynomial in states.items():
        print(name, "terms", len(sp.Poly(polynomial).terms()), "factor", sp.factor(polynomial))
    print("Delta terms", len(sp.Poly(delta).terms()))
    print("Delta factor", sp.factor(delta))


if __name__ == "__main__":
    main()
