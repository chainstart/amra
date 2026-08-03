#!/usr/bin/env python3
"""Discovery only: rational polygonal P-positive path search."""
import json, random
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
data=json.loads((ROOT/'opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json').read_text())['enumeration']
a,b,c,d,e,t=sp.symbols('a b c d e t'); vs=(a,b,c,d,e)
P=sp.sympify(data['P'],locals={v.name:v for v in vs}); Pf=sp.lambdify(vs,P,'math')
S=(sp.Rational(1),)*5
Z=(sp.Rational(-7,5),sp.Integer(-6),sp.Integer(-5),sp.Integer(-3),sp.Integer(-5))

def numok(p,q):
    pp=tuple(map(float,p)); qq=tuple(map(float,q))
    return min(Pf(*[pp[j]+k*(qq[j]-pp[j])/80.0 for j in range(5)]) for k in range(81))>1e-6

def exact_one(p,q):
    f=sp.Poly(sp.expand(P.subs({v:p[i]+t*(q[i]-p[i]) for i,v in enumerate(vs)})),t)
    n=f.degree(); coeff=[f.nth(i) for i in range(n+1)]
    bern=[sum(coeff[i]*sp.binomial(k,i)/sp.binomial(n,i) for i in range(k+1)) for k in range(n+1)]
    return all(x>0 for x in bern),(f,bern)

def exact(p,q,parts=12):
    out=[]
    for k in range(parts):
        u=tuple(p[j]+sp.Rational(k,parts)*(q[j]-p[j]) for j in range(5))
        v=tuple(p[j]+sp.Rational(k+1,parts)*(q[j]-p[j]) for j in range(5))
        ok,cert=exact_one(u,v); out.append((ok,cert))
        if not ok:return False,out
    return True,out

random.seed(175709)
left=[];right=[]
for _ in range(100000):
    den=random.choice((1,2,3,4,5,8,10))
    w=tuple(sp.Rational(random.randint(-80,60),den) for _ in vs)
    if Pf(*map(float,w))<=0:continue
    if len(left)<300 and numok(S,w):left.append(w)
    if len(right)<300 and numok(w,Z):right.append(w)
    if len(left)>=300 and len(right)>=300:break
print('clouds',len(left),len(right),flush=True)
nc=0
for p in left:
    for q in right:
        if not numok(p,q):continue
        nc+=1
        tests=[]
        for u,v in ((S,p),(p,q),(q,Z)):
            ok,f=exact(u,v);tests.append((ok,f))
            if not ok:break
        if all(x[0] for x in tests):
            print('FOUND',nc)
            for w in (S,p,q,Z):print(tuple(map(str,w)))
            for _,pieces in tests:
                print('SEGMENT_PIECES',len(pieces))
                for _,(f,bern) in pieces:
                    print('POLY',sp.factor(f.as_expr()))
                    print('BERN',','.join(map(str,bern)))
            raise SystemExit
        if nc>=100:break
    if nc>=100:break
print('NONE tested',nc)
