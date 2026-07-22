#!/usr/bin/env python3
"""Exact symbolic checks used in SHARP_FIXED_RADIUS_CUBE_COUNT.md.

The script verifies only the Vieta product and the four-point circle
determinant factor.  General position and the combinatorial double count
are proved in the accompanying note.
"""

import json
import sympy as sp

x, y, z, rho = sp.symbols("x y z rho", nonzero=True)
A = x * y + 1
B = 1 + 1 / (x * y)
vieta_product = sp.factor(B / A)

r = sp.symbols("r0:4", nonzero=True)
rows = []
for t in r:
    # A circle is alpha*(X^2+Y^2)+beta*X+gamma*Y+delta=0.
    # On (t,1/t), use columns X^2+Y^2, X, Y, 1.
    rows.append([t**2 + t**-2, t, t**-1, 1])
det = sp.factor(sp.det(sp.Matrix(rows)))
vandermonde = sp.prod(r[j] - r[i] for i in range(4) for j in range(i + 1, 4))
quotient = sp.factor(det / vandermonde)

expected_quotient = sp.factor(-(sp.prod(r) - 1) / sp.prod(r) ** 2)
checks = {
    "vieta_product_equals_1_over_xy": sp.simplify(vieta_product - 1 / (x * y)) == 0,
    "circle_determinant_factor": sp.simplify(quotient - expected_quotient) == 0,
}

print(json.dumps({
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "vieta_product": str(vieta_product),
    "circle_quotient": str(quotient),
}, indent=2, sort_keys=True))
