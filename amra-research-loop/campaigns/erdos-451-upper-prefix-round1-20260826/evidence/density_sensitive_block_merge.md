# Density-sensitive block merge: exact interface, killed guesses, and phase loss

This note remains in `survivor_deepening`.  It does not assume the open CRT
gap lemma and it does not promote the campaign.  The purpose is to identify
exactly what a short-window merge has to control.

## 1. The local data and an exact covering-radius criterion

Let `B` be a periodic old solution set, let `p` be a prime coprime to its
period, let `I subset Z/pZ` be the next allowed interval of size `d`, and let
`J=[x,x+L)` be an integer window.  Put

\[
 X=B\cap J,\quad N=|X|,\quad
 c_a=|\{n\in X:n\equiv a\pmod p\}|,
\]

\[
 R=|\{a:c_a>0\}|,\qquad E=\sum_{a\bmod p}c_a^2.
\]

> **Local support/energy merge lemma.**  The following are sufficient for
> `X` to meet the next constraint:
> \[
> R>p-d,                                                   \tag{1}
> \]
> or, more strongly as a checkable sufficient condition,
> \[
> N^2>(p-d)E.                                             \tag{2}
> \]
> Consequently, if (1), or (2), holds in every length-`L` integer window,
> then
> \[
> W(B\cap\{n:n\bmod p\in I\})\le L-1.                   \tag{3}
> \]

**Proof.**  If `X` misses `I`, its residue support is contained in the
`p-d` point complement of `I`, proving the contrapositive of (1).  Cauchy's
inequality gives

\[
 N^2=\left(\sum_{c_a>0}c_a\right)^2\le R E.
\]

Thus (2) implies `R>p-d` and hence (1).  Applying this to the window starting
at each integer `x` proves (3). `square`

This lemma is pointwise and retains the position of `J`.  It also identifies
the exact missing input: a useful merge needs a *local* upper bound for `E`,
or a local lower bound for `R`; full-period cardinality is not a substitute.

A universally valid but usually weak specialization is

\[
 \max_a c_a\le\lceil L/p\rceil,
 \quad R\ge \frac{N}{\lceil L/p\rceil},
 \quad E\le N\lceil L/p\rceil.                          \tag{4}
\]

It forces a hit only when `N>(p-d)ceil(L/p)`, essentially a local density
larger than the forbidden density.  After two or more half-density old
coordinates, this cannot provide the desired recursion.

## 2. Three phase-blind candidates and their exact failure

For `b` old coordinates, the first candidates were

\[
 R\ge 2^{-b}\min(p,N),                                  \tag{P1}
\]

\[
 \left||X\cap I|-\frac d pN\right|\le p2^b,             \tag{P2}
\]

\[
 E\le \frac{N^2}{p}+2^bN.                               \tag{P3}
\]

P2 would have been decisive.  If it held while adding the interval primes in
order, and `S_j` denoted the survivor count in one fixed initial window after
`j` constraints, then

\[
 S_j\ge \frac{p_j-k}{p_j}S_{j-1}-p_j2^{j-1}.
\]

Iteration would give

\[
 S_m\ge H\prod_j\frac{p_j-k}{p_j}-O(k2^m),              \tag{5}
\]

so `H=poly(k) 2^m product p/(p-k)=exp(O(k/log k))` would
make the right side positive.  Thus P2 was not a cosmetic estimate: it would
have proved the requested upper bound.

All three statements are false, already for one old prime and the exact 451
aligned intervals.  The exact guarded counterexamples are:

| candidate | exact aligned data | strict violation |
|---|---|---|
| P1 | `k=18`, `q=29`, `p=31`, `J=[19,88)`, `N=33`, `R=15` | `2R=30<31=min(p,N)` |
| P2 | `k=70`, `q=137`, `p=139`, `J=[71,1782)`, `N=871`, `d=69`, `|X cap I|=715` | `|139*715-69*871|=39286>2*139^2=38642` |
| P3 | `k=22`, `q=41`, `p=43`, `J=[23,247)`, `N=114`, `E=544` | `43E=23392>114^2+2*43*114=22800` |

