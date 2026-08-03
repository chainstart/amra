#!/usr/bin/env python3
"""Blind audit from the displayed A,C,D,E polynomials only."""

import json
from pathlib import Path
import sympy as sp


e, b = sp.symbols("e b", real=True)
A = 24*e**2 + 48*e + 9
C = 24*e**2 + 20*e + 3
D = 5*e**2 + 10*e + 2
E = 5*e**2 + 6*e + 1
P = sp.expand(b*A+C)
xi = sp.expand(2*(b*D+E))

rt10, rt15 = sp.sqrt(10), sp.sqrt(15)
alpha = -1+rt10/4
beta = -1-rt10/4
d_upper = -1+rt15/5

# Reconstruct all wall formulas directly.
assert sp.simplify(A-24*(e-alpha)*(e-beta)) == 0
assert sp.simplify(C.subs(e,alpha)-(22-7*rt10)) == 0
assert 22**2 < 49*10  # hence C(alpha)<0
assert sp.simplify(P.subs({b:1,e:1})-128) == 0
assert sp.simplify(xi.subs({b:1,e:1})-58) == 0

# Determinant identity and exact cubic data.
Q = sp.expand(E*A-D*C)
assert Q == 44*e**3+94*e**2+32*e+3
assert sp.expand(A*xi/2-D*P-Q) == 0
discQ = sp.discriminant(Q,e)
assert discQ == -9552 < 0
Qalpha = sp.simplify(Q.subs(e,alpha))
assert sp.simplify(Qalpha-(-22+7*rt10)/8) == 0
assert 49*10 > 22**2  # hence Q(alpha)>0

# D has positive leading coefficient and its upper root is below alpha.
assert sp.simplify(D-5*(e-(-1-rt15/5))*(e-d_upper)) == 0
assert 15*16 < 10*25  # (sqrt(15)/5)^2 < (sqrt(10)/4)^2
assert sp.simplify(alpha-d_upper) > 0

# Independent exact real-root count/isolation for Q, supplementing the cubic
# discriminant argument.  Its sole real root lies below alpha.
intervals = sp.Poly(Q,e,domain=sp.QQ).intervals(eps=sp.Rational(1,10**8))
real_intervals = [(lo,hi,mult) for (lo,hi),mult in intervals
                  if not (sp.im(lo) or sp.im(hi))]
assert len(real_intervals) == 1 and real_intervals[0][2] == 1
root_lo,root_hi,_ = real_intervals[0]
assert root_hi < sp.Rational(-1,4) < alpha

# The topology used in the proof is now forced algebraically:
# at e=alpha no b has P>0; on e>alpha, A>0 and each fiber is exactly the
# epigraph b>-C/A.  The coordinate u=b+C/A maps it to
# (alpha,infinity)x(0,infinity), while the anchor maps to positive u.
anchor_u = sp.simplify(1+C.subs(e,1)/A.subs(e,1))
assert anchor_u == sp.Rational(128,81) > 0

# Strict sign chain at representative rational points on both sides is only
# a guard; the theorem uses root ordering and the unique-root argument.
for sample in (sp.Rational(-1,5),0,1,10):
    assert sample > alpha
    assert A.subs(e,sample) > 0
    assert D.subs(e,sample) > 0
    assert Q.subs(e,sample) > 0

result = {
    "schema":"amra.opg1757.k5-cross-be.blind-audit.v1",
    "source":"A,C,D,E formulas reconstructed without importing author verifier",
    "polynomials":{"A":str(A),"C":str(C),"D":str(D),"E":str(E),"P":str(P),"xi":str(xi)},
    "anchor":{"P":128,"xi":58,"u":"128/81"},
    "alpha_wall":{"alpha":"-1+sqrt(10)/4","C_alpha":"22-7sqrt(10)","sign":"negative","consequence":"entire vertical line excluded from P>0"},
    "component":{"exact":"e>alpha and b>-C(e)/A(e)","homeomorphism":"(e,b)->(e,b+C/A) onto (alpha,infinity)x(0,infinity)"},
    "determinant":{"identity":"A*xi/2=D*P+Q","Q":str(Q),"disc_Q":int(discQ),"Q_alpha":"(-22+7sqrt(10))/8","real_root_isolation":[str(root_lo),str(root_hi)]},
    "D_order":{"upper_root":"-1+sqrt(15)/5","relation":"upper_root(D)<alpha"},
    "conclusion":"A,D,P,Q>0 on the complete distinguished component, hence xi>0",
    "scope":"a=c=d=1 two-variable (b,e) slice only; not five-variable stabilizer, transverse directions, G201, or OPG-1757",
    "public_one_eighth_changed":False
}
Path(__file__).with_name("K5_CROSS_BE_INDEPENDENT_AUDIT.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
