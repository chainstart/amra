# OPG-1757 ordinary symbols: Poisson--Newton real-rootedness attack

Date: 2026-07-30

## 0. Status

The all-depth real-rootedness statement remains open.  This note records:

1. a proved forced falling-factorial divisor;
2. an exact Poisson--Newton reduction of the problem;
3. an existing Pochhammer-transform theorem which turns
   Poisson real-rootedness into the desired ordinary-symbol
   real-rootedness;
4. an exact bivariate forest-profile generating function which gives
   a precise stability target;
5. exact finite certificates through depth \(50\); and
6. exact obstructions to two tempting but invalid proof routes.

Finite computations in this note are evidence and certificates, not an
all-depth proof.

## 1. Ordinary symbols and their forced factor

Write
\[
c_k(s)=\sum_{d\geq 0}b_{k,d}s^{2k-4-d}
\]
and let \(P_d(k)\) denote the degree-\(d\), monic polynomial extension
of \(b_{k,d}\).

### Lemma 1 (forced inactive-depth factor)

For every \(d\geq1\),
\[
\boxed{
 P_d(k)=
 \prod_{r=2}^{\lfloor(d+3)/2\rfloor}(k-r)\,Q_d(k),
 \qquad \deg Q_d=\lfloor d/2\rfloor .
}
\tag{1}
\]

#### Proof

The normalized profile formula expresses the numerator of \(b_{k,d}\)
as a binomial average of a polynomial in \(j\) and \(k-j\).  Exact
binomial moments make this numerator a polynomial in \(k\).  The
eventual polynomial identity already proved for \(P_d\), multiplied by
\(2k(k-1)\), therefore holds identically and hence holds at every
integer \(k\geq2\).

If \(d>2k-4\), the requested coefficient lies below the constant term
of the degree-\(2k-4\) polynomial \(c_k(s)\), and is zero.  Thus
\[
P_d(k)=0
\quad\text{for}\quad
2\leq k\leq\left\lfloor\frac{d+3}{2}\right\rfloor .
\]
These are \(\lceil d/2\rceil\) distinct roots.  Division of the monic
degree-\(d\) polynomial gives (1). \(\square\)

The finite experiment shows that all roots of \(Q_d\) are simple,
positive, lie to the right of the forced roots, and strictly interlace
those of \(Q_{d+1}\), through \(d=50\).

## 2. The exact Poisson--Newton transform

Put \(n=k-2\), and define
\[
\boxed{
A_d(z)
=e^{-z}\sum_{n\geq0}P_d(n+2)\frac{z^n}{n!}.
}
\tag{2}
\]
Because \(P_d\) is a polynomial, (2) is a polynomial as well.  Newton's
formula gives
\[
A_d(z)
=\sum_{j=0}^{d}
\frac{\Delta^jP_d(2)}{j!}z^j,
\qquad
P_d(n+2)
=\sum_{j=0}^{d}
\frac{\Delta^jP_d(2)}{j!}(n)_{\underline j}.
\tag{3}
\]

Lemma 1 implies
\[
\Delta^jP_d(2)=0
\quad(0\leq j<\lceil d/2\rceil).
\tag{4}
\]
All exact rows through \(d=50\) additionally satisfy
\[
(-1)^{d-j}\Delta^jP_d(2)>0
\quad(\lceil d/2\rceil\leq j\leq d).
\tag{5}
\]

Define \(H_d\) by
\[
\boxed{
A_d(x^2)=x^dH_d(x).
}
\tag{6}
\]
Then \(H_d\) is monic of degree \(d\), has the parity of \(d\), and
has matching-polynomial sign shape:
\[
H_d(x)=
\sum_{r=0}^{\lfloor d/2\rfloor}
(-1)^r m_{d,r}x^{d-2r},
\qquad m_{d,r}>0
\tag{7}
\]
in the certified range.  The first rows are
\[
\begin{aligned}
H_1(x)&=x,\\
H_2(x)&=x^2-18,\\
H_3(x)&=x(x^2-101/2),\\
H_4(x)&=x^4-\frac{607}{6}x^2+282.
\end{aligned}
\tag{8}
\]

Equation (7) alone does not identify \(H_d\) as the matching polynomial
of an explicit graph.  Such an identification would itself need a
construction or a stability proof.

## 3. A rigorous bridge from \(A_d\) to \(P_d\)

Let \(T\) be the Pochhammer transformation
\[
T\left(\sum_j a_jz^j\right)
=\sum_j a_j(n)_{\underline j}.
\tag{9}
\]
A theorem of Brenti, reproved as Lemma 11 in Brändén--Krasikov--Shapiro,
*Elements of Pólya--Schur theory in the finite difference setting*,
Proc. AMS 144 (2016), 4831--4843, states:

