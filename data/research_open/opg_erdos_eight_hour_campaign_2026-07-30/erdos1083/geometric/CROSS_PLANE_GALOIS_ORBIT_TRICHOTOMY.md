# Cross-plane energy, Galois orbits, and a quantitative chart/expansion/obstruction trichotomy

Date: 2026-07-30

## 0. Outcome

At the Erdős #1083 critical node, write
\[
N=t^5,\qquad
|\Delta^2(P)|\le t^{3+o(1)},\qquad
\mathfrak C_{\rm plane}\ge t^{13-o(1)}.
\tag{1}
\]
The cross-plane energy can be disintegrated over individual squared
distance labels.  This gives a rigorous conclusion that was not visible
from the radial-overlap statistic alone:

\[
\boxed{
\text{a positive proportion of }\mathfrak C_{\rm plane}
\text{ lies on labels having }
t^{5-o(1)}\text{ representations on }
t^{1-o(1)}\text{ plane pairs}.
}
\tag{2}
\]

For algebraic labels, grouping this energy into complete Galois orbits
gives the exact field-orbit inequality
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{R\,\mathfrak C_R}{H_R}.
}
\tag{3}
\]
Here \(\mathfrak C_R\) is the codegree energy carried by complete Galois
orbits of size at least \(R\), and \(H_R\) is the largest total energy
of one such orbit.

Equations (2)--(3), combined with the existing weighted number-field
terminal theorem, yield a strict quantitative trichotomy:

1. a low-complexity chart already gives distance expansion;
2. high-degree complete field orbits with sufficiently dispersed energy
   give many distinct distances by (3);
3. otherwise there is an explicit structural obstruction: energy lies
   outside complete high-degree orbits, or one high-degree orbit itself
   carries near-critical energy.

The last alternative cannot currently be eliminated.  In fact,
`GROWING_CYCLOTOMIC_CRITICAL_ENERGY_ATTACK.md` constructs an abstract
cyclotomic representation tensor that attains equality in (3) at
\[
|\Delta^2|=\Theta(t^3),\quad
\mathfrak C_{\rm plane}=\Theta(t^{13}),\quad
R=\Theta(t),\quad H_R=\Theta(t^{11}).
\tag{4}
\]
Thus the full critical values \(N,D,\mathfrak C_{\rm plane}\), even
together with Galois completeness, do not rule out the growing
cyclotomic alternative without a new Euclidean coefficient theorem.
No unconditional exponent improvement is claimed.

## 1. Labelwise disintegration of cross-plane energy

Use the notation of `ANGULAR_STARVATION_BRANCH_ATTACK.md`.  Let
\(\mathcal P\) be the retained ordered axial-plane pairs and put
\[
W_{e,d}=R_{\alpha,\beta}(d),
\qquad e=(\alpha,\beta)\in\mathcal P.
\tag{5}
\]
For one distance label \(d\), define
\[
S_d=\sum_{e\in\mathcal P}W_{e,d},
\qquad
c_d
=S_d^2-\sum_{e\in\mathcal P}W_{e,d}^2
=\sum_{\substack{e,f\in\mathcal P\\e\ne f}}
W_{e,d}W_{f,d}.
\tag{6}
\]
Then \(c_d\ge0\), and exactly
\[
\boxed{
\mathfrak C_{\rm plane}=\sum_{d\in\Delta^2(P)}c_d.
}
\tag{7}
\]

Let
\[
B=\max_{e,d}W_{e,d}.
\tag{8}
\]
Lemma 2 of `ANGULAR_STARVATION_BRANCH_ATTACK.md` gives
\[
B\ll Q^{4/3}+Q=t^{4+o(1)}
\tag{9}
\]
at the inherited value \(Q=t^{3+o(1)}\).

### Theorem 1 (heavy-label transfer)

