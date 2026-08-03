#!/usr/bin/env python3
"""Discovery only: search rational polygonal paths in the A>0 projection cell."""
import json, random
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
data=json.loads((ROOT/'opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json').read_text())['enumeration']
a,b,c,d,e,t=sp.symbols('a b c d e t'); vs=(a,c,d,e)
P=sp.sympify(data['P'],locals={v.name:v for v in (a,b,c,d,e)})
A=sp.diff(P,b); Af=sp.lambdify(vs,A,'math')
S=(sp.Rational(1),)*4; Z=(sp.Rational(-7,5),sp.Integer(-5),sp.Integer(-3),sp.Integer(-5))

def numok(p,q):
    pp=tuple(map(float,p)); qq=tuple(map(float,q))
    return min(Af(*[pp[j]+k*(qq[j]-pp[j])/40.0 for j in range(4)]) for k in range(41))>1e-7

def exact(p,q):
    f=sp.Poly(sp.expand(A.subs({v:p[i]+t*(q[i]-p[i]) for i,v in enumerate(vs)})),t)
    return sp.count_roots(f,0,1)==0,f

random.seed(1757)
# Two independent clouds and a bridge are substantially easier than one waypoint.
left=[]; right=[]
for _ in range(30000):
    den=random.choice((1,2,3,4,5,8,10))
    w=tuple(sp.Rational(random.randint(-64,48),den) for _ in vs)
    if Af(*map(float,w))<=0: continue
    if len(left)<120 and numok(S,w): left.append(w)
    if len(right)<120 and numok(w,Z): right.append(w)
    if len(left)>=120 and len(right)>=120: break
print('clouds',len(left),len(right),flush=True)
for p in left:
    for q in right:
        if not numok(p,q): continue
        tests=[]
        for u,v in ((S,p),(p,q),(q,Z)):
            ok,f=exact(u,v); tests.append((ok,f))
            if not ok: break
        if all(x[0] for x in tests):
            print('FOUND')
            for w in (S,p,q,Z): print(tuple(map(str,w)))
            for _,f in tests: print(sp.factor(f.as_expr()))
            raise SystemExit
print('NONE')
