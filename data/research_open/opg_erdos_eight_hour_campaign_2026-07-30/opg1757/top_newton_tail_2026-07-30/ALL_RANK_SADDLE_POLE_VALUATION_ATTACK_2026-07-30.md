# OPG-1757: all-rank saddle pole valuation and the cubic-degree target

Date: 2026-07-30

## 0. Result

This note proves the raw all-rank profile pole bound
\[
\boxed{
\operatorname{pole}_{x=1/2}
\frac{F_{h,r}(x)}{\sqrt{1-2x}}
\leq 3r
\qquad(h=0,1,2).
}
\tag{1}
\]

It also proves the marked second-difference estimate
\[
\boxed{
\operatorname{pole}_{x=1/2}
\left(
\frac{F_{2,r}-2F_{1,r}+F_{0,r}}{\sqrt{1-2x}}
\right)
\leq3r-4
\quad(r\geq2).
}
\tag{MD2}
\]

Consequently the determinant and central-binomial recurrences give
\[
\boxed{
\operatorname{pole}_{t=1}B_r(t)\leq3r+1.
}
\tag{2}
\]

Together with the rational-denominator localization implicit in the
exact Lagrange profile recurrence, this yields
\[
\operatorname{den}B_r(t)\mid(1-t)^{3r+1},
\qquad
\deg_d\beta_{d,r}\leq3r.
\tag{2a}
\]
The Laurent cancellation itself is proved below by an all-\(r\)
finite Bell-jet identity; it is not extrapolated from ranks at most
five.

## 1. The \(W\)-valuation of the phase recurrence

Put
\[
W=1-2x.
\]
The saddle variance is
\[
\sigma=-\phi_2^{-1},
\]
so
\[
\operatorname{pole}_{W=0}\sigma=1.
\tag{3}
\]
For \(q\geq2\),
\[
\phi_q=
\frac{(q-1)!}{2^q}
\left(
-(1-x)^{1-q}+(-1)^qx^{1-q}
\right).
\tag{4}
\]
Consequently
\[
\operatorname{ord}_{W=0}\phi_q
\geq
\begin{cases}
1,&q\text{ even},\\
0,&q\text{ odd}.
\end{cases}
\tag{5}
\]
The even derivative vanishes because its two summands agree at
\(x=1/2\).  This parity gain is the local signature of the coalescing
double saddle.

Let \(E_N(z)\) be the phase-exponential polynomial from
\[
NE_N(z)=
\sum_{p=1}^{N}
p\frac{\phi_{p+2}}{(p+2)!}z^{p+2}E_{N-p}(z).
\tag{6}
\]
A monomial indexed by a composition
\[
p_1+\cdots+p_q=N
\]
has \(z\)-degree \(N+2q\).  In the rank-\(r\) Gaussian term with
amplitude derivative \(m\), \(N=2r-m\), and after multiplying by
\(z^m\) the Gaussian moment uses
\[
\sigma^{r+q}.
\tag{7}
\]
Since \(q\leq N=2r-m\),
\[
r+q\leq3r-m\leq3r.
\tag{8}
\]
The extra zeros in (5) can only improve this bound.

The Gamma corrections are rational functions of \(x\) and \(1-x\)
and are regular at \(x=1/2\), so they add no \(W\)-poles.

## 2. Amplitude zero and proof of (1)

For the three main profiles, the saddle amplitude is
\[
g_a(y)=\frac{1-y}{y}(1-y/2)^{-a},
\qquad a=0,2,4.
\tag{9}
\]
At the saddle \(y=2x\), its zeroth derivative contains one factor
\(W\).  The leading integral therefore vanishes to first order in
\(W\).  Dividing the higher integral corrections by this leading
integral can add one pole.  In (8), the \(m=0\) term simultaneously
contains the amplitude factor \(W\); the \(m\geq1\) terms satisfy
\(3r-m+1\leq3r\).  Thus every relative main saddle correction has
pole order at most \(3r\).

Multiplication by the regular Gamma exponential does not change the
bound.  Hence
\[
\operatorname{pole}_{W=0}
\frac{F_{h,r}^{\rm main}}{\sqrt W}
\leq3r.
\tag{10}
\]

