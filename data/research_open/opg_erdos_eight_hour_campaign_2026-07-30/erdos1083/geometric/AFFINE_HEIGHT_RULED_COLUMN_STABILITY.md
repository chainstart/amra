# A Euclidean coefficient-stability lemma for affine-height ruled columns

Date: 2026-07-30

## 1. Result

The tensor no-go in `RULED_STABILITY_EXTRACTION_ATTACK.md` shows that
distance-label energy alone cannot recover a vertical Cartesian model.
This note proves a quantitative Euclidean stability theorem once a
common signed-radial support and long vertical columns have been
recovered.

The theorem is stable under independent integer translations of every
vertical column.  It therefore covers both common-height columns and
affine-height ruled columns.

### Theorem 1 (translated ruled-column expansion)

Let
\[
\mathcal J\subset\mathbb Z,\qquad
\mathcal A\subset\mathbb Z_{>0},
\qquad |\mathcal J|\ge2,
\]
and put
\[
k_0=\min\mathcal J,\qquad
L=\max\mathcal J-\min\mathcal J,\qquad
R=\max\mathcal A.
\]
Let \(H\ge1\).  For every
\((j,a)\in\mathcal J\times\mathcal A\), choose an integer
\(\sigma_{j,a}\), and suppose that the Euclidean point set \(P\)
contains
\[
\boxed{
(a,ja,\sigma_{j,a}+h),
\qquad 0\le h<H.
}
\tag{1}
\]
Assume
\[
|\sigma_{j,a}|\le Z.
\tag{2}
\]
Define
\[
T_\times
=\max_{1\le n\le RL}\tau(n),
\tag{3}
\]
\[
T_2
=\max_{1\le n\le (RL)^2+(2Z+H)^2}4\tau(n).
\tag{4}
\]
Then
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{|\mathcal A|(|\mathcal J|-1)H}
{T_\times T_2}.
}
\tag{5}
\]

Here \(\Delta^2(P)\) denotes the set of squared distances.  No relation
among the shifts \(\sigma_{j,a}\) is required beyond integrality and
(2).

### Corollary 2 (critical coefficient stability)

Fix a constant \(C\).  Suppose
\[
\begin{aligned}
&\mathcal J\subset[-Ct,Ct]\cap\mathbb Z,
&&|\mathcal J|=t^{1-o(1)},\\
&\mathcal A\subset[1,Ct]\cap\mathbb Z,
&&|\mathcal A|=t^{1-o(1)},\\
&H=t^{2-o(1)},\qquad
&&H\le Ct^2,\\
&|\sigma_{j,a}|\le Ct^2.
\end{aligned}
\tag{6}
\]
Then
\[
\boxed{
|\Delta^2(P)|\ge t^{4-o(1)}.
}
\tag{7}
\]

In particular, (7) holds for:

1. **common-height columns:** \(\sigma_{j,a}=0\);
2. **plane-affine height shifts:**
   \[
   \sigma_{j,a}=u_ja+v_j
   \]
   with integral \(u_j,v_j\) and
   \(|u_ja+v_j|\le Ct^2\); and
3. arbitrary bounded integral translations depending on both \(j\)
   and \(a\).

Thus a ruled-stability extraction does not need to align the absolute
heights of the recovered columns.  It only needs common signed-radial
parameters and long consecutive vertical intervals.

## 2. Proof of Theorem 1

For \(j\in\mathcal J\setminus\{k_0\}\) and
\(a\in\mathcal A\), compare the two columns with the same signed radial
parameter \(a\).  Put
\[
\ell=j-k_0>0,\qquad x=a\ell.
\tag{8}
\]
The product set
\[
\mathcal X
=\{a(j-k_0):
a\in\mathcal A,\ j\in\mathcal J\setminus\{k_0\}\}
\tag{9}
\]
has
\[
|\mathcal A|(|\mathcal J|-1)
\]
input representations.  For a fixed positive integer \(x\), every
representation \(x=a\ell\) chooses a positive divisor \(a\mid x\);
the associated \(\ell=x/a\) then determines \(j=k_0+\ell\).
Therefore the fibre has size at most \(\tau(x)\), and
\[
|\mathcal X|
\ge
\frac{|\mathcal A|(|\mathcal J|-1)}{T_\times}.
\tag{10}
\]

