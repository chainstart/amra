# OPG-1757: all-rank ordinary-symbol cubic-degree theorem

Date: 2026-07-30

## 0. Theorem

Write
\[
c_k(s)=\sum_{d\ge0}b_{k,d}s^{2k-4-d},
\qquad
b_{k,d}=\sum_{r=0}^{d}\beta_{d,r}k^{d-r},
\]
and
\[
B_r(t)=\sum_{d\ge r}\beta_{d,r}t^d.
\]

### Theorem 1 (all-rank cubic degree)

For every \(r\ge0\), there is a polynomial
\(N_r(t)\in\mathbb Q[t]\) such that
\[
\boxed{
B_r(t)=\frac{N_r(t)}{(1-t)^{3r+1}},
\qquad
\deg N_r\le4r,
\qquad
t^r\mid N_r.
}
\tag{1}
\]
Consequently there is a polynomial \(P_r(d)\in\mathbb Q[d]\) of
degree exactly \(3r\) for which
\[
\boxed{
\beta_{d,r}=P_r(d)\quad(d\ge r),
\qquad
(-1)^r[d^{3r}]P_r(d)>0.
}
\tag{2}
\]
For \(d<r\), the coefficient \(\beta_{d,r}\) is zero by the ordinary-
symbol convention; (2) does not assert that the polynomial extension
\(P_r(d)\) vanishes there.

The degree and leading-sign assertions are uniform in the rank.  They
are not finite-rank interpolation statements.

## 1. Localized saddle ring

Put
\[
W=1-2x,
\qquad
C_{h,r}(x)=\frac{F_{h,r}(x)}{\sqrt W}.
\]
Use the filtered ring
\[
\mathcal R_q
=
\left\{
\frac{p(x)}{W^q}:p\in\mathbb Q[x],\ \deg p\le q
\right\}.
\tag{3}
\]
Elements of \(\mathcal R_q\) have no finite poles except \(x=1/2\)
and are bounded at infinity.

### Lemma 2 (profile localization)

For every \(h=0,1,2\) and \(r\ge0\),
\[
\boxed{C_{h,r}\in\mathcal R_{3r}.}
\tag{4}
\]

#### Endpoint sublemma

Retain first the exact finite source.  Set
\[
\begin{aligned}
{\mathscr P}_{\alpha,J}(z)
&=\prod_{q=0}^{J-1}(1-(\alpha+q)z),\\
{\mathscr L}_{\alpha,J}(z)
&=\sum_{i=0}^{J}\binom Ji2^{J-i}(-1)^i
  \prod_{q=0}^{i-1}(1-(\alpha+J+q)z).
\end{aligned}
\]
For \(a_h=0,2,4\), the three normalized Lagrange sources are exactly
\[
\begin{aligned}
{\mathscr S}_{h,J}(z)
={}&{\mathscr P}_{a_h,J}(z)
\left({\mathscr L}_{a_h,J}(z)
-2Jz\,{\mathscr L}_{a_h+1,J-1}(z)\right)\\
&+\mathbf1_{h=2}\,
8Jz^2{\mathscr P}_{4,J-1}(z)
{\mathscr L}_{4,J-1}(z).
\end{aligned}
\tag{5a}
\]
The first line is the pair of main falling-factorial factors in the
original profiles; the second is precisely the exceptional \(E\)
term.  Thus (5a) contains no limiting operation.

For \(\alpha,\ell,J\ge0\), put
\[
D_{\alpha,\ell}(i,J)
=[z^\ell]\prod_{q=0}^{i-1}
  \bigl(1-(\alpha+J+q)z\bigr).
\tag{5b}
\]
Faulhaber's formula, or induction after adjoining the last factor,
shows that \(D_{\alpha,\ell}(i,J)\) is a polynomial in \(i\).  More
precisely it has the falling-factorial expansion
\[
D_{\alpha,\ell}(i,J)
=\sum_{v=0}^{2\ell}d_{\alpha,\ell,v}(J)
  (i)_{\underline v}.
\tag{5c}
\]
Consequently its exact Lagrange transform is
\[
\begin{aligned}
\sum_{i=0}^{J}\binom Ji2^{J-i}(-1)^i
D_{\alpha,\ell}(i,J)
&=\sum_{v=0}^{2\ell}d_{\alpha,\ell,v}(J)
\sum_{i=0}^{J}\binom Ji2^{J-i}(-1)^i(i)_{\underline v}\\
&=\sum_{v=0}^{2\ell}d_{\alpha,\ell,v}(J)
(-1)^v(J)_{\underline v}.
\end{aligned}
\tag{5d}
\]
Here the last equality follows by differentiating
\((2-z)^J\) \(v\) times at \(z=1\).  Thus (5d) is an exact finite
identity, not an asymptotic cancellation.

