# Independent audit of weighted ruled-column layer cake

Date: 2026-07-30

Audited target: `WEIGHTED_RULED_COLUMN_LAYER_CAKE_THEOREM.md`

## 0. Verdict

\[
\boxed{\textsf{PASS}.}
\]

The weighted theorem, the dyadic loss, and the improved constant are
correct.  In particular, using the signed product
\[
x=a(j-k_0)
\]
retains both \(j<k_0\) and \(j>k_0\) without a factor-two loss.
Possible merging of \(x\) and \(-x\) after squaring is already included
in the signed two-square representation number \(r_2(n)\).

One formal boundary issue was repaired in the audited theorem: the
parameter sets are now explicitly finite,
\(\mathcal A\ne\varnothing\), and \(Z\ge0\).  These conditions make
\(\max\mathcal A\), the height maximum, and all displayed ranges
well-defined before the later assumption \(\Omega>0\) is invoked.
There was no error in the substantive counting argument.

## 1. Ordered weighted overlap

Put \(h_{j,a}=|\mathcal Z_{j,a}|\).  The weighted overlap can be
represented by explicit ordered layer tokens:
\[
\mathcal Q
=
\left\{
(j,k,a,m):
j\ne k,\quad
0\le m<\min(h_{j,a},h_{k,a})
\right\}.
\tag{A1}
\]
Then
\[
|\mathcal Q|
=
\sum_a\sum_{j\ne k}
\min(h_{j,a},h_{k,a})
=\Omega.
\tag{A2}
\]
This is an ordered count.  If both fibres are nonempty, the directions
\((j,k)\) and \((k,j)\) contribute separately.

Partition (A1) by the second slope \(k\).  The part indexed by \(k\)
has cardinality
\[
\Omega_k
=
\sum_a\sum_{j\ne k}
\min(h_{j,a},h_{k,a}).
\]
Therefore
\[
\sum_k\Omega_k=\Omega,
\qquad
\max_k\Omega_k\ge\frac{\Omega}{|\mathcal J|}.
\tag{A3}
\]
There is no missing or duplicated factor two between the definition of
\(\Omega\) and the weighted-star average.

## 2. Dyadic layer decomposition

For the maximizing base \(k_0\), write
\[
w_{j,a}=\min(h_{j,a},h_{k_0,a})>0
\]
on its positive-weight star.  Let
\[
\mathcal H_U
=\{1,2,\ldots,2^{\lfloor\log_2U\rfloor}\}
\]
where the displayed set means consecutive powers of two.  For every
integer \(1\le w\le U\),
\[
\sum_{\substack{H\in\mathcal H_U\\H\le w}}H
=2^{1+\lfloor\log_2w\rfloor}-1
\ge w.
\tag{A4}
\]
The lowest level \(H=1\) includes every positive weight, so small
columns are not silently discarded.

For
\[
\mathcal E_H=\{(j,a):w_{j,a}\ge H\},
\]
summing (A4) over the star gives
\[
\sum_{H\in\mathcal H_U}H|\mathcal E_H|
\ge\Omega_{k_0}.
\tag{A5}
\]
There are exactly
\[
L_U=1+\lfloor\log_2U\rfloor
\]
terms.  Hence one threshold satisfies
\[
H|\mathcal E_H|
\ge\frac{\Omega_{k_0}}{L_U}
\ge\frac{\Omega}{|\mathcal J|L_U}.
\tag{A6}
\]
No upper comparability of the weights in \(\mathcal E_H\) is needed;
the proof uses a superlevel set, not a dyadic bin.

## 3. Signed multiplication fibres and the constant

For every selected pair, set
\[
x=a(j-k_0)\ne0.
\tag{A7}
\]
Fix a signed integer \(x\).  Since \(a>0\),
\[
a\mid |x|,
\qquad
j=k_0+\frac{x}{a}.
\tag{A8}
\]
Thus each positive divisor \(a\) gives at most one representation, and
\[
\#\{(j,a)\in\mathcal E_H:a(j-k_0)=x\}
\le\tau(|x|)
\le T_\times.
\tag{A9}
\]
Consequently the signed product set satisfies
\[
|\mathcal X_H|
\ge\frac{|\mathcal E_H|}{T_\times}.
\tag{A10}
\]

