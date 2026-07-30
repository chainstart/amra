# Erdős #1083: critical high-rich reverse-circle concentration

Date: 2026-07-30

## 0. Result

Fix one source axial plane \(\Pi_\alpha\), and retain the
nonperpendicular, positive-radius, incidence-active reverse circles
used in `EUCLIDEAN_HUB_INCIDENCE_EXPANSION_THEOREM.md`.
Let
\[
|P_\alpha|\le Q=t^{3+o(1)},\qquad
|\mathcal A|\le M=t^{1+o(1)},\qquad
|\mathcal D|\le t^{3+o(1)}.
\tag{1}
\]
Merge equal normalized circle equations.  For a resulting geometric
circle \(C\), put
\[
s(C)=|P_\alpha\cap C|,
\qquad
\mu(C)=
\#\{(\beta,q,d):\Gamma_{\beta,q,d}=C\}.
\tag{2}
\]

### Theorem

For every fixed \(\eta>0\), let
\[
\mathcal H_\eta
=
\{C:s(C)\ge t^{9/4+\eta}\}.
\tag{3}
\]
For all sufficiently large \(t\):

1. every two distinct circles in \(\mathcal H_\eta\) are aligned;
2. since all circles lie in the fixed plane \(\Pi_\alpha\), they have
   one common centre and common perpendicular axis;
3. the sets \(P_\alpha\cap C\), \(C\in\mathcal H_\eta\), are pairwise
   disjoint;
4. every merged circle weight satisfies
   \[
   \mu(C)\le M;
   \tag{4}
   \]
5. consequently the high-rich weighted incidence mass obeys
   \[
   \boxed{
   W_{\rm high}
   :=
   \sum_{C\in\mathcal H_\eta}\mu(C)s(C)
   \le MQ
   =t^{4+o(1)}.
   }
   \tag{5}
   \]

For the hub parameters
\[
L=t^{2-2\kappa-o(1)},\qquad
H=t^{5-\kappa-o(1)}
\tag{6}
\]
with fixed \(0<\kappa<1\), the principal hub mass is
\[
LH=t^{7-3\kappa-o(1)}.
\tag{7}
\]
Thus
\[
\frac{W_{\rm high}}{LH}
\le
t^{-3(1-\kappa)+o(1)}
=o(1).
\tag{8}
\]
The high-rich sector cannot carry the principal hub mass.  After the
standard empty, perpendicular, and zero-radius removals, mass
\(t^{7-3\kappa-o(1)}\) remains on active circles satisfying
\[
s(C)<t^{9/4+\eta}.
\tag{9}
\]

This is a concentration corollary, not a distinct-distance exponent
improvement.

## 1. Pairwise alignment from the known two-circle theorem

Take distinct \(C_1,C_2\in\mathcal H_\eta\), and write
\[
P_i=P_\alpha\cap C_i,\qquad |P_i|=s_i.
\]
Two distinct circles meet in at most two points.  Deleting their
intersection, if necessary, changes neither exponent.

Every retained reverse circle has nonzero radial centre parameter
\[
A_i=\cos(\alpha-\beta)v\ne0.
\tag{10}
\]
As proved in
`MATHIALAGAN_SHEFFER_CIRCLE_CLASSIFICATION_BRIDGE.md`, the
perpendicular Mathialagan--Sheffer exception would require
\(A_1=A_2=0\), and is therefore impossible.

If \(C_1,C_2\) were not aligned, Mathialagan--Sheffer Theorem 1.4(b)
would give
\[
\begin{aligned}
|\Delta^2(P_1,P_2)|
&\gg
\min\{s_1^{2/3}s_2^{2/3},s_1^2,s_2^2\}\\
&\ge
t^{3+4\eta/3}.
\end{aligned}
\tag{11}
\]
This contradicts the global bound in (1), including its \(t^{o(1)}\)
loss, for sufficiently large \(t\).  Hence all pairs in
\(\mathcal H_\eta\) are aligned.

The source circles all lie in \(\Pi_\alpha\).  Their axes are lines
orthogonal to \(\Pi_\alpha\), so two such axes coincide exactly when
their centres coincide.  Pairwise alignment therefore gives a common
centre.  Distinct normalized circle classes with that centre have
different radii, and concentric circles in one plane are disjoint.
This proves assertions 1--3.

## 2. The triple-multiplicity cap

Fix one retained target plane \(\Pi_\beta\).  The reverse-circle
injectivity lemma states that
\[
(q,d)\longmapsto\Gamma_{\beta,q,d}
\tag{12}
\]
is injective on this plane.  Hence a fixed normalized geometric circle
\(C\) can arise from at most one pair \((q,d)\) for this fixed
\(\beta\).  Summing over at most \(M\) retained target planes gives
\[
\mu(C)\le M.
\tag{13}
\]

This count allows the same label \(d\) to occur on different target
planes and allows different labels to produce the same circle on
different planes.  It only uses the precise statement that one fixed
plane contributes at most one triple to one fixed merged circle
class.

Since the high-rich incidence sets are pairwise disjoint subsets of
\(P_\alpha\),
\[
\sum_{C\in\mathcal H_\eta}s(C)\le Q.
\tag{14}
\]
Equations (13)--(14) prove (5).

## 3. Comparison with the full hub mass

The hub lower bound sums representations over \(L\) labels and is
\(LH\).  Empty circles contribute nothing.  The perpendicular target
plane was deleted before the matching-or-hub extraction.  A
zero-radius circle has at most one source incidence, so all
zero-radius triples contribute at most
\[
MQL
=t^{6-2\kappa+o(1)}.
\tag{15}
\]
For fixed \(\kappa<1\),
\[
(7-3\kappa)-(6-2\kappa)=1-\kappa>0.
\tag{16}
\]
Thus the zero-radius sector is \(o(LH)\), and the retained
positive-radius active circles still carry
\(t^{7-3\kappa-o(1)}\) mass.  Combining this with (5) proves
(8)--(9).

## 4. Exact boundary

The argument does not show that a low-rich circle has few target
triples, nor does it improve the existing multiplicity lower bound.
It proves only that the hub mass cannot hide on circles having more
than \(t^{9/4+\eta}\) source incidences.

The next possible gain must use the simultaneous constraints
\[
s(C)<t^{9/4+\eta},\qquad
\mu(C)\le M,
\tag{17}
\]
together with the total weighted incidence lower bound.  No exponent
gain is claimed here.