For \(x=0\), this closes the endpoint argument.  Indeed, index a main
saddle/Gamma monomial of total rank \(r\) by
\[
\lambda=(a,b,m;(n_p)_{p\ge1}),\qquad
a+b=r,\quad m+\sum_{p\ge1}p n_p=2b.
\tag{5e}
\]
Here \(a\) is the Gamma rank, \(b\) the integral rank, \(m\) the
amplitude derivative, and \(n_p\) is the multiplicity of the phase
jet \(\phi_{p+2}\).  After its factors are put over a common
\(x=0\) denominator, the numerator has degree in the finite-sum index
at most
\[
m+\sum_{p\ge1}(p+1)n_p+2a
=2b+\sum_{p\ge1}n_p+2a
\le4b+2a\le4r.
\tag{5f}
\]
The exceptional block is already separated in the second line of
(5a): it has length \(J-1\), internal rank \(r-1\), and its explicit
prefactor adds at most two degrees.  Thus \(4r+2\) is a common finite
bound.  Applying (5d) to each \({\mathscr L}\)-block makes every
fixed source-loss coefficient a polynomial in \(J=j\).  A term
\(s^{-\ell}J^q\) has rank \(r=\ell-q\) and \(x\)-power \(q\ge0\);
hence no \(x=0\) principal part occurs.

The complementary finite-sum identity and saddle localization proved
in `COMPLEMENTARY_ENDPOINT_LOCALIZATION_LEMMA.md` give the other
endpoint:
\[
\boxed{\text{For all }h,r,\quad C_{h,r}(x)\text{ is regular at }x=1.}
\tag{5g}
\]
The proof there is all-rank: it rewrites each exact length-\(j\)
main Lagrange sum using \(Q=s-j-a_h\), and the exceptional length
\(j-1\) sum using \(P=s-j-3\), identifies the original saddle branch
with the unique maximum \(v=1\) on the overlap \(0<x<1/2\), and
analytically continues the resulting rational Poincare coefficients
to \(x=1\).  The finite verifier is only an indexing and normalization
audit of that proof.

#### Proof of Lemma 2

The exact Cauchy saddle recurrence is a rational expression in
\(x,1-x,W^{-1}\).  Its only apparent finite poles are therefore
\(0,1,1/2\).  Equations (5a)--(5f) remove \(x=0\); the complementary
endpoint lemma (5g)
removes \(x=1\).  Thus the only possible finite pole is \(x=1/2\).

It remains to control the discriminant pole \(W=0\).  The phase
derivatives and variance satisfy
\[
\operatorname{ord}_{W=0}\phi_q\ge
\begin{cases}1,&q\ {\rm even},\\0,&q\ {\rm odd},\end{cases}
\qquad
\operatorname{pole}_{W=0}\sigma=1.
\tag{6}
\]
For a phase Bell monomial with \(q\) parts at saddle rank \(r\), the
Gaussian moment contributes \(\sigma^{r+q}\), and \(q\le2r-m\), where
\(m\) is the amplitude derivative.  The simple zero of the main
amplitude and the exceptional rank shift then give
\[
\operatorname{pole}_{W=0}C_{h,r}\le3r.
\tag{7}
\]

