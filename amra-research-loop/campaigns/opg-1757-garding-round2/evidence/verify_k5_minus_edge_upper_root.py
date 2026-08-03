#!/usr/bin/env python3
"""Exact symbolic verifier for K5-e upper-root component identities."""
import sympy as s

a, y, z, ell = s.symbols("a y z ell")
b = y - 1
L = z * (y + 1) - 2
M = z * (y**2 + 1) - 2
A = (y + 1) * (z**2 * (y**2 + 1) - 2)
F = s.expand(A*a**2 + 2*L*M*a + b*L**2)
G = s.expand(F - a*b*L*(a*(L + 4) + 2*L))
D = (y + 1)*z**2 + y - 3
N = y**2*z + y**2 - 4*y - 3*z + 5

assert s.factor(s.discriminant(F, a) - 8*(y**2 + 1)*(z - 1)**2*L**2) == 0
assert s.factor(s.Poly(G, a).LC() - 2*D) == 0
assert s.factor(s.discriminant(G, a) + 8*(z - 1)*L**2*N) == 0
assert s.discriminant(G, a).subs({y: 2, z: 2}) == -384
assert s.factor(D.subs(z**2, 2/(y**2 + 1)) - (y - 1)**3/(y**2 + 1)) == 0

assert s.factor(F.subs(z, 1) - (y - 1)*(a*(y + 1) + y - 1)**2) == 0
assert s.factor(G.subs(z, 1) - (y - 1)*(2*a + y - 1)**2) == 0
zL = s.Rational(2)/(y + 1)
assert s.factor(F.subs(z, zL) - 2*a**2*(y - 1)**2/(y + 1)) == 0
assert s.factor(G.subs(z, zL) - 2*a**2*(y - 1)**2/(y + 1)) == 0

zN = -(y**2 - 4*y + 5)/(y**2 - 3)
aN = (y - 1)*(y**2 + 1)/(2*(y**2 - 2*y - 1))
FN = (y - 1)**5*(y**2 - 7)*(y**2 + 1)**3 / (4*(y**2 - 3)**2*(y**2 - 2*y - 1)**2)
assert s.factor(N.subs(z, zN)) == 0
assert s.factor(s.diff(G, a).subs({z: zN, a: aN})) == 0
assert s.factor(F.subs({z: zN, a: aN}) - FN) == 0

zH = 1 - ell**2/8
yH = -(ell**2 + 8*ell + 8)/(ell**2 - 8)
aH = -2*ell/(ell + 4)
assert s.factor(L.subs({z: zH, y: yH}) - ell) == 0
assert s.factor((L**2 + 8*(z - 1)).subs({z: zH, y: yH})) == 0
FpH = ell**3*(ell**2 + 4*ell + 8)/(2*(ell**2 - 8))
assert s.factor(F.subs({z: zH, y: yH, a: aH})) == 0
assert s.factor(G.subs({z: zH, y: yH, a: aH})) == 0
assert s.factor(s.diff(F, a).subs({z: zH, y: yH, a: aH}) - FpH) == 0

print("K5-e upper-root identities: PASS")
