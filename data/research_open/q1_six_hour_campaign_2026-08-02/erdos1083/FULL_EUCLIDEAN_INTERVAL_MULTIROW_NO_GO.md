# Erdős #1083: an unbounded full-Euclidean multirow exact-block no-go

Date: 2026-08-02

Status: **NEW / AUTHOR-VERIFIED / NOT BLIND-AUDITED / NOT ADMITTED TO THE FINAL CLAIM LEDGER**

## 0. Result

The full local Euclidean exact-block interface, even together with one
common tangent and centre--leaf transversality, does not by itself force
a distance-budget contradiction.

Let \(S\ge3\) be nonsquare and let \(2\le C<S\).  Put

\[
 U=SC,\qquad
 \mathcal M=\{m:m\mid C,\ m^2<C\}.
\]

There is a genuine finite configuration in \(\mathbb R^3\) with one
centre row and one leaf row for every \(m\in\mathcal M\) such that:

1. all rows use scalar copies of one \(S\)-point source set \(X\);
2. every row has \(U\) positive tangent parameters;
3. every one of the \(SU=S^2C\) source--target pairs in a row gives a
   different squared-distance label;
4. every row gives exactly the same \(SU\)-element label set \(V\);
5. all rows share one literal tangent parameter;
6. the centre is rationally transverse to every leaf; and
7. all leaf rows are pairwise nontransverse.

If \(C\) is squarefree with \(k\) prime factors, then

\[
 |\mathcal M|=2^{k-1},
\]

so the number of full-interface rows is unbounded.  This is not a
counterexample to Erdős #1083 and not a counterexample to the
power-large hub theorem.  Indeed

\[
 |\mathcal M|<\sqrt C.
\]

At the frozen endpoint \(C=t^{1/18+o(1)}\), this construction has at
most

\[
 t^{1/36+o(1)}
\]

leaves, far below the required \(t^{5/9-o(1)}\).  Its role is to prove
that a closure theorem must use the power-large scale quantitatively;
merely upgrading the old theta record to all \(U\) Euclidean tangent
cells is still insufficient.

This candidate was produced after the author-swap admission window.  It
is retained as lane-local work with an executable author check, but it
is not part of the campaign's admitted final results until an independent
blind reconstruction is completed.

## 1. Exact interval tilings

Write

\[
 I_N=\{0,1,\ldots,N-1\},\qquad
 \beta=\frac1{S-1},\qquad
 \alpha=\frac1{\sqrt S},
\]

and take the common source parameter set

\[
 X=\beta I_S\subset[0,1].
\]

For \(m\mid C\), define

\[
 B_m=I_m\oplus Sm\,I_{C/m}.
\]

The mixed-radix identity

\[
 \boxed{mI_S\oplus B_m=I_{SC}}
\tag{1.1}
\]

is direct: every \(n\in I_{SC}\) has a unique expression

\[
 n=r+m(s+Sk),
\quad
 0\le r<m,\quad 0\le s<S,\quad 0\le k<C/m.
\]

Choose a translation \(R\), to be fixed in Section 2, and put

\[
\begin{aligned}
 V&=R+\alpha X\oplus\beta I_{SC},\\
 \lambda_0&=\alpha,
 &A_0&=R+\beta I_{SC},\\
 \lambda_m&=m,
 &A_m&=R+\alpha X\oplus\beta B_m
 \qquad(m\in\mathcal M).
\end{aligned}
\]

Equation (1.1) gives the exact row partitions

\[
\boxed{
 V=A_0\oplus\lambda_0X
   =A_m\oplus\lambda_mX
 \qquad(m\in\mathcal M).
}
\tag{1.2}
\]

All sums are direct.  In particular,

\[
 |X|=S,\qquad |A_i|=SC=U<S^2,\qquad |V|=SU=S^2C.
\]

## 2. Heights and a common positive tangent

Set

\[
 \rho^2=\frac{S-1}{4S}
 \quad\Longleftrightarrow\quad
 \frac1{4\rho^2}=\beta S,
\]

and define positive row heights by

\[
 z_i=\frac{\lambda_i}{2\rho}.
\]

Then

\[
 z_0^2=\beta,\qquad z_m^2=\beta Sm^2.
\tag{2.1}
\]

For \(m^2<C\), the element \(Sm^2\) belongs to \(B_m\): take
\(r=0\) and \(k=m<C/m\).  Thus \(A_0\) contains \(R+z_0^2\), while
every \(A_m\) contains \(R+z_m^2\).