For the exceptional part of \(F_{2,r}\), the amplitude does not
vanish at the saddle.  Its rank is \(r-1\), so its relative saddle
correction has pole at most \(3(r-1)\).  The external factor in
\(F_{2,r}/\sqrt W\) is \(8x/W\), giving
\[
1+3(r-1)=3r-2\leq3r.
\tag{11}
\]
Equations (10)--(11) prove (1).

This is a valuation proof for arbitrary \(r\), not an interpolation
from the five computed ranks.

## 3. First marked difference: an all-rank two-pole gain

Edge transitivity gives the exact normalized identity
\[
\Phi_1(s,x)
=\frac{1}{1-s^{-1}}
\Phi_0(s,x+s^{-1}).
\tag{12}
\]
Equivalently, with \(\epsilon=s^{-1}\),
\[
\Phi_1=(1-\epsilon)^{-1}
\exp(\epsilon\partial_x)\Phi_0.
\tag{13}
\]
After subtracting \(\Phi_0\), every term either:

- lowers the profile rank by at least one, costing three units of the
  bound (1); or
- differentiates at least once while lowering the rank by the same
  amount, with net cost at least two units.

Therefore
\[
\boxed{
\operatorname{pole}_{x=1/2}
\left(
\frac{F_{1,r}-F_{0,r}}{\sqrt{1-2x}}
\right)
\leq3r-2.
}
\tag{14}
\]
The same bound for \(F_{2,r}-F_{1,r}\) is seen in every exact rank
through five.  For the determinant argument below it is enough to
use (14) after symmetrizing the two sides of the rank convolution,
together with MD2.

## 4. All-rank Bell-jet proof of MD2

Let \(C_r^{(a)}\) be the relative main saddle correction with shift
\(a\), so the three main profiles use \(a=0,2,4\).  Put
\[
K_r=\frac{(-1)^r(6r-1)!!}{9^r(2r)!}.
\tag{15}
\]
The highest four Laurent layers have the form
\[
W^{3r}C_r^{(a)}
=K_r\left(
c_0+c_1W+c_2W^2+c_3W^3+O(W^4)
\right).
\tag{16}
\]

### 4.1 Finite Bell support

Let \(n_p\) count uses of the phase perturbation
\(\phi_{p+2}z^{p+2}\), and let \(m\) be the amplitude derivative.
Relative to the maximal pole, the defect is
\[
\mathfrak d=
\sum_{p\ge2}(p-1)n_p+\sum_{\substack{p\ge2\\p\ {\rm even}}}n_p
+
\begin{cases}
0,&m=0,\\
m-1,&m\ge1.
\end{cases}
\tag{17}
\]
The \(m=0\) amplitude zero supplies the otherwise missing unit.
Therefore a configuration with \(\mathfrak d\le3\) uses only
\(p=1,2,3\), at most one of \(p=2,3\), and \(m\le4\).  The complete
list \((m,n_2,n_3;\mathfrak d)\) is
\[
\begin{aligned}
&(0,0,0;0),(1,0,0;0),(2,0,0;1),\\
&(0,1,0;2),(0,0,1;2),(1,1,0;2),(1,0,1;2),
  (3,0,0;2),\\
&(2,1,0;3),(2,0,1;3),(4,0,0;3).
\end{aligned}
\tag{18}
\]
Every omitted Bell monomial contributes \(O(W^4)\) in (16).  Only
\(\Gamma_1\) can enter these layers, and only at defect three.  Its
critical value is
\[
\Gamma_1^{(a)}(0)
=\frac1{12}+\frac a2-\frac{a^2}{2}.
\tag{19}
\]

### 4.2 Four main jets

Evaluation of the eleven terms in (18), including (19), gives
\[
c_0=-\frac1{6r-1},\qquad c_1=0,
\tag{20}
\]
\[
c_2=
\frac{3r(10a^2-10a+6r-1)}
{10(6r-5)(6r-1)},
\tag{21}
\]
\[
c_3=
\frac{
r(24a^3r-24a^3-72a^2r+78a^2+48ar-54a+1)
}{
2(6r-7)(6r-5)(6r-1)
}.
\tag{22}
\]
These are symbolic identities in \(r\), produced by the Gaussian
factorial ratios rather than interpolation in the rank.

