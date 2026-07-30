# Cross-plane codegree to a weighted rational chart: extraction audit

Date: 2026-07-30

## 1. Outcome

This note audits the only remaining Erdős #1083 bridge:
\[
\mathfrak C_{\rm plane}\ge t^{13-o(1)}
\quad\Longrightarrow\quad
\text{a weighted integer/rational ruled chart with large }\Omega,
\]
or direct distance expansion.

No complete extraction dichotomy is proved.  Two rigorous intermediate
theorems are obtained:

1. radial cross-angle energy forces a weighted ordinary-radius overlap;
2. a common-denominator rational chord chart carrying that overlap
   gives a layer-cake distance bound.

The exact failure point is coefficient arithmetic.  Ordinary cylindrical
radius reuse does not equal reuse of the signed radial parameter in an
integer ruled chart, and neither the cross-plane representation tensor nor
the rotation marginals recover this relation.

A regular pentagonal vertical prism gives a finite Euclidean no-go:
it has linear distance count, maximal ordinary-radius overlap, and cubic
cross-plane reuse in its column height, but its two chord lengths have
irrational ratio.  Thus common-denominator rational chord coordinates
cannot be inferred from these statistics alone.

## 2. Audit of the three inherited interfaces

### 2.1 `PROOF_TREE_RECONNECTION.md`

Its negative diagnosis remains correct: aggregate angular marginals do
not force one synchronized source family.  Its proposed sufficient target
is now too strong.  The weighted ruled theorem no longer requires:

- a height arithmetic progression;
- identical or aligned height sets;
- a complete slope--radial grid; or
- an angular arithmetic progression.

The surviving requirement is an arithmetic coefficient chart with
weighted radial overlap
\[
\Omega\ge t^{4+\eta-o(1)}.
\]

### 2.2 `SYNC_EXTRACTION_DRC_ATTACK.md`

Weighted DRC extracts fixed-size families of rotation labels dense on many
fibres.  A rotation label records a difference \(2\alpha\); it does not
assert that the source ray \(\alpha\) occurs on that fibre.  The split
source--rotation extremizer makes the distinction exact.  Consequently,
this route still does not produce the height sets
\(\mathcal Z_{j,a}\) needed by the weighted theorem.

### 2.3 `RULED_STABILITY_EXTRACTION_ATTACK.md`

The plane-pair/distance tensor permits a critical random support model with
\[
D=t^3,\qquad
\mathfrak E_{\rm all}=t^{13+o(1)},\qquad
\mathfrak E_{\rm diag}=t^{12+o(1)}.
\]
It has no polynomial two-sided common-label rectangle.  The tensor forgets
the coefficients \(\cos(\alpha-\beta)\), endpoint radial parameters, and
height coordinates.  Therefore dyadic pigeonholing, tensor DRC, and
label-only BSG cannot recover a ruled chart without an additional
Euclidean coefficient theorem.

## 3. The coordinate mismatch

Write an axial plane of slope \(j\) in a horizontal Cartesian chart as
\[
(a,ja).
\]
Its ordinary cylindrical radius is
\[
\rho=a\sqrt{1+j^2}.                                 \tag{1}
\]
Thus equal ordinary radii on two slopes generally correspond to different
signed Cartesian parameters:
\[
a_j=\frac{\rho}{\sqrt{1+j^2}}.
\]
The weighted theorem uses equality of \(a\), not equality of \(\rho\).
Hence the radius--angle statistic in
`ANGULAR_STARVATION_BRANCH_ATTACK.md` cannot simply be renamed
\(\Omega\).

There is, however, a coordinate-free version of the terminal arithmetic
argument.  It uses rational chord lengths on equal ordinary-radius
circles.

## 4. Radial energy forces weighted overlap

Split every axial plane into its at most two actual off-axis ray columns.
Let \(\mathcal J\) denote these ray angles.  For an ordinary radius
\(\rho\), let
\[
h_{j,\rho}
=|\{z:(\rho v_j,z)\in P\}|,
\qquad v_j\in S^1.
\tag{2}
\]
Put
\[
U=\max_{j,\rho}h_{j,\rho},
\]
\[
\mathfrak C_{\rho\angle}
=\sum_\rho\sum_{j\ne k}h_{j,\rho}h_{k,\rho},
\tag{3}
\]
\[
\Omega_{\rm cyl}
=\sum_\rho\sum_{j\ne k}
\min(h_{j,\rho},h_{k,\rho}).
\tag{4}
\]

### Lemma 1 (energy-to-layer overlap)

If \(U>0\), then
\[
\boxed{
\Omega_{\rm cyl}
\ge\frac{\mathfrak C_{\rho\angle}}{U}.
}
\tag{5}
\]

### Proof

For \(0\le x,y\le U\),
\[
\min(x,y)\ge\frac{xy}{U}.
\]
Apply this to every ordered pair in (3) and sum. \(\square\)

This loss is sharp when all nonzero columns have height \(U\).

## 5. A rational-chord weighted terminal theorem

