#!/usr/bin/env python3
"""Search/certify a base path using the rational lift b=M*A."""
import json,random
from pathlib import Path
from collections import deque
import numpy as np
from scipy.spatial import cKDTree
import sympy as sp
ROOT=Path(__file__).resolve().parents[3]
data=json.loads((ROOT/'opg-1757-k5-cross-round3/evidence/k5_cross_orbit_probe.json').read_text())['enumeration']
a,b,c,d,e,t=sp.symbols('a b c d e t');vs=(a,c,d,e)
P=sp.sympify(data['P'],locals={v.name:v for v in (a,b,c,d,e)});A=sp.diff(P,b);C=P.subs(b,0)
M=sp.Integer(10)**6;Q=sp.expand(M*A*A+C);Qf=sp.lambdify(vs,Q,'numpy')
S=(sp.Rational(1),)*4;Z=(sp.Rational(-7,5),-5,-3,-5)
def exact_piece(p,q):
 f=sp.Poly(sp.expand(Q.subs({v:p[i]+t*(q[i]-p[i]) for i,v in enumerate(vs)})),t)
 n=f.degree();aa=[f.nth(i) for i in range(n+1)]
 be=[sum(aa[i]*sp.binomial(k,i)/sp.binomial(n,i) for i in range(k+1)) for k in range(n+1)]
 return all(x>0 for x in be),be
def exact_edge(p,q,parts=16):
 cert=[]
 for k in range(parts):
  u=tuple(p[j]+sp.Rational(k,parts)*(q[j]-p[j]) for j in range(4));v=tuple(p[j]+sp.Rational(k+1,parts)*(q[j]-p[j]) for j in range(4))
  ok,be=exact_piece(u,v);cert.append(be)
  if not ok:return False,cert
 return True,cert
random.seed(99);pts=[S,Z]
while len(pts)<700:
 den=random.choice((2,3,4,5,6,8,10));w=tuple(sp.Rational(random.randint(-70,50),den) for _ in range(4))
 if float(Qf(*map(float,w)))>1:pts.append(w)
arr=np.array([[float(x) for x in p] for p in pts]);tree=cKDTree(arr);adj=[[] for _ in pts]
for i in range(len(pts)):
 for jj in tree.query(arr[i],k=22)[1][1:]:
  j=int(jj);lam=np.linspace(0,1,101)[:,None];seg=arr[i]+lam*(arr[j]-arr[i]);val=Qf(seg[:,0],seg[:,1],seg[:,2],seg[:,3])
  if np.min(val)>1e-4:adj[i].append(j)
blocked=set()
for attempt in range(100):
 par={0:-1};dq=deque([0])
 while dq and 1 not in par:
  i=dq.popleft()
  for j in adj[i]:
   if (i,j) in blocked or j in par:continue
   par[j]=i;dq.append(j)
 if 1 not in par:print('NO_PATH',attempt);break
 path=[];k=1
 while k!=-1:path.append(k);k=par[k]
 path=path[::-1];allcert=[];bad=None
 if attempt==0:
  print('NUMERIC_PATH',len(path),flush=True)
  for ii in path:print(tuple(map(str,pts[ii])),flush=True)
  break
 for i,j in zip(path,path[1:]):
  ok,ce=exact_edge(pts[i],pts[j]);allcert.append(ce)
  if not ok:bad=(i,j);break
 if bad:blocked|={bad,(bad[1],bad[0])};continue
 print('FOUND',len(path),'attempt',attempt,'M',M)
 for i in path:print(tuple(map(str,pts[i])))
 print('CERT_MINIMA')
 for edgecert in allcert:print(min(min(x for x in be) for be in edgecert))
 break
