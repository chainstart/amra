# OPG-1757: logarithmic localization of the third-active transport gap

Date: 2026-08-02

Status: **PROVED ASYMPTOTIC LOG-BOUNDARY THEOREM; COMPLETE TRANSPORTS OPEN**.

## 1. Theorem

Let

\[
 R_s^{\rm o}=H_{s+1}^{\rm o}-(s+6z)^2H_s^{\rm o},
 \qquad
 R_s^{\rm e}=H_{s+1}^{\rm e}-(s+7z)^2H_s^{\rm e}.
\tag{1}
\]

There is an absolute integer `S` such that, for every `s>=S`,

\[
 \boxed{
 [z^d]R_s^{\rm o}>0,
 \quad
 [z^d]R_s^{\rm e}>0
 \qquad
 (241\log s\le d\le 2s-4),
 }
\tag{2}
\]

where `log` is the natural logarithm and `d` is integral.  The threshold
`S` is not made effective here.  In particular, for `s>=S`, after
combining (2) with the 31 universal low columns already proved, the only
unproved coefficients of either candidate transport lie in

\[
 \boxed{31\le d<241\log s.}
\tag{3}
\]

Thus, for every `s>=S`, the previously isolated high mesoscopic layer is
completely removed: only a logarithmically growing low boundary layer
remains.  Equation (3) does not assert that any coefficient in that layer
is negative.  The existential theorem does not separately classify the
finite parameters below `S` (apart from those already covered by the exact
low/top splice), so (3) is an eventual, not a global finite-parameter,
frontier statement.

## 2. Four exact common-base decompositions

Put `u_a=1+a beta`.  For the sufficient kernels of
`THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md`, let

\[
 W_s^{\rm o}=12s\beta^8L_s^{\rm o},
 \qquad
 W_s^{\rm e}=60s\beta^{10}L_s^{\rm e}.
\tag{4}
\]

The exact decompositions from the interior-symbol calculation are

\[
 W_s^{\rm o}=\sum_{a=2}^6u_a^{2s-15}C_{a,s}^{\rm o},
 \qquad
 W_s^{\rm e}=\sum_{a=2}^7u_a^{2s-17}C_{a,s}^{\rm e}.
\tag{5}
\]

For the two page differences

\[
 D_{p,s}=P_{p,s+1}-u_p^2P_{p,s},
 \qquad p\in\{6,7\},
\tag{6}
\]

one has

\[
 \beta^{2p-4}D_{p,s}
 =\sum_{a=2}^pu_a^{2s-2p-2}G_{p,a,s}.
\tag{7}
\]

All `C` and `G` are fixed-degree polynomials in `beta` whose coefficients
are polynomials in `s`.  Exact collection gives the following finite data.

| object | `p` | common exponent | beta degree `q` | largest lower-base `s` degree `M` |
|---|---:|---:|---:|---:|
| odd sufficient kernel | 6 | `2s-15` | 19 | 11 |
| even sufficient kernel | 7 | `2s-17` | 23 | 13 |
| odd page difference | 6 | `2s-14` | 18 | 8 |
| even page difference | 7 | `2s-16` | 22 | 10 |

Here “lower base” means `a<p`.

## 3. Exact positivity of the dominant kernels

This argument needs more than positivity of the limiting symbols.  Exact
expansion after `s=x+8` in the odd branch and `s=x+9` in the even branch
shows that **every coefficient** of each dominant kernel

\[
 C_{6,s}^{\rm o},\quad C_{7,s}^{\rm e},\quad
 G_{6,6,s},\quad G_{7,7,s}
\tag{8}
\]

is a polynomial in `x` with nonnegative coefficients.  The four certificates
contain respectively 126, 176, 80, and 120 positive monomials; identically
zero monomials are ignored.

For the low half of a coefficient row, retain the following first positive
coefficient of the dominant kernel:

\[
 [\beta^0]C_{6,s}^{\rm o}=[\beta^0]C_{7,s}^{\rm e}=2(s-2),
\tag{9}
\]

\[
 [\beta^2]G_{6,6,s}=36,
 \qquad
 [\beta^2]G_{7,7,s}=50.
\tag{10}
\]

For the high half, retain the last coefficient, at degrees 19, 23, 18,
and 22, respectively.  Their exact factorizations are

\[
 [\beta^{19}]C_{6,s}^{\rm o}
 =120932352s(28s^6+56s^5+70s^4+56s^3+28s^2+8s+1),
\tag{11}
\]