Let \(L=|\Delta^2(P)|\), \(C=\mathfrak C_{\rm plane}>0\), and fix
\(0<\theta<1\).  Define
\[
\mathcal H_\theta
=\left\{d:c_d\ge\frac{\theta C}{L}\right\}.
\tag{10}
\]
Then
\[
\boxed{
\sum_{d\in\mathcal H_\theta}c_d\ge(1-\theta)C.
}
\tag{11}
\]
Moreover, every \(d\in\mathcal H_\theta\) satisfies
\[
\boxed{
S_d\ge\sqrt{\frac{\theta C}{L}},
\qquad
k_d\ge\frac1B\sqrt{\frac{\theta C}{L}},
}
\tag{12}
\]
where
\[
k_d=|\{e:W_{e,d}>0\}|
\tag{13}
\]
is the number of supporting ordered plane pairs.

#### Proof

The labels outside \(\mathcal H_\theta\) contribute less than
\[
L\frac{\theta C}{L}=\theta C,
\]
which proves (11).  Equation (6) gives
\[
c_d\le S_d^2.
\]
It also gives
\[
c_d
\le k_d(k_d-1)B^2
\le k_d^2B^2.
\]
Taking square roots and using (10) proves (12).
\(\square\)

### Critical specialization

Under (1), (9), and \(L\le t^{3+o(1)}\), every fixed
\(0<\theta<1\) gives
\[
\boxed{
\begin{aligned}
\sum_{d\in\mathcal H_\theta}c_d
&\ge(1-\theta)t^{13-o(1)},\\
S_d&\ge t^{5-o(1)},\\
k_d&\ge t^{1-o(1)}
\qquad(d\in\mathcal H_\theta).
\end{aligned}
}
\tag{14}
\]
Thus the full \(t^{13}\) input forces a positive proportion of its
energy onto labels that are simultaneously rich in endpoint
representations and reused across a growing family of plane pairs.
This is stronger than merely knowing that some label occurs often.

The exponents are sharp at the representation-tensor level: the
cyclotomic model cited in (4) has
\[
c_d=\Theta(t^{10}),\quad
S_d=\Theta(t^5),\quad
k_d=\Theta(t)
\tag{15}
\]
for every label.

## 2. The exact Galois-orbit inequality

Let \(\overline{\mathbb Q}\cap\Delta^2(P)\) be the algebraic distance
labels.  For \(d\) in this set, write
\[
\operatorname{Orb}_{\mathbb Q}(d)
=\{\sigma(d):
\sigma:\overline{\mathbb Q}\hookrightarrow\mathbb C
\text{ fixes }\mathbb Q\}.
\tag{16}
\]
Its cardinality is \([\mathbb Q(d):\mathbb Q]\).

A Galois orbit \(\mathcal O\) is called **complete in the distance
set** if
\[
\mathcal O\subseteq\Delta^2(P).
\tag{17}
\]
This is a genuine extra property.  An arbitrary Euclidean distance set
need not contain any missing conjugate, and nonreal conjugates cannot be
squared Euclidean distances.

For \(R\ge1\), let \(\mathscr O_R\) be the pairwise disjoint complete
orbits in \(\Delta^2(P)\) having size at least \(R\).  Put
\[
C(\mathcal O)=\sum_{d\in\mathcal O}c_d,
\qquad
\mathfrak C_R=\sum_{\mathcal O\in\mathscr O_R}C(\mathcal O),
\qquad
H_R=\max_{\mathcal O\in\mathscr O_R}C(\mathcal O),
\tag{18}
\]
with \(H_R=0\) if the collection is empty.

### Theorem 2 (field-orbit expansion)

If \(\mathfrak C_R>0\), then
\[
\boxed{
|\Delta^2(P)|
\ge
\sum_{\mathcal O\in\mathscr O_R}|\mathcal O|
\ge
\frac{R\,\mathfrak C_R}{H_R}.
}
\tag{19}
\]

There is also the density form
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{\mathfrak C_R}{A_R},
\qquad
A_R=
\max_{\mathcal O\in\mathscr O_R}
\frac{C(\mathcal O)}{|\mathcal O|}.
}
\tag{20}
\]

#### Proof

