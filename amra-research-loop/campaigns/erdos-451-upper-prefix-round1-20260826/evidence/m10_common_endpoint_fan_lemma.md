# M10 round 1 deepening: a block-global seed and a coherent fan

## Status and coordinate

This note continues the M10 round-1 checkpoint in the anchored coordinate

\[
 {\cal A}_S=\{s:\ 0\le s\bmod p<p-k\quad(p\in S)\}.       \tag{1}
\]

Every result through Section 4 is an unconditional finite-dimensional
theorem.  No prime-distribution conjecture is used.  Section 5 gives the
exponent ledger and the exact handoff that remains open.  The results do not
prove a new upper bound for Erdos 451.

## 1. A macroscopic block has a common distinguished seed

Let `S` be any nonempty set of integers in `(k,2k)`, and put

\[
 L=\min S,\qquad P=\max S,\qquad D=P-L,\qquad B=L-k.             \tag{2}
\]

> **Common-endpoint block theorem.**  If `D<B`, then `s=P` lies in
> `cal A_S`.  In fact the whole integer interval
> \[
>                    [P,\,P+B-D-1]                              \tag{3}
> \]
> lies in `cal A_S`.

Indeed, write `s=P+h` with `0<=h<B-D`.  For every `q in S`,

\[
 0\le P-q+h\le D+h<B\le q-k<q,                                 \tag{4}
\]

so `s mod q=P-q+h` is in the required anchored interval.  This is a
distinguished-start statement, not a translate-average or a maximum-gap
statement.

There are two useful exact consequences.

1. If `S` is the set of primes in `(3k/2,2k)`, then `D<k/2<B`, so
   its distinguished `s`-successor is at most its largest prime `P<2k`
   (and the corresponding 451 variable is `n=P+k+1`).
2. More generally, every dyadic offset band
   \[
       S_j=\{p:\ k+k/2^{j+1}<p<k+k/2^j\}                       \tag{5}
   \]
   has its largest member as a simultaneous anchored seed.  Thus the full
   451 system is a union of only `O(log k)` blocks, each of which separately
   has a seed below `2k`.

The first consequence is already exponent-level.  By the prime number
theorem, the block `(3k/2,2k)` has `(1/2+o(1))k/log k` coordinates, and its
reciprocal density is

\[
 \begin{split}
 \prod_{3k/2<p<2k}{p\over p-k}
 &=\exp\left(\left(\int_{3/2}^{2}\log{t\over t-1}\,dt+o(1)\right)
                    {k\over\log k}\right)\\
 &=\exp\left(\left({3\over2}\log{4\over3}+o(1)\right)
                    {k\over\log k}\right).                    \tag{6}
 \end{split}
\]

Nevertheless (3) gives a seed at scale `O(k)`.  Hence common-endpoint
alignment really can save an entire `exp(Theta(k/log k))` density payment
for a macroscopic block.  The unresolved issue is preserving that alignment
when different offset blocks are merged.

## 2. The exact coherent fan

The preceding seed extends to a triangular family.  Suppose `D>0` and set

\[
             T=\left\lfloor {B-1\over D}\right\rfloor.          \tag{7}
\]

> **Coherent fan lemma.**  For every `1<=t<=T`, the interval
> \[
 I_t=[tP,\,tP+B-tD-1]                                           \tag{8}
> \]
> is contained in `cal A_S`.  The intervals are disjoint, and therefore
> the prefix ending at `TP+B` contains at least
> \[
 N_{\rm fan}=\sum_{t=1}^{T}(B-tD)
             =TB-{D T(T+1)\over2}                               \tag{9}
> \]
> simultaneous seeds.

For `s=tP+h in I_t` and `q in S`,

\[
 s\bmod q=t(P-q)+h\le tD+h<B\le q-k.                           \tag{10}
\]

The displayed quantity is below `q`, so (10) is the ordinary residue and
proves the claim.  Disjointness follows because each fan interval has length
less than `B<L<P`.

For example, if `B>=2D`, then the first
`N_0=floor(B/(2D))` fan intervals all have length at least `B/2`, and

\[
       N_{\rm fan}\ge {B^2\over 8D}.                             \tag{11}
\]

This is a genuine two-parameter invariant: it retains both an endpoint and
a number of seeds.  For a macroscopic band (`B,D asymp k`) it supplies only
`Theta(k)` displayed seeds, even though the reciprocal density can be
`exp(Theta(k/log k))`.  This last comparison is only a limitation of the
explicit fan; it is not an upper bound on all seeds of `cal A_S`.