Define the complete tangent sets

\[
 T_i=A_i-\rho^2-z_i^2.
\tag{2.2}
\]

They all contain

\[
 \boxed{\tau_*=R-\rho^2.}
\tag{2.3}
\]

Choose

\[
 R>\rho^2+\max_i z_i^2.
\tag{2.4}
\]

Every element of every \(A_i-R\) is nonnegative, so (2.4) makes all
members of all \(T_i\) positive.  Translation changes no direct-sum
or cardinality statement.

## 3. Genuine Euclidean realization of all cells

Fix any \(A>\rho\).  For \(x\in X\), take the source point

\[
 p_x=(A+\rho\sqrt{1-x^2},0,\rho x).
\tag{3.1}
\]

These are \(S\) distinct points on a circle of radius \(\rho\).  For
every row \(i\) and every \(\tau\in T_i\), take the target

\[
 q_{i,\tau}=(A,\sqrt\tau,-z_i).
\tag{3.2}
\]

All square roots are real and nonzero.  Direct expansion gives

\[
\begin{aligned}
 \|p_x-q_{i,\tau}\|^2
 &=\rho^2(1-x^2)+\tau+(\rho x+z_i)^2\\
 &=\rho^2+z_i^2+\tau+2\rho z_i x\\
 &=\rho^2+z_i^2+\tau+\lambda_i x.
\end{aligned}
\tag{3.3}
\]

Because \(A_i=\rho^2+z_i^2+T_i\), (1.2) and (3.3) show that for every
row the map

\[
 T_i\times X\longrightarrow V,\qquad
 (\tau,x)\longmapsto\|p_x-q_{i,\tau}\|^2
\]

is a bijection.  This realizes every one of the \(U\) tangent cells,
not merely one selected theta record.  Equation (2.3) gives an actual
target \(q_{i,\tau_*}\) in every row.

Targets in different rows are distinct because the positive heights
\(z_0,z_m\) are distinct; targets in one row are distinct because
their tangent parameters are distinct.  Their second coordinate is
nonzero, so no target is a source point.

## 4. Exact rational transversality

The source difference space is

\[
 W=\operatorname{span}_{\mathbb Q}(X-X)=\beta\mathbb Q.
\]

Every leaf space is

\[
 \lambda_mW=m\beta\mathbb Q=\beta\mathbb Q,
\]

whereas the centre space is

\[
 \lambda_0W=\alpha\beta\mathbb Q.
\]

Since \(S\) is nonsquare, \(\alpha\notin\mathbb Q\), and hence

\[
 \lambda_0W\cap\lambda_mW=\{0\}.
\]

Thus all centre--leaf pairs are transverse, while all leaf pairs are
nontransverse, exactly as in the fixed-tangent windmill.

## 5. Size boundary and the \(N^{3/5-o(1)}\) interface

For squarefree \(C\), complementary divisors pair as
\(m\leftrightarrow C/m\).  Since \(C\) is not a square, exactly one
member of each pair lies below \(\sqrt C\), giving
\(|\mathcal M|=2^{\omega(C)-1}\).

For arbitrary \(C\), every \(m\in\mathcal M\) is a different positive
integer below \(\sqrt C\), so \(|\mathcal M|<\sqrt C\).  Under
\(C=t^{1/18+o(1)}\), the row exponent is therefore at most \(1/36\),
whereas the heavy-factor hub supplies \(5/9-o(1)\).  The gap is

\[
 \frac59-\frac1{36}=\frac{19}{36}.
\]

Accordingly this no-go does not weaken the signed-switch barriers.  It
isolates their quantitative role: a full Euclidean exact block can
support arbitrarily many clean same-line leaves, but not at the
power-large scale needed by the campaign.

Nothing here improves the inherited public lower bound
\(N^{3/5-o(1)}\).  The construction is a local exact-block interface,
has far fewer than the \(N=t^5\) points in the public problem, and
does not address stability from near-extremal geometry.

## 6. Reproduction

Run

    python3 verify_full_euclidean_interval_multirow_nogo.py
    python3 -m pytest -q test_full_euclidean_interval_multirow_nogo.py

The verifier checks the direct mixed-radix tilings, every row
partition, the common tangent anchors, positivity, exact Euclidean
distance identities, transversality parameters, squarefree row count,
and the frozen exponent comparison.
