# Erdős #809 — opposite-star reserve and residual energy

Date: 2026-08-01

Status: PROVED__OPPOSITE_STAR_MASS_AND_RESIDUAL_FORCE_ACTUAL_B_RESERVE

## 1. Outcome

The weighted residual moment from the seventh attack did not previously
interact directly with the exact global reserve obstruction.  For a
single opposite-neighbourhood zero-star, there is an exact interaction.

Retain
\[
 A=N[v],\qquad B=V(G)\setminus A,\qquad m=|A|,
\]
where \(v\) has maximum degree, so every vertex has degree at most
\(m-1\).  Fix \(b\in B\), and let
\[
 L=\{c_1,\ldots,c_\ell\}\subseteq B
\tag{1}
\]
be distinct opposite-type active zero-shore neighbours of \(b\).
For each \(c\in L\), let
\[
 h_c\ge1
\]
be the colour multiplicity of \(bc\), and define
\[
 \rho_c=n-d(b)-d(c).
\tag{2}
\]
Put
\[
 H_L=\sum_{c\in L}h_c,\qquad
 W_L=\sum_{c\in L}(h_c-1),\qquad
 R_L=\sum_{c\in L}\rho_c,
\tag{3}
\]
and
\[
 \lambda=m+1-\delta(G).
\tag{4}
\]

### Theorem 1.1 (exact opposite-star reserve energy)

The global reserve union satisfies
\[
 \boxed{
 2|\mathcal Q|
 \ge
 2\sum_{c\in L}(h_c+\rho_c-\lambda)
 -
 \sum_{c\in L}
 \min\{\ell-1,\rho_c-2\}.
 }
\tag{5}
\]
In particular,
\[
 \boxed{
 2|\mathcal Q|
 \ge
 2W_L+R_L-2(m-\delta(G)-1)\ell.
 }
\tag{6}
\]

The exact form (5) is strongest for a thin star.  For a one-leaf star
it gives
\[
 |\mathcal Q|\ge h_c+\rho_c-\lambda.
\tag{7}
\]
The coarse form (6) shows that large colour excess and large residual
cannot coexist freely under a genuine reserve obstruction.

## 2. Proof

Fix \(c\in L\).  Since \(bc\) has multiplicity \(h_c\), its \(c\)-side
colour coordinates are \(h_c\) distinct neighbours of \(c\) in \(A\).
Thus
\[
 d_A(c)\ge h_c.
\tag{8}
\]
Using \(d(b)\ge\delta(G)\) in (2) gives
\[
 d(c)\le n-\delta(G)-\rho_c.
\tag{9}
\]
Therefore the missing degree of \(c\) inside \(B\) obeys
\[
 \begin{aligned}
 \overline d_B(c)
 &=|B|-1-d_B(c)\\
 &=|B|-1-d(c)+d_A(c)\\
 &\ge h_c+\rho_c-\lambda.
 \end{aligned}
\tag{10}
\]

Now put \(P=N(b)\) and \(C=V(G)\setminus P\).  Opposite type gives
\[
 N(c)\subseteq C,\qquad
 |C\setminus N(c)|=\rho_c.
\tag{11}
\]
Every leaf lies in \(C\), because \(bc\) is missing.  The set
\(C\setminus N(c)\) contains both \(b\) and \(c\).  Since \(b\notin L\),
the number of missing neighbours of \(c\) inside \(L\) is at most
\[
 \min\{\ell-1,\rho_c-2\}.
\tag{12}
\]
Consequently
\[
 2M_B[L]
 \le
 \sum_{c\in L}\min\{\ell-1,\rho_c-2\}.
\tag{13}
\]

All members of \(L\) are endpoints of active zero-shore pairs.  Hence
every missing \(B\)-edge incident with \(L\) belongs to
\(\mathcal Q\).  If \(I_B(L)\) denotes their number, then
\[
 |\mathcal Q|
 \ge I_B(L)
 =\sum_{c\in L}\overline d_B(c)-M_B[L].
\tag{14}
\]
Substitute (10) and (13), and multiply by two, to obtain (5).

Finally,
\[
 \min\{\ell-1,\rho_c-2\}\le\rho_c-2.
\]
Using \(H_L=W_L+\ell\) in (5) gives
\[
 \begin{aligned}
 2|\mathcal Q|
 &\ge2H_L+R_L-2\lambda\ell+2\ell\\
 &=2W_L+R_L-2(\lambda-2)\ell,
 \end{aligned}
\]
which is (6). \(\square\)

## 3. Obstruction criterion

Under global reserve failure,
\[
 |\mathcal Q|\le D_B-1.
\tag{15}
\]
Every opposite-type active zero-star must therefore satisfy
\[
 \boxed{
 2W_L+R_L
 \le
 2(D_B-1)+2(m-\delta(G)-1)\ell.
 }
\tag{16}
\]
Violation of (16) proves \(D_B\le M_B\) immediately.

This is the first exact inequality in the campaign that places the
opposite-star residual \(R_L\) and its colour excess \(W_L\) on the
same side of the actual reserve budget.  It is stronger than merely
bounding \(\rho_c\le n-2\delta\), and it uses genuine global-obstruction
hardness rather than failure of a one-way sufficient certificate.

## 4. Scope firewall

Equation (16) is a closure criterion, not a proof that every star
violates it.  The penalty proportional to
\((m-\delta)\ell\) can be quadratic at fixed \(s\), and (16) uses the
unweighted residual sum rather than the multiplicity-weighted residual
moment.  Same-neighbourhood stars and the outer-\(A\) residue are not
controlled.  The maximum-degree branch and Erdős #809 remain open.
