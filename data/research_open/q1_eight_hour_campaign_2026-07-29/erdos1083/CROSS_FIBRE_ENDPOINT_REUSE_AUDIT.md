# Cross-fibre endpoint reuse: a retained triangle tensor and its gap

Date: 2026-07-30

## Purpose

`GLOBAL_HYPERBOLA_NETWORK_AUDIT.md` shows that an abstract network of
truncated blocks can saturate every known overlap exponent.  The tensor
becomes non-geometric only when repeated occurrences of the same radius
class are required to use one common height set \(Z_u\).

This note writes that requirement as an exact triangle tensor across product
fibres.  It proves two unconditional facts.

1. Every radius triangle carries \(\Omega(m^2)\) distinct compatible triples
   of full squared-difference values.
2. Under the small-\(M\) hypothesis, one can choose common-size truncations
   that simultaneously retain the forced within-fibre correlation and at
   least
   \[
   L^{3-3\eta-o(1)}
   \]
   cross-fibre compatible triples.

This does not yet supply the missing \(L^{1/3+2\eta}\) propagation.  The
retained compatibility tensor has average degree at most constant, and for
\(\eta>0\) its guaranteed average degree tends to zero when measured against
all block--value incidences.  More importantly, the compatible triples may
use values disjoint from those carrying the large within-fibre correlation.

A dense mod-seven selection on globally shared height sets deletes every
selected triangle test.  Hence endpoint reuse plus marginal selected-value
density does not align the two tensors.  The remaining input is a **joint
overlap--triangle moment**, not another marginal Cauchy or DRC estimate.

No exponent improvement is claimed.

## 1. The exact endpoint hypergraph

Let the radius classes be \(u\in[L]\), each with one fixed \(m\)-point set
\[
 Z_u=\{z_{u,1},\ldots,z_{u,m}\}\subset\mathbb R.
\]
For a radius pair \(uv\), put
\[
 Y_{uv}=(Z_u-Z_v)^2.
\]
The same vertex \(u\) occurs in the \(L-1\) blocks \(Y_{uv}\).  At the
point-pair level this is the image of the complete multipartite edge tensor
\[
 (u,i;v,j)\longmapsto (z_{u,i}-z_{v,j})^2. \tag{1}
\]

For three distinct radius classes \(u,v,w\), every point triple
\((i,j,k)\) produces
\[
\begin{aligned}
 a&=(z_{u,i}-z_{v,j})^2\in Y_{uv},\\
 b&=(z_{u,i}-z_{w,k})^2\in Y_{uw},\\
 c&=(z_{v,j}-z_{w,k})^2\in Y_{vw}.
\end{aligned}
\]
These values lie in three different product fibres and obey
\[
 (a+b-c)^2=4ab. \tag{2}
\]
Indeed, after writing
\(x=z_{u,i}-z_{v,j}\) and \(y=z_{u,i}-z_{w,k}\), one has
\(c=(y-x)^2\), so \(a+b-c=2xy\).

Equation (2) is the minimal cross-fibre consistency equation omitted by the
independent affine-line tensor.

## 2. Full blocks contain many distinct tests

### Theorem 1 (endpoint reuse creates a triangle tensor)

For every three \(m\)-point real sets \(Z_u,Z_v,Z_w\), their three
squared-difference sets contain at least
\[
 \frac{m^2}{4} \tag{3}
\]
distinct triples \((a,b,c)\) satisfying (2).

Consequently all radius triangles together contain
\[
 \Omega(L^3m^2)=\Omega(L^5) \tag{4}
\]
scoped compatible triples in the balanced regime \(m\asymp L\).

### Proof

There are \(m^3\) point triples.  Fix one value triple \((a,b,c)\).
After choosing \(z_{u,i}\), there are at most two possibilities for
\(z_{v,j}=z_{u,i}\pm\sqrt a\) and at most two for
\(z_{w,k}=z_{u,i}\pm\sqrt b\).  Thus one value triple has at most \(4m\)
point preimages.  Division gives (3), and summing over the
\(\binom L3\) scoped radius triangles gives (4). \(\square\)

This also proves that a generic independent-fibre affine tensor cannot be a
global squared-difference system.  Assign its symbol values one product
fibre at a time.  Since the three edges of a radius triangle lie in three
different fibres, each new symbol is constrained by only finitely many
nonzero polynomial equations of the form (2); choose outside their finite
root sets.  The resulting numerical tensor has no compatible cross-fibre
triple, contradicting Theorem 1 if a shared family \((Z_u)\) existed.

## 3. Large full blocks already give the target

Let
\[
 I_{\rm full}=\sum_{u<v}|Y_{uv}|.
\]
Inside one product fibre there are at most \(L\) blocks, so every parameter
value is counted at most \(L\) times.  Therefore
\[
 M\geq \frac{I_{\rm full}}L. \tag{5}
\]
Under the counterassumption
\[
 M\leq L^{8/3+\eta}, \tag{6}
\]
one necessarily has
\[
 I_{\rm full}\leq L^{11/3+\eta}. \tag{7}
\]

Fix any \(\delta>0\), and call a radius-pair block large when
\[
 |Y_{uv}|>S_0,\qquad
 S_0=L^{5/3+\eta+\delta}. \tag{8}
\]
Equation (7) shows that there are at most
\[
 L^{2-\delta} \tag{9}
\]
large blocks.  Hence at most \(L^{3-\delta}\) radius triangles touch a
large block.  All but \(o(L^3)\) radius triangles have three block sizes at
most \(S_0\).

## 4. Joint truncation retaining both marginals