This proves rigorously why the dense theorem's earlier left/right
factor \(2\) disappears.  The sign is stored in \(x\), so the
multiplication map does not identify the two sides.

## 4. Arbitrary height sets and anchoring

For one representation \((j_x,a_x)\) of \(x\), membership in
\(\mathcal E_H\) gives
\[
|\mathcal Z_{j_x,a_x}|\ge H,
\qquad
|\mathcal Z_{k_0,a_x}|\ge H.
\tag{A11}
\]
Choose only one arbitrary base anchor
\[
z_x^0\in\mathcal Z_{k_0,a_x}
\]
and any \(H\) distinct heights \(z\) from the other column.
Translation by \(-z_x^0\) is injective, so the \(H\) integers
\[
y=z-z_x^0
\]
are distinct.  Therefore each signed \(x\) supplies exactly \(H\)
distinct input pairs \((x,y)\), for a total of
\[
H|\mathcal X_H|.
\tag{A12}
\]

This argument does not match the two height sets and does not use an
interval, progression, common translate, or aligned ordering.  Empty
fibres have weight zero and never enter a positive superlevel.

## 5. Two-square fibres

Every input in (A12) is realized by two actual points and has label
\[
n=x^2+y^2.
\tag{A13}
\]
Because \(x\ne0\), \(n>0\).  Its range is
\[
n\le(RL)^2+(2Z)^2.
\]
For a fixed positive \(n\), the number of ordered signed integer pairs
is
\[
r_2(n)
=4\sum_{d\mid n}\chi_4(d)
\le4\tau(n)
\le T_2.
\tag{A14}
\]

In particular, inputs with horizontal coordinates \(x\) and \(-x\)
may have the same squared label, but they occupy two of the signed
representations already counted by \(r_2(n)\).  No new factor two is
required at this stage.

Combining (A6), (A10), and (A14) gives
\[
\begin{aligned}
|\Delta^2(P)|
&\ge\frac{H|\mathcal X_H|}{T_2}\\
&\ge
\frac{H|\mathcal E_H|}{T_\times T_2}\\
&\ge
\frac{\Omega}
{|\mathcal J|L_UT_\times T_2}.
\end{aligned}
\tag{A15}
\]
This confirms the denominator constant \(1\), rather than \(2\).

## 6. Critical exponent

Under the corollary's polynomial coordinate ranges,
\[
|\mathcal J|=O(t),\qquad
L_U=O(\log t)=t^{o(1)},
\]
and
\[
T_\times T_2=t^{o(1)}.
\]
Therefore
\[
\Omega\ge t^{4+\eta-o(1)}
\quad\Longrightarrow\quad
|\Delta^2(P)|
\ge t^{3+\eta-o(1)}.
\tag{A16}
\]
Equivalently, a \(t^{3+o(1)}\) distance upper bound forces
\(\Omega\le t^{4+o(1)}\).  The exponent bookkeeping and the
contrapositive are valid.

## 7. Independent executable audit

`independent_verify_weighted_ruled_layer_cake.py` imports no existing
AMRA verifier.  It:

1. expands \(\Omega\) into explicit ordered layer tokens;
2. reconstructs every weighted star;
3. verifies the dyadic identity separately for every positive weight;
4. keeps both signs in the multiplication map and checks every fibre
   with an independent trial-division implementation of \(\tau\);
5. anchors at an extreme height and uses nonlinear, gapped height sets;
6. brute-counts every relevant signed two-square fibre;
7. constructs the complete Euclidean point set and all genuine squared
   distances;
8. checks (A15) by exact integer cross-multiplication; and
9. exhausts all \(3^6=729\) fibre-size profiles with sizes
   \(0,1,2\) on a six-column universe.

Run:
```bash
python3 independent_verify_weighted_ruled_layer_cake.py \
  > weighted_ruled_layer_cake_independent_certificate.json
pytest -q test_independent_verify_weighted_ruled_layer_cake.py
```

The finite audit is a regression certificate.  The arbitrary-parameter
proof is Sections 1--5 above.