## 3. A carry-sensitive one-coordinate merge

The fan can absorb one further coordinate without taking a density average.
Let `r in (k,P)` be outside `S`, put `c=r-k`, and choose an integer
`1<=N<=T`.  Define

\[
                     w=B-ND.                                   \tag{12}
\]

> **Fan--Dirichlet merge lemma.**  If
> \[
                  \min(c,w)>{r\over N+1},                       \tag{13}
> \]
> then there is an `s<=NP+B` in `cal A_(S union {r})`.

By the one-dimensional Dirichlet pigeonhole lemma, some `1<=t<=N`
satisfies

\[
 \left\|{t(P-r)\over r}\right\|\le {1\over N+1}.               \tag{14}
\]

Let `u=t(P-r) mod r` in `[0,r-1]`.  If `u<=r/2`, then (13)--(14)
give `u<c`, so `s=tP` works.  If `u>r/2`, put `h=r-u`.  Then
`0<h<w<=B-tD`, and `(tP+h) mod r=0`; (8) handles every old coordinate.

When `B>=2D`, take `N=floor(B/(2D))`.  Since `N+1>B/(2D)`, the convenient
sufficient condition

\[
                 \min(c,B/2)>{2rD\over B}                       \tag{15}
\]

implies (13).  Thus a narrow coherent block can absorb one lower prime in a
prefix of polynomial length.  What is retained here and absent from a
phase-blind energy bound is the actual carry `t(P-r)`.

## 4. Simultaneous merge and its exact exponent

There is also a multi-coordinate version.  Let `r_1,...,r_h` be new
pairwise coprime moduli in `(k,P)`, put `c_i=r_i-k`, and let
`R=max_i r_i`, `c=min_i c_i`.  Keep `N,w` as in (12).

> **Centered fan merge lemma.**  If an integer `M>=2` satisfies
> \[
>                   M^h\le N,
>       \qquad {2R\over M}<\min(c,w),                            \tag{16}
> \]
> then some `s<=NP+B` lies in `cal A_(S union {r_1,...,r_h})`.

Apply simultaneous Dirichlet approximation to the `h` numbers
`(P-r_i)/r_i`.  There is `1<=t<=M^h` such that every centered residue
`t(P-r_i) mod r_i` has distance at most `R/M` from zero.  Among coordinates
whose residue is near `r_i`, let `x` be the maximum backward distance
`r_i-u_i`; take `x=0` if there is no such coordinate.  Then `x<=R/M<w`.
For a near-`r_i` coordinate the new residue is `x-(r_i-u_i)` in
`[0,R/M]`; for a near-zero coordinate it is at most `2R/M`.  Both are below
`c<=c_i`, while `tP+x` stays in the old fan interval (8).

This gives a precise exponent rather than a qualitative many-seed claim.
With comparable macroscopic new widths, `M` can be an absolute constant and
the fan absorbs

\[
                         h\le {\log N\over\log M}.               \tag{17}
\]

For `D>=1`, the constructed fan has `N<=B/D<=k`; hence this theorem handles
only `O(log k)` arbitrary additional coordinates.  It cannot by itself
absorb the `Theta(k/log k)` primes in the full 451 system.  This is a
quantitative limitation of the proved centered-fan interface, not an
impossibility theorem for signed or one-sided block cancellation.

The common correction `x` in the proof also pinpoints the endpoint loss.
If the new allowed widths range down to `c_min`, every backward error must
be below `c_min`; a uniform centered Dirichlet argument then takes
`M at least 2R/c_min` at **every** coordinate.  For primes arbitrarily close
to `k`, this returns an `exp(Theta(k))` ledger.  Coordinate-wise error sizes
do not repair it, because a single `x` must fit inside the smallest allowed
interval.

## 5. What this proves and what it does not

The common-start geometry now gives a genuine macroscopic block theorem:
all primes in `(3k/2,2k)` cost no density factor at all at the distinguished
start.  More generally, each of the `O(log k)` dyadic offset blocks (5) has
an `O(k)` distinguished seed.  Therefore the obstruction is not solving an
individual large block.  It is the following exact phase handoff:

> Given seed families for two different dyadic offset blocks, merge them
> while retaining a polynomial loss per **block**, rather than resetting a
> quotient phase separately for every prime.

