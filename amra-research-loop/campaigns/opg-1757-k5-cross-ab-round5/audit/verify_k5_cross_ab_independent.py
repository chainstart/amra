#!/usr/bin/env python3
"""Independent forest reconstruction and exact (a,b) slice audit."""
import itertools
import sympy as sp
V=tuple(range(5)); marked=(0,3); missing=(3,4)
edges=[uv for uv in itertools.combinations(V,2) if uv not in {marked,missing}]
a,b,c,d,e=sp.symbols("a b c d e", real=True)
w={(0,1):a,(0,2):a,(0,4):b,(1,2):c,(1,3):d,(2,3):d,(1,4):e,(2,4):e}
def roots(selected):
 p=list(V)
 def r(x):
  while p[x]!=x: p[x]=p[p[x]]; x=p[x]
  return x
 for u,v in selected:
  x,y=r(u),r(v)
  if x==y:return None
  p[x]=y
 return r
P=sp.Integer(0);xi=sp.Integer(0);counts=[0,0]
for mask in range(1<<len(edges)):
 S={edges[i] for i in range(len(edges)) if (mask>>i)&1}; r=roots(S)
 if r is None: continue
 counts[0]+=1; mon=sp.prod(w[uv] for uv in edges if uv not in S); P+=mon
 if r(0)==r(3): counts[1]+=1; xi+=mon
assert counts==[128,58]
sl={c:1,d:1,e:1}
A=24*a**2+48*a+9;C=24*a**2+20*a+3;D=14*a+3;E=5*a**2+6*a+1
assert sp.expand(P.subs(sl)-(A*b+C))==0
assert sp.expand(xi.subs(sl)-2*(D*b+E))==0
assert (P.subs({**sl,a:1,b:1}),xi.subs({**sl,a:1,b:1}))==(128,58)
Q=sp.factor(E*A-D*C)
assert Q==a**2*(120*a**2+48*a+5)
assert sp.discriminant(120*a**2+48*a+5,a)==-96
beta=-1+sp.sqrt(10)/4
assert sp.simplify(A.subs(a,beta))==0
assert sp.simplify(C.subs(a,beta))==22-7*sp.sqrt(10)
assert 22**2<49*10
assert sp.Rational(-3,14)<beta
print("independent K5-e cross (a,b) component audit: PASS")
print("forests=128 connected=58 anchor=128/58 discriminant=-96")
