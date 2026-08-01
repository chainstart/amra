# Erdős #809 — matching versus coherent zero-star concentration

Date: 2026-08-01

Status: PROVED__GLOBAL_REPEATED_MASS_REDUCES_TO_HEAVY_MATCHING_OR_COHERENT_STAR

## 1. Setup

Let \(Z_+\) be the repeated-zero graph on \(B\).  Thus
\[
 e=bc\in E(Z_+)
\]
is an active zero-shore pair used by \(h_e\ge2\) colours.  Give it
excess weight
\[
 w_e=h_e-1,
\qquad
 E_0=\sum_{e\in E(Z_+)}w_e.
\tag{1}
\]
Put
\[
 \kappa=n-2\delta(G).
\tag{2}
\]

## 2. Exact concentration theorem

### Theorem 2.1 (matching--star concentration)

Assume \(E_0>0\), and let \(F\) be any inclusion-maximal matching of
\(Z_+\), of size \(f\).  Then:

1. \(f\ge1\), and \(F\) is an active zero-shore matching to which all
   synchronization and weighted-transference bounds apply.
2. Some endpoint \(b\) of \(F\) is the centre of a zero-shore star
   whose total excess weight is at least
   \[
   \boxed{
   \sum_{c:bc\in E(Z_+)}w_{bc}
   \ge\frac{E_0}{2f}.
   }
   \tag{3}
   \]
3. The leaves of that star split into the same-neighbourhood and
   opposite-neighbourhood types.  One type carries excess weight at
   least
   \[
   \boxed{
   \frac{E_0}{4f}.
   }
   \tag{4}
   \]
   In the same-neighbourhood type, every two leaves \(c,c'\) satisfy
   \[
   |N(c)\mathbin\triangle N(c')|\le4\kappa.
   \tag{5}
   \]
   In the opposite-neighbourhood type, every two leaves satisfy
   \[
   |N(c)\mathbin\triangle N(c')|\le2\kappa.
   \tag{6}
   \]

Thus all repeated-zero excess not captured numerically by a useful
matching is forced into an explicitly centred, quantitatively
neighbourhood-coherent star.

#### Proof

The \(2f\) endpoints of an inclusion-maximal matching form a vertex
cover of \(Z_+\): an edge with both endpoints outside that set could be
added to \(F\).  Hence every weighted edge is incident with at least one
matching endpoint.  Summing weighted degrees over those \(2f\)
endpoints counts every edge at least once, so it is at least \(E_0\).
One endpoint has weighted degree at least \(E_0/(2f)\), proving (3).

Apply the exact two-type zero-star classification at this centre.
One of its two disjoint leaf classes carries at least half the star
weight, giving (4).  Two same-type leaves are each within
\(2\kappa\) in symmetric difference of the centre neighbourhood,
which proves (5) by the triangle inequality.  Two opposite-type leaves
are each obtained from \(V(G)\setminus N(b)\) by deleting at most
\(\kappa\) vertices, proving (6). \(\square\)

### Corollary 2.2 (reserve-obstruction form)

Let
\[
 d_0=\binom{\delta(G)}2,\qquad
 \overline M=\binom n2-e(G).
\tag{7}
\]
If the global reserve test fails, then every matching satisfies
\[
 f\le
 F_{\max}:=
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}}.
\tag{8}
\]
Consequently Theorem 2.1 produces a same- or opposite-neighbourhood
coherent star of excess weight at least
\[
 \boxed{
 \frac{E_0}{4F_{\max}}.
 }
\tag{9}
\]

For the same matching, write
\[
 H_F=\sum_{e\in F}h_e.
\]
The weighted synchronization theorem simultaneously gives
\[
 \boxed{
 H_F\le
 \frac{\overline M}{d_0}
 \sqrt{M_A(D_B-1)}.
 }
\tag{10}
\]
Therefore a global obstruction has a rigid two-output certificate:
the matching is bounded both in size and captured colour mass, while
the unrepresented total excess is concentrated on a coherent star
with the explicit lower bound (9).

## 3. Fixed-\(s\) interpretation

Suppose \(E_0\ge\varepsilon n^2\) and \(D_B\le dn^2\) at a fixed
\(s\in(0,1/2)\).  Since \(F_{\max}=O_{s,d}(n)\), (9) gives a coherent
zero-star carrying \(\Omega_{s,d,\varepsilon}(n)\) excess colour mass.
This conclusion is unconditional even though individual rectangle
overlaps need not be \(o(n)\).

When \(\kappa=o(n)\), the leaves in the selected type have
asymptotically identical neighbourhoods, recovering the near-Dirac
alignment mechanism.  At fixed \(s\), the error in (5)--(6) is linear;
the remaining proof problem is to convert the weighted coherent star
and its colour rectangles into the exact edge-energy slack or an
aligned compatible core.

## 4. Scope firewall

The theorem is a structural reduction, not the final fixed-\(s\)
alignment theorem.  A lower bound on coherent star weight is not by
itself a lower bound on its number of leaves, and the
\(O(\kappa)\) neighbourhood error need not be sublinear when \(s\) is
fixed.  The outer-\(A\) residue and Erdős #809 remain open.