Finally, direct homogeneity at \(x=\infty\) gives
\[
\phi_q=O(x^{1-q}),\qquad
\sigma=O(x),\qquad
\frac{g^{(m)}(2x)}{g(2x)}=O(x^{-m}).
\]
For a Bell monomial in integral rank \(b\), (5e) gives the sharper
total order
\[
x^{-m}x^{-\sum(p+1)n_p}x^{b+\sum n_p}
=x^{-b}.
\tag{7a}
\]
A Gamma monomial is \(O(1)\): the \(z=x\) and \(z=1-x\) terms in
the signed Gamma list decay, while the \(z=1\) term can have a
nonzero finite limit.  Thus every main rank-\(r\) convolution is
bounded (and the positive integral-rank terms in fact decay).  The
exceptional internal correction is bounded as well, and its
multiplier \(8x/W\) is \(O(1)\), including its first occurrence at
\(r=1\).  Hence \(C_{h,r}=O(1)\).
After the endpoint poles have been removed and (7) is imposed, this
is exactly (4). \(\square\)

In particular, substituting \(tx\) or \(t(1-x)\) introduces only the
denominators
\[
1-2tx,\qquad1-2t(1-x).
\tag{8}
\]
There is no hidden \(x^{-1}\), \((1-x)^{-1}\), or, after setting
\(x=1/2\), \(2-t\) denominator.

## 2. Marked differences

Define
\[
\delta_r=C_{1,r}-C_{0,r},
\qquad
\varepsilon_r=C_{2,r}-2C_{1,r}+C_{0,r}.
\tag{9}
\]

The exact edge-transitivity identity
\[
\Phi_1(s,x)
=\frac1{1-s^{-1}}\Phi_0(s,x+s^{-1})
\tag{10}
\]
and Lemma 2 give
\[
\boxed{
\delta_0=0,\qquad
\delta_r\in W^{-(3r-2)}\mathbb Q[x]\quad(r\ge1).
}
\tag{11}
\]

The low second differences are exactly
\[
\boxed{\varepsilon_0=\varepsilon_1=0.}
\tag{12}
\]

### Lemma 3 (all-rank second marked difference)

For every \(r\ge2\),
\[
\boxed{
\varepsilon_r\in W^{-(3r-4)}\mathbb Q[x],
\qquad
[W^{-(3r-4)}]\varepsilon_r=-6(r-1)c_{r-1},
}
\tag{13}
\]
where \(c_q=[W^{-3q}]C_{0,q}\).  In particular, the displayed pole
order is exact.

#### Proof

Let \(C_r^{(a)}\) be the main relative saddle correction with shift
\(a=0,2,4\), and set
\[
K_r=\frac{(-1)^r(6r-1)!!}{9^r(2r)!}.
\]
A pole-defect filtration shows that only eleven Bell configurations
can enter the highest four Laurent layers.  Their exact sum, including
the only possible Gamma correction, is
\[
W^{3r}C_r^{(a)}
=K_r(c_0+c_1W+c_2W^2+c_3W^3+O(W^4)),
\tag{14}
\]
where
\[
c_0=-\frac1{6r-1},\qquad c_1=0,
\]
\[
c_2=
\frac{3r(10a^2-10a+6r-1)}
{10(6r-5)(6r-1)},
\]
\[
c_3=
\frac{
r(24a^3r-24a^3-72a^2r+78a^2+48ar-54a+1)
}{
2(6r-7)(6r-5)(6r-1)
}.
\tag{15}
\]
Thus the second shift difference \(f(4)-2f(2)+f(0)\) vanishes in
layers zero and one and equals
\[
\frac{24r}{(6r-5)(6r-1)}
\tag{16}
\]
in layer two and
\[
\frac{24r(12r-11)}
{(6r-7)(6r-5)(6r-1)}
\tag{17}
\]
in layer three.

The exceptional rank-\((r-1)\) saddle, including its external factor
\(8x/W\), contributes the negatives of (16)--(17).  Hence all four
layers cancel and \(W^{3r}\varepsilon_r=O(W^4)\).  Lemma 2 excludes
all other finite denominators, proving the containment in (13).