Choose a common
\[
 k=cm=\Theta(L)
\]
not exceeding any \(|Y_{uv}|\), and independently select a uniformly random
\(k\)-subset
\[
 \widetilde Y_{uv}\subseteq Y_{uv}. \tag{10}
\]
Let \({\cal T}\) count scoped compatible triples from Theorem 1 that survive
in the three corresponding truncated blocks.

### Theorem 2 (simultaneous correlation and compatibility retention)

Under (6), there is a deterministic choice of the truncations (10) such
that:

1. their within-product-fibre correlation mass is at least
   \[
   L^{10/3-\eta-o(1)}; \tag{11}
   \]
2. they contain at least
   \[
   {\cal T}\geq L^{3-3\eta-o(1)} \tag{12}
   \]
   scoped cross-fibre triples satisfying (2).

### Proof

The shifted truncated blocks have total incidence
\[
 I_0=\Theta(L^3)
\]
and union contained in the full parameter-line union of size \(M\).
Therefore Cauchy--Schwarz gives (11) for **every** choice of truncations.

Now restrict to the \(L^3-o(L^3)\) radius triangles with all three block
sizes at most \(S_0\).  Each has at least \(m^2/4\) distinct compatible
triples.  One fixed triple survives with probability at least
\[
 \left(\frac{k}{S_0}\right)^3.
\]
Consequently
\[
\begin{aligned}
 \mathbb E{\cal T}
 &\gtrsim
 L^3m^2\left(\frac{k}{S_0}\right)^3\\
 &\gtrsim
 L^{3-3\eta-3\delta}. \tag{13}
\end{aligned}
\]
Some realization attains the expectation and still satisfies the
deterministic correlation bound (11).  Taking \(\delta=o(1)\), or an
arbitrarily small fixed loss, gives (12). \(\square\)

Theorem 2 is a genuine coupling of the two previously separate global
marginals.  It does not say that the values counted in (11) occur in the
triples counted in (12).

## 5. Why DRC, entropy and incidence still stop

There are \(\Theta(L^2)\) blocks and \(\Theta(L^3)\) truncated block--value
incidences.  The guaranteed triangle-test count (12) has incidence-normalized
average
\[
 \frac{\mathcal T}{I_0}
 =L^{-3\eta-o(1)}. \tag{14}
\]
For \(\eta>0\), a generic incidence participates in no guaranteed compatible
test; even at \(\eta=0\), only constant average test degree is forced.
Standard DRC cannot extract a polynomial-degree common neighbourhood from
this marginal.

Shearer or entropy inequalities recover the same retention product
\((k/|Y_{uv}|)(k/|Y_{uw}|)(k/|Y_{vw}|)\); without an upper bound better than
(8), they do not improve (13).  Generic polynomial incidence estimates also
do not help: (2) is the one-dimensional group-like sign equation and the
sets on its three coordinates vary with the radius triangle.

Most importantly, let
\[
 {\cal C}=\{(e,t):t\in\widetilde Y_e
 \text{ has high within-fibre multiplicity}\}
\]
and let \({\cal A}\) be the block--value incidences occurring in compatible
triples.  Equations (11) and (12) are separate lower bounds on weighted
\({\cal C}\) and on triples supported by \({\cal A}\).  They give no lower
bound on
\[
 |{\cal A}\cap{\cal C}|. \tag{15}
\]
An abstract direct-sum tensor can reserve disjoint halves of every block for
the affine-line correlation cores and for triangle-compatible symbols,
saturating both marginals while making (15) zero.

## 6. A shared-endpoint selection can erase every test

The failure of (15) is not only an arbitrary-set phenomenon.

### Proposition 3 (dense selected values with zero triangle tests)

Let \(m\) be divisible by seven and take
\[
 Z_u=\{0,1,\ldots,m-1\}
\]
for every radius class \(u\).  On every radius-pair block select squared
differences whose signed roots are congruent to \(\pm1\pmod7\).

Each selected block has exactly \(2m/7\) values and its representation graph
has exactly \(2m^2/7\) point pairs, but no radius triangle has a selected
compatible value triple, hence no compatible point triple.

### Proof

The counts are the same uniform residue counts as in the mod-seven audit.
For a point triangle, the three oriented signed differences sum to zero.
If all three were congruent to \(\pm1\pmod7\), their sum would be one of
\(\pm1,\pm3\), never zero modulo seven.  The polynomial identity (2) is
equivalent to the existence of signs for which the three square roots obey
this signed sum, so it also has no selected value solution. \(\square\)

Thus even globally shared \(Z_u\), linear selected-value density and
constant representation density do not force selected cross-fibre tests.
The strong within-fibre correlations must be shown to align with the full
endpoint triangle tensor; endpoint reuse alone is insufficient.

## 7. Exact remaining input

The remaining desired statement is deliberately **conditional and
unproved**:

> A small global parameter-line union forces a positive-power lower bound
> for a joint overlap--triangle moment in which the same selected
> block--value incidences both have high within-fibre reuse and participate
> in cross-fibre equations (2).

To close the previously identified gap, that joint moment must yield at
least \(L^{1/3+2\eta}\) more propagation than the common-value reuse bound.
Neither Theorem 2 nor any marginal Cauchy, DRC, entropy or generic incidence
estimate supplies it.

The minimal obstruction to the global affine tensor is now known exactly:
full shared-endpoint systems must contain \(\Omega(L^5)\) polynomially
compatible value triples.  The minimal unresolved step is to prove that
enough of those triples survive on the values carrying the forced
within-fibre correlation.

## 8. Verification

`verify_cross_fibre_endpoint_reuse.py` checks the triangle polynomial,
the \(4m\) fibre bound on point preimages, exhaustive small-set instances of
Theorem 1, the full exponent ledger, and the mod-seven zero-test
construction.
