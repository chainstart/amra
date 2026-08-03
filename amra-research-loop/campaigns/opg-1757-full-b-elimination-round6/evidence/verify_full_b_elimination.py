#!/usr/bin/env python3
"""Exact full-b elimination and topology-firewall checks."""
import json
from pathlib import Path
import sympy as sp

src=Path(__file__).parents[2]/"opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json"
data=json.loads(src.read_text())["enumeration"]
a,b,c,d,e,t=sp.symbols("a b c d e t")
loc={str(x):x for x in (a,b,c,d,e)}
P=sp.sympify(data["P"],locals=loc); xi=sp.sympify(data["xi"],locals=loc)
A=sp.diff(P,b); C=P.subs(b,0); D=sp.diff(xi,b); E=xi.subs(b,0)
assert sp.degree(P,b)==sp.degree(xi,b)==1
Delta=sp.factor(A*E-D*C); R=sp.cancel(Delta/(2*a**2))
poly=sp.Poly(sp.expand(R),a,c,d,e)
assert poly.total_degree()==10 and len(poly.terms())==41
assert all(coefficient>0 for _,coefficient in poly.terms())
pc=sp.Poly(R,c); r2,r1,r0=pc.all_coeffs()
assert sp.factor(r2)==(d*e+d+e+2)*(a*d*e+a*d+a*e+d*e)**2
assert sp.factor(r0)==2*a**2*d**2*e**2*(d+2)*(e+2)
expected_disc=a**2*d**4*e**4*(
 a**2*d**2*e**2+2*a**2*d**2*e+a**2*d**2+2*a**2*d*e**2
 +2*a**2*d*e+a**2*e**2-4*a*d**2*e**2-12*a*d**2*e-8*a*d**2
 -12*a*d*e**2-32*a*d*e-16*a*d-8*a*e**2-16*a*e
 -4*d**2*e**2-8*d**2*e-8*d*e**2-16*d*e)
assert sp.expand(sp.discriminant(pc.as_expr(),c)-expected_disc)==0
anchor_path=sp.factor(P.subs({a:1-sp.Rational(11,10)*t,b:1,c:1,d:1,e:1}))
assert sp.expand(anchor_path-2*(726*t**2-2255*t+1600)/25)==0
assert sp.Rational(205,132)-5*sp.sqrt(145)/132>1
z={a:sp.Rational(-7,5),b:-6,c:-5,d:-3,e:-5}
assert (P.subs(z),xi.subs(z))==(65,sp.Rational(-1588,5))
assert (A.subs(z),C.subs(z),D.subs(z),E.subs(z),Delta.subs(z))==(
 sp.Rational(9,5),sp.Rational(379,5),198,sp.Rational(4352,5),sp.Rational(-336042,25))
tangent=sp.factor(P.subs({a:2,b:sp.Rational(-1,2),c:0,d:1,e:1-6*t}))
assert tangent==12*(6*t-1)**2
print("full-b elimination ledger: PASS")
print("Delta=2*a^2*R, degree(R)=10, terms(R)=41, all coefficients positive")
print("exact negative xi point recorded; distinguished-component membership OPEN")
