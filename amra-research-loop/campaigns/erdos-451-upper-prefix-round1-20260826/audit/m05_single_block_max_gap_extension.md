# M05 extension audit: can one dyadic block control its maximum gap?

## Verdict

**OPEN, WITH A PRECISE AFFINE-COVERING GAP.**  The M05 one-block theorem is a
genuine anchored successor theorem, but its quantitative Blichfeldt proof
does not extend uniformly to an arbitrary gap start.  Rank one and rank two
do admit polynomial-times-density maximum-gap bounds; the actual close-pair
family shows that a `k^(2-o(1))` factor is necessary already at rank two.
For unbounded block rank, no counterexample to a `k^B C^q/density` theorem
was found, but neither Blichfeldt differences nor generic dimension losses
prove it.

This file is an extension/cross-audit by the M10 line.  It does not modify
the M05 author evidence.

## 1. The theorem needed by a block merger

Let `B` be a set of `q` primes, put `d_i=p_i-k`, and assume one dyadic scale

\[
                    \Delta\le d_i<2\Delta.                     \tag{1}
\]

Let

\[
 {\cal A}_B=\{n\bmod P_B:-n\bmod p_i\in[0,d_i-1]\},
 \qquad \delta_B=\prod_{i\in B}{d_i\over p_i}.                 \tag{2}
\]

The useful missing statement is:

> **Single-scale maximum-gap theorem (open).**  There are absolute
> `B_0,C_0` such that every block (1) satisfies
> \[
>              G({\cal A}_B)\le k^{B_0}C_0^q\delta_B^{-1}. \tag{3}
> \]

This is stronger than finding one `n` from the anchored start.  It must hold
after every cyclic starting point, because a block merger sees the phase
left by all previously processed blocks.

If (3) and an absolute relaxed block merger

\[
                  G(X\cap Y)\le C_1G(X)G(Y)                    \tag{4}
\]

both held, the `L=O(log k)` dyadic blocks would give

\[
 G({\cal A}_{\rm full})
 \le k^{B_0L}C_0^m C_1^{L-1}\prod_{k<p<2k}{p\over p-k}.        \tag{5}
\]

The logarithm of the right side is

\[
 O((\log k)^2)+O(m)+\left(\log4+o(1)\right){k\over\log k}
 =o(k).                                                         \tag{6}
\]

Thus (3) is exactly strong enough to combine with a constant-cost merger.
The actual counterexamples in the M10 note kill (4) with `C_1=1`, but do
not kill an unspecified absolute `C_1`.

## 2. The affine lattice coset at a gap start

Fix an integer start `x` and seek an increment `y>0`.  The congruences are

\[
                     x+y+s_i=p_i a_i.                          \tag{7}
\]

Put `v=(1/p_i)_i`.  In the quotient coordinates this asks for an integer
vector `a` in an affine translate

\[
 a-xv=\operatorname{diag}(1/p_i)(y{\bf1}+s).               \tag{8}
\]

For the half-width used in M05, let

\[
 w=\lfloor(\Delta-1)/2\rfloor,\qquad b=w+1/2.                  \tag{9}
\]

A sufficient located target is

\[
 \begin{split}
 Z_{H,w}=\operatorname{diag}(1/p_i)
 \{y{\bf1}+u:
       w+1/2<y<H+1/2,\ |u_i|<b\}.                              \tag{10}
 \end{split}
\]

If `(xv+Z_{H,w}) cap Z^q` is nonempty, the same half-integer endpoint
argument as M05 reconstructs an integer `w<y<=H` and integers `|s_i|<=w`.
The common shift `t=min_i s_i` then gives actual offsets in `[0,d_i-1]` and
a forward increment

\[
                       0<y+t\le H+w.                           \tag{11}
\]

Consequently, uniform intersection of (10) for all `x mod P_B` would prove a
maximum-gap form of the one-block theorem.

This is where quantitative Blichfeldt stops.  Translating the body by `xv`
and averaging over lattice cosets may find two points of a favorable
translate, but subtracting them cancels `xv`.  The difference lies in the
homogeneous symmetric body and supplies a short lattice **difference**, not
a point in the prescribed affine coset.  Global negation also changes the
affine right side in (7), so it cannot turn a backward increment at fixed
`x` into a forward one.  Volume alone therefore proves the anchored
difference theorem, not (10) for every start.

The starts occupy the cyclic diagonal orbit

\[
             \{xv\bmod\mathbb Z^q:0\le x<P_B\},                \tag{12}
\]

rather than all torus translates.  This is genuine extra structure, but no
covering theorem for this orbit is established in M05.

## 3. Exact dual ledger and the surviving high-support case

For the symmetric difference zonotope with time half-width `h`, M05 proved
the exact support function

\[
 R(z)=h\left|\sum_i{z_i\over p_i}\right|
       +\sum_i b{|z_i|\over p_i},\qquad z\in\mathbb Z^q.        \tag{13}
\]

The three relevant classes can be audited without invoking an unspecified
transference theorem.

### 3.1 Zero diagonal frequency

If `sum z_i/p_i=0`, then `z_i=p_i t_i` and `sum t_i=0`.  A nonzero vector
has two active coordinates, so

\[
                         R(z)\ge2b\ge\Delta/2.                 \tag{14}
\]

