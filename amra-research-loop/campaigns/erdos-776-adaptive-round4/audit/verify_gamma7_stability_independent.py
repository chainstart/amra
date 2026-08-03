#!/usr/bin/env python3
"""Independent Macaulay audit of the proposed K4,r9 gamma7 stable family."""

from math import comb
import sympy as sp


def C(n, k): return comb(n, k) if n >= k else 0


def canonical(value, rank):
    remainder = value
    ceiling = None
    out = []
    for lower in range(rank, 0, -1):
        if not remainder: break
        lo = lower-1
        hi = ceiling if ceiling is not None else max(2,lower+1)
        if ceiling is None:
            while C(hi,lower) <= remainder: hi *= 2
        while lo+1 < hi:
            mid = (lo+hi)//2
            if C(mid,lower) <= remainder: lo = mid
            else: hi = mid
        if lo >= lower:
            out.append((lo,lower))
            remainder -= C(lo,lower)
            ceiling = lo
    assert remainder == 0
    return tuple(out)


def upper(value, rank):
    return sum(C(top,lower+1) for top,lower in canonical(value,rank))


def family(j):
    assert j >= 3 and j % 2
    h = 112*2**(j-1)
    q = (2*h+4)//3
    b = q+4
    n = C(q,2)+9
    H = C(b,2)+1
    tau = H-n
    x = C(h+b-2,3)+C(b-1,2)+2-2*h
    y = C(h+b-1,3)+C(b,2)+2-2*h
    gammas = {}
    states = {}
    for rank in range(3,9):
        ux,uy = upper(x,rank),upper(y,rank)
        gammas[rank] = uy-ux-x-tau
        states[rank] = (x,y)
        x,y = ux-tau+1,uy-tau
    return q,gammas,states


q = sp.symbols('q', integer=True, positive=True)
Cb = lambda n,k: sp.prod(n-i for i in range(k))/sp.factorial(k)

# Actual normalized rank-five remainders obtained from the already stable P,V words.
A = Cb(q-6,5)+Cb(q-11,4)+Cb(q-15,3)+Cb(35995,2)-4*q+3
B = Cb(q-5,5)+Cb(q-10,4)+Cb(q-14,3)+Cb(1319452,2)-4*q+2

Aword = Cb(q-6,5)+Cb(q-11,4)+Cb(q-16,3)+Cb(q-20,2)+647801944
B_oneoff = Cb(q-5,5)+Cb(q-10,4)+Cb(q-15,3)+Cb(q-17,2)+229094347523
Bstable = Cb(q-5,5)+Cb(q-10,4)+Cb(q-15,3)+Cb(q-19,2)+870476130358
q33 = 320690891436

assert sp.factor(A-Aword) == 0
assert sp.expand(B-B_oneoff+2*(q-q33)) == 0
assert sp.factor(B-Bstable) == 0

# The genuine stable words require strict final digit ordering.
A_threshold = 647801944+20
B_threshold = 870476130358+19
assert A_threshold == 647801964
assert B_threshold == 870476130377

# Pascal cancellation from the genuine stable A/B words.
Cval = Cb(q-6,6)+Cb(q-11,5)+Cb(q-16,4)+Cb(q-20,3)+Cb(647801944,2)-4*q+3
Dval = Cb(q-5,6)+Cb(q-10,5)+Cb(q-15,4)+Cb(q-19,3)+Cb(870476130358,2)-4*q+2
Pup = Cb(q-6,5)+Cb(q-11,4)+Cb(q-15,3)+Cb(35995,2)
gamma7 = sp.factor(Dval-Cval-Pup)
stable_constant = 378864136937404017548365
assert sp.expand(gamma7-(stable_constant-4*q)) == 0

# Independently normalize the next pair of rank-six states.  The D73 word is
# another isolated canonical cell; the displayed Dstable word is exact later.
Cword = (Cb(q-6,6)+Cb(q-11,5)+Cb(q-16,4)+Cb(q-21,3)
         +Cb(q-25,2)+209823679001188505)
D_oneoff = (Cb(q-5,6)+Cb(q-10,5)+Cb(q-15,4)+Cb(q-20,3)
            +Cb(q-23,2)+26260982706816823916203)
Dstable = (Cb(q-5,6)+Cb(q-10,5)+Cb(q-15,4)+Cb(q-20,3)
           +Cb(q-24,2)+378864346761083666538815)
q73 = 352603364054266842622636

assert sp.factor(Cval-Cword) == 0
assert sp.expand(Dval-D_oneoff-(q73-q)) == 0
assert sp.factor(Dval-Dstable) == 0

C_threshold = 209823679001188505+25
D_threshold = 378864346761083666538815+24
assert C_threshold == 209823679001188530
assert D_threshold == 378864346761083666538839

gamma8 = sp.factor(
    (Cb(q-5,7)+Cb(q-10,6)+Cb(q-15,5)+Cb(q-20,4)
     +Cb(q-24,3)+Cb(378864346761083666538815,2))
    -(Cb(q-6,7)+Cb(q-11,6)+Cb(q-16,5)+Cb(q-21,4)
      +Cb(q-25,3)+Cb(209823679001188505,2))
    -(Cb(q-6,6)+Cb(q-11,5)+Cb(q-16,4)+Cb(q-20,3)
      +Cb(647801944,2))-1)
stable8_constant = 71769096623329310875999415996803170658344870942
assert sp.expand(gamma8-(stable8_constant-4*q)) == 0

claimed = q**2-42*q+26241900209700351953826

for j in (33,35,37,69,71,73,75):
    qj,gammas,_ = family(j)
    if j >= 35:
        assert qj > B_threshold
        assert gammas[7] == stable_constant-4*qj
    if j == 33:
        assert qj < B_threshold
        assert gammas[7] == claimed.subs(q,qj)
    if j == 35:
        assert gammas[7] != claimed.subs(q,qj)

q71,g71,_ = family(71)
q73,g73,_ = family(73)
assert g71[7] > 0
assert g73[7] == -1031549319279663352942179 < 0
assert family(75)[1][7] < 0

for j in (75,77,147,149):
    qj,gammas,_ = family(j)
    assert qj > D_threshold
    assert gammas[8] == stable8_constant-4*qj

q147,g147,_ = family(147)
q149,g149,_ = family(149)
assert g147[8] > 0
assert g149[8] == -34798731098715693576352603055425799524900210322 < 0

print('PASS: independent gamma7/gamma8 canonical-cell audit')
print('one-off q33 word drift: -2*(q-q33)')
print('one-off q73 word drift: q73-q')
print('true stable gamma7 = 378864136937404017548365-4q')
print('true stable gamma8 = 71769096623329310875999415996803170658344870942-4q')
print('first odd negative stable member: j=73')
print('first odd negative stable gamma8 member: j=149')
