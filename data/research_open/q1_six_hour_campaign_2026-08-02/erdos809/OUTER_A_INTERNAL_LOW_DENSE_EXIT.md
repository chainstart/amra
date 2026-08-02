# Erdős #809 — dense internal exit for the canonical outer residue

Date: 2026-08-02

Status: PROVED__PENDING_INDEPENDENT_CROSS_AUDIT

## 1. Setup

Use the maximum-degree partition

\[
 A=N[v],\qquad B=V(G)\setminus A,\qquad
 m=|A|,\qquad g=m-\delta(G)-1.
\tag{1}
\]

For an integer \(q\ge2\), put

\[
 A_{<q}=\{a\in A:d_B(a)<q\},\qquad h=|A_{<q}|,
\qquad H=G[A_{<q}].
\tag{2}
\]

These are exactly the possible endpoints of the internal-\(A\) part
of the low-edge residue in the canonical localization theorem.

## 2. Forced internal density

### Lemma 2.1

\[
 \boxed{\delta(H)\ge h-g-q.}
\tag{3}
\]

Consequently,

\[
 \boxed{e(H)\ge\frac{h(h-g-q)}2.}
\tag{4}
\]

#### Proof

For \(a\in A_{<q}\), minimum degree and \(d_B(a)\le q-1\) give

\[
 d_A(a)\ge\delta(G)-q+1.
\]

At most \(m-h\) of these \(A\)-neighbours lie outside \(A_{<q}\).
Therefore

\[
\begin{aligned}
 d_H(a)
 &\ge\delta(G)-q+1-(m-h)\\
 &=h-(m-\delta(G)-1)-q\\
 &=h-g-q.
\end{aligned}
\]

This proves (3), and the degree sum proves (4).  \(\square\)

## 3. Direct \(C_7\)-colour exit

The inherited dense-subgraph compatibility lemma states that every two
edges of a graph \(J\) lie on a common \(C_7\) if

\[
 2\delta(J)-|V(J)|\ge5.
\tag{5}
\]

By Lemma 2.1, condition

\[
 \boxed{h\ge2g+2q+5}
\tag{6}
\]

implies (5) for \(H\).  All edges of \(H\) must then have distinct
colours in a rainbow-\(C_7\) colouring.  Hence:

### Theorem 3.1 (internal-low direct closure)

If

\[
 h\ge2g+2q+5
\tag{7}
\]

and

\[
 \boxed{
 \frac{h(h-g-q)}2\ge\Phi(n,e),
 }
\tag{8}
\]

then the graph already uses at least \(\Phi(n,e)\) colours.

The same conclusion holds with the exact condition
\(e(H)\ge\Phi(n,e)\) in place of (8).

## 4. Canonical hard-instance restriction

Take

\[
 q=q_*(M_B)=
 2+\left\lfloor
 \frac{1+\sqrt{1+8M_B}}2
 \right\rfloor.
\tag{9}
\]

The exact outer localization is

\[
 D_A=e(H)+e(A,B_{<q})-N_{<q}.
\tag{10}
\]

Theorem 3.1 says that every hard maximum-degree witness must satisfy at
least one of

\[
\boxed{
\begin{aligned}
 h&\le2g+2q+4,\\
 e(H)&<\Phi(n,e).
\end{aligned}}
\tag{11}
\]

In the second line, (4) gives the explicit scalar restriction

\[
 h(h-g-q)<2\Phi(n,e).
\tag{12}
\]

Thus whenever the low-\(A\) set is both large and forced dense, the
internal term of the canonical residue is not merely chargeable: it
directly supplies the required colour family.  Any remaining large
outer residue must concentrate in the cross term
\(e(A,B_{<q})-N_{<q}\), or occur when \(g+q\) is itself large.

## 5. Scope firewall

This theorem does not control the cross-low term
\(e(A,B_{<q})-N_{<q}\).  When \(M_B\) is quadratic, the canonical
threshold \(q_*\) can be linear and (6) may be unavailable.  The result
is a genuine new exit and a sharper normal form, not a proof of
maximum-degree Case 1 or Erdős #809.
