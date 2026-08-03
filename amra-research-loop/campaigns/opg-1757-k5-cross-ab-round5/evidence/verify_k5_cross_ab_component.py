#!/usr/bin/env python3
"""Bounded exact replay for the K5-e cross-edge (a,b) slice theorem."""
import sympy as s

a, b = s.symbols("a b", real=True)
P = 24*a**2*b + 24*a**2 + 48*a*b + 20*a + 9*b + 3
xi = 2*(5*a**2 + 14*a*b + 6*a + 3*b + 1)
A = 24*a**2 + 48*a + 9
C = 24*a**2 + 20*a + 3
D = 14*a + 3
E = 5*a**2 + 6*a + 1
Q = 120*a**2 + 48*a + 5
beta = -1 + s.sqrt(10)/4

assert s.expand(P - (A*b + C)) == 0
assert s.expand(xi/2 - (D*b + E)) == 0
assert s.factor(A*xi/2 - D*P) == a**2*Q
assert s.factor(s.resultant(P, xi, b)) == 2*a**2*Q
assert s.simplify(C.subs(a, beta) - (22 - 7*s.sqrt(10))) == 0
assert bool((22 - 7*s.sqrt(10)) < 0)
assert s.discriminant(Q, a) == -96
assert bool(s.Rational(-3, 14) < beta)
assert P.subs({a: 1, b: 1}) == 128
assert xi.subs({a: 1, b: 1}) == 58
assert s.expand(P.subs(a, 0) - 3*(3*b + 1)) == 0
assert s.expand(xi.subs(a, 0) - 2*(3*b + 1)) == 0

print("K5 cross (a,b) exact component certificate: PASS")
