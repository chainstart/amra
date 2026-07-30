# Weighted ruled-column expansion by layer cake

Date: 2026-07-30

## 1. Result

The dense-column theorem assumes one uniform lower bound for every
occupied vertical fibre.  The following weighted version allows every
slope--radial column to carry an arbitrary finite integer height set,
including the empty set.

Let the following parameter sets be finite:
\[
\mathcal J\subset\mathbb Z,\qquad
\varnothing\ne\mathcal A\subset\mathbb Z_{>0},\qquad
|\mathcal J|\ge2,\qquad Z\ge0.
\]
For every \((j,a)\in\mathcal J\times\mathcal A\), let
\[
\mathcal Z_{j,a}\subset[-Z,Z]\cap\mathbb Z
\]
be an arbitrary finite set; it may be empty.  Suppose \(P\) contains
all points
\[
(a,ja,z),\qquad z\in\mathcal Z_{j,a}.               \tag{1}
\]
Write
\[
h_{j,a}=|\mathcal Z_{j,a}|,
\qquad
U=\max\left\{1,\max_{j,a}h_{j,a}\right\},
\tag{2}
\]
and define the weighted radial overlap
\[
\boxed{
\Omega
=
\sum_{a\in\mathcal A}
\sum_{\substack{j,k\in\mathcal J\\j\ne k}}
\min(h_{j,a},h_{k,a}).
}
\tag{3}
\]
Put
\[
L_U=1+\lfloor\log_2U\rfloor,
\qquad
L=\max\mathcal J-\min\mathcal J,
\qquad
R=\max\mathcal A,
\tag{4}
\]
\[
T_\times=\max_{1\le n\le RL}\tau(n),
\qquad
T_2=\max_{1\le n\le(RL)^2+(2Z)^2}4\tau(n).
\tag{5}
\]

### Theorem 1 (weighted layer-cake expansion)

If \(\Omega>0\), then
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{\Omega}
{|\mathcal J|L_UT_\times T_2}.
}
\tag{6}
\]

All three losses in (6) are explicit:

1. \(1/|\mathcal J|\) selects a base slope;
2. \(1/L_U\) selects a dyadic height layer; and
3. \(T_\times T_2\) bounds the multiplication-table and
   two-square fibres.

No common height, interval, progression, translation pattern, or
alignment between two height sets is assumed.

### Corollary 2 (critical weighted-overlap interface)

Fix \(C>0\) and \(\eta>0\).  Suppose
\[
\mathcal J\subset[-Ct,Ct]\cap\mathbb Z,\qquad
\mathcal A\subset[1,Ct]\cap\mathbb Z,
\tag{7}
\]
\[
\mathcal Z_{j,a}\subset[-Ct^2,Ct^2]\cap\mathbb Z,
\tag{8}
\]
and
\[
\boxed{\Omega\ge t^{4+\eta-o(1)}.}                 \tag{9}
\]
Then
\[
\boxed{|\Delta^2(P)|\ge t^{3+\eta-o(1)}.}          \tag{10}
\]

In particular, for every fixed \(\varepsilon<\eta\),
\[
|\Delta^2(P)|\ge t^{3+\varepsilon}
\]
for all sufficiently large \(t\).  Conversely, the critical
few-distance hypothesis
\[
|\Delta^2(P)|\le t^{3+o(1)}
\]
forces
\[
\boxed{\Omega\le t^{4+o(1)}}                       \tag{11}
\]
inside every such polynomial-range integer ruled chart.

Thus \(t^{4+\eta}\) is the precise weighted-overlap threshold delivered
by this method for a fixed \(t^\eta\) improvement over the critical
\(t^3\) distance scale.

## 2. Weighted star selection

For \(k\in\mathcal J\), define
\[
\Omega_k
=
\sum_{a\in\mathcal A}
\sum_{\substack{j\in\mathcal J\\j\ne k}}
\min(h_{j,a},h_{k,a}).
\tag{12}
\]
Every ordered pair in (3) occurs once, so
\[
\sum_{k\in\mathcal J}\Omega_k=\Omega.
\tag{13}
\]
Choose \(k_0\) satisfying
\[
\Omega_{k_0}\ge\frac{\Omega}{|\mathcal J|}.
\tag{14}
\]

Let
\[
\mathcal S=\{(j,a)\in\mathcal J\times\mathcal A:
 j\ne k_0,\ \min(h_{j,a},h_{k_0,a})>0\}.
\]
If
\[
w_{j,a}=\min(h_{j,a},h_{k_0,a}),
\]
then
\[
W_{\mathcal S}
:=\sum_{(j,a)\in\mathcal S}w_{j,a}
=\Omega_{k_0}
\ge\frac{\Omega}{|\mathcal J|}.
\tag{15}
\]
Thus every retained pair has two nonempty height fibres.  Keeping both
signs of \(j-k_0\) is harmless: the signed product used below already
distinguishes them.

## 3. Dyadic layer cake

