# Independent cross-audit of the OPG-1757 logarithmic-layer result

Date: 2026-08-02

Auditor: Erdős #776 lane

## Verdict

**PASS.**  The effective logarithmic-gap theorem and the existential
eventual complete-transport corollary survive independent reconstruction,
including their quantifiers and endpoint conventions.  No repair to the
frozen author statement is required.

This verdict is only for the stage theorem.  Universal finite-parameter
transports and the original OPG-1757 proposition remain **OPEN**.

## Independence and provenance

The audit program is `cross_audit_by_erdos776.py`.  It does not import
`verify_complete_log_layer.py`, `effective_gap_bound.py`, either author test,
or any helper from them.  Its only mathematical input is the old fixed-page
recurrence source

```text
data/research_open/q1_six_hour_campaign_2026-08-02/opg1757/
third_active_transport_recurrence_attack.py
```

whose independently recomputed SHA-256 is

```text
a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125.
```

The program expands those old formulas into raw
`(base,beta-shift,s-degree,integer coefficient)` monomials and rebuilds the
certificates from those monomials.  It does not call an author certificate
routine.  The frozen-artifact hashes in `AUTHOR_FREEZE_2120.md` were also
recomputed before the mathematical audit and matched the manifest.

## 1. Exact height spectra and complete channels

For a monomial `c s^m beta^j`, I independently recomputed the effective
height `m-j`.

For every sufficient base `2<=a<=p`, with `r=p-a`, the exact maximum-height
signature is

\[
h=1,
\qquad
(j,m,c)=\left(j,j+1,
2(-1)^r\binom{p-2}{r}\binom{2r}{j}\right),
\quad 0\le j\le 2r.
\]

For each page base `2<=a<p`, with `r=p-1-a`, it is

\[
h=-1,
\qquad
(j,m,c)=\left(j,j-1,
2(p-2)(-1)^r\binom{p-3}{r}\binom{2r+1}{j-2}\right),
\quad 2\le j\le 2r+3.
\]

At the page base `a=p`, the unique maximum-height term has height `-2` and
is `36 beta^2` for `p=6`, respectively `50 beta^2` for `p=7`.  Every omitted
term is at least one height lower.  The raw counts were:

| object | top monomials | strictly lower monomials |
|---|---:|---:|
| odd sufficient | 25 | 710 |
| even sufficient | 36 | 1222 |
| odd page | 21 | 525 |
| even page | 31 | 949 |

Summing the extracted top monomials, rather than inserting the claimed
closed forms, gives exactly

\[
2y^2\{y-(1+x)^2\}^{p-2}
\]

for a sufficient sum and

\[
2(p-2)x^2(1+x)y^2\{y-(1+x)^2\}^{p-3}
\]

for the lower-base page sum.  Direct term-by-term exponential-generating
substitution `y=e^(2x)` was also reconstructed: a term `c x^j y^a`
contributes

\[
c\frac{(2a)^{k-j}}{(k-j)!}
\]

at degree `k`.  The decisive core is

\[
e^{2x}-(1+x)^2=x^2+\sum_{n\ge3}\frac{2^n}{n!}x^n,
\]

so coefficients vanish below `2p-4` and are strictly positive at every
degree at least `2p-4`.  The first nonzero coefficients reconstructed by the
audit are, respectively,

| object | first degree | first coefficient |
|---|---:|---:|
| odd sufficient | 8 | 2 |
| even sufficient | 10 | 2 |
| odd page | 8 | 8 |
| even page | 10 | 10 |

Thus the endpoint is strict in the required direction; testing the degrees
immediately below it does not reveal a hidden boundary term.

## 2. Growing indices, the two page scales, and uniformity

For a sufficient sum with `k->infinity`, the height-one `a=p` term is
positive, and every `a<p` top term is smaller by

\[
O\!\left(k^{2(p-a)}(a/p)^k\right).
\]

Every height loss adds `s^(-1) poly(k)`.  These errors are uniformly `o(1)`
for `k=O(log s)` because the list of monomials is finite.

For a page sum, putting `q=p-1`, direct inspection of the extracted top
signatures finds exactly the two potentially comparable positive scales:

\[
A_q=2(p-2)s^2\binom{M_s}{k-3}q^{k-3},
\qquad
A_p=c_p\binom{M_s}{k-2}p^{k-2},
\]

with `(c_6,c_7)=(36,50)`.  The `q` signature has precisely shifts 2 and 3;
its shift-3 coefficient supplies `A_q`, while its shift-2 term is
`O(1/k)A_q`.  Lower-height `q` terms are `o(A_q)`.  At base `p`, the displayed
shift-2 monomial is the unique height-minus-two term and all its errors are
`o(A_p)`.  Every `a<q` base is

\[
O(poly(k)(a/q)^k)A_q=o(A_q).
\]

The errors are therefore grouped independently as `o(A_q)` and `o(A_p)`;
no lower or upper bound on `A_q/A_p` is used.  This validates

\[
A_q(1+o(1))+A_p(1+o(1))>0
\]

also at the transition, not only on either side of it.

The coefficient-scaling identity is uniform in the entire interval because
`k<=241 log s+10`: the finite collection of shifts is fixed, every
one-height loss is bounded by `s^(-1)poly(log s)=o(1)`, and every lower-base
ratio is an exponential in `k` times a fixed polynomial.  The hostile
subsequence check is complete: a bounded sequence of integer indices has a
constant subsequence, while an unbounded one has a subsequence tending to
infinity.  The first invokes the complete-channel leading coefficient and
the second invokes the growing-index estimate.