The fan lemmas do not provide this handoff.  If an old CRT seed `x` is
shifted by `tP+h`, the new residues are

\[
        x+t(P-q)+h\pmod q,                                      \tag{18}
\]

and the uncontrolled residues `x mod q` destroy (10).  Conversely, taking
the CRT product of a completed block as the shift replaces `P-q` by an
arbitrary unit phase modulo the next primes.  Thus merely iterating (8) is
not a proof.

The exponent distinction is sharp enough for planning.  A fixed polynomial
loss for each of `O(log k)` dyadic blocks would total
`exp(O((log k)^2))`, which is harmless.  A fixed polynomial loss for each of
`Theta(k/log k)` primes totals `exp(Theta(k))`, as already seen in the pair
condition-number ledger.  The next viable M10 lemma must therefore be a
translation/carry-aware **block-to-block** version of (16), or a direct
distinguished inequality that bypasses this handoff.

## 6. Audit of the pair theorem used at the checkpoint

The two delicate endpoints in the preceding checkpoint were rechecked.

1. In an empty-block run the phases lie in `[a,k]`.  Since
   `k+Delta<p` is exactly `k<q`, no step inside the run wraps modulo `p`.
   Hence the run contains at most
   `floor((k-a)/Delta)+1` phases, exactly the stated `R`.
2. The PNT supplies `(1/4+o(1))k/log k` primes in `(3k/2,7k/4)`.
   For their increasing list, the sum of consecutive gaps telescopes to
   less than `k/4`; hence one actual globally adjacent pair has
   `Delta=O(log k)`.  Both distance-to-endpoint parameters are at least
   `k/4`, so the lower witness gives `Omega(k^2/log k)` without an endpoint
   assumption.

Thus the pure `C^m` maximum-gap counterexample and the distinguished/far-gap
split remain valid.

## 7. Audit of an `L`-dimensional block-shift merger

Let the dyadic blocks be `S_1,...,S_L`, let

\[
 Q_j=\prod_{p\in S_j}p,\qquad
 A_j=\{a\bmod Q_j:a\bmod p\in[0,p-k-1]\ (p\in S_j)\}.           \tag{19}
\]

The `Q_j` are pairwise coprime, and CRT gives the exact identity

\[
 {\cal A}_{\cup S_j}\pmod{\prod_jQ_j}
       \longleftrightarrow \prod_{j=1}^{L}A_j.                  \tag{20}
\]

Thus only `L=O(log k)` block coordinates remain after grouping.  This fact
is useful only if each `A_j` is retained with near-full entropy.  Replacing
`A_j` by the single seed from Section 1, or even by all displayed fan seeds,
does not do so.

For example, for the top block `(3k/2,2k)`, the prime number theorem gives

\[
       \log Q_{\rm top}=(1/2+o(1))k,                            \tag{21}
\]

whereas the fan (9) has at most `k^2` displayed residues.  Periodizing only
those residues modulo `Q_top` has density at most

\[
              {k^2\over Q_{\rm top}}=\exp(-(1/2+o(1))k).        \tag{22}
\]

The true block density, by (6), is merely
`exp(-Theta(k/log k))`.  Consequently fan-only compression discards
`exp(Theta(k))` relative entropy before any `L`-dimensional lemma is applied.
An `L^{O(L)}` merger cannot repay that loss.

Likewise, selecting one successful representative `a_j in A_j` and solving
the `L` congruences `s=a_j mod Q_j` has no small-representative guarantee:
the CRT modulus in (20) is still the full product.  The small value of `L`
does not turn the exponentially large `Q_j` into affordable moduli.

This does not kill an `L`-dimensional block merger.  It identifies its
necessary input precisely: for every block one must pass forward a family
of size/density comparable to `A_j`, together with enough location or carry
information to select a small representative of (20).  The M10 fan proves
strong anchored control for one block, and the one-block orthant theorem
proves existence at density scale, but neither currently supplies that
near-full-entropy located family.  This is the surviving nested-common-
endpoint interface.

There is, however, a rigorous no-go for the most literal nested-endpoint
version.  For a fixed block and a fixed common quotient `t`, the intersection
of its local allowed intervals is **exactly**

\[
 \begin{split}
 &\bigcap_{q\in S}[tq,(t+1)q-k-1]\\
 &\hspace{25mm}=[tP,(t+1)L-k-1]=I_t.                            \tag{23}
 \end{split}
\]