> If a polynomial has only real nonnegative zeros, then its
> Pochhammer transform has only real nonnegative zeros and mesh at
> least one.

See arXiv:1204.2963, Lemma 11.

Combining this theorem with (3) gives the following sufficient
condition.

### Proposition 2 (Poisson reduction)

If \(A_d\) has only nonnegative real zeros, equivalently if \(H_d\) is
real-rooted, then \(P_d\) has only positive real zeros.  In fact the
zeros of \(P_d(k)\) have mutual distance at least one.

Thus the all-depth target is reduced to
\[
\boxed{
H_d\text{ is real-rooted for every }d\geq1.
}
\tag{10}
\]
The repeated zero of \(A_d\) at the origin causes no problem in the
Pochhammer theorem.

This reduction is useful because \(H_d\) has half as many independent
root squares and a symmetric matching-polynomial shape.

## 4. Exact bivariate forest-profile identity

Let
\[
\mathcal U_h(y;s)=\sum_{j\geq0}U_{h,j}(s)y^j
\qquad(h=0,1,2)
\tag{11}
\]
be the three exact weighted complete-graph forest-profile series.
Define
\[
\mathcal A(z,t)=\sum_{d\geq0}A_d(z)t^d .
\tag{12}
\]
Using
\[
c_k(s)=\frac{(k-2)!}{2}
\sum_{j=0}^{k}
\left(
U_{1,j}(s)U_{1,k-j}(s)
-U_{0,j}(s)U_{2,k-j}(s)
\right)
\tag{13}
\]
in (2), and setting \(y=zt^2\), gives the exact formal identity
\[
\boxed{
\mathcal A(z,t)
=
\frac{e^{-z}}{2y^2}
\left[
\mathcal U_1(y;1/t)^2
-\mathcal U_0(y;1/t)\mathcal U_2(y;1/t)
\right],
\qquad y=zt^2.
}
\tag{14}
\]
The apparent negative powers cancel because the determinant begins at
total profile loss four.

With
\[
\mathcal H(x,w)=\sum_{d\geq0}H_d(x)w^d
=\mathcal A(x^2,w/x),
\]
equation (14) becomes
\[
\boxed{
\mathcal H(x,w)
=\frac{e^{-x^2}}{2w^4}
\left[
\mathcal U_1(w^2;x/w)^2
-\mathcal U_0(w^2;x/w)\mathcal U_2(w^2;x/w)
\right].
}
\tag{15}
\]

Equation (15) is the most precise current stability target.  A proof
that its finite truncations have the relevant real-stability/proper-
position property would imply that the \(H_d\) are real-rooted and
that consecutive \(H_d\)'s interlace.  Via Proposition 2 this would
settle the ordinary-symbol real-rootedness.

The unresolved step is to transfer stability or a compatible
Lorentzian property from the weighted forest profiles through the
Rayleigh determinant and the diagonal substitutions in (15).

## 5. Recurrence experiments and exact obstructions

### 5.1 Ordinary Favard recurrence fails

The monic three-term ansatz
\[
P_{d+1}(k)=(k-\alpha_d)P_d(k)-\beta_dP_{d-1}(k)
\tag{16}
\]
holds accidentally for \(d=1,2\), but fails at \(d=3\).  Leading
coefficients force
\[
\alpha_3=\frac{167}{3},
\qquad
\beta_3=\frac{13963}{6},
\]
and the remaining exact residual is
\[
\boxed{-41889(k-2)\neq0.}
\tag{17}
\]
Therefore the \(P_d\) are not an ordinary orthogonal-polynomial
sequence.

### 5.2 Weighted-path recurrence for \(H_d\) also fails

The path-matching ansatz
\[
H_{d+1}=xH_d-\lambda_dH_{d-1}
\tag{18}
\]
also first fails at \(d=3\):
\[
xH_3-H_4=\frac{152}{3}H_2+630H_0.
\tag{19}
\]

However, the longer same-parity expansion
\[
\boxed{
xH_d-H_{d+1}
=
\sum_{q=0}^{\lfloor(d-1)/2\rfloor}
\gamma_{d,q}H_{d-1-2q}
}
\tag{20}
\]
has strictly positive rational coefficients
\(\gamma_{d,q}\) in every exactly checked row \(1\leq d\leq49\).
The first cases are
\[
\begin{aligned}
xH_1-H_2&=18H_0,\\
xH_2-H_3&=\frac{65}{2}H_1,\\
xH_3-H_4&=\frac{152}{3}H_2+630H_0.
\end{aligned}
\tag{21}
\]