The script `work/generic_block_merge_search.py` reproduces these examples.
The run recorded in `evidence/generic_block_merge_counterexamples.json` used
the OpenMath memory guard and checked 213740 aligned parameter tuples before
all three examples had appeared.  This is falsification, not extrapolation.

## 2.5. A proved canonical-carry decomposition, and its thin-slab obstruction

Carry count itself is not exponential.  Let `q_1,...,q_b` be the old moduli,
`Q=product q_i`, and choose the CRT idempotents

\[
 e_i=\frac Q{q_i}u_i,\qquad
 1\le u_i<q_i,\qquad \frac Q{q_i}u_i\equiv1\pmod {q_i}.
\]

For a coordinate vector `a=(a_i)` with `0<=a_i<q_i`, put

\[
 z(a)=\sum_i a_i e_i,
 \qquad t(a)=\lfloor z(a)/Q\rfloor,
 \qquad n(a)=z(a)-t(a)Q\in[0,Q).
\]

> **Canonical carry-layer lemma.**  The carry has at most
> \[
> 1+\sum_i(q_i-1)                                       \tag{18a}
> \]
> possible values.  For every integer interval `J subset [0,Q)`, the old
> CRT representatives in `J` are in bijection with the disjoint slab slices
> \[
> V_t(J)=\{a\in\prod_i A_i:z(a)\in tQ+J\}.             \tag{18b}
> \]
> At an external prime `p` their residues are exactly
> \[
> n(a)\equiv\sum_i a_i(e_i\bmod p)-t(Q\bmod p)\pmod p.\tag{18c}
> \]

**Proof.**  Since `0<=a_i<=q_i-1` and `0<e_i<Q`, one has
`0<=z(a)<Q sum_i(q_i-1)`, proving (18a).  The definition of canonical
reduction gives (18b), and reducing that identity modulo `p` gives (18c).
`square`

For the 451 family the number in (18a) is `O(bk)=O(k^2/log k)`, only
polynomial.  But this does not make a carry layer a sumset.  Indeed

\[
 e_i\ge Q/q_i>Q/(2k).                                  \tag{18d}
\]

If `|J|<Q/(2k)`, then after all coordinates except `a_i` are fixed, the slab
`tQ+J` contains at most one value of `a_i`: changing `a_i` by one changes
`z` by at least `e_i>|J|`.  Thus every coordinate fiber of every `V_t(J)` has
size at most one.  At the target `|J|=exp(o(k))`, a positive-proportion old
block already has `Q=exp(Theta(k))` (and the full product has
`Q=exp((1+o(1))k)`), so this thin-fiber regime holds.  Cauchy--Davenport
cannot be iterated inside `V_t(J)` merely because there are polynomially many
carries.  A new theorem would have to exploit correlations *between* these
thin slabs; recording the carry label alone preserves too little product
structure.

## 3. Exact phase formulas for one old prime

The counterexamples have a common closed form.  Let `q<p` be two 451 primes,
write

\[
 \Delta=p-q,\qquad a=q-k,qquad d=p-k=a+\Delta.
\]

Translate the common cyclic endpoint `k+1` to zero.  The old allowed interval
is `[0,a)` modulo `q`, the new interval is `[0,d)` modulo `p`, and take the
structured short window

\[
 J=[0,(t-1)q+a).
\]

It contains exactly the `t` old blocks

\[
 jq+[0,a),\qquad 0\le j<t.
\]

Modulo `p` their starts are `-j Delta`.  Let `c_r` be the resulting residue
multiplicities.  For arbitrary parameters there are exact identities

\[
 \operatorname{supp}(c)
   =[0,a)+\{0,-\Delta,\ldots,-(t-1)\Delta\}\pmod p,     \tag{6}
\]