The complete orbits are disjoint subsets of the distance set.  Hence
\[
|\Delta^2(P)|\ge\sum_{\mathcal O\in\mathscr O_R}|\mathcal O|
\ge R|\mathscr O_R|.
\]
On the other hand,
\[
\mathfrak C_R
=\sum_{\mathcal O\in\mathscr O_R}C(\mathcal O)
\le H_R|\mathscr O_R|.
\]
Combining the two inequalities proves (19).  Similarly,
\[
\mathfrak C_R
\le
A_R\sum_{\mathcal O\in\mathscr O_R}|\mathcal O|
\le A_R|\Delta^2(P)|,
\]
which proves (20).
\(\square\)

The degree \(R\) creates distance labels only when orbit energy does not
grow proportionally with \(R\).  This qualification is essential; it
is exactly what the cyclotomic sharp model saturates.

## 3. Quantitative chart/field/obstruction trichotomy

Fix:

* a desired distance threshold \(D_*>0\);
* a degree threshold \(R\ge1\);
* an energy fraction \(0<\alpha<1\); and
* a family of admissible low-complexity charts satisfying all
  common-scale, algebraic-integrality, all-conjugate height, and
  nonzero-label hypotheses of
  `GROWING_NUMBER_FIELD_WEIGHTED_CHART_THEOREM.md`.

For a chart \(\mathcal X\), denote its weighted radial overlap by
\(\Omega(\mathcal X)\), its ray count by \(J(\mathcal X)\), its
dyadic height loss by \(L(\mathcal X)\), its anchored chord
multiplicity by \(K(\mathcal X)\), and its explicit varying-field
two-square fibre by \(G(\mathcal X)\).

### Theorem 3 (strict trichotomy)

At least one of the following holds.

#### I. Low-complexity chart

There is an admissible chart \(\mathcal X\) such that
\[
\boxed{
\frac{\Omega(\mathcal X)}
{J(\mathcal X)L(\mathcal X)K(\mathcal X)G(\mathcal X)}
\ge D_*.
}
\tag{21}
\]
The weighted number-field theorem then proves
\[
|\Delta^2(P)|\ge D_*.
\tag{22}
\]

#### II. High-degree field-orbit expansion

The complete degree-\(\ge R\) orbits carry
\[
\mathfrak C_R\ge\alpha\mathfrak C_{\rm plane}
\tag{23}
\]
and obey
\[
\boxed{
H_R\le\frac{R\mathfrak C_R}{D_*}.
}
\tag{24}
\]
Then Theorem 2 proves
\[
|\Delta^2(P)|\ge D_*.
\tag{25}
\]

#### III. Explicit structural obstruction

No chart satisfies (21), and at least one of the following holds:
\[
\boxed{
\mathfrak C_{\rm plane}-\mathfrak C_R
>(1-\alpha)\mathfrak C_{\rm plane};
}
\tag{26}
\]
or
\[
\boxed{
\exists\mathcal O\in\mathscr O_R:
C(\mathcal O)>
\frac{R\mathfrak C_R}{D_*}.
}
\tag{27}
\]

The energy in (26) is carried by labels that are at least one of:

1. transcendental;
2. algebraic of degree \(<R\); or
3. algebraic of degree at least \(R\) whose full Galois orbit is not
   contained in the Euclidean distance set.

Equation (27) is the **heavy growing-field orbit obstruction**.  It
pinpoints the remaining alternative more sharply than saying only that
the coefficient field grows.

#### Proof

If I fails, inspect \(\mathfrak C_R\).  If (23) fails, then (26)
holds.  If (23) holds but (24) fails, the definition of \(H_R\) gives
(27).  Otherwise II holds, and Theorem 2 gives (25).
\(\square\)

Strict versus non-strict boundary choices in (24), (26), and (27) may
be assigned to either adjacent branch; they have no exponent effect.

## 4. Critical exponent form

Take
\[
D_*=t^{3+\delta},\qquad
R=t^{r-o(1)},\qquad
\mathfrak C_{\rm plane}\ge t^{13-o(1)}
\tag{28}
\]
with fixed \(\delta,r>0\).  If a fixed positive fraction of the energy
lies on complete degree-\(\ge R\) orbits, then field-orbit expansion
holds provided
\[
\boxed{
H_R\le t^{10+r-\delta-o(1)}.
}
\tag{29}
\]
Equivalently, the average codegree energy per label on every such orbit
must be at most
\[
t^{10-\delta-o(1)}.
\tag{30}
\]

