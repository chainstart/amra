# OPG-1757: an effective bound for the logarithmic gap theorem

Date: 2026-08-02

Status: **PROVED EFFECTIVE GAP BOUND; POST-FREEZE INDEPENDENT AUDIT PROMOTES
THE SAME BOUND TO AN EFFECTIVE EVENTUAL COMPLETE-TRANSPORT THRESHOLD**.

## 1. Explicit statement

The `S_gap` in `COMPLETE_LOG_LAYER_THEOREM.md` may be chosen no larger than

\[
\boxed{
557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374.
}
\tag{1}
\]

Thus, for every integer `s` at least the number in (1), and every integer

\[
31\le d<241\log s,
\]

both actual third-active transport coefficients are strictly positive.

The independently audited high-range threshold is a 42-digit integer smaller
than (1).  Together with the universal low columns and all-parameter top
bands, this makes the same number in (1) an effective upper bound for
coefficientwise positivity of both complete candidate transports.

The bound has 117 decimal digits and is intentionally crude.  Its purpose is
to make every uniform constant computable, not to approximate the true first
valid parameter.

## 2. Exact finite data

For a kernel coefficient write

\[
 c_{a,j}(s)=\ell_{a,j}s^{m_{a,j}}+
 \text{lower powers},
\]

and let `A_(a,j)` be the sum of the absolute values of all coefficients of
this polynomial.  These integers are extracted from the pinned common-base
source by `effective_gap_bound.py`.

Set

\[
 K=1000.
\tag{2}
\]

The proof treats `k<K` and `k>=K` separately.  The transport index is
`k=d+8` in the odd branch and `k=d+10` in the even branch.

## 3. Effective fixed-index bound

Let `L=2s+ell`, `r=k-j`, and

\[
 b_{a,r}=\frac{(2a)^r}{r!},
 \qquad
 Q_{r,\ell}=r(|\ell|+r).
\]

For `s>=Q_(r,ell)`, factor the binomial coefficient as

\[
 a^r\binom{2s+\ell}{r}
 =b_{a,r}s^r
 \prod_{t=0}^{r-1}\left(1+\frac{\ell-t}{2s}\right).
\tag{3}
\]

The sum of the absolute perturbations in the product is at most
`Q_(r,ell)/(2s)<=1/2`.  Therefore

\[
 \left|
 \frac{a^r\binom{2s+\ell}{r}}{b_{a,r}s^r}-1
 \right|
 \le \exp(Q_{r,\ell}/(2s))-1
 \le \frac{Q_{r,\ell}}s,
\tag{4}
\]

and the absolute ratio itself is at most `2`.

For a fixed `k`, let `D=k+H`, where `H=1` for a sufficient sum and `H=-1`
for a page sum.  The complete-channel identities prove that the coefficient
of `s^D`, denoted `L_k`, is strictly positive.  Applying (4) term by term
gives an explicit integer `E_k` such that

\[
 T_{s,k}\ge L_ks^D-E_ks^{D-1}.
\tag{5}
\]

The program computes this without rational roundoff.  Multiplication by
`k!` clears every factorial, since

\[
 k!b_{a,k-j}=(2a)^{k-j}(k)_j.
\]

For a top-degree term its contribution to the scaled error is

\[
 \{ |\ell_{a,j}|Q_{k-j,\ell}
      +2(\text{lower-coefficient }\ell^1\text{-norm})\}
 (2a)^{k-j}(k)_j;
\tag{6}
\]

for a lower-degree term it is at most twice its full coefficient
`ell^1`-norm times the same factor.  Hence

\[
 s> E_k/L_k
\tag{7}
\]

is a rigorous positivity condition.

The exact maxima for `2p-4<=k<1000` are:

| object | maximum `floor(E_k/L_k)+1` | attained at `k` | max `Q` |
|---|---:|---:|---:|
| odd sufficient | `84084178721600836612491482881224005603079639962` | 999 | 1,012,986 |
| even sufficient | `103990364851545016369295143433465885138144397960117967018` | 999 | 1,014,984 |
| odd page | number in (1) | 999 | 1,007,967 |
| even page | `559330005252417606463492302337154032928086116534685423818097225862646092302799175753733844066084675514273958813224` | 999 | 1,009,961 |

Thus (1) dominates every fixed-index requirement.

## 4. Effective growing-index bound: sufficient sums