This is finite evidence for a compatible-polynomial or branched
continued-fraction proof.  Positivity in (20), by itself, has not yet
been shown to preserve interlacing; that implication must be proved,
not assumed.

### 5.3 Entrywise-positive production matrix is not totally nonnegative

Expanding \(kP_d\) in the monic basis \(P_0,P_1,\ldots\) gives positive
connection coefficients in the checked initial rows.  Nevertheless,
the resulting Hessenberg production matrix is not totally
nonnegative.  Already the minor with rows \((2,3)\) and columns
\((1,2)\) equals
\[
-125667.
\tag{22}
\]
Thus a direct Gantmacher--Krein argument from total nonnegativity is
blocked.

## 6. Exact finite certificate through depth 50

The script `verify_ordinary_real_rootedness.py` reconstructs every
\(P_d\) directly from the normalized exact Lagrange profiles, using
two unused interpolation holdouts per row.  It then checks with exact
rational arithmetic:

- all coefficients of \(P_d\) strictly alternate;
- the divisor in (1);
- all residual roots of \(Q_d\) are positive and simple;
- the residual roots of \(Q_d,Q_{d+1}\) strictly interlace;
- the falling-factorial coefficients satisfy (4)--(5);
- all nonzero roots of \(A_d\) are positive and simple;
- consecutive \(H_d,H_{d+1}\) strictly interlace;
- all connection coefficients in (20) are positive; and
- the exact Favard obstruction (17).

The root claims use rational isolating intervals over
\(\mathbb Q\), not floating-point approximations.

Results:
\[
\begin{array}{c|c}
\text{property}&\text{exact certified range}\\ \hline
P_d\text{ positive simple roots}&1\leq d\leq50\\
Q_d,Q_{d+1}\text{ strict interlacing}&1\leq d<50\\
A_d\text{ nonzero positive simple roots}&1\leq d\leq50\\
H_d,H_{d+1}\text{ strict interlacing}&1\leq d<50\\
\text{positive recurrence (20)}&1\leq d<50
\end{array}
\tag{23}
\]

The independent unreduced Sturm run through \(d=50\) also passed.  It
took about 15 minutes and at most 242 MB.  The factorized rational-
interval audit is substantially faster.

Reproduction:

```bash
pytest -q test_verify_ordinary_real_rootedness.py
python3 verify_ordinary_real_rootedness.py \
  --maximum-depth 50 \
  --interval-decimal-digits 12
```

## 7. Conditional weighted-symbol consequence

Suppose (10) is proved.  Write the positive roots of \(P_d\) as
\(\rho_1,\ldots,\rho_d\).  Then
\[
(-1)^r\beta_{d,r}=e_r(\rho_1,\ldots,\rho_d).
\]
Maclaurin's inequality gives
\[
|\beta_{d,r}|
\leq
\binom dr
\left(\frac{e_1}{d}\right)^r.
\tag{24}
\]
The proved first defect is
\[
e_1=
\frac{22d^3+147d^2+161d-258}{36}.
\]
For \(d=1\) the desired comparison is immediate; for \(d\geq2\), put
\(u=d-2\) and observe
\[
3d^3-e_1
=
\frac{
86u^3+369u^2+283u+36
}{36}>0.
\tag{25}
\]
Consequently
\[
\boxed{
|\beta_{d,r}|
\leq \binom dr(3d^2)^r.
}
\tag{26}
\]

Thus all-depth real-rootedness proves the weighted constant \(C=3\)
and supplies the missing \(k^{1/3}\) ordinary-symbol window.

## 8. Next proof targets

The highest-value routes are now:

1. derive a closed Lagrange equation for the three
   \(\mathcal U_h(y;s)\) in (15) and prove proper position of the
   Rayleigh determinant;
2. prove coefficientwise real stability of finite truncations of
   \(\mathcal H(x,w)\);
3. derive an all-\(d\) formula or recurrence for the positive
   coefficients \(\gamma_{d,q}\) in (20), then prove that recurrence
   preserves compatibility/interlacing; or
4. construct an explicit weighted matching or independence model for
   \(H_d\).

The simple Favard, weighted-path, and totally-nonnegative production
matrix routes should not receive further time unless new structure
changes their exact obstructions.

An all-depth proof along one of routes 1--4, combined with the
\(C=3\) and \(k^{1/3}\) consequence, would be a credible paper-level
result.  The current finite certificate alone is not publishable as a
theorem.
