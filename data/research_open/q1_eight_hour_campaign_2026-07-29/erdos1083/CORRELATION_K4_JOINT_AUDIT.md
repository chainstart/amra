# Joint audit: from shifted correlation to \(K_4\) cocycles

Date: 2026-07-29

## Purpose

This note combines two earlier facts: a small parameter-line count forces
large shifted correlation inside radius-product fibres, while four original
radius vertices impose an exact sign-cocycle identity.

It proves a dyadic dichotomy: at the line-count threshold relevant to an
exponent gain, either one obtains very strong individual block correlations
or the active radius-pair graph contains an original-radius \(4\)-cycle.
It then identifies a remaining obstruction: set-level correlation does not
guarantee that the four active edge relations admit one coherent quadruple
of height points.

No exponent improvement is claimed.

## 1. Regularized block system

Work in the balanced regime
\[
 L\asymp m,\qquad F\asymp Lm\asymp L^2.
\]
Assume every radius class contains between \(cm\) and \(m\) heights for one
fixed \(c>0\).  From every squared-difference block
\[
 Y_{uv}=(Z_u-Z_v)^2
\]
choose an arbitrary subset \(\widetilde Y_{uv}\) of a common size
\(k\asymp m\).  This is possible because
\[
 |Y_{uv}|\geq\frac12\max\{|Z_u|,|Z_v|\}\geq cm/2.
\]
Put \(\widetilde S_{uv}=C_{uv}+\widetilde Y_{uv}\).  Their total incidence
mass is
\[
 I_0=\Theta(L^2m)=\Theta(L^3). \tag{1}
\]
Their union is contained in the full parameter-line set, so its size is at
most \(M\).

## 2. Correlation relations as additive quadruples

Two different radius pairs can be correlated only when
\[
 u+v=u'+v'. \tag{2}
\]
For each such unordered relation \(q=\{\{u,v\},\{u',v'\}\}\), give it weight
\[
 w(q)=|\widetilde S_{uv}\cap\widetilde S_{u'v'}|,
 \qquad 0\leq w(q)\leq k. \tag{3}
\]
There are \(O(L^3)\) possible relations.

## Theorem 1 (line threshold to active-\(C_4\) dichotomy)

Let
\[
 M\leq L^{8/3+\eta},\qquad 0\leq\eta<5/6.
\]
Up to logarithmic factors, at least one of the following holds.

1. **Strong-pair branch:**
   \[
   r\geq L^{5/6-\eta-o(1)}. \tag{4}
   \]
2. **Shared-radius-cycle branch:** the graph on the \(L\) original radius
   indices whose active edges participate in a weight-\(\geq r\) relation
   contains a \(4\)-cycle.

For a desired bound \(M\geq F^{4/3+\varepsilon}\), one has
\(\eta=2\varepsilon\), so the dividing overlap scale is
\[
 r=L^{5/6-2\varepsilon-o(1)}. \tag{5}
\]

### Proof

The second-moment stability inequality applied to the truncated blocks gives
\[
 {\cal K}_0
 \geq \frac{I_0^2}{M}-I_0
 \geq L^{10/3-\eta-o(1)}. \tag{6}
\]
After dividing by two and dyadically pigeonholing the unordered weights,
there is a scale \(r\) with \(Q_r\) significant relations satisfying
\[
 rQ_r\geq L^{10/3-\eta-o(1)}. \tag{7}
\]

Let \(A_r\) be the number of active original-radius edges.  One block belongs
to only one product fibre and has at most \(L\) partners there.  Hence
\[
 A_r\geq\frac{2Q_r}{L}
 \geq\frac{L^{7/3-\eta-o(1)}}r. \tag{8}
\]

A graph on \(L\) vertices with no \(4\)-cycle has \(O(L^{3/2})\) edges:
any two vertices have at most one common neighbour, so
\[
 \sum_v\binom{d(v)}2\leq\binom L2,
\]
and convexity gives the bound.  If the active graph has no \(4\)-cycle, (8)
therefore forces (4). \(\square\)

At the \(F^{4/3+\varepsilon}\) threshold, diffuse low-overlap correlation
cannot avoid producing a shared-radius \(4\)-cycle.