For
\[
\Delta_a^2f=f(4)-2f(2)+f(0),
\]
one obtains
\[
\Delta_a^2c_0=\Delta_a^2c_1=0,
\tag{23}
\]
\[
\Delta_a^2c_2
=\frac{24r}{(6r-5)(6r-1)},
\tag{24}
\]
\[
\Delta_a^2c_3
=\frac{24r(12r-11)}
{(6r-7)(6r-5)(6r-1)}.
\tag{25}
\]

### 4.3 Exceptional cancellation

Let \(C^*_{r-1}\) be the exceptional relative saddle correction.  Its
leading two layers are
\[
W^{3r-3}C^*_{r-1}
=K^*_{r-1}
\left(
1+\frac{18(r-1)}{6r-7}W+O(W^2)
\right),
\tag{26}
\]
where
\[
K^*_{r-1}
=\frac{(-1)^{r-1}(6r-7)!!}{9^{r-1}(2r-2)!}.
\]
The exceptional contribution to \(C_{2,r}\) is
\[
\frac{8x}{W}C^*_{r-1}
=\frac{4(1-W)}{W}C^*_{r-1}.
\]
The ratio
\[
\frac{4K^*_{r-1}}{K_r}
=-\frac{24r}{(6r-5)(6r-1)}
\tag{27}
\]
makes its defect-two layer the negative of (24).  Its defect-three
layer is
\[
-\frac{24r(12r-11)}
{(6r-7)(6r-5)(6r-1)},
\tag{28}
\]
the negative of (25).  Hence
\[
W^{3r}
\left(C_{2,r}-2C_{1,r}+C_{0,r}\right)=O(W^4),
\tag{29}
\]
which proves MD2 for every \(r\ge2\).

### 4.4 Exact first surviving layer

The same finite-defect method can be continued one layer.  Defect
four has 24 main configurations: in addition to the multiplicities
in (18), one allows two \(p=2\) or \(p=3\) jets and one \(p=4\) or
\(p=5\) jet.  Gamma rank one enters through
\[
[W]\Gamma_1^{(a)}=a^2-a+\frac13.
\]
Their complete second shift difference is
\[
-\frac{216r(r-1)(r-2)}
{5(6r-7)(6r-5)(6r-1)}.
\tag{29a}
\]

The exceptional saddle needs only five configurations through its
second jet:
\[
W^{3r-3}C^*_{r-1}
=K^*_{r-1}\left(
1+\frac{18(r-1)}{6r-7}W
-\frac{3(r-1)(6r-77)}{10(6r-7)}W^2
+O(W^3)\right).
\tag{29b}
\]
After the multiplier \(4(1-W)/W\), its defect-four contribution,
normalized by \(K_r\), is
\[
\frac{36r(r-1)(6r-17)}
{5(6r-7)(6r-5)(6r-1)}.
\tag{29c}
\]
Adding (29a) and (29c) gives
\[
\frac{[W^{-(3r-4)}]\varepsilon_r}{K_r}
=-\frac{36r(r-1)}
{(6r-7)(6r-5)(6r-1)}.
\tag{29d}
\]
Since
\[
c_{r-1}:=[W^{-3r+3}]C_{0,r-1}
=\frac{(-1)^r(6r-9)!!}{9^{r-1}(2r-2)!},
\]
equation (29d) is exactly
\[
\boxed{
[W^{-(3r-4)}]\varepsilon_r=-6(r-1)c_{r-1}.
}
\tag{29e}
\]
Thus the MD2 bound is sharp, and the sign of its first surviving
layer is known at every rank.  The symbolic-\(r\) certificate is
`verify_md2_laurent_identity.py`; it enumerates all 24 main and five
exceptional configurations rather than interpolating ranks.

## 5. Why the second marked difference gives exactly four orders

