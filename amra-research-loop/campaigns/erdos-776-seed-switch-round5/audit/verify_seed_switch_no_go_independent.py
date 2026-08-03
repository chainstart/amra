#!/usr/bin/env python3
"""Blind algebraic audit of finite-menu and canonical one-step no-go claims."""

from math import comb
import sympy as sp


q, n, A, B = sp.symbols("q n A B", integer=True)


def cb(x, k):
    return sp.prod(x-i for i in range(k))/sp.factorial(k)


# Reconstruct the bottom Pascal transfers directly.  The affine tops are the
# last q-dependent digits in the fixed H/q staircase.
tx = q-(5*n-15)
ty = q-(5*n-16)
Anext = cb(A, 2)-(20*n-49)
Bnext = cb(B, 2)-(20*n-52)
x_transfer = (cb(tx,3)+cb(A,2)-4*q+3
              -cb(tx-1,3)-cb(tx-5,2)-Anext)
y_transfer = (cb(ty,3)+cb(B,2)-4*q+2
              -cb(ty-1,3)-cb(ty-5,2)-Bnext)
assert sp.expand(x_transfer) == 0
assert sp.expand(y_transfer) == 0

# Independently reconstruct aligned surplus cancellation for several generic
# ranks.  This is a guard on the full word, not merely the author's bottom
# recurrence formula.
H = sp.symbols("H", integer=True)


def stable_words(rank):
    x = [(H,rank),(q-1,rank-1)]
    y = [(H+1,rank),(q,rank-1)]
    x += [(q-(1+5*((rank-1)-k)),k) for k in range(rank-2,2,-1)]
    y += [(q-5*((rank-1)-k),k) for k in range(rank-2,2,-1)]
    x += [(q-(5*rank-15),2),(A,1)]
    y += [(q-(5*rank-16),2),(B,1)]
    return x,y


def val(word):
    return sum(cb(t,k) for t,k in word)


def upper(word):
    return sum(cb(t,k+1) for t,k in word)


for rank in range(4,10):
    xw,yw = stable_words(rank)
    gamma = sp.expand(upper(yw)-upper(xw)-val(xw)-(4*q-2))
    claimed = sp.expand(cb(B,2)-cb(A+1,2)+2-4*q)
    assert sp.expand(gamma-claimed) == 0

# Pointwise q-dependent one-step obstruction.  A canonical lower digit has
# A>=0, so C(A+1,2)>=0.  The strict next-word order is
# Bnext < q-(5n-11).
canonical_bound = sp.expand((q-(5*n-11))+(20*n-52)+2-4*q)
assert canonical_bound == -3*q+15*n-39
assert sp.expand(canonical_bound.subs(q,5*n-13)) == 0

# Every actual K4,r9 odd strip has q>=q_3=300, so the pointwise hypothesis is
# automatic at every pre-rank-42 step n<=42.
def q_of(j):
    h = 112*2**(j-1)
    return (2*h+4)//3


assert q_of(3) == 300
assert 300 >= 5*42-13
assert all(q_of(j+2) == 4*q_of(j)-4 for j in range(3,25,2))

# A finite-profile cross-check.  The theorem uses only finiteness: for each
# menu/rank profile the constant part is fixed, and one maximum handles all.
profiles = {
    "base": {4:(25,58),5:(269,1625),6:(35995,1319452)},
    "reset_a": {4:(30,70),5:(400,1900),6:(50000,1400000)},
    "reset_b": {4:(40,90),5:(600,2100),6:(70000,1600000)},
}
threshold = 0
for profile in profiles.values():
    for rank,(aa,bb) in profile.items():
        constant = comb(bb,2)-comb(aa+1,2)+2
        threshold = max(threshold, constant//4+1, aa+5*rank, bb+5*rank)
test_q = threshold+1
for profile in profiles.values():
    for rank,(aa,bb) in profile.items():
        assert comb(bb,2)-comb(aa+1,2)+2-4*test_q < 0
        assert test_q-(5*rank-15) > aa
        assert test_q-(5*rank-16) > bb

print("PASS: independent seed-switch no-go audit")
print("stable-word surplus reconstructed for generic ranks 4..9")
print("pointwise q-dependent lower-tail reset bound: gamma < -3q+15n-39")
print("actual pre-rank42 condition: q>=300>=197")
print("finite-profile simultaneous threshold bit_length", threshold.bit_length())
