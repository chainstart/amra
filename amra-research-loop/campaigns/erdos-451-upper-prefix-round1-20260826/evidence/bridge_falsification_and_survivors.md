# Fixed-prefix bridge falsification and survivor contract

All finite values in this note are reproduced by `work/finite_kill_tests.py`
under the OpenMath 34 GiB hard memory guard.  They are kill tests, not evidence
for extrapolating a bound to all `k`.

## Exact equivalence retained

For a prime `k<p<2k`,

\[
n\bmod p\notin\{1,\ldots,k\}
\quad\Longleftrightarrow\quad
\exists s_p\in\{0,\ldots,p-k-1\}:p\mid n+s_p.
\]

Thus the upper-bound problem is the least positive representative, after
`2k`, of the one-sided CRT box

\[
 A_k=\prod_{k<p<2k}\{0,-1,\ldots,-(p-k-1)\}.
\]

The endpoint and the sign are part of the problem.

## M01: density does not locate the representative

For moduli `(5,7,11)` and widths `(2,3,5)`, every independently translated
local interval box has exactly `30` points in the period `385`.  The anchored
box has first positive representative `19`, while local shifts `(1,0,4)` have
first positive representative `26`.  Hence exact density, including all local
widths, does not determine the first representative.  This finite example does
not refute a future theorem exploiting the common endpoint; it kills the
M01 density-only transfer.

## M02: the translated-window quantifier is wrong

At the actual `k=20` system, the exact period is `765049`.  Of its cyclic
windows of length `100`, exactly `241423` contain a survivor.  Nevertheless,
the distinguished window `(40,140]` contains none; the exact first survivor
after `40` is `550`.  Therefore

\[
 \mathbb P_x((x,x+H]\cap A_k\ne\varnothing)>0
\]

cannot be specialized to `x=2k`.  The same defect remains in a second-moment
or Paley--Zygmund statement over `x`.

## M03: proper Bonferroni lower truncation misses the rare event

Let `m` independent forbidden events each have probability `1/2`.  The exact
all-allowed probability is `2^{-m}`.  Its degree-`r` Bonferroni polynomial is

\[
 B_{m,r}=\sum_{j=0}^{r}(-1)^j {m\choose j}2^{-j}.
\]

For every odd `r<m`, `B_{m,r}<=0`.  Here is a short proof.  Put
`U_{m,r}=(-1)^r B_{m,r}`.  Pascal's identity gives

\[
 U_{m,r}=U_{m-1,r}+\tfrac12 U_{m-1,r-1}
 \qquad (r<m-1).
\]

The edge values are `U_{m,0}=1` and

\[
 B_{m,m-1}=2^{-m}-(-1)^m2^{-m},
\]

which has the sign `(-1)^{m-1}` or is zero.  Induction gives
`U_{m,r}>=0`, hence the claim.  In particular, even perfect independent
moments through any proper odd order give a nonpositive lower bound.  At
`H=exp(epsilon k)`, the uncompressed distribution level sees only
`r/m=epsilon+o(1)` orders, so the proposed bridge cannot prove the result for
arbitrarily small `epsilon`.

## M04: symmetric recurrence loses independent signs

This failure occurs inside an actual 451 modulus family.  For `k=7`, the
primes are `11,13`.  The integer `n=12` has centered residues

\[
 12\equiv +1\pmod {11},\qquad 12\equiv -1\pmod {13},
\]

and `1<11-7`, `1<13-7`.  It is therefore a valid short *symmetric*
recurrence.  But `12` fails the one-sided condition at `11`, while `-12`
fails it at `13`.  A choice between `n` and `-n` cannot repair the signs.

## M06: high-support near-zero Fourier obstruction

Let `P=product p` and let `f_p` be the indicator of the nonempty proper local
interval.  In the CRT Fourier factorization, the global character `h=1` has
local frequencies

\[
 a_p\equiv (P/p)^{-1}\pmod p.
\]

