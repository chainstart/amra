# Edge-character synchronization: an agreement lemma and a geometric no-go

Date: 2026-07-30

## Purpose

`SIGNED_DIFFERENCE_FINITE_QUOTIENT_AUDIT.md` isolates a possible route from
large squared-difference correlations to a coherent point cycle:

1. attach a bounded finite-quotient character and phase to each active edge;
2. synchronize those edge labels into vertex coordinates;
3. use a dense \(K_{2,t}\) to force a lift.

This note proves a quantitative agreement theorem that would execute step 2
if almost all complete \(K_4\) tests supplied the appropriate local
constraints.  It then checks the actual squared-difference Gram cocycle.
That cocycle supplies neither character agreement nor phase consistency.

An explicit six-edge geometric construction makes the failure strict:
all six edges of one radius \(K_4\) have genuine, linear-sized shifted
correlations arising from real height sets; their finite quotients vary from
edge to edge and have no common nontrivial quotient; the four cycle
relations have no transversal point cycle.  The Gram identity remains true
for every actual height quadruple, but it is vacuous on the six selected
relations because they have no common quadruple.

## 1. A finite-label agreement theorem

Let \(K_N\) have an arbitrary orientation of each edge.  Give every oriented
edge \(uv\) a label
\[
 (c_{uv},\ell_{uv})\in{\cal C}\times\Gamma,
\]
where \({\cal C}\) is a finite character alphabet, \(\Gamma\) is a finite
abelian phase group, \(c_{uv}=c_{vu}\), and
\(\ell_{vu}=-\ell_{uv}\).

Call a \(K_4\) **good** when:

1. all six of its edges have the same character label \(c\); and
2. on every one of its four oriented triangular faces,
   \[
   \ell_{uv}+\ell_{vw}+\ell_{wu}=0. \tag{1}
   \]

### Theorem 1 (quantitative complete-graph synchronization)

Suppose at least a \(1-\varepsilon\) fraction of the copies of \(K_4\) in
\(K_N\) are good.  Then there are a character \(c_*\) and vertex potentials
\(p_v\in\Gamma\) such that
\[
 c_{uv}=c_*,\qquad \ell_{uv}=p_u-p_v \tag{2}
\]
on all but
\[
 \left(4\varepsilon+O(N^{-1})\right)\binom N2 \tag{3}
\]
edges.

In particular, if the bad-\(K_4\) proportion is \(o(1)\), deleting
\(o(N^2)\) edges gives one global character and exact vertex potentials.
The estimate is uniform in the sizes of \({\cal C}\) and \(\Gamma\).

### Proof

Choose two uniformly random disjoint edges.  Their union is one of the three
perfect matchings of a uniformly random \(K_4\).  If their character labels
differ, that \(K_4\) is bad.  Therefore
\[
 {\mathbb P}(c_e\ne c_f\mid e\cap f=\varnothing)\leq\varepsilon. \tag{4}
\]
The disjoint-edge distribution differs from two independent uniform edges
by \(O(N^{-1})\).  If \(p_c\) is the proportion of edges of colour \(c\),
(4) gives
\[
 \sum_c p_c^2\geq1-\varepsilon-O(N^{-1}).
\]
Since \(\max_c p_c\geq\sum_c p_c^2\), one colour \(c_*\) occurs on all but
\[
 \delta\binom N2,\qquad
 \delta\leq\varepsilon+O(N^{-1}) \tag{5}
\]
edges.

A triangle all of whose edges have colour \(c_*\) but fails (1) makes every
containing \(K_4\) bad.  Double-counting triangle--\(K_4\) incidences shows
that there are at most
\[
 \varepsilon\binom N3 \tag{6}
\]
such triangles.

