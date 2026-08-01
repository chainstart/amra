# Erdős #1083: classification and realization of the coherent short-cycle branch

Date: 2026-08-01

## 0. Verdict

The coherent exceptional branch of the bounded-cycle theorem cannot
be excluded from simple-cycle structure and adjacent transversality
alone.

There is a genuine four-row reverse-circle local model with:

- one nonzero difference \(\delta=1\);
- a simple four-cycle;
- rationally transverse dilation spaces on every adjacent pair;
- one coherent source label at every cycle vertex; and
- the balanced orientation signature \(++--\).

Thus the exceptional branch is real, not a proof artifact.  On the
positive side, every coherent cycle has one of only 36 orientation
signatures up to cyclic relabelling and reversal, and it admits an
exact bounded arithmetic-potential normal form.

The local model is not an exact full spectral block and is not a
counterexample to #1083.  It proves that any exclusion must use the
full block partitions or repetition of many cycles, not one cycle in
isolation.

## 1. Finite signature classification

In a coherent cycle of length \(\ell\le10\), the bounded-cycle
identity gives

\[
 \sum_{k=1}^{\ell}\sigma_k=0,
\qquad \sigma_k\in\{-1,+1\}.
\tag{1.1}
\]

Therefore \(\ell\) is even:

\[
 \ell\in\{4,6,8,10\}.
\tag{1.2}
\]

There are

\[
 \binom{\ell}{\ell/2}
\]

raw balanced sign words.  Hence there are at most

\[
 \binom42+\binom63+\binom84+\binom{10}5
 =6+20+70+252
 =348
\tag{1.3}
\]

types even before quotienting by cycle symmetries.

Changing the starting vertex cyclically rotates the word.  Reversing
the traversal reverses the word and changes every sign.  Exhaustive
finite orbit enumeration gives:

| cycle length | raw balanced words | cyclic/reversal types |
|---:|---:|---:|
| 4 | 6 | 2 |
| 6 | 20 | 4 |
| 8 | 70 | 9 |
| 10 | 252 | 21 |
| **total** | **348** | **36** |

The verifier enumerates every one of the 348 words and the exact
equivalence action; this count is not sampled.

## 2. Arithmetic-potential normal form

For a coherent cycle, let \(x_k\in X\) be the common source label at
vertex \(v_k\), and put

\[
 F_k=z_{v_k}^2+2\rho z_{v_k}x_k.
\tag{2.1}
\]

The edge identities are

\[
 F_k-F_{k+1}=\sigma_k\delta.
\tag{2.2}
\]

Define integer levels by

\[
 h_1=0,\qquad h_{k+1}=h_k-\sigma_k.
\tag{2.3}
\]

Then (1.1) makes the walk close, and

\[
 \boxed{
 F_k=F_1+h_k\delta.}
\tag{2.4}
\]

Since the word has at most five plus and five minus signs, after a
common level translation all levels lie in

\[
 \{0,1,\ldots,5\}.
\tag{2.5}
\]

Thus every coherent exception is described by:

1. one of 36 sign orbits;
2. at most six integer potential levels;
3. at most ten source labels \(x_k\in X\); and
4. the quadratic equations

   \[
   z_{v_k}^2+2\rho x_kz_{v_k}
   =F_1+h_k\delta.
   \tag{2.6}
   \]

For a fixed pair \((h,x)\), equation (2.6) is a quadratic in \(z\)
and has at most two real solutions.  Consequently:

\[
 \boxed{
 \text{each level--source pair }(h,x)
 \text{ occurs at most twice on a simple coherent cycle}.}
\tag{2.7}
\]

This is the complete finite normal form available from one cycle.

## 3. A strict coherent transverse four-cycle

Take

\[
 \rho=1,\qquad X=\{0,1\},\qquad\delta=1.
\]

Use four distinct nonzero heights

\[
 z_1=\sqrt5,\qquad z_2=2,\qquad
 z_3=\sqrt3,\qquad z_4=-2,
\tag{3.1}
\]

and assign the coherent source value

\[
 x_1=x_2=x_3=x_4=0.
\tag{3.2}
\]

The potentials are

\[
 (F_1,F_2,F_3,F_4)=(5,4,3,4).
\tag{3.3}
\]

Choose the directed edges

\[
 1\to2,\qquad 2\to3,\qquad
 4\to3,\qquad 1\to4.
\tag{3.4}
\]

Traversing the undirected cycle \(1,2,3,4,1\) gives signs

\[
 (+,+,-,-).
\]

Every directed edge \(i\to j\) satisfies

\[
 z_i^2-z_j^2=\delta.
\tag{3.5}
\]

Since \(\operatorname{span}_{\mathbb Q}(X-X)=\mathbb Q\), the row
space is \(W_i=z_i\mathbb Q\).  Every adjacent ratio is irrational:

\[
 \frac{\sqrt5}{2},\quad
 \frac{2}{\sqrt3},\quad
 \frac{\sqrt3}{-2},\quad
 \frac{-2}{\sqrt5}.
\]

Thus all four adjacent pairs are rationally transverse.  The
nonadjacent rows \(z_2=2\) and \(z_4=-2\) are deliberately
commensurate; the bounded-cycle theorem never claimed all cycle
vertices were pairwise transverse.

## 4. Tangent and Euclidean realization

For every directed edge, use the tangent pair

\[
 \tau=10,\qquad\tau'=11,
\qquad \tau'-\tau=\delta.
\]

It is enough to take

\[
 T_1=\{10\},\quad
 T_2=\{10,11\},\quad
 T_3=\{11\},\quad
 T_4=\{10,11\}.
\tag{4.1}
\]

For edges \(1\to2\) and \(1\to4\), the common squared-distance label
at source \(0\) is

\[
 1+5+10=1+4+11=16.
\]

For edges \(2\to3\) and \(4\to3\), it is

\[
 1+4+10=1+3+11=15.
\]

All tangent squares are positive.  Using target points

\[
 (A,\sqrt\tau,-z_i),\qquad A>1,
\]

gives actual radius-one reverse circles and exact producer
incidences.  Distinct heights give distinct row axes.

### Firewall

The tangent sets in (4.1) have unequal sizes, and the four full row
spectra are not one identical direct tiling.  The model realizes the
local fixed-difference cycle equations and their Euclidean interface,
not the entire frozen block.

Therefore it proves:

> simple cycle + adjacent transversality + one nonzero difference
> does not exclude the coherent branch.

It does not prove that a critical exact block can be assembled from
such cycles.

## 5. Revised target

The coherent branch must now be attacked at network level.  A viable
theorem must show that \(t^{\Omega(1)}\) short coherent cycles force
one of:

1. repetition of a level--source pair beyond the quadratic
   multiplicity two in (2.7);
2. a common bounded-level potential chart on many rows;
3. a large commensurate-height subgraph; or
4. enough distinct potential values to exceed the distance budget.

One isolated cycle cannot provide the contradiction.