\[
 E=ta+2\sum_{h=1}^{t-1}(t-h)\kappa_a(h\Delta),          \tag{7}
\]

where

\[
 \kappa_a(s)=|[0,a)\cap(s+[0,a))|\quad\text{in }Z/pZ.
\]

Equation (7) follows by counting an ordered pair of old blocks according to
their index difference.  It is an identity, not an estimate.

If

\[
 (t-1)\Delta\le\min(a,k),                              \tag{8}
\]

then the shifted intervals overlap without cycling through each other.  In
that range (6)--(7) become

\[
 N=ta,\qquad R=a+(t-1)\Delta,                          \tag{9}
\]

\[
 E=a t^2-\frac{\Delta}{3}t(t^2-1),                    \tag{10}
\]

and the number `M` of points also lying in the next aligned allowed interval
is

\[
 M=ta-\frac{\Delta t(t-1)}2.                           \tag{11}
\]

Indeed the `j`-th lifted interval is
`[-j Delta,a-j Delta)`.  Its negative part wraps into the final `j Delta`
residues modulo `p`, outside `[0,d)` under (8), while its positive part gives
exactly `a-j Delta` hits.  Summing proves (11).  The pairwise intersection of
blocks at distance `h` is `a-h Delta`; summing these intersections proves
(10).  In particular the exact conditional discrepancy is

\[
 pM-dN=t a k-\frac{p\Delta t(t-1)}2.                   \tag{12}
\]

Equations (9)--(12) reproduce all three aligned counterexamples above.  They
also show why changing `2^b` to a different fixed `C^b` does not repair the
general phase-blind claim.  In the unrestricted coprime family `q=p+1`, take
`a=t=s`.  The multiplicities are the triangular convolution

\[
 1,2,\ldots,s-1,s,s-1,\ldots,1,
\]

so

\[
 N=s^2,\quad R=2s-1,\quad E=(2s^3+s)/3.                \tag{13}
\]

Taking `s` near `sqrt(p)` defeats P1 for every fixed constant, while taking
`s` proportional to `p` defeats fixed-constant forms of P2 and P3.  This
unrestricted family diagnoses the mechanism.  It is not asserted to be an
infinite family of exact 451 prime pairs; no twin-prime or other unproved
prime-gap input is being used.

## 4. A proved phase-aware short-window discrepancy lemma

There is a clean replacement for P2 which records the missing phase cost.
Let the old set be one cyclic interval of length `a` modulo `q`, with `q<p`,
and let the new interval have length `d` modulo `p`.  Intersect an arbitrary
integer window `J` with the old periodic set.  Apart from at most two partial
old blocks, it consists of `u` consecutive complete old blocks.  Put
`r=u mod p`, and define

\[
 h(s)=|[0,a)\cap(s+[0,d))|-ad/p,
\]

with both intervals read cyclically modulo `p`.  If the first complete block
has phase `s_0`, the exact complete-block error is

\[
 \sum_{j=0}^{u-1}h(s_0+j(q\bmod p)).                   \tag{14}
\]

Since `q` is invertible modulo `p`, one full run of `p` block phases is a
permutation of all residues, and

\[
 \sum_{j=0}^{p-1}h(s_0+jq)=0.                          \tag{15}
\]

Each of the two partial blocks has discrepancy at most `p`.  Therefore

> **One-prime phase-aware discrepancy lemma.**
> \[
> \left||B_q\cap J\cap I_p|-\frac d p|B_q\cap J|\right|
> \le 2p+
> \left|\sum_{j=0}^{r-1}h(s_0+j(q\bmod p))\right|       \tag{16}
> \]
> for the appropriate first phase `s_0`, and in particular
> \[
> \left||B_q\cap J\cap I_p|-\frac d p|B_q\cap J|\right|
> \le p\bigl(2+\min(r,p-r)\bigr).                      \tag{17}
> \]

