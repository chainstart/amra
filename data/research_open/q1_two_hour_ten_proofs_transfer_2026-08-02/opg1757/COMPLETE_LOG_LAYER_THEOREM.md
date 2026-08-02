# OPG-1757: complete-channel closure of the logarithmic layer

Date: 2026-08-02

Status: **PROVED EFFECTIVE EVENTUAL GAP THEOREM AND EFFECTIVE EVENTUAL
COMPLETE THIRD-ACTIVE TRANSPORTS; UNIVERSAL TRANSPORTS AND OPG-1757 REMAIN
OPEN**.

## 1. The new theorem

Let

\[
 R_s^{\rm o}=H_{s+1}^{\rm o}-(s+6z)^2H_s^{\rm o},
 \qquad
 R_s^{\rm e}=H_{s+1}^{\rm e}-(s+7z)^2H_s^{\rm e}.
\tag{1}
\]

There is an absolute integer `S_gap` such that, for every `s>=S_gap`,

\[
 \boxed{
 [z^d]R_s^{\rm o}>0,\qquad [z^d]R_s^{\rm e}>0
 \quad(31\le d<241\log s).
 }
\tag{2}
\]

The upper limit may be intersected with the natural supports, but this is
automatic for all sufficiently large `s`.  The companion
`EFFECTIVE_GAP_BOUND.md` gives a rigorous 117-digit upper bound for
`S_gap`.  Combining (2) with the old
universal columns `0<=d<=30`, the old theorem for `d>=241 log s`, and the old
top bands yields:

> **Effective eventual complete-transport corollary.**  The same 117-digit
> upper bound for `S_gap` may be used as `S_transport`: both polynomials in
> (1) are coefficientwise strictly positive for every integer
> `s>=S_transport`.

The post-freeze independent audit `HIGH_RANGE_CROSS_AUDIT_BY_ERDOS776.md`
makes the old high-range constant explicit and proves that its 42-digit
threshold is smaller than `S_gap`.  This does not classify all finite `s`,
so it is not a universal transport theorem.

## 2. Exact input

Write `u_a=1+a beta`.  The old exact decompositions are

\[
 W_{p,s}=\sum_{a=2}^p u_a^{L_s}C_{p,a,s}(\beta),
 \qquad p\in\{6,7\},
\tag{3}
\]

for the odd/even sufficient kernels, with `L_s=2s-15` for `p=6` and
`L_s=2s-17` for `p=7`, and

\[
 Q_{p,s}=\beta^{2p-4}D_{p,s}
 =\sum_{a=2}^p u_a^{M_s}G_{p,a,s}(\beta),
\tag{4}
\]

for the page remainders, with `M_s=2s-14` for `p=6` and `M_s=2s-16`
for `p=7`.  A kernel monomial

\[
 c\,s^m\beta^j
\tag{5}
\]

has **effective height** `h=m-j` in the regime `k=O(log s)`.  This is the
normalization lost by the previous absolute-value bound.

The verifier extracts the following exact top-height data.

### Sufficient kernels

For every `2<=a<=p`, the maximum height is `1`.  Put `r=p-a`.  Its complete
height-one part is

\[
 2(-1)^r\binom{p-2}{r}
 \sum_{j=0}^{2r}\binom{2r}{j}s^{j+1}\beta^j.
\tag{6}
\]

Every omitted monomial has height at most `0`.

### Page remainders

For `2<=a<p`, put `r=p-1-a`.  The maximum height is `-1`, and its complete
height-minus-one part is

\[
 2(p-2)(-1)^r\binom{p-3}{r}
 \sum_{j=2}^{2r+3}\binom{2r+1}{j-2}s^{j-1}\beta^j.
\tag{7}
\]

Every omitted monomial in these bases has height at most `-2`.  The `a=p`
base has maximum height `-2`; its unique top monomial is

