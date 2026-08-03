#!/usr/bin/env python3
"""Exact symbolic and finite-menu guard for the stable-tail no-go."""
from math import comb
import sympy as s

q, A, B = s.symbols("q A B", integer=True)

def C(x, k):
    if isinstance(x, int):
        return comb(x, k) if x >= k else 0
    return s.binomial(x, k)

# Bottom Pascal transfers, with d=5n-15 on x and d=5n-16 on y.
n = s.symbols("n", integer=True, positive=True)
tx = q-(5*n-15)
ty = q-(5*n-16)
An = C(A,2)-(20*n-49)
Bn = C(B,2)-(20*n-52)
assert s.simplify(C(tx,3)+C(A,2)-4*q+3 - (C(tx-1,3)+C(tx-5,2)+An)) == 0
assert s.simplify(C(ty,3)+C(B,2)-4*q+2 - (C(ty-1,3)+C(ty-5,2)+Bn)) == 0
assert s.simplify(C(B,2)-C(A+1,2)+2-4*q - (Bn-An-A-1-4*q)) == 0

def constants(pair, R):
    aa, bb = {4: pair[0]}, {4: pair[1]}
    for rank in range(4,R):
        aa[rank+1]=C(aa[rank],2)-(20*rank-49)
        bb[rank+1]=C(bb[rank],2)-(20*rank-52)
    return aa,bb

menu=[(25,58),(30,70),(40,90),(100,140)]
R=10
threshold=0
for pair in menu:
    aa,bb=constants(pair,R+1)
    assert all(v>=0 for v in aa.values()) and all(v>=0 for v in bb.values())
    for rank in range(4,R+1):
        threshold=max(threshold,aa[rank]+5*rank,bb[rank]+5*rank)
        constant=bb[rank+1]-aa[rank+1]-aa[rank]-1
        threshold=max(threshold,constant//4+1)

test_q=threshold+2
for pair in menu:
    aa,bb=constants(pair,R+1)
    for rank in range(4,R+1):
        assert bb[rank+1]-aa[rank+1]-aa[rank]-1-4*test_q < 0
        assert test_q-(5*rank-15)>aa[rank]
        assert test_q-(5*rank-16)>bb[rank]

print("finite-menu stable-tail no-go identities: PASS")
print(f"menu={len(menu)}, ranks=4..{R}, simultaneous threshold bit_length={threshold.bit_length()}")