**Proof.**  Split the old interval pattern on the line into its consecutive
period blocks.  Only the first and last intersected blocks can be partial.
Equation (14) is the definition of the full-block contribution.  Equation
(15) follows because `j q mod p` permutes `Z/pZ`: for each of the `a` points
in an old block, exactly `d` of the `p` phases put it in the new interval.
Delete `floor(u/p)` complete phase cycles.  The remaining `r` terms have
absolute sum at most `rp`; using their complementary `p-r` terms and (15)
also gives `(p-r)p`.  The two boundary pieces cost at most `2p`. `square`

Combining (16) with the local merge lemma gives a genuine covering-radius
interface: if its right-hand side is strictly smaller than
`(d/p)|B_q cap J|` in every length-`L` window, then the merged covering radius
is at most `L-1`.  Unlike P2, the bound cannot hide `r` or the step
`q mod p`; equations (9)--(12) show that the phase sum can really be of order
`p r`.

## 5. Why adjacent prime gaps do not amortize through a CRT recursion

For the one-old-prime calculation, a small `Delta=p-q` makes consecutive
blocks move slowly, so it creates more coherence rather than less.  From
(9), merely forcing the projection to have more than the `k` forbidden
residues requires roughly

\[
 t>1+\frac{k-a}{\Delta}
   =1+\frac{2k-q}{\Delta}.                              \tag{18}
\]

Thus the natural loss is inverse in the prime gap.  The elementary identity
that the sum of adjacent gaps across `(k,2k)` is at most `k` supplies no upper
bound for a sum of `log(k/Delta)` or for a product of `1/Delta` losses.  A
claim that typical gaps repair (18) would require an additional prime-gap
theorem; none is assumed here.

More decisively, after several primes have been imposed the shifts that
preserve all old constraints are multiples of their product `Q`, not of the
last prime `q`.  The next phase step is

\[
 Q\bmod p,
\]

whose least cyclic residue and continued-fraction data are not controlled by
the adjacent gap `p-q`.  For example, in the actual `k=20` system,

\[
 Q=23\cdot29=667\equiv16\pmod {31},                    \tag{19}
\]

so the least phase magnitude is `15` although the last adjacent prime gap is
only `31-29=2`.  In general

\[
 Q=\prod_i q_i\equiv(-1)^b\prod_i(p-q_i)\pmod p,       \tag{20}

\]

and multiplication followed by reduction modulo `p` destroys any additive
gap ledger.  Continued-fraction control faces the same obstruction: the
partial quotients of `(Q mod p)/p` can be arbitrarily bad from the viewpoint
of the adjacent prime gaps, and a step `1` already permits interval
discrepancy of order `p` over a coherent partial orbit.

Hence the single-prime phase lemma is a true standalone result but does not
compose into an `exp(o(k))` recursion.  A surviving block theorem must control
the phase orbit of *many short-prefix seeds* after the product step `Q mod p`,
or supply a new averaged-to-pointwise argument.  Replacing `Q mod p` by the
last adjacent gap is an invalid handoff.

## 6. Full-period Cauchy--Davenport versus the short window

Over `p` consecutive complete old periods, (15) gives exact equidistribution;
over a complete old period, the earlier multi-seed lemma can use
Cauchy--Davenport.  Neither statement localizes to a short arbitrary `J`.
The aligned examples above consist of only `t<p` coherent old blocks, and
their multiplicity profiles are triangular rather than uniform.  Paying a
full phase cycle costs `pq` already in the one-coordinate case; after a block
product it costs `Qp`.  This is precisely the old exponential period loss.

The remaining closure gap is therefore quantitative and explicit: bound the
phase sum in (16), or its many-seed/block analogue, at total cost
`exp(O(block_size))` while retaining the distinguished initial window.  No
such bound is proved here, and the campaign's `closes` field remains empty.

## 7. Successive-product phase audit under five merge orders