\[
 [\beta^{23}]C_{7,s}^{\rm e}
 =27682574402s(45s^8+120s^7+210s^6+252s^5
 +210s^4+120s^3+45s^2+10s+1),
\tag{12}
\]

\[
 [\beta^{18}]G_{6,6,s}
 =20155392(2s+1)(2s^2+2s+1)
 (2s^4+4s^3+6s^2+4s+1),
\tag{13}
\]

\[
 [\beta^{22}]G_{7,7,s}
 =3954653486(2s+1)(s^4+2s^3+4s^2+3s+1)
 (5s^4+10s^3+10s^2+5s+1).
\tag{14}
\]

All retained coefficients are strictly positive on the stated parameter
ranges.  Since the other dominant-base coefficients are nonnegative, they
may be discarded in a lower bound.

## 4. Uniform dominant-base lemma

Consider any of the four sums

\[
 T_{s,k}= [\beta^k]\sum_{a=2}^p u_a^L C_{a,s}(\beta),
\tag{15}
\]

with the data in the table.  Choose the low endpoint coefficient from
(9)--(10) whenever its binomial index lies in `[0,L]`; otherwise choose the
high endpoint coefficient from (11)--(14).  On all target degrees used
below, one of these choices is legal.  In particular, in the high choice
the residual binomial index is at most `L-8` in the odd branch and at most
`L-10` in the even branch.

Let `i` be the retained dominant shift and let `j` be any shift in a lower
base `a<p`.  If its binomial coefficient is nonzero, then

\[
 \frac{
  |[\beta^j]C_{a,s}|a^{k-j}\binom L{k-j}}
  { [\beta^i]C_{p,s}p^{k-i}\binom L{k-i}}
 \le C s^{M+q}\left(\frac{p-1}{p}\right)^k.
\tag{16}
\]

Indeed, the lower coefficient is `O(s^M)`, the retained positive
coefficient is bounded below by a positive constant, and

\[
 \frac{\binom L{k-j}}{\binom L{k-i}}\le(L+1)^{|i-j|}
 \le(L+1)^q.
\tag{17}
\]

All powers depending only on the fixed shifts are absorbed into `C`.
There are only finitely many lower-base monomials, so (16) also bounds
their total absolute contribution after changing `C`.

The worst polynomial budgets are

\[
 M+q\le30\quad(p=6),
 \qquad
 M+q\le36\quad(p=7).
\tag{18}
\]

The elementary lower bounds

\[
 \log(6/5)>\frac9{50},
 \qquad
 \log(7/6)>\frac{11}{72}
\tag{19}
\]

follow from `log(1+x)>x-x^2/2`.  Hence

\[
 241\log(6/5)>30,
 \qquad
 241\log(7/6)>36.
\tag{20}
\]

If `k>=d>=241 log s`, the right side of (16) tends to zero uniformly.
For all sufficiently large `s`, the sum of every lower-base absolute value
is therefore smaller than the single retained positive dominant term.
This proves strict positivity of all four sums.

## 5. Passage to the transports

For an odd bulk coefficient `d<=2s-12`, the indices in (5) and (7) are
both `k=d+8`.  For an even bulk coefficient `d<=2s-14`, they are
`k=d+10`.  The index ranges in Section 4 therefore cover every bulk
coefficient with `d>=241 log s`.  Thus the page differences (6) are
positive, making the Bernoulli scale step legal, and the sufficient kernels
(4) are positive.  The exact lower bounds of the low-column proof give

\[
 [z^d]R_s^{\rm o}>0\quad(d\le2s-12),
 \qquad
 [z^d]R_s^{\rm e}>0\quad(d\le2s-14)
\tag{21}
\]

throughout the logarithmic range.  The already proved top bands cover the
remaining degrees up to `2s-4`, proving (2).

## 6. Verification and boundary

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 third_active_transport_recurrence_attack.py
```

The verifier reconstructs all four common-base sums (including 96 direct
page-difference coefficients), checks their degree budgets, checks the four
dominant shifted-positive certificates, and records all eight retained
endpoint coefficients.  The asymptotic domination step is the uniform
inequality (16), not a finite scan.

The threshold `S` is existential, and the interval (3) is still unbounded.
Consequently neither complete transport, the universal third-active row, nor
the original OPG-1757 proposition is claimed proved.
