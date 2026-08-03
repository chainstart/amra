#!/usr/bin/env python3
"""Exact verifier for the prism triangle-edge z=1 component theorem."""
import sympy as s

x, y, z = s.symbols("x y z")
P = x**4*y**2*z**2-x**2*y*z**2-2*x**2*y*z-x**2*y-2*x**2*z+4*x*z+4*x-y**2+4*y-6
Q = x**4*y+x**2*y**2*z**2+x**2*y**2+2*x**2*y*z-4*x**2*y+2*x**2*z-8*x**2-4*x*y*z-4*x*y-8*x*z+24*x-2*y**2-y*z**2+10*y+8*z-18
C = (x+1)*(x**2+1)*y**2-4*(x+1)*y+6-2*x
D = 2*(x+1)*y**2+(x**3+x**2-x-9)*y+10-6*x
assert s.factor(P.subs(z,1) - (x-1)*C) == 0
assert s.factor(Q.subs(z,1) - (x-1)*D) == 0
assert s.factor(s.discriminant(C,y) - 8*(x-1)**3*(x+1)) == 0
assert s.factor(s.discriminant(D,y) - (x-1)**3*(x**3+5*x**2+11*x-1)) == 0
assert s.expand((x-1)*(x**2+6*x+17)+16 - (x**3+5*x**2+11*x-1)) == 0
assert s.factor(s.resultant(C,D,y) + 2*(x-1)**7*(x+1)*(x+3)**2) == 0
assert s.solve(D.subs(x,2),y) == [s.Rational(-2,3), s.Rational(1,2)]
assert s.factor(C.subs({x:s.Rational(3,2),y:s.Rational(1,2)})) == s.Rational(1,32)
print("prism triangle-edge z=1 component: PASS")