Thus exact zero-frequency vectors are not the thin direction when the block
width is macroscopic.

### 3.2 Sparse nonzero frequency

Write

\[
                 A=P_B\sum_i{z_i\over p_i}\in\mathbb Z\setminus\{0\},
 \qquad S=\{i:z_i\ne0\},\quad r=|S|.                           \tag{15}
\]

For every `j notin S`, reduction modulo `p_j` gives `p_j|A`.  Hence

\[
 |A|\ge\prod_{j\notin S}p_j,
 \qquad {|A|\over P_B}\ge{1\over\prod_{i\in S}p_i}
                         >{1\over(2k)^r}.                      \tag{16}
\]

Also `b>=Delta/4`, so every active coordinate contributes more than
`Delta/(8k)`.  Therefore the following unconditional lower bound holds:

\[
             \boxed{R(z)>{h\over(2k)^r}+{r\Delta\over8k}.}     \tag{17}
\]

This is a reusable intermediate inequality.  It shows that a large `h`
automatically removes low-support affine obstructions.

### 3.3 Small nonzero A and high support

The unresolved case is `r` large while the exact integer `A` in (15) is
small.  Reduction modulo `p_i` fixes

\[
                 z_i(P_B/p_i)\equiv A\pmod {p_i}.              \tag{18}
\]

Proving (3) by a covering argument would require a lower bound for the
weighted centered representatives in (18), uniformly in small nonzero `A`.
The support-size term in (17) is only `r Delta/k`; for submacroscopic
`Delta` this is much smaller than `r`.  No coefficient-quality or signed
CRT cancellation estimate closing this case is currently proved.

This audit deliberately does not assert a sharp transference constant.
Whatever covering theorem is used, a multiplicative loss `q^{alpha q}`
with fixed `alpha>0` has

\[
                  \log q^{\alpha q}=(\alpha+o(1))k            \tag{19}
\]

for a macroscopic block `q asymp k/log k`, and therefore fails the target.
Only a special-zonotope loss such as `C^q` or
`(log k)^{O(q)}` is exponent-compatible.  Generic dimension losses cannot be
silently called harmless.

## 4. What is proved at low rank

For one coordinate the anchored set is one cyclic interval and

\[
                          G=k+1.                               \tag{20}
\]

For two coordinates, the exact empty-block theorem from the M10 round gives

\[
 G\le\left(\left\lfloor{k-a\over p-q}\right\rfloor+3\right)q
   \le4k^2                                                      \tag{21}
\]

for distinct primes `q=k+a<p<2k` and `k>=3`.  Consequently every rank-two
single-scale block satisfies the genuine maximum-gap theorem

\[
                         G\le4k^2\delta_B^{-1}.                \tag{22}
\]

Conversely, PNT supplies actual adjacent primes in
`(3k/2,7k/4)` with gap `O(log k)`.  The exact lower witness gives

\[
             G\gg{k^2\over\log k},\qquad \delta_B^{-1}=O(1).  \tag{23}
\]

Thus any all-rank theorem of the shape (3) needs `B_0>=2`; the polynomial
cannot be removed.  Rank two pays it only once, which is compatible with the
desired block-global statement.

For arbitrary rank the only immediate universal estimate is the period:

\[
 G\le P_B=\delta_B^{-1}\prod_{i\in B}d_i
          <\delta_B^{-1}(2\Delta)^q.                            \tag{24}
\]

Across all dyadic blocks the additional logarithm
`sum_(k<p<2k) log(p-k)=(1+o(1))k`; (24) therefore returns the full
`exp((1+o(1))k)` scale.  It is not a nontrivial 451 upper bound.

## 5. Guarded finite falsification

An exact scan enumerated `342` actual-prime dyadic blocks with `k<=100` and
at most two million allowed CRT residues.  The largest observed value of

\[
             {G\delta_B\over k^2}                              \tag{25}
\]

was `0.1027544...`, at `k=7`, block `(11,13)`.  For example, at `k=80` the
rank-three block `(149,151,157)`, of widths `(69,71,77)`, had
`G=3359` and `G delta_B/k^2=0.0560487...`.  These rows are compatible with
(3) with `B_0=2`, but are finite diagnostics and supply no uniform constant.

```text
command: /home/biostar/work/projects/openmath/bin/openmath-memory-guard -- /usr/bin/time -v python3 amra-research-loop/campaigns/erdos-451-upper-prefix-round1-20260826/work/m10_round1/m05_single_block_gap_scan.py
unit: openmath-task-20260826-231525-331579.scope
exit: 0
wall: 2.60s
maximum RSS: 36048 KiB
swaps: 0
script sha256: 88e2fbfd150d354dae1d2d454e6ffe48f46bb91a01d0d49a44c9817f2e548cad
```

## 6. Exact remaining statement

No actual 451 single-scale counterexample to (3) is known from this round.
The extension is reduced to a strictly narrower arithmetic covering lemma:

> Control the diagonal-orbit affine covering (10)--(12) with total loss
> `k^B C^q/density`, equivalently rule out the high-support small-`A` dual
> configurations (18) at a `C^q` or polylogarithmic-per-coordinate cost,
> while retaining the one-sided forward endpoint.

Even a proof of this statement would still require an absolute-cost relaxed
block merger such as (4), which remains open after the constant-one
counterexamples.  No improvement to Erdős 451 is claimed.
