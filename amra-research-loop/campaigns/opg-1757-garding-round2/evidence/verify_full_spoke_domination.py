#!/usr/bin/env python3
"""Exact symbolic verifier for full four-variable W4 spoke domination."""

import json
import sympy as sp


a, b, c, d = sp.symbols("a b c d")
x, y, z, w, r = sp.symbols("x y z w r", positive=True)

S = c*d + c + d
P = sp.expand(
    (b + 1)*S*(S + 2)*a**2
    + 2*(
        b*c**2*d**2 + 2*b*c**2*d + b*c**2
        + 2*b*c*d**2 + 4*b*c*d + 2*b*c + b*d**2 + 2*b*d
        + c**2*d**2 + c**2*d + 2*c*d**2 + 2*c*d + d**2
    )*a
    + c*d*(c + 2)*(b*d + 2*b + d)
)
Q = sp.expand(
    2*S*a**2
    + 2*(
        b*c*d**2 + 2*b*c*d + 2*b*c + b*d**2 + 2*b*d
        + c*d**2 + 2*c*d + d**2
    )*a
    + 2*c*d*(b*d + 2*b + d)
)

shift = {a: x - 1, b: y - 1, c: z - 1, d: w - 1}
Ps = sp.expand(P.subs(shift))
Qs = sp.expand(Q.subs(shift))

A = (w*x - 1)*(w*x*y + y - 2)
H = w**2*y + 2*w*x - 4*w + x**2*y - 4*x - 2*y + 6
C = 2*(w**2*x*y + w*x**2 - 2*w*x - w + x*y - 2*x - 2*y + 4)
E = -2*(w**2*y + 2*w*x - 4*w + x**2 + 2*x*y - 6*x - 3*y + 7)
J = w**2*y + 2*w*x + 2*w*y - 4*w + y - 2
R = (w - 1)**2*(x - 1)**4*(y - 1)**2

assert sp.expand(Ps - (A*z**2 - H)) == 0
assert sp.expand(Qs - (C*z + E)) == 0
assert sp.expand(H*C**2 - A*E**2 - 4*R*J) == 0

# Put r=wx.  On the anchor branch r>1 and y>2/(r+1).
# J and C/2 are affine increasing functions of y.  Their boundary values
# are manifest squares.
J_r = sp.factor(J.subs(x, r/w))
C0_r = sp.factor((C/2).subs(x, r/w))
y0 = 2/(r + 1)
assert sp.factor(J_r.subs(y, y0) - 2*(r - w)**2/(r + 1)) == 0
assert sp.factor(C0_r.subs(y, y0) - (r - 1)*(r - w)**2/(w*(r + 1))) == 0
assert sp.factor(sp.diff(J_r, y) - (w + 1)**2) == 0
assert sp.factor(
    sp.diff(C0_r, y) - (r*(w**2 + 1) - 2*w)/w
) == 0
# The last slope is strictly positive for r>1,w>0 because
# r(w^2+1)-2w > (w-1)^2 >= 0.
assert sp.factor((r*(w**2 + 1) - 2*w) - (w - 1)**2) == (r - 1)*(w**2 + 1)

# The two possible A=0 exit walls have nonnegative H, hence P=-H<=0.
H_r1 = sp.factor(H.subs(w, 1/x))
assert sp.factor(H_r1 - (x - 1)**2*(y*(x + 1)**2 - 4*x)/x**2) == 0
H_ywall = sp.factor(H.subs(y, 2/(w*x + 1)))
assert sp.factor(H_ywall - 2*(w - 1)**2*(x - 1)**2/(w*x + 1)) == 0

# If R=0 on the open anchor base, H is still strictly positive.
assert sp.factor(H.subs(w, 1) - A.subs(w, 1)) == 0
assert sp.factor(H.subs(x, 1) - A.subs(x, 1)) == 0
assert sp.factor(H.subs(y, 1) - (w + x - 2)**2) == 0
assert sp.factor(A.subs(y, 1) - (w*x - 1)**2) == 0

assert Ps.subs({x: 2, y: 2, z: 2, w: 2}) == 86
assert Qs.subs({x: 2, y: 2, z: 2, w: 2}) == 38

print(json.dumps({
    "schema": "amra.opg1757.full-w4-spoke-domination.v1",
    "shift": "x=a+1,y=b+1,z=c+1,w=d+1",
    "P_identity": "P=A*z^2-H",
    "xi_identity": "xi=C*z+E",
    "A": str(A),
    "H": str(H),
    "C": str(C),
    "E": str(E),
    "J": str(J),
    "boundary_identity": "H*C^2-A*E^2=4*(w-1)^2*(x-1)^4*(y-1)^2*J",
    "distinguished_component": "x,w,z>0; w*x>1; y*(w*x+1)>2; z>sqrt(H/A)",
    "base_certificate": {
        "J_at_y_boundary": "2*(r-w)^2/(r+1)",
        "dJ_dy": "(w+1)^2",
        "C_over_2_at_y_boundary": "(r-1)*(r-w)^2/(w*(r+1))",
        "d_C_over_2_dy": "(r*(w^2+1)-2*w)/w > 0"
    },
    "conclusion": "xi>0 on the full four-variable distinguished spoke component",
    "scope": "W4 marked-spoke stabilizer specialization only; not the global graphic moving-edge lemma",
    "public_problem_closed": False
}, indent=2, sort_keys=True))