Every `a_p` is nonzero, and the Fourier coefficient of a proper interval at a
nonzero frequency is nonzero: its geometric sum cannot vanish because `p` is
prime and the interval length is strictly between `0` and `p`.  Thus `h=1`
is a genuinely full-support nonzero term.  For `1<=H<=P/2`,

\[
 \left|\sum_{n=1}^{H}e(n/P)\right|
 =\frac{|\sin(\pi H/P)|}{|\sin(\pi/P)|}
 \ge \frac{2H}{\pi}.
\]

Consequently support size alone does not make the prefix factor small: a
full-support character can carry an order-`H` geometric sum.  Taking absolute
values term by term cannot establish M06.  A future Fourier route would need a
new cancellation theorem among near-zero characters, not the proposed support
ledger.

## M07: additive energy has the density quantifier defect

Local translations of a CRT box are a global translation under CRT.  Additive
energy is translation invariant, while the first positive representative is
not; the exact `(5,7,11)` test already gives first points `19` and `26` for
equal-energy translates.  Energy alone therefore cannot supply the fixed
prefix incidence asserted by M07.  Common-endpoint information must enter as a
separate inequality; M10 retains exactly that missing possibility.

## M09: quotient-state count does not contract

For any fixed prime `p`, the coordinate `floor(n/p)` assumes at least
`floor(H/p)` distinct values for `1<=n<=H`.  Hence the complete quotient vector
has at least `floor(H/p)` states.  At `H=exp(epsilon k)` and `p<2k`, this is
`exp(epsilon k-O(log k))`, not `exp(O(m))` for
`m=pi(2k)-pi(k)=Theta(k/log k)`.  Quotient stability makes individual blocks
easy to describe, but the proposed total-state contraction is false.

## M11: absorption destroys the anchored interval structure

If `Q` is the product of absorbed primes and `n=Qt`, then at a remaining prime
`p` the allowed residues for `t` are

\[
 Q^{-1}\{0,-1,\ldots,-(p-k-1)\}\pmod p.
\]

This is an arithmetic progression of step `Q^{-1}`, not generally a unit-step
interval.  Exactly at `k=20`, absorbing `23` and `29` gives `Q=667`; modulo
`31`, `Q^{-1}=2`, and the width-`11` allowed set for `t` is

\[
 \{0,11,13,15,17,19,21,23,25,27,29\},
\]

not a cyclic interval.  M11 therefore cannot invoke an anchored-interval
theorem after absorption unless that theorem is strengthened to arbitrary
dilates.

## M12: quotient-vector compression is circular

For one coordinate, `q_p=ceil(n/p)` already has size `Theta(n/k)`, so recording
it exactly costs `log n-O(log k)` bits.  Moreover the exact first survivors at
`k=10,15,20,25,30` have as many distinct quotients as interval primes in every
tested row.  No low-complexity quotient law was found.  Without a theorem that
derives `q_p` from fewer data, the encoding pays essentially the quantity it
was meant to bound and is only the original congruence system in new notation.

## Three survivors and exact closure gaps

1. **M05, orthant geometry.**  It must prove a lattice point in the *specified*
   orthant, including positive `n`, with dimension loss at most
   `exp(O(m log log k))`.  Symmetric Minkowski is insufficient by M04.
2. **M08, ordered covering entropy.**  It must give a defined injective code or
   dual inequality using the aligned boundary phases, with total cost
   `O(m log log k)`; translation-averaged coverage is insufficient by M02.
3. **M10, anchored monotone CRT sumset.**  It must prove a least-element bound
   for the common-endpoint sumset itself.  Difference-set pigeonhole bounds are
   insufficient because they lose coordinatewise sign.

Any one bound of the form

\[
 n_k\le \exp(O(m\log\log k))
      =\exp\!\left(O\!\left(\frac{k\log\log k}{\log k}\right)\right)
      =\exp(o(k))
\]

would close the requested upper half.  No survivor currently proves this
bound.
