# Independent audit of the general-\(k\) extremal coefficients

Date: 2026-07-30

## Verdict

The two endpoint arguments in `GENERAL_K_POSITIVITY_ATTACK.md` pass an
independent algebraic and combinatorial audit.  In the stable range
\(s\geq k+3\),

\[
(A_1^{(k)})^2-A_0^{(k)}A_2^{(k)}
=2k(k-1)\beta^4K_k(s,\beta)
\]

has exact degree \(4k-4\), and hence

\[
\deg_\beta K_k=4(k-2),\qquad
[\beta^{4(k-2)}]K_k
=2k^{2k-5}s^{2k-4}.
\]

This audit does **not** prove that the intermediate coefficients of \(K_k\)
are nonnegative and does not prove \(B_k\geq_{\rm coeff}0\) for arbitrary
\(k\).

## Low endpoint

For profile \(h\), a contracted core block of weight \(w\in\{1,2\}\) and a
fixed page form one weighted edge position with generating factor
\(1+wz\).  A weight-two position is not two independently selectable parallel
edges: its coefficient two records the two original spoke choices after
contracting a forced core edge.  With that interpretation, the cycle-free
argument is sound.

Across the two factors of \(H_1^2\), and likewise across \(H_0H_2\), there
are exactly \(2k\) positions of weight two and \(2k(s-2)\) positions of
weight one.  Therefore the unrestricted edge-selection polynomials agree:

\[
E_1(z)^2=E_0(z)E_2(z).
\]

At fewer than four selected edges a simple bipartite graph has no cycle.  At
four edges the only possible cycle is \(K_{2,2}\).  Its total weight in
profile \(h\) is

\[
C_h=\binom{k}{2}\sum_{i<j}w_i^2w_j^2.
\]

Writing \(s-2h\) unit blocks and \(h\) double blocks gives

\[
\sum_{i<j}w_i^2w_j^2
=\binom{s-2h}{2}+4h(s-2h)+16\binom h2.
\]

Direct second differencing at \(h=0,1,2\) yields four.  Since forest weight is
unrestricted weight minus rejected-cycle weight,

\[
[\beta^4](H_1^2-H_0H_2)
=C_0+C_2-2C_1
=2k(k-1).
\]

All lower coefficients vanish.  The extracted power
\((1+k\beta)^{2s-2k-2}\) has constant term one, so this is also the low
coefficient of the \(A\)-determinant.

## High endpoint

For a connected component containing core-block set \(I\) and page set
\(J\), with \(a=|I|\), \(b=|J|\), the weighted complete-bipartite
Matrix--Tree formula is

\[
\beta^{a+b-1}b^{a-1}
\left(\sum_{i\in I}w_i\right)^{b-1}
\prod_{i\in I}w_i.
\]

Partitioning all labelled vertices into their connected components therefore
gives an exact positive sum.  Temporarily labelling \(c\) nonempty
components counts every set partition \(c!\) times, so the factor \(1/c!\)
in the displayed multinomial formula is legitimate even when two components
have the same size profile.

Let \(W_{h,c}\) be the coefficient contributed by forests with \(c\)
components.  Since

\[
H_h=(1+k\beta)^{e_h}A_h,\qquad
e_h=s-2h-k+1,
\]

the leading three coefficients of \(A_h\) are obtained triangularly from
\(W_{h,1},W_{h,2},W_{h,3}\).  The stability hypothesis is exactly what is
needed to ensure \(e_h\geq0\) simultaneously for \(h=0,1,2\).

The leading coefficient is

\[
L_h=2^hk^{h+k-2}s^{k-1},
\]

so \(L_1^2=L_0L_2\).  The normalized next coefficient \(r_h\) is affine in
\(h\), with common first difference

\[
\delta=\frac{s+2k-2}{2sk}.
\]

Thus the top two determinant degrees cancel.  At the next degree the
three-component calculation gives

\[
2q_1-q_0-q_2
=\frac{4(k-1)-(s+2k-2)^2}{4k^2s^2},
\]

while affineness gives

\[
r_1^2-r_0r_2=\delta^2.
\]

The square terms cancel exactly and leave

\[
L_1^2\frac{k-1}{k^2s^2}
=4k^{2k-4}(k-1)s^{2k-4}>0.
\]

Because \(\deg A_h=h+2k-2\), no higher determinant term survives.  Dividing
by \(2k(k-1)\beta^4\) gives the claimed degree and top coefficient of
\(K_k\).

## Executable cross-check

The independent component-partition verifier was rerun successfully.  It:

- reconstructs the one-, two-, and three-component sums without using the
  Bell-state transfer;
- checks the formulas at \(k=2,\ldots,7\) and two stable \(s\)-values;
- compares with the saved \(K_2,\ldots,K_7\) top coefficients;
- checks the four-cycle second difference for \(k=2,\ldots,19\).

The static audit certificate has SHA-256
`1daa8d899a69dcb036582fc9b3d41421737fad656ae16378ccd122fac1738e5d`.

## Scope firewall

Endpoint positivity is substantially weaker than coefficientwise positivity.
In particular, it cannot be used to infer any of the following:

- nonnegativity of every coefficient of \(K_k\);
- total positivity of the nilpotent transfer layers;
- coefficientwise nonnegativity of \(F_k\);
- the complete-split-graph Rayleigh conjecture for unbounded \(k\).

The saved negative minor at the \((0,1)\) layer remains a genuine obstruction
to a layer-preserving TP2 or Lindström proof.  Any general proof must perform
cross-layer cancellation.
