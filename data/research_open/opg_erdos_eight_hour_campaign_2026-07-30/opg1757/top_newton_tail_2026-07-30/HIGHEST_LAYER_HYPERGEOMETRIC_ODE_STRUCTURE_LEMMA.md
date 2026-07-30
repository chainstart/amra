# OPG-1757: hypergeometric and ODE structure of the highest layer

Date: 2026-07-30

## 0. Result and sign convention

Let \(\mathcal A_n\) be the original highest Laurent layer from the
ordinary-symbol theorem, so
\[
(-1)^n\mathcal A_n>0.
\]
Put
\[
S_n=(-1)^n\mathcal A_n,\qquad
A_+(z)=\sum_{n\ge2}S_nz^n.
\tag{1}
\]
The plus sign is part of the notation: \(A_+\) is the
sign-normalized series.  Confusing \(S_n\) with \(\mathcal A_n\)
reverses every other long-recurrence leading coefficient.

Define the formal hypergeometric series
\[
\begin{aligned}
U(z)&={}_2F_0\left(\frac16,-\frac16;;6z\right),\\
V(z)&={}_2F_0\left(\frac16,\frac56;;6z\right).
\end{aligned}
\tag{2}
\]
Then
\[
\boxed{
Q(z)=zV(z)=z(1-6\theta)U(z),
\qquad \theta=z\frac d{dz},
}
\tag{3}
\]
and
\[
\boxed{
A_+(z)=z^2B(z),\qquad
B(z)=(U-6zU')^2-6UU'.
}
\tag{4}
\]
These are formal identities; the \({}_2F_0\) series themselves have
zero radius of convergence.

## 1. Third-order equation and coefficient recurrence

The \({}_2F_0\) equation for \(U\) is
\[
\boxed{
36z^2U''+(36z-6)U'-U=0.
}
\tag{5}
\]
Differential elimination of \(U''\) from (4), followed by two
derivatives of (5), gives
\[
\boxed{
\begin{aligned}
0={}&54z^4(z+2)B'''
+27z^2(10z^2+23z-2)B''\\
&+3(76z^3+218z^2-41z+2)B'\\
&+(12z^2+55z-22)B.
\end{aligned}
}
\tag{6}
\]
Thus the proposed third-order operator is correct.

Write
\[
B(z)=\sum_{n\ge0}b_nz^n,\qquad
b_{-1}=b_{-2}=0,\qquad b_0=2.
\tag{7}
\]
Coefficient extraction from (6) gives the exact three-step
recurrence
\[
\boxed{
\begin{aligned}
6(n+1)b_{n+1}={}&(54n^2+69n+22)b_n\\
&-(108n^3-27n^2-21n-5)b_{n-1}\\
&-6(n-1)(3n-5)(3n-4)b_{n-2}.
\end{aligned}
}
\tag{8}
\]
Its first values are
\[
2,\quad\frac{22}{3},\quad\frac{715}{9},\quad
\frac{110915}{81},\quad\frac{31199245}{972}.
\tag{9}
\]
They are \(S_2,S_3,\ldots\).  Positivity of all \(b_n\) is already a
consequence of the highest-layer sign theorem; it is not transparent
term by term from (8), which contains two subtractive terms.

## 2. Whittaker, Bessel, and Airy interpretation

Set
\[
t=-\frac1{6z}.
\]
The sectorial Tricomi representatives whose asymptotic expansions
give (2) are
\[
\begin{aligned}
U(z)
&\sim t^{1/6}\mathrm U\left(\frac16,\frac43,t\right)
=e^{t/2}t^{-1/2}W_{1/2,1/6}(t),\\
V(z)
&\sim t^{1/6}\mathrm U\left(\frac16,\frac13,t\right)
=e^{t/2}W_{0,1/3}(t).
\end{aligned}
\tag{10}
\]
The second expression is genuinely Bessel:
\[
\boxed{
V(z)\sim
e^{t/2}\sqrt{\frac{t}{\pi}}K_{1/3}(t/2).
}
\tag{11}
\]
Using
\[
\operatorname{Ai}(x)
=\frac1\pi\sqrt{\frac{x}{3}}\,
K_{1/3}\left(\frac23x^{3/2}\right),
\]
equation (11) is also an Airy representation after
\[
x=(3t/4)^{2/3}.
\tag{12}
\]
All statements in (10)--(12) are understood in compatible
asymptotic sectors and branches.

There is also a precise symmetric-square explanation of the order
three in (6).  In the \(t\)-variable,
\[
V=U+6tU_t,\qquad
U=\left(1+\frac1{6t}\right)V-V_t.
\tag{13}
\]
Substitution into (4) gives
\[
\boxed{
B=
\left(2+\frac1{6t}\right)V^2
-(6t+2)VV_t+6tV_t^2.
}
\tag{14}
\]
Thus \(B\) is a rational quadratic form in one solution of the
Bessel/Airy second-order module and its derivative.  Equation (6) is
the scalar cyclic-vector equation induced from the corresponding
symmetric-square differential module.  This explains the order
three, but does not by itself impose coefficient or logarithmic
positivity after the factorial transform below.

## 3. The factorial transform is entire of order at most \(1/2\)

Define
\[
H_+(z)
=\sum_{r\ge0}\lambda_rz^r,
\qquad
\lambda_r=\frac{S_{r+2}}{2(3r)!}
=\frac{b_r}{2(3r)!}>0.
\tag{15}
\]
An explicit coefficient bound follows from the earlier convolution.
If
\[
p_r=\frac{(6r-3)!!}{9^r(2r)!},
\]
then
\[
\frac{p_{r+1}}{p_r}
=\frac{36r^2-1}{6(r+1)}<6r,
\]
and hence
\[
p_r\le6^{r-1}(r-1)!\qquad(r\ge1).
\tag{16}
\]
Moreover \(q_r=6r\,p_r/(6r-5)\le6p_r\).  Since the signed highest
layer satisfies
\[
0<S_n
\le [z^n]Q(z)^2+6(n-1)p_{n-1},
\]
equation (16) gives the completely explicit bound
\[
\boxed{
S_n\le7\cdot6^{n-1}(n-1)!
\qquad(n\ge2).
}
\tag{17}
\]
Consequently
\[
\boxed{
0<\lambda_r
\le\frac{7\cdot6^{r+1}(r+1)!}{2(3r)!}.
}
\tag{18}
\]
Stirling's formula yields
\[
\log\frac1{\lambda_r}
\ge2r\log r+O(r),
\]
so \(H_+\) is entire and
\[
\boxed{\operatorname{ord}H_+\le\frac12.}
\tag{19}
\]
The original alternating leading series is
\[
H_-(z)=H_+(-z)
=\sum_{r\ge0}
\frac{\mathcal A_{r+2}}{2(3r)!}z^r.
\tag{20}
\]
It has the same order.  Since its order is strictly below one and
\(H_-(0)=1\), Hadamard factorization has genus zero and no
nonconstant exponential factor:
\[
\boxed{
H_-(z)=\prod_k\left(1-\frac z{\rho_k}\right),
\qquad
\sum_k|\rho_k|^{-1}<\infty.
}
\tag{21}
\]
Complex zeros are listed with multiplicity.

## 4. Exact zero-power-sum reduction and positivity closure

Let \(G_q\) be the degree-\((3q+2)\) coefficient of the \(q\)-th
long band.  The falling-triangle identity gives
\[
\widetilde G(z)
:=\sum_{q\ge0}G_qz^{q+1}
=-3z\frac{H_-'(z)}{H_-(z)}.
\tag{22}
\]
Combining (21)--(22) gives the absolutely convergent power sums
\[
\boxed{
G_{n-1}=3\sum_k\rho_k^{-n}
\qquad(n\ge1).
}
\tag{23}
\]
Therefore
\[
\boxed{
G_q>0\text{ for all }q
\quad\Longleftrightarrow\quad
\sum_k\rho_k^{-n}>0\text{ for all }n\ge1.
}
\tag{24}
\]
This is the precise zero-theoretic form of the positivity problem.
Positive real zeros contribute positively to every power sum;
negative or nonreal-conjugate zeros require quantitative control.

The sign normalization matters.  From (15),
\[
-3zH_+'(z)/H_+(z)
\]
starts
\[
-\frac{11}{6}z+\frac{341}{432}z^2
-\frac{74317}{186624}z^3+\cdots;
\]
it is alternating, not coefficientwise positive.  The positive
long-recurrence series is (22), equivalently
\[
-3z\frac d{dz}\log H_+(-z).
\tag{25}
\]

Neither the linear ODE (6) for the pre-factorial series \(B\), nor
the Airy representation alone, proves the signs in (24).  The
factorial transform and logarithm are essential, and recurrence (8)
has mixed signs.  The missing global control is supplied in
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`:
a coefficient majorant and Rouché's theorem isolate a unique
positive dominant zero, while Jensen's formula bounds all remaining
zeros.  Dominance proves (24) for \(n\ge100\), and exact rational
verification closes \(1\le n\le99\).  Thus (24), and hence
\(G_q>0\), now holds for every \(q\ge0\).

## 5. Verification

`verify_highest_layer_hypergeometric_ode.py` independently checks:

- both \({}_2F_0\) coefficient recurrences and (3);
- exact differential elimination of (5) to (6);
- recurrence (8);
- agreement with the first known highest layers and long-band
  leading coefficients; and
- a redundant finite sign scan.

The differential elimination is symbolic, not a finite-series guess.
