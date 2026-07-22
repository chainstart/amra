#!/usr/bin/env python3
"""Exact algebraic certificate for the fixed-hyperbola Elekes--Szabo route.

This checks the factorized radius surface, irreducibility certificate, and a
point evaluation of the differential obstruction to local additive-group form.
The incidence theorem itself is cited, not reproved, in the accompanying note.
"""

import json
import sympy as sp

x, y, z, R = sp.symbols("x y z R")
F = (1 + x*y) * (1 + x*z) * (1 + y*z) - R*x*y*z
phi_numerator = sp.expand(x*y*z * (
    x*y*z + x + y + z + 1/x + 1/y + 1/z + 1/(x*y*z)
))

# Regard F as a quadratic in z.  For R>8 its discriminant cannot be a square:
# after y=1 it is a quartic in x with nonzero discriminant.
Fz_poly = sp.Poly(F, z)
disc_z = sp.factor(sp.discriminant(Fz_poly, z))
disc_y1 = sp.factor(disc_z.subs(y, 1))
disc_y1_in_x = sp.factor(sp.discriminant(disc_y1, x))

# On a local graph z=g(x,y), tangent differentiation is
# D_x=d_x-(F_x/F_z)d_z and similarly for D_y.  Local additive group form
# forces D_x D_y log(g_x/g_y)=0, while g_x/g_y=F_x/F_y.
Fx, Fy, Fz = (sp.diff(F, v) for v in (x, y, z))
Dx = lambda h: sp.diff(h, x) - Fx/Fz * sp.diff(h, z)
Dy = lambda h: sp.diff(h, y) - Fy/Fz * sp.diff(h, z)
first_y = Dy(Fx)/Fx - Dy(Fy)/Fy
mixed = Dx(first_y)
mixed_num, mixed_den = sp.together(mixed).as_numer_denom()
test_point = {x: 0, y: 1, z: -1}

checks = {
    "radius_surface_factorization": sp.expand(phi_numerator - (F + R*x*y*z)) == 0,
    "test_point_lies_on_surface": sp.simplify(F.subs(test_point)) == 0,
    "all_partials_nonzero_at_test_point": all(
        sp.simplify(v.subs(test_point)) != 0 for v in (Fx, Fy, Fz)
    ),
    "mixed_log_derivative_equals_minus_4": sp.simplify(
        mixed_num.subs(test_point) / mixed_den.subs(test_point) + 4
    ) == 0,
    "quartic_discriminant_nonzero_for_R_gt_8": sp.factor(disc_y1_in_x)
        == 256*R**3*(R - 8)*(R + 1)**2,
}

result = {
    "status": "PASS" if all(checks.values()) else "FAIL",
    "checks": checks,
    "F": str(sp.factor(F)),
    "quadratic_discriminant_at_y_1": str(disc_y1),
    "quartic_discriminant_in_x": str(disc_y1_in_x),
    "test_point": {"x": 0, "y": 1, "z": -1},
    "partials_at_test_point": [str(v.subs(test_point)) for v in (Fx, Fy, Fz)],
    "mixed_log_derivative_at_test_point": str(sp.factor(
        mixed_num.subs(test_point) / mixed_den.subs(test_point)
    )),
}
print(json.dumps(result, indent=2, sort_keys=True))
