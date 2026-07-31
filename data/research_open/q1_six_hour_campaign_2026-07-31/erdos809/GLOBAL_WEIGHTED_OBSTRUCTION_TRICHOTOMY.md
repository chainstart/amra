# Erdős #809 — global weighted zero-obstruction trichotomy

Date: 2026-08-01

Status: PROVED__GLOBAL_FAILURE_REDUCED_TO_EXPLICIT_OPPOSITE_STAR_RESIDUE

## 1. The theorem

Retain the maximum-degree witness and write
\[
 d_0=\binom{\delta(G)}2,\qquad
 \overline M=\binom n2-e(G),\qquad
 \kappa=n-2\delta(G).
\tag{1}
\]
Let \(Z_+\) be the repeated-zero graph, with edge multiplicities
\(h_e\ge2\), and put
\[
 E_0=\sum_{e\in E(Z_+)}(h_e-1).
\tag{2}
\]

### Theorem 1.1 (canonical global obstruction trichotomy)

Assume \(\delta(G)\ge2\), \(E_0>0\), and global reserve failure
\[
 |\mathcal Q|\le D_B-1.
\tag{3}
\]
Let \(F\) be any inclusion-maximal matching in \(Z_+\), with
\[
 f=|F|,\qquad H_F=\sum_{e\in F}h_e.
\]
Then all of the following hold.

First, the matching is constrained simultaneously in size and colour
mass:
\[
 \boxed{
 f\le
 \sqrt{\frac{(D_B-1)(2\overline M-d_0)}{d_0}},
 }
\tag{4}
\]
\[
 \boxed{
 H_F\le
 \min\left\{
 \frac{|A|}{2}\sqrt{D_B-1},\
 \frac{\overline M}{d_0}\sqrt{M_A(D_B-1)}
 \right\}.
 }
\tag{5}
\]

Second, some matching endpoint is the centre of a coherent zero-star
with excess mass
\[
 W\ge\frac{E_0}{4f}.
\tag{6}
\]
One of the following structural residues can be selected.

1. **Same-neighbourhood residue.**  In this case every global
   obstruction satisfies
   \[
   \boxed{
   E_0
   \le
   4f(\kappa-1)L(D_B-1,\kappa),
   }
   \tag{7}
   \]
   where
   \[
   L(q,\kappa)=
   \left\lfloor
   \frac{2\kappa+1+\sqrt{(2\kappa+1)^2+8q}}2
   \right\rfloor.
   \tag{8}
   \]
2. **Opposite-neighbourhood residue.**  There are \(\ell\) coherent
   leaves with total excess \(W\) and residual sum
   \[
   R=\sum_c\bigl(n-d(b)-d(c)\bigr)
   \]
   such that
   \[
   \boxed{
   W\ge\frac{E_0}{4f},
   \qquad
   2W+R
   \le
   2(D_B-1)+2(|A|-\delta(G)-1)\ell.
   }
   \tag{9}
   \]

Thus a global obstruction with (7) false is forced into one explicitly
centred opposite-neighbourhood star satisfying (9).  No unsynchronized
collection of arbitrary zero pairs remains.

#### Proof

Equations (4)--(5) are respectively the exact iterated
synchronization bound and the weighted two-energy transference bound.
The endpoints of the maximal matching cover \(Z_+\), so weighted
averaging followed by the two-type zero-star lemma gives (6).

If the selected type is the same-neighbourhood type,
SAME_STAR_RESERVE_ENERGY.md bounds its number of leaves by
\(L(D_B-1,\kappa)\), and each leaf has excess at most \(\kappa-1\).
Combine this upper bound on \(W\) with (6) to obtain (7).

If the selected type is opposite, apply the coarse exact
reserve--residual inequality from
OPPOSITE_STAR_RESERVE_ENERGY.md and then (3).  Together with (6), this
is precisely (9). \(\square\)

## 2. Significance and remaining gate

Before this campaign, the fixed-\(s\) zero-shore branch consisted of
an uncontrolled aggregate \(E_0\), and both a uniform-overlap bound
and \(E_0=o(n^2)\) were known to be false.  Theorem 1.1 replaces that
aggregate by a canonical finite list of exact inequalities:

- a matching-size cap;
- a matching-colour-mass cap involving \(M_A\);
- a closed quadratic same-star exit;
- one opposite-star residue coupling actual reserve, colour mass, and
  degree residual.

The remaining \(B\)-side theorem is therefore narrow: rule out (9)
using the exact edge-energy ledger and the \(L_4(2)\) connector
condition, or convert its common complementary host into the aligned
compatible core.  The separate outer-\(A\) residue \(R_A\) must still
be absorbed before the full maximum-degree branch can close.

No claim that Erdős #809 is solved is made.
