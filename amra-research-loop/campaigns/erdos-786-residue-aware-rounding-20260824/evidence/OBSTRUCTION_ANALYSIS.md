# Obstruction analysis: residue is necessary but not automatically simpler

## Inherited exact state

The log-defect LP is feasible at cost `(1+o(1))N/log N`; IR.1 rules out
every affordable hard/nested threshold and unaltered proportional product
sample.  The surviving host deletes a lower tail, a smooth core, and repeated
large-prime powers, leaving squarefree active primes `p>y=N^(1/L)`.

At a largest active prime `p`, equal products balance the number of
`p`-incidences.  Stripping `p` does not cancel those terms: their cofactors
carry a signed product ratio into lower fibres.  The present campaign keeps
that ratio exactly.

## Preliminary all-parameter host RR.1: rough ordered path

Fix integers `L>=3` and `s>=L`.  For arbitrarily large `K`, put `N=2^K` and
`y=N^(1/L)`.  Take the path on vertices `v_0,...,v_(2s)`.  By repeated
Bertrand intervals choose strictly increasing distinct odd primes

\[
y<p_1<p_2<\cdots<p_{2s}<2^{2s+1}y                  \tag{1}
\]

and label edge `v_(i-1)v_i` by `p_i`.  Let `q_i` be the product of incident
edge primes at `v_i`.  The even and odd path vertices have sizes `s+1` and
`s`, and both shore products of the `q_i` equal `prod_i p_i`.

Put `c_i=ceil(log_2 q_i)` and initial exponent `e_i^0=K-c_i`.  Because path
degree is at most two, (1) gives

\[
\max_i c_i\le 2K/L+4s+O(1).                         \tag{2}
\]

For sufficiently large `K`, all initial exponents are nonnegative.  The
difference of their sums on the shores is

\[
\Delta=K-C,\qquad -s<C<s+1,                         \tag{3}
\]

because the unpadded shore products agree and each ceiling error lies in
`[0,1)`.  Reduce the exponents on the larger shore by nonnegative integers
with total `Delta`, distributed as evenly as possible.  The largest
decrement is at most `K/(s+1)+2`.  From (2), when `K` is sufficiently large
the final exponents remain nonnegative, since

\[
1-2/L-1/(s+1)>0.                                    \tag{4}
\]

The padded values `a_i=2^(e_i)q_i` are distinct, at most `N`, and their shore
products agree.  Every value initially exceeds `N/2`, and after redistribution
every value exceeds

\[
N^{1-1/(s+1)-3/K}>N^{1-1/L}.                        \tag{5}
\]

Every active prime `p_i>y` occurs squarefreely, endpoints have active degree
one, internal vertices active degree two, and the active-incidence graph is
the original path.  Unique edge-prime valuation equations force every signed
subrelation either to vanish or to use the full connected bipartition, so the
relation is support-minimal.

Ordering the `p_i` increasingly along the path makes the largest-prime peel
start at one endpoint and transfer a nontrivial residue to the next edge.
Since `s` is arbitrary, neither active degree two, forest incidence, nor a
bound depending only on `L` controls the number of successive residue
transfers.  This is a theorem about the adversarial host; it does not show
that a global owner or parallel alteration cannot hit the whole path cheaply.

## Preliminary all-parameter host RR.2: universal residue extension

Let `A={a_1,...,a_r}` and `B={b_1,...,b_s}` be disjoint sets of distinct
primes, with `r,s>=1` and `r!=s`, and choose a new prime
`p>max(A union B)`.  Put

\[
X=\prod_i a_i,\qquad Y=\prod_j b_j.
\]

Then

\[
 A\cup\{pY\}\quad\hbox{and}\quad B\cup\{pX\}      \tag{6}
\]

have equal products `pXY` and cardinalities `r+1,s+1`.  Their prime-
incidence graph is the connected double-star tree: every `a_i` connects its
singleton to `pX`, every `b_j` connects `pY` to its singleton, and `p`
connects the two composite vertices.  Hence the signed edge equations prove
support minimality.

At the largest prime `p`, the fibre counts are one and one.  Stripping `p`
leaves cofactors `Y` and `X`, so the transferred residue is the arbitrary
ratio `Y/X`; its numerator and denominator can have independently unbounded
prime support.  Residue-aware peeling is correct, but no bounded residue
alphabet, fan size, or coprime-factor split follows.

The same identity proves a coherence warning.  Any two lower prime products
can be completed later by one new larger prime into an unequal relation.
A prefix rule that irrevocably admits both lower configurations therefore
needs a future reserve/isolation theorem.

## Consequences for the three required families

* Arithmetic alteration must compress complete connected components; bounded
  active degree, forest structure, or bounded circuit support is unavailable.
* Largest-prime ownership must amortize a residue of unbounded fan and path
  depth.  A one-step strict drop of the largest prime is not by itself a
  sublogarithmic load bound.
* Recursive tokens need a global potential.  Token count, cycle rank, maximum
  active degree, and a fixed residue alphabet all lose information on RR.1 or
  RR.2.
* Coherent stabilization needs revision or reserved deletion capacity for
  later prime extensions; finite-prefix safety is not hereditary upward.