\[
 36\beta^2\quad(p=6),\qquad 50\beta^2\quad(p=7),
\tag{8}
\]

and every omitted `a=p` monomial has height at most `-3`.

Equations (6)--(8) are exact identities in the frozen common-base kernels,
not fitted asymptotics.

## 3. Coefficient scaling lemma

Let `L=2s+ell`, where `ell` is fixed, and let `k=O(log s)`.  For fixed
`a>0`, `j`, and a coefficient `c s^m+O(s^(m-1))`,

\[
\begin{aligned}
 &[\beta^k](1+a\beta)^L
   (c s^m\beta^j+O(s^{m-1})\beta^j)\\
 &\quad=\binom Lk a^k s^{m-j}
 \left(\frac{c}{(2a)^j}(k)_j+o(k^j)\right),
\end{aligned}
\tag{9}
\]

when `k` tends to infinity.  Here `(k)_j=k(k-1)...(k-j+1)`.  The identity

\[
 \frac{\binom L{k-j}}{\binom Lk}
 =\frac{(k)_j}{(L-k+1)(L-k+2)\cdots(L-k+j)}
\tag{10}
\]

proves (9), uniformly for `k=O(log s)`.  A one-unit height loss costs
`s^(-1)` times a fixed power of `k`, hence is `o(1)` in this range.

If `k` is fixed instead, the coefficient in (3) or (4) is an exact polynomial
in `s`; its leading coefficient is obtained by replacing every
`binom(2s+ell,k-j)` with `2^(k-j)s^(k-j)/(k-j)!`.

## 4. Bounded-index chamber: a positive complete-channel certificate

Introduce formal variables `x,y`.  Summing **all** top-height terms in (6)
over the bases gives the exact finite identity

\[
 \sum_{a=2}^p\sum_j c_{p,a,j}x^jy^a
 =2y^2\{y-(1+x)^2\}^{p-2}.
\tag{11}
\]

After `y=e^(2x)`, the leading fixed-`k` coefficient is therefore

\[
 [x^k]\,2e^{4x}
 \{e^{2x}-(1+x)^2\}^{p-2}.
\tag{12}
\]

Similarly, the complete lower-base height-minus-one part (7) satisfies

\[
 \sum_{a=2}^{p-1}\sum_j g_{p,a,j}x^jy^a
 =2(p-2)x^2(1+x)y^2
 \{y-(1+x)^2\}^{p-3},
\tag{13}
\]

so the leading fixed-`k` page coefficient is

\[
 [x^k]\,2(p-2)x^2(1+x)e^{4x}
 \{e^{2x}-(1+x)^2\}^{p-3}.
\tag{14}
\]

The core series has the transparent coefficient certificate

\[
 e^{2x}-(1+x)^2
 =x^2+\sum_{n\ge3}\frac{2^n}{n!}x^n,
\tag{15}
\]

so (12) and (14) are strictly positive at every degree
`k>=2p-4`.  The transport indices are exactly `k=d+8` for `p=6` and
`k=d+10` for `p=7`, hence this condition is `d>=0` in both branches.

Consequently, for every fixed transport column, both the sufficient kernel
and page remainder are eventually positive.  This is an exact
complete-channel certificate: several individual bases in (6) and (7) have
negative top terms, but their assembled leading coefficient is positive.

## 5. Growing-index chambers and their positive transition

Suppose now that `k->infinity` while `k=O(log s)`.

For a sufficient kernel, the `a=p` height-one term `2s` dominates.  Indeed,
the largest top term from a lower base `a<p`, divided by the `p` term, is

\[
 O\!\left(k^{2(p-a)}(a/p)^k\right)=o(1),
\tag{16}
\]

and every lower-height term has an additional `s^(-1)poly(k)` loss.  Thus the
sufficient coefficient is asymptotic to

\[
 A_p=2s\binom{L_s}{k}p^k>0.
\tag{17}
\]

For a page remainder, let `q=p-1`.  There are two possibly comparable positive
terms:

\[
 A_q=2(p-2)s^2\binom{M_s}{k-3}q^{k-3}>0,
\tag{18}
\]

from the maximum-shift term of (7), and

\[
 A_p=c_p\binom{M_s}{k-2}p^{k-2}>0,
 \qquad(c_6,c_7)=(36,50),
\tag{19}
\]

from (8).  All other `q`-base terms are `o(A_q)`, all `p`-base errors are
`o(A_p)`, and every `a<q` base is
`O(poly(k)(a/q)^k)A_q=o(A_q)`.  Therefore

\[
 [\beta^k]Q_{p,s}=A_q(1+o(1))+A_p(1+o(1))>0.
\tag{20}
\]

This covers all three scale chambers at once.  More explicitly,

\[
 \frac{A_5}{A_6}\sim \frac4{125}\,sk(5/6)^k,
 \qquad
 \frac{A_6}{A_7}\sim \frac{49}{2160}\,sk(6/7)^k.
\tag{21}
\]

Below the transition, the `p-1` base dominates positively; above it, the `p`
base dominates positively; at the transition both terms add with positive
sign.  At first order the two transition slopes are

\[
 \frac1{\log(6/5)}\approx5.4848,
 \qquad
 \frac1{\log(7/6)}\approx6.4872,
\tag{22}
\]

not the old coarse absolute-value constant `241`.

## 6. Uniformity and proof of (2)

It remains to justify that the preceding alternatives are uniform over the
whole moving interval.  First apply the argument to the four certificate
sums separately.  If any one of them lacked a uniform threshold, there would
be `s_n->infinity` and offending indices

\[
 31\le d_n<241\log s_n.
\]

Put `k_n=d_n+8` or `d_n+10`.  After passing to a subsequence, either:

1. `k_n` is constant, contradicting the positive fixed-index leading
   coefficients (12), (14); or
2. `k_n->infinity`, contradicting (17), (20).

This sequential contradiction gives one threshold for each certificate sum;
the maximum of the four thresholds is a single threshold for all four sums.
Equivalently, if one starts from a hypothetical sequence of nonpositive
actual transport coefficients, the old lower-bound implication says that at
least one of the four certificate conditions fails at every index, and a
finite-pigeonhole subsequence fixes which condition fails.  The same
contradiction applies.  Finally enlarge the threshold until
`241 log s<2s-14`, so all degrees under discussion lie in both natural bulk
ranges.  The old sufficient-kernel inequalities then turn simultaneous
positivity of (3)--(4) into positivity of the actual transport coefficients,
proving (2).

## 7. Executable evidence and firewall

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_complete_log_layer.py
```

The verifier:

- pins the old exact decomposition by SHA-256;
- extracts every `(base,beta-shift,s-degree,coefficient)` monomial;
- checks (6)--(8) and the strict one-height gap for all omitted terms;
- checks the exact bivariate identities (11), (13);
- checks 65 positive fixed-index leading coefficients per object; and
- performs a separately labelled finite corroborating scan.

The effective high-range promotion is independently reconstructed by

```bash
PYTHONDONTWRITEBYTECODE=1 python3 cross_audit_high_range_by_erdos776.py
```

The audit report and verifier have SHA-256 hashes
`c5c99cf29ffb500f76fbc8b02300d53bb604e7130666c759429685839fd63a32`
and `bf982323a57370440cab9fad55643267b5f06709325425dbaebe2fa2f27fb0a8`,
respectively.  They recover the four exact rational constants, the 42-digit
high-range maximum, retained-index legality, and the bulk/top splice.

The scan is not used to prove the theorem.  Conversely, (2) and its corollary
are eventual proofs, not finite scans and not universal all-parameter claims.
The complete transports for every finite `s`, the full third-active row for
every `s`, later active rows, arbitrary-host transfer, and the original
OPG-1757 proposition all remain **OPEN**.