This argument is applied to four separate certificate sums.  Taking the
maximum of their four eventual thresholds is legitimate.  Equivalently, a
hypothetical sequence of failing actual coefficients selects at least one
failed certificate at each index; finite pigeonhole fixes one certificate on
a subsequence, contradicting its uniform threshold.  There is no illicit
interchange of four independent `o(1)` statements.

I also checked the old implication back to the transports.  Page positivity
licenses the Bernoulli scale step, and strict sufficient-kernel positivity
then gives strict positivity of the actual coefficients.  The lower-bound
domains are `d<=2s-12` in the odd branch and `d<=2s-14` in the even branch;
the new `d<241 log s` interval lies in both for all sufficiently large `s`.

## 3. Effective fixed-index reconstruction

For `r=k-j`, `L=2s+ell`, and

\[
Q=r(|\ell|+r),
\]

the product perturbations in

\[
a^r\binom{2s+\ell}{r}
=\frac{(2a)^r}{r!}s^r
\prod_{t=0}^{r-1}\left(1+\frac{\ell-t}{2s}\right)
\]

have total absolute size at most `Q/(2s)`.  For `s>=Q`, the standard product
bound gives

\[
\left|\prod(1+x_t)-1\right|
\le e^{\sum|x_t|}-1\le Q/s,
\]

and the product itself has absolute value at most 2.  Reversing the final
inequality would be invalid; the proof uses it only as an upper error bound.

Multiplication by `k!` was independently checked to give

\[
k!\frac{(2a)^{k-j}}{(k-j)!}
=(2a)^{k-j}(k)_j.
\]

For every `2p-4<=k<1000`, I then rebuilt the signed leading sum `L_k`, the
absolute error majorant `E_k`, and the strict integer threshold
`floor(E_k/L_k)+1`.  The four maxima are:

| object | maximum threshold | `k` | max `Q` |
|---|---:|---:|---:|
| odd sufficient | `84084178721600836612491482881224005603079639962` | 999 | 1,012,986 |
| even sufficient | `103990364851545016369295143433465885138144397960117967018` | 999 | 1,014,984 |
| odd page | `557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374` | 999 | 1,007,967 |
| even page | `559330005252417606463492302337154032928086116534685423818097225862646092302799175753733844066084675514273958813224` | 999 | 1,009,961 |

The odd-page value is the maximum, is attained at `k=999`, and has exactly
117 decimal digits.  It dominates all four `Q` requirements as well.

## 4. Effective growing-index and geometry checks

After shifting `s` by the claimed starts, every coefficient in each of the
six retained dominant kernels is nonnegative: the two sufficient `p`
kernels at starts 8 and 9, and the page `(q,p)` kernels at starts `(50,8)`
and `(100,9)`.  The page `q` beta-three coefficients reconstructed directly
are

\[
8(s^2+35s-1074),
\qquad
10(s^2+49s-2178),
\]

and have the required lower bounds from `s>=100`.

For all discarded bases, the audit rebuilt the growing majorants at
`K=1000` with `fractions.Fraction`.  The exact sums are below `1/2`, and the
exact consecutive ratio of every summand is below 1 at `K` and decreases
thereafter.  Their decimal logarithms, used only as readable summaries, are:

| object | `log10` of exact sum | bounded monomials |
|---|---:|---:|
| odd sufficient | -25.153920 | 80 |
| even sufficient | -2.477331 | 120 |
| odd page | -67.668217 | 51 |
| even page | -42.472415 | 84 |

For page shift `j=2`, the exceptional binomial ratio is bounded by
`2s/(k-2)`; for `j>=3`, it is bounded by `(k/s)^(j-3)`.  With
`delta=j-m-1>=0`, the direction of the logarithmic replacement is also
correct:

\[
s^{-\delta}
<(242/241)^{\delta(2p-4)}(241/242)^{\delta k},
\]

because `k-(2p-4)<241 log s` and
`exp(1/241)>242/241`.

Finally, `s>=242^2=58564` gives, with `t=sqrt(s)>=242`,

\[
t^2-241t\ge242,
\]

with equality at `t=242`.  This is more than the fixed additive loss needed
to make every binomial denominator at least `s`.  The 117-digit threshold
dominates this geometry threshold and all shifted-positivity starts.

## 5. Integer splice and firewall

Let `x=241 log s`.  The three integer regions are

1. `0<=d<=30`;
2. `31<=d<x`;
3. `x<=d<=2s-4`.

For integral `d`, the second region ends at `ceil(x)-1`, and every remaining
integer at least 31 is at least `x`; if `x` itself is integral, equality is
included in the third region.  Hence there is no integer endpoint gap.  The
old bulk ranges and top bands splice contiguously at `2s-12/2s-11` in the
odd branch and `2s-14/2s-13` in the even branch.

The following boundaries are essential to the verdict:

- finite stress scans are corroboration only;
- the 117-digit number is an effective threshold only for the new low
  logarithmic gap;
- the old `d>=241 log s` threshold is still ineffective, so the combined
  eventual complete-transport threshold is existential, not effective;
- eventual positivity is not positivity for every stable finite `s`;
- neither the transport stage theorem nor this audit proves the original
  OPG-1757 proposition.

## Reproduction

From the repository root, run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/opg1757/\
cross_audit_by_erdos776.py
```

The independent run terminates with

```text
INDEPENDENT OPG1757 CROSS-AUDIT: PASS
S_gap_digits 117
```
