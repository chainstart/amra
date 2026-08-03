#!/usr/bin/env python3
"""Independent symbolic and finite audit of the high-half kernel proof."""

from fractions import Fraction
from math import comb, isqrt
import sympy as sp


def C(n, k): return comb(n, k) if n >= k else 0


def first_true(pred, lo, hi):
    while lo < hi:
        mid = (lo+hi)//2
        if pred(mid): hi = mid
        else: lo = mid+1
    return lo


def top2(x):
    n = (1+isqrt(1+8*x))//2
    while C(n+1, 2) <= x: n += 1
    while C(n, 2) > x: n -= 1
    return n


def rho(ai, ci):
    x = max(ai*ai+3*ai, C(ai+1,3)-C(ci+1,3)+1)
    r = (1+isqrt(1+8*x))//2
    while C(r,2) < x: r += 1
    return r


def D_threshold(ai, ci):
    x = C(ci+1,4)+C(ai+1,3)
    hi = max(ci+2,4)
    while C(hi,4) < x: hi *= 2
    return first_true(lambda d:C(d,4)>=x,ci+2,hi)


def A_star(ai, ci, d):
    x = C(d,3)+C(ai+1,3)-C(ci,3)
    hi = ai+2
    while C(hi,3) < x: hi *= 2
    return first_true(lambda t:C(t,3)>=x,ai+2,hi)


pairs = 0
for ai in range(3,69):
    for ci in range(max(3,(ai+1)//2),ai+1):
        pairs += 1
        B = top2(C(ai,2)+3*rho(ai,ci)+2)
        d = D_threshold(ai,ci)
        assert B >= A_star(ai,ci,d)
assert pairs == 1219

a,c,m = sp.symbols('a c m', positive=True)
C3=lambda x:x*(x-1)*(x-2)/6
E=lambda q:sp.factor(C3(c)+C3(a+4)-C3(a+1)-C3(c+q+1))
assert sp.factor(E(1).subs(c,a)-(a+1)*(a+8)/2)==0
assert sp.factor(6*E(2)-9*(a-c+1)*(a+c+2))==0

lams={3:Fraction(4,5),4:Fraction(7,10),5:Fraction(2,3),6:Fraction(3,5),7:Fraction(14,25),8:Fraction(8,15)}
for q,lam in lams.items():
    x=sp.Rational(lam.numerator,lam.denominator)*a
    margin=sp.factor(((q-1)*(x+1)*x*(x-1)-(a+1)*a*(a-1))/6)
    lower=sp.factor(E(q).subs(c,x))
    for poly in (margin,lower):
        assert poly.subs(a,69)>0
        derivative=sp.diff(poly,a)
        assert derivative.subs(a,69)>0
        # Its next derivative is positive on a>=69, so no later reversal.
        assert sp.diff(derivative,a).subs(a,69)>0
        assert sp.Poly(sp.diff(derivative,a),a).LC()>=0

assert sp.factor(6*(8*C3(m+2)-C3(2*m+2))-12*m*(m+1))==0
assert sp.factor(6*(8*C3(m+2)-C3(2*m+1))-6*m*(4*m+3))==0
assert sp.factor(6*(C3(2*m+1)-8*C3(m+1))-6*m)==0
assert sp.factor(E(9).subs({a:2*m,c:m})-((2*m)**2-62*(2*m)-464)/4)==0
assert E(9).subs({a:70,c:35})==24

print('PASS: independent high-half closure audit')
print('exact base: 1,219 pairs; q7=14/25; q9 parity verified')
