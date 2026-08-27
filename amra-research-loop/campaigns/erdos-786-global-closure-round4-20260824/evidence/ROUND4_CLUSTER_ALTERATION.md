# Round 4: full failure-cluster alteration

## Outcome and exact scope

This round studies failure clusters while retaining the full signed valuation
kernel and the normalized cardinality defect. It proves an all-parameter
obstruction to the following precise cross-cluster theorem.

> **Packing-local cluster theorem (PLCT).** There is a function
> `h(N)=o(log N)` such that every connected subfamily `F` of bad supports in
> `H_N` has a repair set contained in the union of its supports with
> `|R|<=h(N) nu(F)`, where `nu(F)` is the maximum number of pairwise
> vertex-disjoint supports in `F`. The repair may use the complete signed
> valuation kernels, normalized defects, arbitrary petal vertices, common
> witnesses, and globally reusable choices inside `F`.

PLCT is refuted. For every sufficiently large `K`, with `N=2^K`, there is a
single connected failure cluster `F_K` whose circuits all lie in `(N/32,N]`
and satisfy

\[
\nu(F_K)=1,
\qquad
\tau(F_K)=q+1>K=\log_2N,                              \tag{1}
\]

where `q` is a prime with `K<q<2K`.

This kills deterministic repair charged uniformly to the internal disjoint
packing number of each realized failure cluster. It does not refute an
expectation-weighted alteration which charges rare clusters to their
probability, a charge using circuits outside the realized failure family, or
the finite transversal target itself.

## 1. Incidence skeleton: a projective-plane cluster

Choose by Bertrand a prime `q` with `K<q<2K`, and let `P` and `L` be the
points and lines of the projective plane of order `q`. Thus

\[
|P|=|L|=q^2+q+1,
\]

every line contains `q+1` points, every point lies on `q+1` lines, and any
two distinct lines meet in exactly one point.

Put `m=q+1`. For each point `x`, choose a block `Q_x` of `r` point-private
odd primes, where

\[
r=\lceil\log_2(m+1)\rceil+1.
\]

The blocks are pairwise disjoint. There are
`2^(r-1)-1>=m` unordered nontrivial bipartitions of `Q_x`. Assign a distinct
bipartition

\[
Q_x=Q_{x,L}^-\mathbin{\dot\cup}Q_{x,L}^+             \tag{2}
\]

to each of the `m` lines `L` through `x`, and put

\[
A_{x,L}=\prod_{p\in Q_{x,L}^-}p,qquad
B_{x,L}=\prod_{p\in Q_{x,L}^+}p,qquad
a_x=A_{x,L}B_{x,L}=\prod_{p\in Q_x}p.                \tag{3}
\]

The value `a_x` is independent of the incident line. Distinct partitions
also make all factors used at a fixed point distinct across its incident
lines.

The number of required primes is `O(q^2 log q)=O(K^2 log K)`. The standard
elementary lower bound `pi(X) >> X/log X` lets all of them be chosen below
`K^6`. Hence

\[
\max_x\log_2a_x=O((\log K)^2)=o(K).                  \tag{4}
\]

Every product of factors from two point blocks obeys the same `o(K)`
logarithmic bound.

## 2. One signed minimal circuit for every line

Fix a line `L={x_1,...,x_m}` in any order. Make a path on `2m+1` vertices
whose `2m` consecutive edge labels are