The next theorem is a coordinate-free analogue of
`WEIGHTED_RULED_COLUMN_LAYER_CAKE_THEOREM.md`.

Suppose all heights lie in finite sets
\[
\mathcal Z_{j,\rho}\subset\mathbb R,
\qquad
h_{j,\rho}=|\mathcal Z_{j,\rho}|.
\]
Assume there is a positive scale \(q\) such that
\[
qz\in\mathbb Z,\qquad |qz|\le Y
\quad(z\in\mathcal Z_{j,\rho}),                    \tag{6}
\]
and
\[
x_{j,k,\rho}
:=q\rho\|v_j-v_k\|
\in\mathbb Z_{>0},
\qquad x_{j,k,\rho}\le X                           \tag{7}
\]
whenever \(j\ne k\) and both corresponding fibres are nonempty.
Define the anchored chord multiplicity
\[
K
=\max_{k,x}
|\{(j,\rho):
j\ne k,\ h_{j,\rho}h_{k,\rho}>0,\
x_{j,k,\rho}=x\}|.
\tag{8}
\]
Let
\[
L_U=1+\lfloor\log_2U\rfloor,
\qquad
T_2=\max_{1\le n\le X^2+(2Y)^2}4\tau(n).
\tag{9}
\]

### Theorem 2 (weighted rational-chord expansion)

If \(\Omega_{\rm cyl}>0\), then
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{\Omega_{\rm cyl}}
{|\mathcal J|L_UKT_2}.
}
\tag{10}
\]

### Proof

Define the weighted star at base ray \(k\) by
\[
\Omega_k
=\sum_\rho\sum_{j\ne k}
\min(h_{j,\rho},h_{k,\rho}).
\]
Some \(k_0\) has
\[
\Omega_{k_0}\ge\Omega_{\rm cyl}/|\mathcal J|.
\]
For dyadic \(H\le U\), let
\[
\mathcal E_H
=\{(j,\rho):
j\ne k_0,\
\min(h_{j,\rho},h_{k_0,\rho})\ge H\}.
\]
The same layer-cake identity as in the weighted ruled theorem gives one
\(H\) satisfying
\[
H|\mathcal E_H|
\ge\frac{\Omega_{\rm cyl}}{|\mathcal J|L_U}.
\tag{11}
\]

Map \((j,\rho)\in\mathcal E_H\) to the positive integer
\[
x=x_{j,k_0,\rho}.
\]
By (8), every fibre has size at most \(K\), so at least
\[
|\mathcal E_H|/K
\]
different \(x\)'s occur.  Retain one \((j_x,\rho_x)\) for every \(x\).
Choose one anchor \(z_x^0\in\mathcal Z_{k_0,\rho_x}\) and any \(H\)
distinct heights \(z\in\mathcal Z_{j_x,\rho_x}\).

After multiplying squared distances by \(q^2\), the resulting genuine
point pairs have labels
\[
q^2d^2
=x^2+\bigl(q(z-z_x^0)\bigr)^2.                    \tag{12}
\]
For fixed \(x\), the \(H\) second coordinates in (12) are distinct
integers.  Every label is positive and at most \(X^2+(2Y)^2\), and a
fixed label has at most
\[
r_2(n)\le4\tau(n)\le T_2
\]
signed two-square representations.  Thus
\[
|\Delta^2(P)|
\ge\frac{H|\mathcal E_H|}{KT_2}.
\]
Combine this with (11). \(\square\)

The integer ruled chart is a special case: there
\[
x=a|j-k_0|
\]
and \(K\) is bounded by the multiplication-table divisor loss.

## 6. Critical exponent interface

Assume polynomial coordinate ranges, so
\[
L_U,T_2=t^{o(1)},
\qquad |\mathcal J|=t^{1+o(1)}.
\]
If
\[
K=t^{\kappa+o(1)},
\qquad
\Omega_{\rm cyl}=t^{\omega+o(1)},
\]
then Theorem 2 gives
\[
\boxed{
|\Delta^2(P)|
\ge t^{\,\omega-1-\kappa-o(1)}.
}
\tag{13}
\]
Therefore a fixed improvement \(t^{3+\delta}\) follows whenever
\[
\boxed{\omega>4+\kappa+\delta.}                   \tag{14}
\]

Combining Lemma 1 with a height cap
\[
U=t^{u+o(1)}
\]
and
\[
\mathfrak C_{\rho\angle}=t^{\gamma+o(1)}
\]
gives
\[
\omega\ge\gamma-u.
\]
Hence the rational-chord branch succeeds when
\[
\boxed{
\gamma>5+u+\kappa+\delta.
}
\tag{15}
\]
At the natural values
\[
\gamma=7,\qquad u=2,\qquad\kappa=0,
\]
Theorem 2 gives the strong bound
\[
|\Delta^2(P)|\ge t^{4-o(1)}.                       \tag{16}
\]