For the leading surviving layer, defect four requires 24 main Bell
configurations.  Gamma rank one enters only through its linear
\(W\)-jet.  Their main second shift difference is
\[
-\frac{216r(r-1)(r-2)}
{5(6r-7)(6r-5)(6r-1)}.
\]
The exceptional internal correction needs only five configurations;
if
\[
W^{3r-3}C^*_{r-1}
=K^*_{r-1}(1+s_1W+s_2W^2+O(W^3)),
\]
then
\[
s_1=\frac{18(r-1)}{6r-7},\qquad
s_2=-\frac{3(r-1)(6r-77)}{10(6r-7)}.
\]
After multiplication by \(8x/W\), its defect-four contribution is
\[
\frac{36r(r-1)(6r-17)}
{5(6r-7)(6r-5)(6r-1)}.
\]
The sum is
\[
-\frac{36r(r-1)}
{(6r-7)(6r-5)(6r-1)}
=-6(r-1)\frac{c_{r-1}}{K_r}.
\]
Restoring \(K_r\) proves the leading-coefficient identity in (13).
\(\square\)

The complete eleven-configuration derivation is recorded in
`ALL_RANK_SADDLE_POLE_VALUATION_ATTACK_2026-07-30.md` and checked
symbolically, with \(r\) left indeterminate, by
`verify_md2_laurent_identity.py`.

## 3. Determinant propagation

At determinant rank \(n\), put
\[
u=tx,\qquad v=t(1-x).
\]
After summing over every \(a+b=n\), the normalized determinant is
\[
\begin{aligned}
\sum_{a+b=n}
\bigl(C_{1,a}(u)C_{1,b}(v)-C_{0,a}(u)C_{2,b}(v)\bigr)
={}&
\sum_{a+b=n}
\bigl(\delta_a(u)C_{0,b}(v)-C_{0,a}(u)\delta_b(v)\bigr)\\
&+
\sum_{a+b=n}
\bigl(\delta_a(u)\delta_b(v)-C_{0,a}(u)\varepsilon_b(v)\bigr).
\end{aligned}
\tag{18}
\]

The first sum on the right is antisymmetric under
\(x\leftrightarrow1-x\): this uses the complete convolution
\(a+b=n\) and the relabelling \(a\leftrightarrow b\).  A single fixed
\((a,b)\) summand need not be antisymmetric.  Therefore every even
\(x\)-derivative of the first sum vanishes at \(x=1/2\).

Only even derivatives occur in the centered binomial recurrence.  In
the second sum, \(\delta_0=0\), so every nonzero
\(\delta_a\delta_b\) term has \(a,b\ge1\) and gains two pole orders on
each side.  Likewise \(\varepsilon_0=\varepsilon_1=0\), so every
nonzero \(C_{0,a}\varepsilon_b\) term has \(b\ge2\), where Lemma 3
applies.  Hence both types gain four orders.

Restoring the two square-root factors supplies one factor \(1-t\) at
\(x=1/2\).  It follows that
\[
\boxed{
\operatorname{pole}_{t=1}
\partial_x^mG_n(1/2,t)\le3n-5+m.
}
\tag{19}
\]
By Lemma 2, its denominator contains no finite factor other than a
power of \(1-t\).

## 4. Central-binomial propagation

In \(H_n(t)\), determinant rank \(a\) is differentiated only through
\[
m\le2(n-a).
\]
Equation (19) gives
\[
3a-5+m
\le3a-5+2(n-a)
\le3n-5.
\]
Therefore
\[
\boxed{
H_n(t)\in
\frac{\mathbb Q[t]}{(1-t)^{3n-5}},
\qquad
H_n(t)=O(t^{n+1})\quad(t\to\infty).
}
\tag{20}
\]
For completeness, the growth assertion remains valid after every
derivative in the central recurrence.  If
\(C(z)=p(z)/(1-2z)^q\) with \(\deg p\le q\), then differentiating
\(\sqrt{1-2z}\,C(z)\) any fixed number of times and subsequently
putting \(z=tx\) is \(O(t^{1/2})\), uniformly for \(x\) in a compact
neighbourhood of \(1/2\).  Leibniz's rule therefore makes the product
of the two differentiated profiles \(O(t)\).  Together with the
external \(t^a\), each summand
\(\partial_x^mG_a(1/2,t)\) is \(O(t^{a+1})\), and hence
\(O(t^{n+1})\) when \(a\le n\).  This argument includes the
exceptional profile because its normalized correction is
\((8z/(1-2z))C_{*,r-1}(z)=O(1)\), as proved in Lemma 2.