For the growing cyclotomic scale \(R=t^{1-o(1)}\), the critical barrier
is
\[
\boxed{H_R=t^{11-o(1)}.}
\tag{31}
\]
Any fixed saving from \(t^{11}\) in the energy of every complete
cyclotomic orbit would imply a fixed improvement over \(t^3\) distances.
The sharp model has exactly \(t^{11+o(1)}\), so such a saving cannot
follow from tensor cardinalities and the cell cap alone.

If instead (26) holds, Theorem 1 applied to that part of the energy
forces an individual non-complete/low-degree/transcendental label with
\[
c_d\ge t^{10-o(1)},\quad
S_d\ge t^{5-o(1)},\quad
k_d\ge t^{1-o(1)}.
\tag{32}
\]
Thus the residual obstruction is not diffuse noise: it contains a
single highly reused Euclidean distance equation.

## 5. Why low-degree distance labels do not imply a chart

It is tempting to replace (26) by a low-degree chart conclusion.  This
is invalid.  Even the rational identity
\[
x^2+y^2=1
\tag{33}
\]
does not make \(x\) or \(y\) algebraic: for any transcendental
\(0<x<1\), the positive value \(y=\sqrt{1-x^2}\) is also
transcendental.  Repeating (33) across many plane pairs does not produce
one common scale, one coefficient field, bounded conjugate heights, or
small anchored chord multiplicity.

Therefore the chart branch in Theorem 3 deliberately retains the
actual hypotheses of the weighted terminal theorem.  Replacing them by
“the squared-distance label has bounded degree” would conceal a false
step.

## 6. Minimum viable next lemma

The new target is now quantitative and genuinely uses
\(\mathfrak C_{\rm plane}\):

> **Cyclotomic-orbit dispersion or chart lemma.**  Under the full
> critical Euclidean hypotheses, either an admissible chart satisfies
> (21) for \(D_*=t^{3+\delta}\), or the complete degree-\(\ge
> t^{1-o(1)}\) orbit energy satisfies
> \[
> H_R\le t^{11-\delta-o(1)},
> \]
> or the energy in (26) forces a ruled Cartesian family that directly
> determines \(t^{3+\delta}\) distances.

The first conclusion is discharged by the weighted number-field
theorem, the second by Theorem 2, and the third by
`RULED_CARTESIAN_ESCAPE_THEOREM.md` once the required stability
extraction is proved.

The cyclotomic sharp model proves that the saving in the middle
conclusion must use actual Euclidean coupling between endpoint
coordinates, the rotation reservoir, or a ruled inverse theorem.  It
cannot be obtained from \(N,D,\mathfrak C_{\rm plane}\), algebraic
degrees, and Galois closure as abstract statistics.

## 7. Claim status

### Proved

* the heavy-label transfer (10)--(14);
* the field-orbit inequalities (19)--(20);
* the strict trichotomy (21)--(27);
* the critical threshold \(H_R=t^{10+r-\delta-o(1)}\);
* the fact that a low-degree squared-distance label alone does not
  yield a number-field chord chart.

### Sharp abstract evidence

The accompanying cyclotomic tensor has every label in a complete
degree-\(\Theta(t)\) Galois orbit and attains equality in (19) at the
critical exponents.

### Open

* an upper bound \(H_R\le t^{11-\delta}\) for actual Euclidean
  configurations;
* extraction of a terminal chart from the energy in (26) or (27);
* any unconditional improvement for Erdős #1083.

## 8. Verification

`verify_cross_plane_galois_orbit_trichotomy.py` checks the exact
heavy-label inequalities, the orbit bound, the critical exponent
ledger, and the finite cyclotomic tensor formulas.

Run:

```bash
pytest -q test_verify_cross_plane_galois_orbit_trichotomy.py
python3 verify_cross_plane_galois_orbit_trichotomy.py
```