More generally, suppose only a fraction \(t^{-\chi+o(1)}\) of the radial
overlap is captured by one admissible rational chart.  Then the exponent
in (13) becomes
\[
\gamma-u-\chi-1-\kappa.
\]
At \((\gamma,u)=(7,2)\), any
\[
\boxed{\chi+\kappa<1}
\tag{17}
\]
still yields a fixed improvement over \(t^3\).

## 7. Why this does not close the extraction

The forced statistic is
\[
\mathfrak C_{\rm plane}\ge t^{13-o(1)}.
\]
No theorem currently proves
\[
\mathfrak C_{\rho\angle}\ge t^{7+\eta-o(1)}
\]
from it under the few-distance hypothesis.  The universal transfer with
coefficient \(t^{6-\eta}\) is false without a non-ruled hypothesis.

Even if radial energy is large, Lemma 1 produces overlap in ordinary
radius \(\rho\), while Theorem 2 additionally requires:

1. one common scale \(q\) making all selected heights integral;
2. the same \(q\) making the relevant horizontal chord lengths integral;
3. polynomial bounds on the scaled coordinates; and
4. chord multiplicity \(K=t^{o(1)}\), or at least \(K=t^\kappa\) with
   enough exponent slack.

None of these arithmetic conclusions follows from the existing tensor or
rotation DRC.

## 8. A Euclidean rationality no-go

For \(H\ge1\), let
\[
P_H
=
\{(\cos(2\pi j/5),\sin(2\pi j/5),h):
0\le j<5,\ 0\le h<H\}.
\tag{18}
\]
All five vertical columns have ordinary radius one and height \(H\), so
\[
\Omega_{\rm cyl}=5\cdot4H=20H.                    \tag{19}
\]
The two nonzero horizontal squared chord lengths are
\[
a=\frac{5-\sqrt5}{2},
\qquad
b=\frac{5+\sqrt5}{2}.                              \tag{20}
\]
Together with the vertical difference squares, all squared distances lie
in
\[
\{u^2,\ a+u^2,\ b+u^2:0\le u<H\},
\]
so
\[
|\Delta^2(P_H)|=3H.                                \tag{21}
\]

For each of the two chord types there are ten ordered plane pairs.  If
\[
r_H(0)=H,\qquad r_H(u)=2(H-u)\quad(1\le u<H),
\]
then
\[
\mathfrak C_{\rm plane}
=180\sum_{u=0}^{H-1}r_H(u)^2
=\Theta(H^3).                                      \tag{22}
\]

However,
\[
\frac ba=\frac{3+\sqrt5}{2}\notin\mathbb Q.
\]
If one scale \(q\) made both chord lengths \(\sqrt a,\sqrt b\) rational
(and hence integers after another rational scaling), their ratio would be
rational, contradicting (20).  Thus large radial overlap, few distances,
and large cross-plane reuse do not force a common-denominator rational
chord chart even in a literal Euclidean configuration.

This example has only five active planes and is not a critical
\(M=t\) counterexample.  It is a local no-go to the arithmetic inference,
not a counterexample to Erdős #1083.

## 9. The honest extraction trichotomy

At the current proof boundary, a critical configuration must fall into at
least one of the following unresolved branches:

1. **radial-transfer failure**
   \[
   \mathfrak C_{\rho\angle}<t^{7+\eta}
   \quad\text{despite}\quad
   \mathfrak C_{\rm plane}\ge t^{13-o(1)};
   \]
2. **coefficient escape:** radial overlap is large, but every
   polynomial-range common-denominator rational chord chart captures only
   a \(t^{-1+o(1)}\) fraction or has chord multiplicity \(t^{1-o(1)}\);
3. **arithmetic-chart success:** a chart satisfies (15) or (17), and
   Theorem 2 directly yields more than \(t^{3+\delta}\) distances.

The third branch is now rigorous.  No existing argument eliminates the
first two.  Calling this a two-way extraction theorem would hide precisely
the missing work.

## 10. Minimum next lemma

A sufficient new Euclidean statement is:

> Under
> \[
> D\le t^{3+o(1)},\qquad
> \mathfrak C_{\rm plane}\ge t^{13-o(1)},
> \]
> either \(\mathfrak C_{\rho\angle}\ge t^{7+\eta}\), and a fraction
> \(t^{-\chi}\) of its induced overlap lies in a polynomial-range rational
> chord chart with \(\chi+\kappa<1\), or
> \(D\ge t^{3+\delta}\).

The pentagonal example shows that “rational” may need replacement by a
bounded-degree number-field chart.  The tensor no-go shows that the proof
must use the four-plane quadratic before any BSG/DRC extraction.

## 11. Verification

`verify_cross_plane_weighted_chart_interface.py` checks:

- Lemma 1 on arbitrary finite height arrays;
- Theorem 2 on an exact rational unit-circle chart;
- the exponent ledger (13)--(17);
- the pentagonal values (19)--(22); and
- irrationality of the ratio in (20).

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_cross_plane_weighted_chart_interface.py
python3 verify_cross_plane_weighted_chart_interface.py
```