Thus the fan is not merely a convenient subset: it is the whole part of the
block solution set on which every modulus has the same quotient.

Take again the top prime block `(3k/2,2k)`.  The PNT gives

\[
 L=(3/2+o(1))k,\qquad P=(2+o(1))k,\qquad B/D\longrightarrow1.   \tag{24}
\]

Consequently `T=1` for all sufficiently large `k`; its only positive
common-quotient interval is

\[
                         I_1=[P,2L-k-1],                        \tag{25}
\]

whose points all satisfy `s=(2+o(1))k`.  No such point can solve the full
451 system.  Indeed, for every `s in I_1`, the interval

\[
                         (s/2,(s+k)/2]                          \tag{26}
\]

has length `k/2` and contains a prime `r in (k,2k)` for all sufficiently
large `k`.  To avoid any uniformity shorthand, (24)--(25) show that the fixed
interval `(1.01k,1.49k)` is contained in (26) for all sufficiently large
`k`, and the PNT supplies `r` there.  Then
`s<2r<=s+k`, so the multiple `2r` lies in the forbidden window `(s,s+k]`.

Therefore a merger which insists on keeping the common quotient inside the
macroscopic top block is rigorously impossible asymptotically.  A surviving
`L`-block theorem must keep quotient changes/wraps—and hence substantially
more than the nested fan intervals—even though the first anchored seed of
the top block itself is exceptionally small.

## 8. Exact kill of anchored gap submultiplicativity

The especially attractive block interface

\[
                         G(A\cap B)\le G(A)G(B)                 \tag{27}
\]

is false even when every local coordinate is an actual 451 prime interval
`[0,p-k-1]` with one common `k`.

The first witness in the targeted search has `k=22`.  Let `A` use
the primes `(23,29)` with widths `(1,7)`, and let `B` use `(31,43)` with
widths `(9,21)`.  Exact CRT enumeration gives

\[
 \begin{array}{c|c|c|c}
 &\text{period}&\text{cardinality}&G\\ \hline
 A&667&7&115\\
 B&1333&189&85\\
 A\cap B&889111&1323&25691.
 \end{array}                                                    \tag{28}
\]

Here `25691>115*85=9775`.  The respective maximizing gaps are
`437 to 552`, `1000 to 1085`, and `508346 to 534037` (ordinary endpoints
inside the displayed periods), so the violation ratio is
`2.628235294...`.

There is also a witness in the exact sequential-dyadic scope.  For `k=88`,
let the accumulated left factor use `(89,97)`, of widths `(1,9)`, and let
the new block use `(131,173)`, of widths `(43,85)`.  The latter is one
dyadic width block because `43<=d<86`.  Exact enumeration gives

\[
       G(A)=1068,\qquad G(B)=351,\qquad
       G(A\cap B)=930139,                                      \tag{29}
\]

and

\[
             {G(A\cap B)\over G(A)G(B)}=2.481244064\ldots.      \tag{30}
\]

Thus (27) cannot be used to merge even one new actual dyadic block into an
accumulated actual anchored box.  This is a rigorous finite counterexample
to a universally quantified inequality, not an empirical extrapolation.
The deterministic enumerator constructs every CRT residue, sorts them, and
checks the cyclic terminal gap; its replay metadata and hash are recorded in
`evidence/m10_submultiplicativity_counterexample.json`.

The counterexample does **not** kill a relaxed inequality

\[
                         G(A\cap B)\le C G(A)G(B)               \tag{31}
\]

with an absolute `C`; it only forces `C>=25691/9775=2.628235294...` for the
universal actual-prime version.  Such a constant would still be affordable across
`L=O(log k)` blocks.  But there is a second, logically independent gap:
both (27) and (31) require a bound for the **maximum cyclic gap** of each
block.  The one-block orthant theorem and Section 1 prove only an anchored
successor.  The close-pair theorem shows why that distinction cannot be
silently erased.  Hence a relaxed submultiplicative theorem would close the
block interface only after a genuine single-block max-gap theorem is also
proved.

## 9. Guarded checks

The off-by-one diagnostic for Sections 2--4 exhaustively checked `8854`
small fan systems, `31486` common-quotient rows, `7865` applicable
one-coordinate merges, and `66` applicable two-coordinate merges.  Its
accepted replay was