\[
A_{x_1,L},B_{x_1,L},A_{x_2,L},B_{x_2,L},\ldots,
A_{x_m,L},B_{x_m,L}.                                  \tag{5}

The odd path vertices have raw values exactly `a_(x_i)`. The even raw
values are

\[
A_{x_1,L},\quad
B_{x_i,L}A_{x_{i+1},L}\ (1\le i<m),\quad
B_{x_m,L}.                                             \tag{6}

Every edge label in this line has a prime which occurs in no other edge
label of the same line: point blocks are disjoint, and the two factors in
(2) are disjoint and nonempty. Therefore the private-prime valuation on
each path edge forces the two endpoint coefficients to be opposite in any
signed kernel vector. Connectivity forces either the zero vector or the
full alternating path vector.

Orient the line relation with coefficient `+1` on its `m` odd point
vertices and `-1` on its `m+1` even private vertices. Its normalized defect
is

\[
\delta_L=m-(m+1)=-1.                                  \tag{7}

Thus every line has the same normalized defect at every shared point.

## 3. Common padding and the strict high band

Let `c_x=ceil(log_2 a_x)` and fix the shared integer

\[
u_x=2^{K-c_x-2}a_x.                                   \tag{8}

By (4), its exponent is nonnegative for large `K`, and

\[
N/8<u_x\le N/4.                                      \tag{9}

The same `u_x` is used on all `q+1` lines through `x`.

For one line let `b_0,...,b_m` be the even raw values in (6), put
`d_j=ceil(log_2 b_j)`, and initially give the even vertex exponent
`K-d_j`. Define

\[
C_L=\sum_{j=0}^{m}d_j-\sum_{i=1}^{m}c_{x_i}.
\]

The raw path products agree, so the ceiling errors give

\[
-m<C_L<m+1.                                           \tag{10}

The initial even-minus-odd total exponent is

\[
\Delta_L=K-C_L+2m.                                   \tag{11}

It is positive. Moreover `m=q+1>K`, so

\[
0<\Delta_L<K+3m<4(m+1).                              \tag{12}

Distribute exactly `Delta_L` integer decrements over the `m+1` even
vertices as evenly as possible. Every decrement is at most four. Equation
(4) makes every initial exponent `K-o(K)`, so all final exponents are
nonnegative. The final even values lie in `(N/32,N]`; (9) gives the same
band for the odd values. Equation (11) makes the total powers of two equal
on the two shores. Combined with the raw edge-label identity, this proves an
exact equal-product relation.

The odd prime supports also prove global distinctness. A shared point value
uses one complete point block. A private endpoint uses a proper subset of
one block, and an internal private vertex uses proper subsets of two
different blocks. Across two lines, distinct factor partitions and the fact
that two projective lines share only one point prevent equality of private
odd supports. Consequently two line circuits meet exactly in the padded
integer belonging to their unique projective intersection point.

The private-prime propagation above remains valid after adding powers of
two, so every line support is a distinct-Finset support-minimal bad circuit.

## 4. Exact packing and repair numbers

Let `F_K` be the family of all `q^2+q+1` line circuits. Any two of them meet
in their unique shared point integer. Hence the failure cluster is connected
(indeed its event-intersection graph is complete) and

\[
\nu(F_K)=1.                                            \tag{13}

Every private even vertex belongs to exactly one line circuit. A shared
point integer belongs to exactly `q+1` line circuits.

Suppose a repair set has at most `q` vertices. If `s` of them are shared
point integers, these hit at most `s(q+1)` lines. The remaining at most
`q-s` private vertices hit at most one line each. Thus the total number of
hit line circuits is at most

\[
s(q+1)+(q-s)=q(s+1)\le q^2+q<q^2+q+1.                \tag{14}

So at least one failure remains, proving `tau(F_K)>=q+1`. Conversely, the
`q+1` point integers on any fixed projective line hit every line circuit,
because every two projective lines intersect. Therefore

\[
\tau(F_K)=q+1.                                        \tag{15}

Equations (13)--(15), with `q>K`, prove (1) and refute PLCT for every
sufficiently large `K`.

The same count refutes the randomized support-owner claim `M786G-07`.
Any realized owner set that actually covers every circuit in `F_K` is a
transversal, regardless of correlations or the distribution used to select
owners. Its size is therefore at least `q+1>K`, so its expected number of
distinct owners cannot be `O(log log N)`. A fractional current which does
not select a covering support vertex for every circuit is a different
mechanism and is not refuted here.

## 5. Why subtraction and the predecessor tests do not collapse the host

Let `z_L,z_M` be two line kernel vectors and normalize their shared point
coefficient to `+1`. Their intersection is exactly that point. Circuit
subtraction therefore gives

\[
A(z_L-z_M)=0,
\qquad
\delta(z_L-z_M)=(-1)-(-1)=0.                          \tag{16}

The shared point cancels, but the resulting petal relation is
cardinality-balanced, not a bad support. Thus the host lies precisely in the
equal-normalized-defect exception which a valid cluster quotient must keep.

This host strictly extends both inherited stress tests.

- A common-witness star has `nu=tau=1`; contracting its common deletion is
  correct. Here every pair has a witness but there is no global witness, and
  the exact blocking number is `q+1`.
- In a core with private satellites, repacking the disjoint satellites pays
  for the repair. Here every two satellites intersect, so no augmenting
  disjoint repacking exists, while arbitrary petal choices and reuse are
  already included in (14).

The obstruction retains the signed valuation rows and normalized defect; it
does not arise from raw maximum degree or from restricting representatives
to a packed circuit.

## 6. Classification and surviving alteration scope

- The projective-plane failure-cluster theorem (1): **proved**, all
  sufficiently large `K`.
- PLCT with any `h(N)=o(log N)`: **refuted**.
- Raw max-degree LLL and per-packed-circuit internal representatives are not
  reproved; the new host kills a strictly stronger global, petal-aware,
  optimal-within-the-realized-cluster packing charge.
- `tau(H_N)=o(N)`: **open**. The obstruction costs only `Theta(log N)`
  deletions in one sparse cluster and is not an integral-density lower bound.
- The infinite coherent natural-density assertion and original Erdős 786:
  **open**.

A surviving full-cluster alteration must use information beyond the realized
cluster's matching number: for example, probability-weighted occurrence of
large blocking clusters, fractional/log-defect mass inside the cluster, or
an external cross-cluster charge. Proposing an optimal hitting set for each
cluster is circular and is not a mechanism.

`evidence/verify_round4_cluster_alteration.py` checks finite projective-plane
incidence, the abstract circuit intersection pattern, and the exact
packing/blocking numbers. The asymptotic arithmetic realization and padding
are proved symbolically above.