For every \(x\in\mathcal X\), retain one representing pair
\((j_x,a_x)\).  For \(0\le h<H\), use the actual points
\[
p_{x,h}
=(a_x,j_xa_x,\sigma_{j_x,a_x}+h),
\]
\[
q_x
=(a_x,k_0a_x,\sigma_{k_0,a_x}).
\tag{11}
\]
Their squared distance is
\[
\begin{aligned}
|p_{x,h}-q_x|^2
&=a_x^2(j_x-k_0)^2\\
&\quad+
(\sigma_{j_x,a_x}
 -\sigma_{k_0,a_x}+h)^2\\
&=x^2+y_{x,h}^2,
\end{aligned}
\tag{12}
\]
where
\[
y_{x,h}
=\sigma_{j_x,a_x}-\sigma_{k_0,a_x}+h.
\]
For fixed \(x\), the \(H\) integers \(y_{x,h}\) are distinct.  Hence
the construction supplies exactly \(|\mathcal X|H\) distinct input
pairs \((x,y)\).

Every label in (12) is positive and at most
\[
(RL)^2+(2Z+H)^2.
\tag{13}
\]
For a fixed positive integer \(n\), the number of integer pairs
\((x,y)\) with
\[
x^2+y^2=n
\]
is the classical two-square representation number \(r_2(n)\), and
\[
r_2(n)
=4\sum_{d\mid n}\chi_4(d)
\le4\tau(n)
\le T_2.
\tag{14}
\]
Therefore each squared-distance label receives at most \(T_2\) of the
selected inputs.  Combining (10) and (14) gives
\[
|\Delta^2(P)|
\ge\frac{|\mathcal X|H}{T_2}
\ge
\frac{|\mathcal A|(|\mathcal J|-1)H}
{T_\times T_2},
\]
which proves (5). \(\square\)

## 3. Proof of Corollary 2

Under (6),
\[
RL=O(t^2),
\qquad
(RL)^2+(2Z+H)^2=O(t^4).
\]
The uniform divisor bound
\[
\max_{n\le t^C}\tau(n)=t^{o(1)}
\]
for every fixed \(C\) gives
\[
T_\times T_2=t^{o(1)}.
\]
The numerator in (5) is
\[
|\mathcal A|(|\mathcal J|-1)H=t^{4-o(1)}.
\]
Equation (7) follows. \(\square\)

## 4. Relation to the four-plane quadratic

For general signed cylindrical coordinates, the horizontal part of a
cross-plane squared distance is
\[
a^2+b^2-2ab\cos(\alpha-\beta).
\]
For the ruled coefficient chart
\[
(a,ja,z),
\]
this becomes
\[
(a-b)^2+(ja-kb)^2.
\tag{15}
\]
The theorem uses the stable diagonal coefficient slice \(a=b\), on
which (15) collapses to
\[
a^2(j-k)^2.
\tag{16}
\]
The common radial support makes (16) a multiplication table; the
vertical intervals supply the independent square variable.  Divisor
bounds control both coefficient collisions.

This is a genuine coefficient-stability statement:

- the slopes need only form a large integer set, not an interval;
- the radial parameters need only form a large integer set, not an
  interval;
- the vertical columns may be translated independently; and
- no alignment of the translated height origins is needed.

The remaining unsolved extraction problem is to derive the common
integer coefficient chart and the common radial support from the
four-plane energy.  The tensor no-go proves that this step must use
Euclidean algebra.

## 5. Quantitative interface with the critical branch

At
\[
M=t,\qquad Q=t^3,
\]
a substructure satisfying (6) has
\[
|\mathcal J||\mathcal A|H=t^{4-o(1)}
\]
points and already determines \(t^{4-o(1)}\) distances.  This is a full
factor \(t^{1-o(1)}\) above the critical bound \(D=t^{3+o(1)}\).

Consequently, under the few-distance hypothesis, no such translated
ruled-column substructure can occur.  A future stability dichotomy may
therefore use the following rigorous terminal branch:

> either coefficient alignment fails on every
> \(t^{4-o(1)}\)-mass translated ruled-column subsystem, or the subsystem
> itself contradicts \(D\le t^{3+o(1)}\).

This does not yet prove that high cross-plane energy forces the
subsystem.  It proves that affine-height drift is not an obstruction
once the radial coefficient chart has been recovered.

## 6. Verification

`verify_affine_height_ruled_columns.py` independently:

- constructs the multiplication-table product set;
- checks every product fibre against \(\tau(n)\);
- builds the genuine Euclidean point pairs (11);
- checks every squared-distance fibre against \(4\tau(n)\); and
- verifies (5) for common, affine, and arbitrary bounded integer column
  shifts.

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_affine_height_ruled_columns.py
python3 verify_affine_height_ruled_columns.py
```

The finite verifier corroborates the exact arithmetic.  The proof of
Theorem 1 is the divisor argument above and is valid for all finite
parameter sets satisfying the hypotheses.
