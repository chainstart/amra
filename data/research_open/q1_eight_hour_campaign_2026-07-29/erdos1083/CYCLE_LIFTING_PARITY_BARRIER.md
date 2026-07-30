# A realizable parity barrier to lifting active radius cycles

Date: 2026-07-29

## Purpose

`CORRELATION_K4_JOINT_AUDIT.md` proves that a small line count yields either a
very strongly correlated block pair or an active \(4\)-cycle on the original
radius indices.  The missing step was to lift such a radius cycle to one
quadruple of height points, so that the \(K_4\) Gram cocycle could be used.

This note gives a negative answer to that local lifting step.  Four actual
real height sets, with genuine squared-difference value selections, can have
representation density \(1/2\) on every cycle edge and still have no
transversal point cycle.  Moreover, every selected edge-value set can be
made part of a genuine same-product shifted correlation of linear size.

The construction is local.  It is not a counterexample to the global
parameter-line conjecture.

## 1. The four original height sets

Let \(m\geq4\) be even, and put
\[
 Z_0=Z_1=Z_2=Z_3=\{0,1,\ldots,m-1\}.
\]
Define
\[
 E_m=\{d^2:0\leq d<m,\ d\equiv0\pmod2\},
\]
\[
 O_m=\{d^2:0<d<m,\ d\equiv1\pmod2\}.
\]
On the four cycle edges \(01,12,23,30\), select respectively
\[
 E_m,\ E_m,\ E_m,\ O_m. \tag{1}
\]

### Theorem 1 (genuine squared-difference parity obstruction)

For the selections in (1):

1. every selected set is contained in the corresponding
   \((Z_i-Z_j)^2\);
2. the first three representation graphs contain exactly the same-parity
   point pairs;
3. the last contains exactly the opposite-parity point pairs;
4. each graph has \(m^2/2\) edges;
5. there is no transversal point \(4\)-cycle.

### Proof

For integers \(x,y\), the parity of \(|x-y|\) is even exactly when \(x,y\)
have the same parity.  Thus membership of \((x-y)^2\) in \(E_m\) or \(O_m\)
gives the stated representation graphs.  Each parity class in \(Z_i\) has
size \(m/2\), so both the same-parity and opposite-parity graphs have
\[
 2(m/2)^2=m^2/2
\]
edges.

A transversal cycle would require the first three consecutive point pairs
to have equal parity, forcing all four selected points to have the same
parity.  The final edge requires opposite parity, a contradiction.
\(\square\)

Every selected edge value has many representations on average:
\[
 \frac{m^2/2}{|E_m|}=m,\qquad
 \frac{m^2/2}{|O_m|}=m.
\]
Thus the obstruction persists at the maximum-order representation
multiplicity \(\lambda\asymp m\), far above the
\(L^{2/3+\eta}\) coarse threshold from the previous audit.

## 2. Embedding all four selections into shifted correlations

Use geometric radii \(2^u\).  Assign the four cycle parts above to radius
indices
\[
 r_0=0,\qquad r_1=7,\qquad r_2=1,\qquad r_3=16. \tag{2}
\]
The cycle edges have sums
\[
 7,\ 8,\ 17,\ 16.
\]
Choose the following disjoint external radius pairs with the same respective
sums:
\[
 (3,4),\qquad(2,6),\qquad(8,9),\qquad(5,11). \tag{3}
\]
For an edge \(uv\), write
\[
 C_{uv}=(2^u-2^v)^2.
\]
Every pair in (3) is closer to the midpoint of its sum than the
corresponding cycle pair, so
\[
 \Delta_e=C_{\text{cycle},e}-C_{\text{external},e}>0. \tag{4}
\]

### Theorem 2 (balanced shifted-correlation realization)

For every even \(m\geq4\), the eight external radius classes in (3) can be
given \(m\)-point real height sets so that the shifted block on each external
pair contains
\[
 C_{\text{cycle},e}+A_e,
\]
where \(A_e\) is the corresponding set \(E_m\) or \(O_m\) from (1).
Consequently every cycle edge has a genuine same-product block correlation
of size
\[
 |A_e|\geq m/2. \tag{5}
\]

### Proof

For one external pair, prescribe the nonnegative set
\[
 Y_e^{\rm target}=\Delta_e+A_e.
\]
Give one endpoint a height set containing
\[
 \{\sqrt y:y\in Y_e^{\rm target}\}
\]
and the other a height set containing \(0\).  Then their squared-difference
set contains \(Y_e^{\rm target}\).  Since \(|A_e|\leq m/2\), pad both
endpoint sets with arbitrary new real values until each has exactly \(m\)
elements.  The eight external radius indices in (3) are distinct, so the
four constructions are independent.

