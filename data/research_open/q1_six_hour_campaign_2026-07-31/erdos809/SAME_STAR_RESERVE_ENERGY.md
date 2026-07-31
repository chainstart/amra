# Erdős #809 — same-neighbourhood star reserve energy

Date: 2026-08-01

Status: PROVED__SAME_TYPE_STAR_LEAVES_FORCE_QUADRATIC_B_RESERVE

## 1. Main theorem

Put
\[
 \kappa=n-2\delta(G).
\tag{1}
\]
Fix an active zero-shore centre \(b\in B\), and let
\[
 L=\{c_1,\ldots,c_\ell\}\subseteq B
\tag{2}
\]
be distinct same-neighbourhood-type zero-shore neighbours of \(b\).

### Theorem 1.1 (same-star reserve energy)

\[
 \boxed{
 |\mathcal Q|
 \ge
 M_B[L]
 \ge
 \binom{\ell}{2}-\kappa\ell.
 }
\tag{3}
\]
In particular, the lower bound is positive once
\(\ell\ge2\kappa+2\), and is quadratic when
\(\ell\gg\kappa\).

#### Proof

Put \(P=N(b)\).  Every leaf lies outside \(P\), because \(bc\) is a
missing pair.  For a same-type leaf \(c\), the exact zero-star
classification gives
\[
 |N(c)\mathbin\triangle P|\le2\kappa.
\tag{4}
\]
Therefore
\[
 |N(c)\setminus P|\le2\kappa.
\tag{5}
\]
Since all leaves lie outside \(P\), the degree of \(c\) inside \(G[L]\)
is at most \(2\kappa\).  Summing degrees gives
\[
 e(G[L])\le\kappa\ell.
\tag{6}
\]
Consequently
\[
 M_B[L]
 =\binom{\ell}{2}-e(G[L])
 \ge\binom{\ell}{2}-\kappa\ell.
\]
Every missing edge internal to \(L\) is incident with endpoints of
active zero-shore pairs, so it belongs to the global reserve union
\(\mathcal Q\).  This proves (3). \(\square\)

## 2. Weighted consequence

Let \(h_c\ge2\) be the multiplicity of the repeated zero pair \(bc\),
and put
\[
 W_L=\sum_{c\in L}(h_c-1).
\tag{7}
\]
The same-type multiplicity theorem gives
\[
 h_c\le\kappa.
\tag{8}
\]
Thus \(\kappa\ge2\) and
\[
 \ell\ge
 \ell_0:=
 \left\lceil\frac{W_L}{\kappa-1}\right\rceil.
\tag{9}
\]
If \(\ell_0\ge2\kappa+2\), the right side of (3) is increasing for
all \(\ell\ge\ell_0\), and hence
\[
 \boxed{
 |\mathcal Q|
 \ge
 \binom{\ell_0}{2}-\kappa\ell_0.
 }
\tag{10}
\]

Under global reserve failure, (10) must be at most \(D_B-1\).  Its
violation closes the \(B\)-defect budget.  Combined with the
matching--star concentration theorem, this is an explicit exit for
the same-type branch whenever the forced coherent star carries enough
excess relative to \(\kappa^2\).

There is also a closed-form upper bound valid without the threshold in
(10).  Put
\[
 L(q,\kappa)=
 \left\lfloor
 \frac{2\kappa+1+
 \sqrt{(2\kappa+1)^2+8q}}2
 \right\rfloor.
\tag{11}
\]
Equation (3) implies
\[
 \ell^2-(2\kappa+1)\ell-2|\mathcal Q|\le0,
\]
and hence
\[
 \boxed{
 \ell\le L(|\mathcal Q|,\kappa),
 \qquad
 W_L\le(\kappa-1)L(|\mathcal Q|,\kappa).
 }
\tag{12}
\]
Under reserve failure one may replace \(|\mathcal Q|\) by \(D_B-1\).
If the coherent star selected from a maximal matching of size \(f\)
is of the same type, Theorem 2.1 of
MATCHING_STAR_CONCENTRATION.md and (12) give the global necessary
condition
\[
 \boxed{
 E_0
 \le
 4f(\kappa-1)L(D_B-1,\kappa).
 }
\tag{13}
\]
Thus a violation of (13) rules out the same-type concentration branch
entirely.

## 3. Scope firewall

At fixed \(s\), one has \(\kappa=(2s+o(1))n\), so a merely linear
coherent-star weight need not make \(\ell_0\) large.  Equation (3)
does not synchronize different centres and does not control the
outer-\(A\) residue.  It is an exact quadratic reserve criterion, not
a solution of the maximum-degree branch or Erdős #809.