```text
unit: openmath-task-20260826-225201-325863.scope
exit: 0
wall: 0.63s
maximum RSS: 11200 KiB
swaps: 0
script sha256: 4349eab28d62a1510437b17d86746450740691fc5c3ac0468cdf57abea93a8cc
command: /home/biostar/work/projects/openmath/bin/openmath-memory-guard -- /usr/bin/time -v python3 amra-research-loop/campaigns/erdos-451-upper-prefix-round1-20260826/work/m10_round1/fan_lemma_check.py
```

The exact submultiplicativity counterexample replay was

```text
unit: openmath-task-20260826-225802-327669.scope
exit: 0
wall: 31.89s
maximum RSS: 60092 KiB
swaps: 0
script sha256: 8e20bd915c86ea948d8eb985a418807c20a6562064162ff528e80089b82b60a2
command: /home/biostar/work/projects/openmath/bin/openmath-memory-guard -- /usr/bin/time -v python3 amra-research-loop/campaigns/erdos-451-upper-prefix-round1-20260826/work/m10_round1/anchored_block_submultiplicativity_search.py
```

Both commands were run through `openmath-memory-guard`; the finite checks
support the endpoint audits, while the written proofs establish the fan
lemmas.

## 10. The relaxed constant and the strongest unconditional correction

The exact witnesses in Section 8 do not decide whether an absolute constant
`C` exists in (31).  Gap data alone cannot prove such a statement, even for
coprime periodic systems containing zero.  Here is an unbounded abstract
family.  Let `R=2N+1`, let `A` be the even integers (period `2`), and modulo
`R` let

\[
 B=\{b\le N:b\text{ is even}\}
   \cup\{b>N:b\text{ is odd}\}.                                \tag{32}
\]

Then `G(A)=2` and `G(B)<=3`.  In period `2R`, an even lift of an even `b`
is `b`, whereas an even lift of an odd `b` is `b+R`.  Hence `A cap B` has a
gap of length `2N+O(1)`, and

\[
                 {G(A\cap B)\over G(A)G(B)}\longrightarrow\infty. \tag{33}
\]

This family is not an anchored CRT interval box.  It proves that any
constant-`C` theorem must use the interval-box arithmetic, not only the two
input gaps, densities, zero anchoring, or coprimality.

For arbitrary periodic factors there is an exact phase-aware replacement.
Let `A` have period `Q`, let `B` have coprime period `R`, and for a unit
`u mod R` write `G_u(B)=G(u^{-1}B)`.  Then

> **Fiber merge lemma.**
> \[
>              G(A\cap B)\le G(A)+QG_Q(B).                     \tag{34}
> \]

Starting from any integer `x`, choose `a in A` with
`x<a<=x+G(A)`.  The progression `a+tQ` remains in `A`, and modulo `R` its
orbit is the ordinary unit-step orbit through `Q^{-1}a` after multiplication
by `Q^{-1}`.  Within `G_Q(B)` steps it hits `B`, proving (34).

Since a nonempty `M`-point subset of a cyclic group of order `R` has maximum
gap at most `R-M+1`, (34) yields the completely explicit correction

\[
 G(A\cap B)
 \le G(A)+Q\bigl(R-|B|+1\bigr).                                \tag{35}
\]

This is the strongest unconditional composable inequality obtained in this
round.  It exposes both missing quantities: dilation stability of the new
block and enough old seeds to replace the single-fiber factor `Q` by a
density-scale quantity.  It is strictly more informative than the old
one-seed recursion because the exact dilated block radius is retained, but
its unconditional exponent is still fatal.  For the full 451 product,

\[
 QR=\prod_{k<p<2k}p=\exp((1+o(1))k),                            \tag{36}
\]

while `|B|/R` is exponentially small on the `k/log k` scale, so (35) remains
`exp((1+o(1))k)`.  Balanced merging across `O(log k)` blocks does not change
this root-period payment.

Thus the round ends with a genuine dichotomy rather than the slogan
"estimate the merge":

1. prove (31) using anchored interval arithmetic and a **single-block
   maximum-gap** input; or
2. prove a many-fiber strengthening of (34) that replaces `Q` by at most
   `k^{O(1)} C^{|S_A|}/density(A)` without separating the seed phases.

The current fan/successor theorems supply neither input.  No improvement to
the public 451 upper bound is claimed.