For every \(a\in A_e\), the external shifted block contains
\[
 C_{\rm external,e}+(\Delta_e+a)
 =C_{\rm cycle,e}+a,
\]
which is also in the original cycle-edge shifted block.  This proves (5).
\(\square\)

The overlap scale \(m/2\) is larger than
\(m^{5/6-\eta}\) for every fixed \(\eta<5/6\) and sufficiently large \(m\).
Hence this construction defeats both local conclusions one might hope to
draw from the dichotomy:

- linear-sized individual block correlation does not force a lift;
- an active radius \(4\)-cycle with representation density \(1/2\) on every
  edge does not force a point cycle.

## 3. Why the \(K_4\) Gram cocycle cannot repair the lift

The Gram identity applies to six squared values arising from one actual
quadruple of height points.  Theorem 1 proves that no quadruple realizes the
four selected cycle-edge constraints simultaneously.  Therefore there are
no diagonal values on which to test or fail the \(K_4\) identity.

This is a quantifier obstruction:

1. every edge separately has many represented selected values;
2. every selected value participates in a genuine shifted correlation;
3. but the four existential choices cannot be made consistently.

The cocycle verifies a candidate point quadruple; it does not create one.

## 4. Consequence for the global strategy

Any valid lifting lemma must use more than:

1. overlap size on each active edge;
2. representation multiplicity of the overlapping values;
3. the existence of an active original-radius \(4\)-cycle; and
4. the \(K_4\) Gram identity.

All four inputs are present here at linear or constant-density scale, yet
lifting fails.

The remaining possible route must impose **cross-edge sign coherence** before
the \(K_4\) step.  One sufficient hypothesis would be a quantitative lower
bound on the number of transversal cycles in the four representation graphs.
But that quantity is not controlled by the current shifted-correlation
energy, even at its strongest local scale.

This construction does not show that the global line count can be small:
padding the external height sets creates many additional parameter values,
and the other product fibres are uncontrolled.  It is a rigorous local
barrier, not an Erdős #1083 counterexample.

## 5. A conditional network-level repair for exact parity models

The local parity obstruction cannot be assigned inconsistently on every
cycle of a sufficiently rich active graph.

### Theorem 3 (conditional \(K_{2,3}\) parity lifting)

Let \(G\) be an active graph on the radius indices.  Suppose every height set
has a partition
\[
 Z_u=Z_u^0\sqcup Z_u^1
\]
with both classes nonempty, and every active edge \(uv\) has a representation
graph of the exact form
\[
 (x,y)\in{\cal R}_{uv}
 \quad\Longleftrightarrow\quad
 \operatorname{class}(x)+\operatorname{class}(y)=\ell_{uv}\pmod2
 \tag{6}
\]
for some edge label \(\ell_{uv}\).

If \(G\) contains \(K_{2,3}\), then it contains an active \(4\)-cycle with a
transversal point cycle.  If every parity class has at least \(\alpha m\)
points, that radius cycle supports at least
\[
 2(\alpha m)^4 \tag{7}
\]
transversal point cycles.

In particular, \(O(L^{3/2})\) active edges is the extremal threshold: any
fixed-power excess over \(L^{3/2}\) forces such a lift in this exact parity
model.

### Proof

Write the two vertices on one side of \(K_{2,3}\) as \(a,b\), and the other
three as \(x,y,z\).  The three \(4\)-cycles correspond to the pairs
\(\{x,y\},\{x,z\},\{y,z\}\).  The mod-two sums of their edge labels add to
zero, because every one of the six edges occurs exactly twice.  Hence not
all three cycle sums can equal one; at least one cycle has label sum zero.

On a zero-sum cycle, choosing the parity at one vertex determines consistent
parities at the other three via (6).  There are two initial choices.  With
class sizes at least \(\alpha m\), each choice gives at least
\((\alpha m)^4\) point cycles.

Finally, a \(K_{2,3}\)-free graph has \(O(L^{3/2})\) edges.  Indeed, every
pair of vertices has at most two common neighbours, so
\[
 \sum_v\binom{d(v)}2\leq2\binom L2,
\]
and convexity gives the bound. \(\square\)

This theorem is conditional on the exact two-class form (6).  General
squared-difference representation graphs need not admit such a common
two-class description.  It nevertheless clarifies the global situation:
one parity-frustrated \(C_4\) is a real obstruction, while a dense overlapping
network of exact parity gadgets must contain a consistent cycle.

## 6. Verification

`verify_cycle_lifting_parity_barrier.py` checks the parity representation
graphs, zero transversal-cycle count, the exact radius-sum matching, positive
radial-offset differences, containment of every selected value in the
external squared-difference targets, and the \(K_{2,3}\) parity identity.