Write
\[
C_{h,r}(x)=\frac{F_{h,r}(x)}{\sqrt{1-2x}},
\quad
\delta_r=C_{1,r}-C_{0,r},
\quad
\varepsilon_r=C_{2,r}-2C_{1,r}+C_{0,r}.
\tag{30}
\]
At determinant rank \(n\), suppressing the rank convolution notation,
\[
\begin{aligned}
C_1(u)C_1(v)-C_0(u)C_2(v)
={}&
\delta(u)C_0(v)-C_0(u)\delta(v)\\
&+\delta(u)\delta(v)-C_0(u)\varepsilon(v),
\end{aligned}
\tag{31}
\]
where \(u=tx\) and \(v=t(1-x)\).

The first line is antisymmetric under \(x\leftrightarrow1-x\).
Every even derivative at \(x=1/2\) therefore vanishes.  Only even
derivatives occur in the central binomial recurrence.

By (1), (14), and (MD2), each product in the second line gains four
poles relative to the raw product:
\[
(3a-2)+(3b-2)=3n-4,
\]
or
\[
3a+(3b-4)=3n-4.
\tag{32}
\]
The two square-root profile factors multiply at \(x=1/2\) to
\(1-t\).  Hence, before \(x\)-differentiation,
\[
\operatorname{pole}_{t=1}G_n(1/2,t)\leq3n-5.
\tag{33}
\]
After \(m\) derivatives,
\[
\operatorname{pole}_{t=1}
\partial_x^mG_n(1/2,t)
\leq3n-5+m.
\tag{34}
\]

## 6. Propagation through central binomial moments

In \(H_n(t)\), a determinant rank \(a\) is differentiated only through
\[
m\leq2(n-a).
\]
Using (34),
\[
3a-5+m
\leq3a-5+2(n-a)
=2n+a-5
\leq3n-5.
\tag{35}
\]
Thus MD2 and its first-difference companion imply
\[
\operatorname{pole}_{t=1}H_n(t)\leq3n-5.
\tag{36}
\]

Finally,
\[
B_r(t)=\frac1{2t^4}\sum_{n=2}^{r+2}H_n(t),
\]
so
\[
\operatorname{pole}_{t=1}B_r(t)
\leq3(r+2)-5
=3r+1.
\tag{37}
\]
Using the denominator localization from the exact profile recurrence,
(37) gives
\[
\operatorname{den}B_r(t)\mid(1-t)^{3r+1}.
\]
The coefficients of such a rational generating function are
polynomials in \(d\) of degree at most \(3r\), proving (2a).

## 7. Symbolic and finite certificates

`verify_md2_laurent_identity.py` independently enumerates (18),
extracts the four symbolic jets (20)--(22), and verifies the exact
exceptional cancellations (27)--(28).  Its conclusion is an all-rank
symbolic identity.

`verify_saddle_pole_orders.py` computes the saddle/Gamma recurrence
at complete fixed ranks and additionally certifies:

\[
\begin{array}{c|c}
\text{object}&\text{exact pole order through rank 5}\\ \hline
C_{h,r}&3r\\
C_{1,r}-C_{0,r}&3r-2\\
C_{2,r}-C_{1,r}&3r-2\\
C_{2,r}-2C_{1,r}+C_{0,r}&3r-4\quad(r\ge2)\\
G_r(1/2,t)&3r-5\\
H_r(t)&3r-5
\end{array}
\tag{38}
\]

For example,
\[
\begin{array}{c|rrrr}
r&2&3&4&5\\ \hline
\operatorname{pole}G_r&1&4&7&10\\
\operatorname{pole}H_r&1&4&7&10
\end{array}
\]
exactly follows \(3r-5\).

Reproduction:

```bash
pytest -q test_verify_saddle_pole_orders.py
pytest -q test_verify_md2_laurent_identity.py
python3 verify_md2_laurent_identity.py
python3 verify_saddle_pole_orders.py --maximum-rank 5
```

## 8. Remaining presentation work

The marked-jet cancellation is now closed.  The remaining task for a
self-contained cubic-degree theorem is to state explicitly the
denominator-localization lemma for the rational profile recurrence:
after its removable \(x\) and \(1-x\) singularities are cancelled,
the only depth-generating singularity is \(t=1\).  Exact ranks through
five have denominators consisting solely of the predicted powers of
\(1-2x\), and the original finite Lagrange recurrence supplies the
natural coefficientwise proof.