The factor \(t^{-4}\) in
\[
B_r(t)=\frac1{2t^4}\sum_{n=2}^{r+2}H_n(t)
\tag{21}
\]
is removable term by term.  For \(n\ge4\), this follows from the
central summands, not merely from the \(G_n\) summand.  Indeed,
\(G_a\) has an external \(t^a\), and \(m\) differentiations of
profiles evaluated at \(tx,t(1-x)\) supply another \(t^m\).  If
\(a=n\), then \(m=0\) and \(a=n\ge4\).  If \(a<n\), then
\(\mu_{0,n-a}=0\); hence every nonzero summand has \(m\ge2\), while
\(a\ge2\), and again \(a+m\ge4\).  The two lower cases are the exact
identities
\[
H_2(t)=\frac{2t^4}{1-t},
\qquad
t^4\mid H_3(t).
\tag{22}
\]
Thus no pole at \(t=0\) is hidden in (21).

## 5. Proof of Theorem 1

The largest denominator in (21) occurs at \(n=r+2\), so (20) gives
\[
\operatorname{den}B_r(t)\mid(1-t)^{3r+1}.
\]
The largest growth at infinity is
\[
t^{-4}H_{r+2}(t)=O(t^{r-1}).
\]
Writing \(B_r=N_r/(1-t)^{3r+1}\) therefore gives
\[
\deg N_r\le(3r+1)+(r-1)=4r.
\]
By definition, \([t^d]B_r=0\) for \(d<r\), so \(t^r\mid N_r\).
This proves (1).

Put \(p=3r+1\) and write
\[
N_r(t)=\sum_{j=0}^{4r}n_{r,j}t^j.
\]
For every \(d\ge r\), the bound \(j\le4r=r+p-1\le d+p-1\) permits
coefficient extraction without any exceptional negative index:
\[
\beta_{d,r}
=\sum_{j=0}^{4r}
n_{r,j}
\binom{d-j+p-1}{p-1}.
\tag{23}
\]
Terms with \(d-j<0\) vanish because their upper binomial argument lies
between \(0\) and \(p-2\).  The right side of (23) is a polynomial in
\(d\) of degree at most \(p-1=3r\).  The exact degree and leading
sign are proved next.

## 6. Highest Laurent layer, exact degree, and leading sign

The argument also isolates the only datum needed to upgrade
\(\deg P_r\le3r\) to exact degree and determine its final sign.  Put
\[
\begin{aligned}
c_r&=[W^{-3r}]\,C_{0,r},\\
d_r&=[W^{-(3r-2)}]\,\delta_r,\\
e_r&=[W^{-(3r-4)}]\,\varepsilon_r,
\end{aligned}
\]
with \(c_0=1\), \(d_0=0\), and \(e_0=e_1=0\).  Equations
(14)--(15) give, for \(r\ge1\),
\[
c_r=\frac{(-1)^{r+1}(6r-3)!!}{9^r(2r)!},
\qquad
d_r=-\frac{6r}{6r-5}c_r.
\tag{24}
\]

At central rank \(n\), every term coming from determinant rank
\(a<n\) has pole at most
\[
3a-5+2(n-a)<3n-5.
\]
Thus the highest Laurent layer of \(H_n\) comes only from
\(G_n(1/2,t)\), with no central derivative.  Taking the highest layer
in (18) gives
\[
A_n:=[(1-t)^{-(3n-5)}]H_n(t)
=\sum_{a+b=n}\bigl(d_ad_b-c_ae_b\bigr).
\tag{25}
\]
Consequently the leading coefficient \(L_r=[d^{3r}]P_r(d)\) is
\[
\boxed{
L_r=\frac{A_{r+2}}{2(3r)!}.
}
\tag{26}
\]
In particular, exact degree and the eventual alternating sign reduce
to the single all-rank assertion
\[
(-1)^nA_n>0\qquad(n\ge2).
\tag{27}
\]

