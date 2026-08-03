#!/usr/bin/env python3
"""Discovery PRM with exact Bernstein certification of every retained edge."""
import json, random
from pathlib import Path
from collections import deque
import numpy as np
from scipy.spatial import cKDTree
import sympy as sp

ROOT=Path(__file__).resolve().parents[3]
data=json.loads((ROOT/'opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json').read_text())['enumeration']
a,b,c,d,e,t=sp.symbols('a b c d e t');vs=(a,b,c,d,e)
P=sp.sympify(data['P'],locals={v.name:v for v in vs});Pf=sp.lambdify(vs,P,'numpy')
S=(sp.Rational(1),)*5; Z=(sp.Rational(-7,5),-6,-5,-3,-5)

def exact_edge(p,q):
 f=sp.Poly(sp.expand(P.subs({v:p[i]+t*(q[i]-p[i]) for i,v in enumerate(vs)})),t)
 n=f.degree();aa=[f.nth(i) for i in range(n+1)]
 be=[sum(aa[i]*sp.binomial(k,i)/sp.binomial(n,i) for i in range(k+1)) for k in range(n+1)]
 return all(x>0 for x in be),(be,f)

random.seed(79)
pts=[S,Z]
while len(pts)<3500:
 den=random.choice((2,3,4,5,6,8,10))
 w=tuple(sp.Rational(random.randint(-80,50),den) for _ in range(5))
 val=float(Pf(*map(float,w)))
 if val>0.5:pts.append(w)
arr=np.array([[float(x) for x in p] for p in pts]); tree=cKDTree(arr)
adj=[[] for _ in pts]
for i,p in enumerate(pts):
 for j in tree.query(arr[i],k=30)[1][1:]:
  j=int(j)
  # dense numeric filter
  lam=np.linspace(0,1,31)[:,None];seg=arr[i]+lam*(arr[j]-arr[i])
  vals=Pf(seg[:,0],seg[:,1],seg[:,2],seg[:,3],seg[:,4])
  if np.min(vals)<=1e-5:continue
  adj[i].append(j)

blocked=set()
for attempt in range(200):
 par={0:-1};dq=deque([0])
 while dq and 1 not in par:
  i=dq.popleft()
  for j in adj[i]:
   if (i,j) in blocked or j in par:continue
   par[j]=i;dq.append(j)
 if 1 not in par:
  print('NO_NUMERIC_PATH',attempt);break
 path=[];k=1
 while k!=-1:path.append(k);k=par[k]
 path=path[::-1]
 bad=None;certs=[]
 for i,j in zip(path,path[1:]):
  ok,pack=exact_edge(pts[i],pts[j]);be,f=pack;certs.append(be)
  if not ok:bad=(i,j);break
 if bad:
  print('BAD',tuple(map(str,pts[bad[0]])),tuple(map(str,pts[bad[1]])))
  print('BADPOLY',sp.factor(f.as_expr()),'ROOTS',sp.intervals(f))
  blocked.add(bad);blocked.add((bad[1],bad[0]));continue
 print('FOUND',len(path),attempt)
 for i in path:print(tuple(map(str,pts[i])))
 print('BERNSTEIN')
 for be in certs:print(','.join(map(str,be)))
 break
