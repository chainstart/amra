# Interface audit of the endpoint Følner counterexample

Date: 2026-08-01

## Verdict

All five interfaces requested for the construction pass.  The exact
logical consequence is the falsity of Qualitative Stability assertion
QS in APPROXIMATE_STABILITY_COUNTEREXAMPLE.md.  The audit does not
upgrade the construction to a full critical spectral block or to a
counterexample to Erdős #1083.

## 1. One genuinely common spectrum

The set

\[
 V=C+\{a+b\sqrt2:0\le a,b<L\}
\]

is defined before and independently of \(r\).  The embedding
\((a,b)\mapsto a+b\sqrt2\) is injective on \(\mathbb Z^2\).

For each \(r\), the core \(S\)-blocks are subsets of the same lattice
box \(Q_L\).  Every remote block starts at second coordinate \(2L\)
and moves in the positive direction \((1,r)\), so none of its points
belongs to \(Q_L\).  Injectivity of the embedding therefore gives the
exact identity

\[
 V_r\cap V
 =C+\iota(\text{covered core in direction }(1,r)).
\]

There is no \(r\)-dependent translation hidden in \(V\).

## 2. Cardinality and set status of \(T_r\)

The directional line partition has \(E_r\) uncovered points.  Since
\(S\mid L^2\) and the covered portion is a union of \(S\)-blocks,
\(S\mid E_r\).  Hence

\[
 |\mathcal A_r^{\rm core}|=(L^2-E_r)/S,\qquad
 |\mathcal A_r^{\rm out}|=E_r/S.
\]

The two start sets are disjoint, so

\[
 |A_r|=|\mathcal A_r|=L^2/S=U.
\]

Translation by the fixed real \(1+z_r^2\) is a bijection, and

\[
 T_r=A_r-1-z_r^2
\]

is therefore a genuine \(U\)-element set, not a multiset.

The union estimate uses no assumed overlap:

\[
 \left|\bigcup_{r=1}^mT_r\right|
 \le\sum_{r=1}^m|T_r|
 =mU=m^{61}<m^{72}=t.
\]

Thus the tangent cap holds even in the worst case that all the
\(T_r\)'s are disjoint.

## 3. Positivity and distinct summands

All lattice starts have nonnegative coordinates, hence positive real
embedding after the common translation.  For \(r\le m\),

\[
 z_r^2
 =\frac{(S-1)^2}{4}(1+2r^2+2r\sqrt2)
 <3S^2m^2.
\]

With \(C=10S^2m^2+10\), every
\(\tau\in T_r\) satisfies

\[
 \tau>C-1-z_r^2>7S^2m^2+9>0.
\]

The \(S\) elements \(j/(S-1)\) of \(X\) are distinct.  The \(U\)
tangent squares are distinct because the base starts are distinct.
Within a row, the core blocks are disjoint by the maximal-line
partition; the remote blocks are disjoint because equality of their
second coordinates forces equal step indices and then equal start
indices.  Core and remote blocks are separated by their second
coordinates.  Consequently every one of the \(SU\) sums

\[
 1+z_r^2+\tau+2z_rx
\]

has a unique pair \((\tau,x)\).

## 4. Error normalization

Both \(V_r\) and \(V\) have exactly

\[
 |V_r|=|V|=SU=L^2
\]

elements.  Their intersection has \(SU-E_r\) elements, so

\[
 |V_r\mathbin\triangle V|=2E_r.
\]

Therefore “relative to \(SU\)” and “relative to \(|V|\)” are literally
the same normalization.  Uniformly for \(1\le r\le m\),

\[
 \frac{|V_r\mathbin\triangle V|}{SU}
 <\frac{2(r+1)S}{L}
 \le\frac{2(m+1)}{m^2}\longrightarrow0.
\]

## 5. Exact scope of the refutation

The construction refutes this universal implication:

> if endpoint-sized rows are exact direct sums and all lie within
> \(o(SU)\) symmetric difference of one \(SU\)-element spectrum, then
> their pairwise transverse rational dilation rank is bounded.

It does **not** refute any of the following stronger statements:

1. stability with error \(o(t^{-1/36}SU)\);
2. stability assuming \(t^{13/18}\) rows in one block together with
   critical average tangent multiplicity;
3. a theorem that uses multirow parabolic identities rather than
   rowwise near-tiling alone;
4. the global distinct-distance conjecture in Erdős #1083.

The construction has only \(t^{1/72}\) transverse representatives.
That tends to infinity and is sufficient to disprove QS, but it is
far below the critical block row count.  This distinction must remain
in every summary.
