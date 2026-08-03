#!/usr/bin/env python3
"""Independent forest reconstruction and exact (b,e) sign audit."""
import itertools
import sympy as sp

V = tuple(range(5)); marked=(0,3); missing=(3,4)
edges=[uv for uv in itertools.combinations(V,2) if uv not in {marked,missing}]
a,b,c,d,e=sp.symbols("a b c d e", real=True)
w={(0,1):a,(0,2):a,(0,4):b,(1,2):c,
   (1,3):d,(2,3):d,(1,4):e,(2,4):e}

def forest_root(selected):
    parent=list(V)
    def root(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]; x=parent[x]
        return x
    for u,v in selected:
        ru,rv=root(u),root(v)
        if ru==rv: return None
        parent[ru]=rv
    return root

P=sp.Integer(0); xi=sp.Integer(0); counts=[0,0]
for mask in range(1<<len(edges)):
    selected={edges[i] for i in range(len(edges)) if (mask>>i)&1}
    root=forest_root(selected)
    if root is None: continue
    counts[0]+=1
    mon=sp.prod(w[uv] for uv in edges if uv not in selected)
    P+=mon
    if root(0)==root(3): counts[1]+=1; xi+=mon
assert counts == [128,58]
sl={a:1,c:1,d:1}
A=24*e**2+48*e+9; C=24*e**2+20*e+3
D=5*e**2+10*e+2; E=5*e**2+6*e+1
assert sp.expand(P.subs(sl)-(b*A+C)) == 0
assert sp.expand(xi.subs(sl)-2*(b*D+E)) == 0
assert P.subs({**sl,b:1,e:1}) == 128
assert xi.subs({**sl,b:1,e:1}) == 58
Q=sp.expand(E*A-D*C)
assert Q == 44*e**3+94*e**2+32*e+3
assert sp.discriminant(Q,e) == -9552
alpha=-1+sp.sqrt(10)/4
assert sp.simplify(A.subs(e,alpha)) == 0
assert sp.simplify(C.subs(e,alpha)) == 22-7*sp.sqrt(10)
assert sp.simplify(Q.subs(e,alpha)) == (-22+7*sp.sqrt(10))/8
assert 22**2 < 49*10
assert sp.Rational(15,25) < sp.Rational(10,16)
print("independent K5-e cross (b,e) component audit: PASS")
print("forest counts=128/58; anchor P/xi=128/58; disc(Q)=-9552")