Lemma 3 gives the all-rank identity
\[
e_r=-6(r-1)c_{r-1}\qquad(r\ge2).
\tag{28}
\]
With
\[
C(z)=\sum_{r\ge0}c_rz^r,\qquad
D(z)=\sum_{r\ge1}d_rz^r,
\]
equation (25) is the one-variable coefficient identity
\[
A_n=[z^n]\left(D(z)^2+6zC(z)\,\theta C(z)\right),
\qquad \theta=z\frac d{dz}.
\tag{29}
\]

It remains to prove (27), which can be done by a direct convolution
bound.  For \(r\ge1\), put
\[
p_r=(-1)^{r+1}c_r>0,\qquad
q_r=(-1)^rd_r=\frac{6r}{6r-5}p_r>0,
\]
and let \(P(z)=\sum_{r\ge1}p_rz^r\),
\(Q(z)=\sum_{r\ge1}q_rz^r\).  Replacing \(z\) by \(-z\) in (29)
gives
\[
(-1)^nA_n
=[z^n]\left(Q(z)^2+6z(1-P(z))\theta P(z)\right).
\tag{30}
\]

The sequence \(p_r\) is strictly log-convex, since
\[
\frac{p_{r+1}}{p_r}
=\frac{(6r+3)(6r+1)(6r-1)}
{9(2r+2)(2r+1)}
\]
and the difference between two successive ratios is
\[
\frac{36r^2+108r+37}{6(r+1)(r+2)}>0.
\tag{31}
\]
Hence, for \(m\ge2\), every product \(p_ap_{m-a}\) is at most the
endpoint product \(p_1p_{m-1}\).  Moreover
\[
\begin{aligned}
\frac{(m-1)p_1p_{m-1}}{p_m}
&=
\frac{3(m-1)(2m)(2m-1)}
{2(6m-3)(6m-5)(6m-7)}
<\frac12.
\end{aligned}
\tag{32}
\]
The last inequality follows termwise from
\(6m-7\ge2m-1\), \(6m-5\ge2m\), and
\(6m-3>3(m-1)\).  Therefore
\[
[z^m]P(z)^2<\frac12p_m.
\tag{33}
\]

Now put \(m=n-1\).  Symmetry gives
\([z^m]P\theta P=\frac m2[z^m]P^2\), so (30) and (33) yield
\[
\begin{aligned}
(-1)^nA_n
&=[z^n]Q^2+6mp_m-3m[z^m]P^2\\
&>[z^n]Q^2+\frac92mp_m>0.
\end{aligned}
\tag{34}
\]
For \(n=2\), the same formula holds with \([z]P^2=0\).
Thus (27) holds for every \(n\ge2\).  Equations (26)--(27) prove
\(\deg P_r=3r\) and
\((-1)^r[d^{3r}]P_r>0\), completing Theorem 1. \(\square\)

## 7. Verification

Four complementary exact verifiers accompany the proof:

- `verify_md2_laurent_identity.py` checks the all-\(r\) Bell-jet
  identity and the exact leading \(\varepsilon_r\) layer symbolically;
- `verify_leading_coefficient_sign_identity.py` checks the symbolic
  ratio identities and convolution margin used in (31)--(34);
- `verify_saddle_pole_orders.py` constructs complete saddle/Gamma
  ranks through five and checks every predicted pole order; and
- `verify_all_rank_degree_localization.py` audits the localized rings,
  low-rank identities, removable \(t^4\), denominators and numerator
  degrees through the requested finite rank.

Reproduction:

```bash
pytest -q \
  test_verify_md2_laurent_identity.py \
  test_verify_leading_coefficient_sign_identity.py \
  test_verify_saddle_pole_orders.py \
  test_verify_all_rank_degree_localization.py

python3 verify_md2_laurent_identity.py
python3 verify_leading_coefficient_sign_identity.py
python3 verify_all_rank_degree_localization.py --maximum-rank 5
```

The finite audits are consistency certificates, not the proof of an
all-rank assertion.  Lemma 3, the propagation argument, and the
complementary endpoint lemma proving (5g) are arbitrary-rank
statements.  Equation (28) is independently certified with \(r\)
symbolic by the defect-four Bell/Gamma calculation.