The guarded program `work/successive_product_phase.py` computes, for a merge
with old product `Q` and new prime `p`, the exact rational-rotation quantity

\[
 \mathcal D_k(Q,p)=
 \max_{x,T}\left|
   \#\{0\le t<T:x+tQ\bmod p\in[0,p-k)\}
       -\frac{p-k}{p}T
 \right|.                                               \tag{21}
\]

It also records the centered phase, Euclidean partial quotients, the largest
cyclic gap among the first `ceil(sqrt(p))` orbit points, and the same
discrepancy restricted to orbits of that short length.  Five orders were
compared: increasing, decreasing, alternating low/high, oracle-greedy minimum
of (21), and oracle-greedy maximum centered phase.  The word *oracle* is
important: at every stage the greedy rule inspects every remaining prime.

The increasing order has exactly maximally coherent product phases in genuine
451 instances.  The smallest is already

\[
 k=10,\quad Q=11\cdot13\cdot17\equiv-1\pmod {19}.       \tag{22}
\]

Here the allowed width is `9` and

\[
 \mathcal D_{10}(Q,19)=\frac{90}{19}=4.7368\ldots,
 \qquad \frac{\mathcal D_{10}(Q,19)}{19}=0.2493\ldots. \tag{23}
\]

The same exact unit-phase phenomenon appears in the scan at `(k,p)=(271,487)`,
`(650,1229)`, `(760,1451)`, and `(1480,2917)`.  At the last row
`Q=-1 mod 2917` and `D/p=0.249945...`.  These finite rows do not prove an
infinite family, but one exact row is already enough to reject any recursion
step claiming that actual product phases are automatically noncoherent.

Centered phase size is also the wrong proxy.  In the `k=271`
centered-phase-greedy order, one merge has

\[
 p=347,\quad Q\equiv173=(p-1)/2\pmod p.                 \tag{24}
\]

The centered phase `173` is as large as possible, yet the continued fraction
has quotients `[2,173]` and

\[
 \mathcal D_{271}(Q,347)=14896/347=42.9279\ldots
 =0.12371\ldots\,p.                                    \tag{25}
\]

Thus a lower bound for `min(Q mod p,-Q mod p)` loses the ordering information
that the continued fraction retains.

For reference, the diagnostic cumulative cost

\[
 L(\sigma)=\sum_{j\ge1}\log(1+\mathcal D_k(Q_j,p_{j+1})) \tag{26}
\]

gave the following exact finite values:

| `k` | primes | increasing | decreasing | alternating | centered-greedy | discrepancy-greedy |
|---:|---:|---:|---:|---:|---:|---:|
| 650 | 93 | 168.46 | 166.23 | 164.10 | 197.26 | 100.18 |
| 760 | 106 | 193.12 | 193.06 | 180.29 | 238.13 | 113.71 |
| 1000 | 135 | 243.52 | 257.35 | 245.65 | 328.78 | 144.29 |
| 1480 | 193 | 366.96 | 368.98 | 370.06 | 537.27 | 213.34 |

The discrepancy-greedy order is substantially better and its values are
numerically compatible with an `O(m polylog(k))` ledger.  This is not a
theorem, and it exposes rather than closes two gaps:

1. One needs a deterministic ordering theorem bounding (26), uniformly for
   every `k`, without a prime-gap or pseudorandom-residue conjecture.
2. Even such an ordering theorem concerns the orbit of one seed under shifts
   by `Q`.  The shift `tQ` has real size `Q`; using it directly retains the
   old `Q` factor.  A second theorem must show that the same phase ledger
   controls the residues of the many *distinct old seeds already present in
   a short prefix*.  This does not follow from (21).

Accordingly, the data do not support a standalone block-average lemma yet.
They kill the centered-phase-only bridge, show worst coherence in the actual
system, and leave a precise conditional pair: an ordering inequality for
(26) plus a many-seed short-prefix propagation inequality.  Neither is
inserted into `decisive_lemma.json` as an assumption.
