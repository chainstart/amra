# Erdős #809 — opposite-star defect-slack energy

Date: 2026-08-02

Status: PROVED__CORE_INDEPENDENTLY_AUDITED__MAXIMUM_WITNESS_SHARPENING_PENDING

## 1. The sharpened obstruction

Retain the selected opposite zero-star notation

\[
 H=\sum_{c\in L}h_c,\qquad
 R_L=\sum_{c\in L}\rho_c,\qquad
 \ell=|L|,\qquad
 g=|A|-\delta(G)-1.
\]

Define the unused outer-colour defect and the large-residual surcharge by

\[
 Z=D_B-H,
 \qquad
 \Xi=\sum_{c\in L}(\rho_c-\ell-1)_+.
\tag{1}
\]

The zero-star mass ledger gives \(Z\ge0\).  Under global reserve failure
\(|\mathcal Q|\le D_B-1\), every selected opposite star satisfies

\[
\boxed{
 R_L+\Xi\le2(g+1)\ell+2Z-2.
}
\tag{2}
\]

Since \(R_L=\ell r+A_L\) in the common-host coordinates, equivalently

\[
\boxed{
 \ell r+A_L+\Xi
 \le2(g+1)\ell+2(D_B-H)-2.
}
\tag{3}
\]

In the maximum-witness branch, both the star centre and the maximum
witness lie in \(R\), in addition to the isolated leaves.  Thus
\(r\ge t+2\), and (3) yields

\[
\boxed{
 \ell t+A_L+\Xi
 \le2g\ell+2(D_B-H)-2.
}
\tag{3a}
\]

Finally, \(C\setminus N(c)\) contains the three distinct vertices
\(b,c,v\), so every \(\rho_c\ge3\).  Consequently (2) has the clean
maximum-witness endpoint
corollary

\[
\boxed{
 (2g-1)\ell+2(D_B-H)\ge2.
}
\tag{3b}
\]

The stronger edge-count argument in
`MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md` in fact proves the
parity-sharp square-root bound (22), and hence \(g\ge4\).

This strictly strengthens the inherited coarse reserve--residual bound
whenever some \(\rho_c>\ell+1\).  It also makes explicit that residual
mass can exceed the degree-spread allowance only by consuming defect
not already used by the selected star.

## 2. Proof

The inherited exact opposite-star reserve energy is

\[
2|\mathcal Q|
\ge
2\sum_{c\in L}(h_c+\rho_c-\lambda)
-\sum_{c\in L}\min\{\ell-1,\rho_c-2\},
\tag{4}
\]

where \(\lambda=|A|+1-\delta(G)=g+2\).  For every leaf, the elementary
identity

\[
\min\{\ell-1,\rho_c-2\}
=\rho_c-2-(\rho_c-\ell-1)_+
\tag{5}
\]

holds.  Substituting (5) into (4) gives the exact strengthened lower
bound

\[
2|\mathcal Q|
\ge
2H+R_L+\Xi-2(g+1)\ell.
\tag{6}
\]

Reserve failure and \(H=D_B-Z\) now imply

\[
2D_B-2
\ge2D_B-2Z+R_L+\Xi-2(g+1)\ell,
\]

which rearranges to (2).  The common-host identity
\(R_L=\ell r+A_L\) gives (3), and the maximum-witness inclusion
\(\{b,v\}\dot\cup T\subseteq R\) gives (3a).
Finally \(R_L\ge3\ell\) in (2) gives (3b).  QED.

## 3. Boundary

Equation (2) is an exact necessary condition, not an emptiness proof.
It can be weak when \(g\ell\) or \(Z=D_B-H\) is large, and it does not
control Branch A or B-same.  Erdős #809 remains open.

## 4. Reproduction

\[
\texttt{python3 verify\_opposite\_star\_defect\_slack.py}
\]

The verifier exhausts the scalar identity and finite feasible reserve
profiles.  The all-parameter result is the proof above.