For a vertex \(r\), let \(b_r\) be the number of failing all-\(c_*\)
triangles through \(r\), and let \(d_r\) be the number of non-\(c_*\) edges
at \(r\).  Averaging
\[
 b_r+(N-2)d_r
\]
over \(r\), using (5)--(6), gives a root for which
\[
 b_r+(N-2)d_r
\leq(\varepsilon+2\delta)\binom{N-1}{2}. \tag{7}
\]
Set \(p_r=0\) and \(p_v=\ell_{vr}\).  If \(uv\) has colour \(c_*\), both
root edges have colour \(c_*\), and triangle \(uvr\) satisfies (1), then
\[
 \ell_{uv}=p_u-p_v.
\]
The exceptions are covered by the non-\(c_*\) edges, the \(b_r\) failing
root triangles, and at most \((N-2)d_r\) pairs spoiled by a non-\(c_*\)
root edge.  Equations (5) and (7) bound their total by
\[
 (\varepsilon+3\delta)\binom N2
 \leq(4\varepsilon+O(N^{-1}))\binom N2.
\]
\(\square\)

This theorem is deliberately stated for a complete graph.  On a merely
dense active graph, the analogous conclusion requires a coboundary-expansion
or agreement-testing hypothesis: bad triangles can otherwise hide in edges
that lie in few tested \(K_4\)'s.

## 2. What the height Gram cocycle actually says

For four actual heights \(z_0,z_1,z_2,z_3\), put
\[
 a_{ij}=(z_i-z_j)^2,\qquad
 g_{ij}=\frac{a_{0i}+a_{0j}-a_{ij}}2.
\]
Then
\[
 g_{12}g_{13}g_{23}=a_{01}a_{02}a_{03}. \tag{8}
\]
Indeed \(g_{ij}=(z_i-z_0)(z_j-z_0)\), so both sides of (8) equal
\[
 (z_1-z_0)^2(z_2-z_0)^2(z_3-z_0)^2.
\]

Equation (8) is a compatibility test for six squared values already arising
from one point quadruple.  It does **not** imply either premise defining a
good labelled \(K_4\):

- it contains no edge-character labels and therefore cannot assert that the
  six quotient characters agree;
- it contains no independently selected signed differences and therefore
  cannot assert the triangular phase equations (1);
- if four selected cycle relations have no common point quadruple, there are
  no six selected values on which (8) can be evaluated.

Thus Theorem 1 is quantitatively useful but currently disconnected from the
geometric input.

## 3. A six-edge, edgewise-varying finite-quotient obstruction

Take four original radius indices
\[
 R=\{0,4,8,19\}. \tag{9}
\]
Every one of their six pairs has a disjoint same-sum external partner:
\[
\begin{array}{c|c}
\text{original pair}&\text{external pair}\\ \hline
(0,4)&(1,3)\\
(4,8)&(5,7)\\
(0,8)&(2,6)\\
(8,19)&(13,14)\\
(4,19)&(11,12)\\
(0,19)&(9,10).
\end{array} \tag{10}
\]
All twelve external indices are distinct and disjoint from \(R\).  For
geometric radii \(2^u\), every external pair is closer to the midpoint of
its common sum, hence its radial offset is strictly smaller.

Let \(m\) be divisible by \(1260\), and give all four original radius
classes the height set
\[
 Z=\{0,1,\ldots,m-1\}. \tag{11}
\]
For an edge \(e\), choose a modulus \(q_e\), a nonzero symmetric colour
\(\{\pm a_e\}\), and select
\[
 A_e=\{d^2:1\leq d<m,\ d\equiv\pm a_e\pmod{q_e}\}. \tag{12}
\]
Use the following data:
\[
\begin{array}{c|c|c}
e&q_e&a_e\\ \hline
(0,4)&7&1\\
(4,8)&14&1\\
(8,19)&21&1\\
(0,19)&28&2\\
(0,8)&5&1\\
(4,19)&9&1.
\end{array} \tag{13}
\]
The moduli have greatest common divisor one, so the six labels do not
descend from any common nontrivial cyclic quotient.

### Theorem 2 (real geometric label-synchronization no-go)

The construction (9)--(13) has the following properties.

1. Every selected set has exactly \(2m/q_e\) squared values.
2. Its representation graph on \(Z\times Z\) has exactly \(2m^2/q_e\)
   edges.