## 3. Why a radius \(4\)-cycle is not yet a point \(4\)-cycle

For an active radius edge \(uv\), let \(A_{uv}\subseteq\widetilde Y_{uv}\)
be the values participating in its significant external correlation.  Lift
it to
\[
 {\cal R}_{uv}
 =\{(x,y)\in Z_u\times Z_v:(x-y)^2\in A_{uv}\}. \tag{9}
\]
The \(K_4\) cocycle applies only after choosing one height point at each of
four radius vertices so that all four cycle edges occur simultaneously.
Set-level overlap gives \(|A_{uv}|\geq r\), hence only
\[
 |{\cal R}_{uv}|\geq r. \tag{10}
\]

### Proposition 2 (parity-frustrated representation cycle)

Let four height parts \(V_0,V_1,V_2,V_3\) each be split into two equal parity
classes.  On the first three cycle edges \(01,12,23\), join equal parities;
on the last edge \(30\), join opposite parities.  Every representation graph
has density \(1/2\), but there is no transversal \(4\)-cycle.

### Proof

The first three conditions force all selected parities to agree, while the
last requires the \(V_3,V_0\) parities to differ. \(\square\)

Thus even constant representation density on all four active edges does not
force a coherent point quadruple.  Dependent-random-choice estimates applied
to the four graphs separately are insufficient unless they retain cycle
consistency.

## 4. Representation threshold ledger

Let \(\lambda\) be the average number of point-pair representations per
selected value on active edges.  From (7), the represented edge mass is at
best
\[
 A_r r\lambda
 \gtrsim L^{7/3-\eta-o(1)}\lambda. \tag{11}
\]
The full height-point universe has \(Lm\asymp L^2\) vertices.  Even the
uncoloured threshold for forcing a graph \(4\)-cycle is of order
\[
 (L^2)^{3/2}=L^3.
\]
Thus this coarse route would require
\[
 \lambda\geq L^{2/3+\eta+o(1)}. \tag{12}
\]
The automatic lower bound is only one, while the maximum is \(O(L)\).
Moreover, an uncoloured \(4\)-cycle could use only two radius classes.
Therefore (12) is necessary for that coarse strategy but not sufficient.

At the dividing scale \(r=L^{5/6-\eta}\), the automatic representation
density on one \(m\times m\) edge is only
\[
 \frac r{m^2}=L^{-7/6-\eta}. \tag{13}
\]
Even the absolute upper bound of \(2m\) representations per squared value
would give density at most
\[
 \frac{2mr}{m^2}=O(L^{-1/6-\eta}). \tag{14}
\]
Thus no constant-density four-partite counting lemma or routine
dependent-random-choice argument is quantitatively reachable from the
current hypotheses.

The exact missing hypothesis is a **cycle-consistent representation
density**: on many active original-radius \(4\)-cycles, the four graphs in
(9) must contain a quantitatively adequate number of transversal point
cycles.  The parity example proves that marginal edge densities alone cannot
supply it.

The other side of Theorem 1 also remains open: a single block-pair overlap of
size \(L^{5/6-\eta-o(1)}\) is large but still \(o(m)\).  The one-pair
\(\cosh/\sinh\) construction from `HIGH_ENERGY_OVERLAP_STABILITY.md` shows
that large shifted square correlation alone does not force translate or
reflection structure.  A complete proof needs either a stronger inverse
statement for this strong-pair scale or the cycle-consistent statement above.

## 5. Labelled capacity barrier

All currently proved marginal capacities are consistent with an abstract
model in which every product fibre has the required correlations, the active
radius graph has many \(4\)-cycles, every active edge has the required
representation size, but parity labels frustrate every transversal cycle.

This model is not asserted to arise from real height sets.  It shows that the
next theorem must link algebraic representation signs to shifted-correlation
labels across products.  Edge counts, triangle capacities, and marginal
representation counts do not do so.

## 6. Verification

`verify_correlation_k4_joint_audit.py` checks the exponent ledger, the
\(C_4\)-free path-count inequality on exhaustive small graphs, and the
parity-frustrated four-partite construction.