The full `p`-base sufficient kernels are coefficientwise nonnegative for
`s>=8` (odd) and `s>=9` (even).  Their beta-zero coefficient is
`2(s-2)>=s`, so retain

\[
 P_p=s\binom Lk p^k.
\tag{8}
\]

For `s` large enough that `L-k+1>=s`, a lower-base coefficient satisfies

\[
 \frac{
 |c_{a,j}(s)|a^{k-j}\binom L{k-j}}
 {P_p}
 \le \frac{A_{a,j}}{a^j}
 k^j(a/p)^k.
\tag{9}
\]

Here the effective-height inequality `m-j<=1` removes every remaining power
of `s`.  At `K=1000`, the sum of the right side of (9) is, in exact rational
arithmetic, approximately

\[
 10^{-25.154}\quad(p=6),
 \qquad
 10^{-2.477}\quad(p=7),
\]

both below `1/2`.  For every summand the exact consecutive ratio

\[
 (a/p)(1+1/K)^j
\]

is below one.  It decreases with `k`, so the bound holds for all `k>=1000`.

## 5. Effective growing-index bound: page sums

Put `q=p-1`.  Exact shifted-positive certificates show that the entire `q`
and `p` page kernels are coefficientwise nonnegative for

\[
 s\ge50\quad(p=6),
 \qquad
 s\ge100\quad(p=7).
\]

The `q`-base beta-three coefficients are exactly

\[
8(s^2+35s-1074),
\qquad
10(s^2+49s-2178),
\]

and for `s>=100` they are at least `(p-2)s^2`.  Retain the positive term

\[
 P_q=(p-2)s^2\binom M{k-3}q^{k-3}.
\tag{10}
\]

Only bases `a<q` need an absolute bound.  For `j>=3`, binomial ratios give

\[
 \frac{\binom M{k-j}}{\binom M{k-3}}
 \le(k/s)^{j-3};
\tag{11}
\]

for `j=2`, the ratio is at most `2s/(k-2)`.  If

\[
 \delta=j-m-1\ge0,
\]

the remaining scale factor is `s^(-delta)`.  Since
`k-(2p-4)=d<241 log s` and
`exp(1/241)>1+1/241=242/241`,

\[
 s^{-\delta}
 <(242/241)^{\delta(2p-4)}
   (241/242)^{\delta k}.
\tag{12}
\]

Equations (10)--(12) turn every error into `C k^u rho^k`, or into
`C rho^k/(k-2)`, with explicit rational `C` and `rho<1`.  At `K=1000` their
exact sums are approximately

\[
10^{-67.668}\quad(p=6),
\qquad
10^{-42.472}\quad(p=7),
\]

again below `1/2`.  The verifier checks the exact consecutive ratios at
`K`; they decrease thereafter.  Hence the lower bases cannot cancel (10).

## 6. Geometry threshold and conclusion

For `s>=242^2=58564`, use `log s<=sqrt(s)`.  Writing `t=sqrt(s)>=242`,

\[
 t^2-241t\ge242,
\]

so `k<241 log s+10` lies far enough below both common exponents that every
binomial-ratio denominator used above is at least `s`.  The number in (1)
dominates `58564`, `100`, and every binomial-error threshold.

Thus:

- `k<1000` is covered by (5)--(7);
- `k>=1000` is covered by Sections 4--5;
- both page remainders and both sufficient kernels are strictly positive;
- the old exact lower-bound implications give the actual coefficients.

This proves the logarithmic-gap assertion in (1).  The independently
effectivized complementary high range, recorded in
`HIGH_RANGE_CROSS_AUDIT_BY_ERDOS776.md`, then gives complete eventual
transport positivity for every integer `s` at least (1).

## 7. Verification and firewall

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 effective_gap_bound.py
```

The script uses exact integers and `fractions.Fraction` for every decisive
comparison.  Decimal logarithms in its output are summaries only.

The high-range promotion is checked by
`cross_audit_high_range_by_erdos776.py`; the audit report and verifier have
SHA-256 hashes
`c5c99cf29ffb500f76fbc8b02300d53bb604e7130666c759429685839fd63a32`
and `bf982323a57370440cab9fad55643267b5f06709325425dbaebe2fa2f27fb0a8`,
respectively.  Thus the explicit number is now also an effective upper bound
for the complete eventual transports.  Universal finite-`s` transports and
OPG-1757 remain **OPEN**.