3. Its average representation multiplicity is exactly \(m\).
4. The cycle \(0,4,8,19,0\) has no transversal point cycle.
5. All six selected sets are simultaneously contained in genuine
   same-product shifted correlations of sizes \(2m/q_e=\Theta(m)\), using
   the six external pairs in (10).
6. The Gram identity (8) holds for every actual quadruple of heights, but it
   yields no character agreement or vertex potentials for the six selected
   edge labels.

### Proof

Because \(m\) is divisible by every \(q_e\), every residue class modulo
\(q_e\) contains \(m/q_e\) heights.  The two nonzero residues
\(\pm a_e\) are distinct in every row of (13).  The same residue count as in
the mod-seven construction gives \(2m/q_e\) values and \(2m^2/q_e\)
representations, hence average multiplicity \(m\).

On the four displayed cycle edges, reduction modulo seven gives difference
classes
\[
 \{\pm1\},\{\pm1\},\{\pm1\},\{\pm2\}. \tag{14}
\]
Their oriented sum cannot vanish modulo seven, so no point cycle exists.
In particular no point quadruple realizes all six selected edge relations.

For one original/external pair in (10), put
\[
 \Delta_e=C_{\rm original,e}-C_{\rm external,e}>0,
\qquad C_{uv}=(2^u-2^v)^2.
\]
Give one external endpoint a height set containing
\(\{\sqrt{\Delta_e+a}:a\in A_e\}\), give the other a set containing zero,
and pad both to \(m\) distinct real heights.  Since all external indices are
different and \(|A_e|<m\), the six constructions are independent.  Every
shifted block pair then shares \(C_{\rm original,e}+A_e\).

Finally, (8) is an identity for actual quadruples and therefore remains
true.  The selected relations have no common quadruple, so it cannot impose
a condition on their edgewise moduli or colours. \(\square\)

## 4. Updated exponent ledger

In the balanced regime \(m\asymp L\), every modulus in (13) is an absolute
constant.  Uniformly over all six edges,
\[
 |A_e|=\Theta(L),\qquad
 |{\cal R}_e|=\Theta(L^2),\qquad
 \lambda_e=\Theta(L). \tag{15}
\]
The smallest overlap is \(m/14\), still larger than
\(L^{5/6-\eta}\) by a fixed-power factor.  Yet:

- character identity varies edgewise;
- the six moduli have no common nontrivial quotient;
- a selected point \(K_4\), and already one selected point \(C_4\), does not
  exist;
- the Gram cocycle supplies zero labelled \(K_4\) tests.

Therefore no exponent improvement follows by feeding the existing Gram
identity into Theorem 1.  The synchronization theorem needs a new incidence
input producing many **nonvacuous labelled \(K_4\) tests**.

## 5. Exact remaining alternatives

There are now two honest routes.

1. **Labelled agreement route.**  Prove that the shifted-correlation energy
   produces a dense test complex in which a \(1-o(1)\) fraction of tested
   \(K_4\)'s have a common bounded-order character and satisfy triangular
   phase equations.  Theorem 1 then converts those local tests into vertex
   potentials with \(o(E)\) deletions.
2. **Avoid labels.**  Prove a direct one-pair inverse theorem in the
   strong-correlation branch.  The construction above shows that overlap,
   representation density and the unconditioned Gram identity alone are
   insufficient hypotheses.

The missing statement is no longer merely “synchronize edge labels.”  Before
agreement testing can start, the geometry must create nonvacuous local tests
that compare labels on different edges.  The current \(K_4\) Gram cocycle
does not do that.

## 6. Verification

`verify_edge_character_synchronization.py` checks:

- the root reconstruction when all triangle phase tests pass;
- the six disjoint same-sum external pairs and their smaller offsets;
- the exact finite-quotient value and representation counts;
- the absence of a selected transversal cycle;
- the gcd-one assertion for the six moduli; and
- the Gram identity on exhaustive small integer height quadruples.