Let
\[
\mathcal H_U=\{1,2,4,\ldots,2^{\lfloor\log_2U\rfloor}\}.
\]
For \(H\in\mathcal H_U\), define the superlevel set
\[
\mathcal E_H
=\{(j,a)\in\mathcal S:w_{j,a}\ge H\}.
\tag{16}
\]
For every positive integer \(w\le U\),
\[
\sum_{\substack{H\in\mathcal H_U\\H\le w}}H
=2^{1+\lfloor\log_2w\rfloor}-1
\ge w.
\tag{17}
\]
Summing (17) over \(\mathcal S\) gives
\[
\sum_{H\in\mathcal H_U}H|\mathcal E_H|
\ge W_{\mathcal S}.
\tag{18}
\]
There are exactly \(L_U\) levels.  Therefore one dyadic \(H\) satisfies
\[
\boxed{
H|\mathcal E_H|
\ge
\frac{W_{\mathcal S}}{L_U}
\ge
\frac{\Omega}{|\mathcal J|L_U}.
}
\tag{19}
\]

This is the only logarithmic loss.  Notice that (19) uses a superlevel
set, not a bin in which the fibre sizes must be comparable above as
well as below.

## 4. Distance extraction on the selected layer

Fix the \(H\) from (19).  For every \((j,a)\in\mathcal E_H\), put
\[
x=a(j-k_0).
\tag{20}
\]
For fixed nonzero signed \(x\), a positive divisor \(a\mid |x|\)
determines \(j=k_0+x/a\).  Hence every signed-product fibre has size at
most
\[
\tau(|x|)\le T_\times.
\]
The product set \(\mathcal X_H\) therefore satisfies
\[
|\mathcal X_H|
\ge\frac{|\mathcal E_H|}{T_\times}.
\tag{21}
\]

For every \(x\in\mathcal X_H\), retain one representing pair
\((j_x,a_x)\).  The threshold condition says
\[
|\mathcal Z_{j_x,a_x}|\ge H,
\qquad
|\mathcal Z_{k_0,a_x}|\ge H.
\]
Choose one arbitrary anchor
\[
z_x^0\in\mathcal Z_{k_0,a_x}
\]
and choose any \(H\) distinct heights
\[
\mathcal Y_x\subseteq\mathcal Z_{j_x,a_x}.
\tag{22}
\]
Only one anchor is used; no matching between the two height sets is
needed.

For \(z\in\mathcal Y_x\), the actual points
\[
(a_x,j_xa_x,z),
\qquad
(a_x,k_0a_x,z_x^0)
\]
have squared distance
\[
x^2+(z-z_x^0)^2.                                   \tag{23}
\]
For fixed \(x\), the \(H\) integers \(z-z_x^0\) are distinct.  Thus
(23) supplies exactly \(|\mathcal X_H|H\) distinct input pairs
\((x,y)\).

Every label in (23) is a positive integer bounded by
\[
(RL)^2+(2Z)^2.                                      \tag{24}
\]
For fixed \(n\), at most
\[
r_2(n)\le4\tau(n)\le T_2
\]
signed integer pairs satisfy \(x^2+y^2=n\).  Consequently,
\[
|\Delta^2(P)|
\ge
\frac{H|\mathcal X_H|}{T_2}
\ge
\frac{H|\mathcal E_H|}{T_\times T_2}.
\]
Equation (19) now proves (6). \(\square\)

## 5. Proof of Corollary 2

The coordinate ranges give
\[
RL=O(t^2),
\qquad
(RL)^2+(2Z)^2=O(t^4).
\]
Because each height set consists of distinct integers in an interval of
length \(O(t^2)\),
\[
U=O(t^2),
\qquad
L_U=O(\log t)=t^{o(1)}.
\]
The uniform divisor bound over polynomial ranges gives
\[
T_\times T_2=t^{o(1)}.
\]
Finally, \(|\mathcal J|=O(t)\).  Substituting (9) into (6) yields
\[
|\Delta^2(P)|
\ge
\frac{t^{4+\eta-o(1)}}{t^{1+o(1)}}
=t^{3+\eta-o(1)}.
\]
This proves (10), and its contrapositive gives (11). \(\square\)

## 6. Relation to the uniform dense theorem

If every occupied fibre in an incidence graph \(\mathcal E\) has size
at least \(H_0\), then
\[
\Omega
\ge
H_0\sum_a d_a(d_a-1)
=H_0\Psi(\mathcal E).
\]
Theorem 1 therefore recovers the power-scale conclusion of
`DENSE_RULED_COLUMN_STABILITY.md`, with the expected layer-cake
logarithm.  Its gain is that no single height threshold is assumed in
advance: the weighted overlap itself selects the useful \(H\).

## 7. Verification

`verify_weighted_ruled_layer_cake.py`:

- computes \(\Omega\) and the maximizing weighted star, retaining both
  signs through a signed product;
- checks the exact dyadic identity (17) and extracts \(H\);
- retains arbitrary \(H\)-subsets from gapped, translated height sets;
- checks multiplication fibres against \(\tau(n)\);
- checks genuine Euclidean distance fibres against \(4\tau(n)\); and
- includes empty fibres and highly nonuniform fibre sizes.

Run:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q test_verify_weighted_ruled_layer_cake.py
python3 verify_weighted_ruled_layer_cake.py
```
