# OPG-1757: leading long-recurrence logarithmic derivative

Date: 2026-07-30

> **Historical scope note.**  This audit records the intermediate
> logarithmic-derivative reduction before the dominant-zero argument
> was found.  Its statements below that the reduction alone does not
> prove all-rank positivity remain correct as descriptions of that
> intermediate argument.  The missing step is subsequently supplied,
> with two independent audits, in
> `ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`.

## 0. Outcome

Let
\[
L_j=[d^{3j}]P_j(d),\qquad
H(z)=\sum_{j\ge0}L_jz^j,
\qquad
\mathcal G(z)=-3z\frac{H'(z)}{H(z)}
=\sum_{q\ge1}G_qz^q.
\tag{1}
\]
The all-rank highest-Laurent calculation proves
\((-1)^jL_j>0\).  This note obtains three further rigorous results:

1. the positive numbers \(h_j=(-1)^jL_j\) satisfy a new
   second-order polynomial recurrence;
2. \(K(z)=H(-z)=\sum h_jz^j\) is an entire function of order at most
   \(1/2\); and
3. positivity of every \(G_q\) is reduced exactly to coefficientwise
   infinite divisibility of \(1/H\), with the stronger
   \(PF_\infty\)/Laguerre--Pólya route isolated as a sufficient
   condition.

The available argument does **not** yet prove \(G_q>0\) for every
\(q\).  The accompanying exact verifier extends the finite check from
24 to 120 coefficients and records positive Hankel and continued-
fraction evidence, but labels these checks as finite evidence.

## 1. Hypergeometric form of the highest Laurent layer

Use the notation from the all-rank leading-sign proof:
\[
p_r=(-1)^{r+1}c_r
=\frac{(6r-3)!!}{9^r(2r)!}>0,
\qquad
q_r=(-1)^rd_r=\frac{6r}{6r-5}p_r.
\tag{2}
\]
Put
\[
F(z)=C(-z),\qquad Q(z)=D(-z).
\]
The ratio in (2) gives the formal hypergeometric identity
\[
\boxed{
F(z)={}_2F_0\left(-\frac16,\frac16;\ ;6z\right),
\qquad
Q(z)=z\bigl(F(z)-6\theta F(z)\bigr),
}
\tag{3}
\]
where \(\theta=z\,d/dz\).  These are formal series; no convergence of
the \({}_2F_0\) series is asserted.

If \(A_n\) is the highest Laurent layer at central rank \(n\), the
proved identity \(e_r=-6(r-1)c_{r-1}\) gives
\[
\sum_{n\ge2}(-1)^nA_nz^n
=Q(z)^2-6zF(z)\theta F(z).
\tag{4}
\]
Since
\[
h_j=\frac{(-1)^jA_{j+2}}{2(3j)!},
\tag{5}
\]
write the right side of (4) as \(z^2S(z)\).  Then
\[
\boxed{
S(z)=\bigl(F(z)-6zF'(z)\bigr)^2-6F(z)F'(z)
=2\sum_{j\ge0}(3j)!h_jz^j.
}
\tag{6}
\]

## 2. A new exact second-order recurrence

The hypergeometric equation for \(F\) is
\[
36z^2F''+(36z-6)F'-F=0.
\tag{7}
\]
Apply (7) to the quadratic vector
\((F^2,FF',(F')^2)\).  Direct elimination gives
\[
\begin{aligned}
0={}&54z^4(z+2)S'''
+27z^2(10z^2+23z-2)S''\\
&+3(76z^3+218z^2-41z+2)S'
+(12z^2+55z-22)S.
\end{aligned}
\tag{8}
\]
This symmetric-square calculation is checked symbolically in the
verifier, not inferred from numerical coefficients.

Define
\[
\begin{aligned}
R_n={}&
9(n+2)^2(3n+4)(3n+5)(6n+5)h_{n+2}\\
&-(162n^3+675n^2+885n+361)h_{n+1}
+2(6n+11)h_n.
\end{aligned}
\tag{9}
\]
Substitution of (6) into (8) makes its \(n\)-th coefficient
\[
\frac{(3n+3)!}{6n+11}R_n
+\frac{2(3n+6)!}{6n+11}R_{n+1}.
\tag{10}
\]
The initial values
\[
h_0=1,\qquad h_1=\frac{11}{18},\qquad
h_2=\frac{143}{2592}
\]
give \(R_0=0\).  Equations (8)--(10) then imply inductively
\[
\boxed{
R_n=0\qquad(n\ge0).
}
\tag{11}
\]
Thus (9) is an all-rank identity, not a guessed recurrence.

## 3. Entire order

Let
\[
M_n=162n^3+675n^2+885n+361
\]
and let \(U_n\) denote the coefficient of \(h_{n+2}\) in (9).
Since all \(h_j\) are positive, (11) gives
\[
0<\frac{h_{n+2}}{h_{n+1}}<\frac{M_n}{U_n}.
\]
Moreover
\[
\begin{aligned}
U_n-(n+1)^2M_n
={}&324n^5+2808n^4+9294n^3\\
&+14726n^2+11173n+3239>0.
\end{aligned}
\tag{12}
\]
Consequently
\[
\frac{h_{n+2}}{h_{n+1}}<\frac1{(n+1)^2}.
\tag{13}
\]
It follows directly that \(K(z)=\sum h_jz^j\) is entire of order at
most \(1/2\).

## 4. Exact equivalences for \(G_q>0\)

Since \(H(z)=K(-z)\), coefficient extraction in (1) gives
\[
\boxed{
G_q=3q(-1)^{q+1}[z^q]\log K(z).
}
\tag{14}
\]
Equivalently,
\[
H(z)^{-\tau}
=\exp\left(
\tau\sum_{q\ge1}\frac{G_q}{3q}z^q
\right).
\tag{15}
\]
Therefore the following are equivalent:

1. \(G_q\ge0\) for every \(q\ge1\);
2. \(H(z)^{-\tau}\) has nonnegative coefficients for every
   real \(\tau>0\); and
3. \(1/H(z)\) is coefficientwise infinitely divisible in the
   semiring of nonnegative formal power series.

The reverse implication follows by differentiating the coefficient
of \(z^q\) in (15) at \(\tau=0\).  Strict positivity follows if no
coefficient in the exponent vanishes.

This is the precise weakest target found here.  Positivity of the
coefficients of \(1/H\) alone is not sufficient; infinite
divisibility is the missing property.

## 5. The \(PF_\infty\) route

A stronger, geometrically transparent sufficient condition is
\[
\boxed{(h_j)_{j\ge0}\text{ is a }PF_\infty\text{ sequence}.}
\tag{16}
\]
Indeed, the Edrei representation and the order bound (13) would then
force
\[
K(z)=\prod_{\nu\ge1}(1+\alpha_\nu z),
\qquad
\alpha_\nu\ge0,\qquad
\sum_\nu\alpha_\nu<\infty.
\tag{17}
\]
There can be no exponential factor because \(K\) has order below
one, and no denominator factor because \(K\) is entire.  Hence
\[
\mathcal G(z)
=3\sum_{\nu\ge1}\frac{\alpha_\nu z}{1-\alpha_\nu z},
\qquad
G_q=3\sum_{\nu\ge1}\alpha_\nu^q>0.
\tag{18}
\]
Thus a proof that \(K\) lies in the Laguerre--Pólya class with
negative zeros would finish the leading long-recurrence problem.

The recurrence (11) is compatible with this picture but does not by
itself invoke a standard \(PF_\infty\)-preserving theorem: it contains
the subtraction
\[
U_nh_{n+2}=M_nh_{n+1}-2(6n+11)h_n.
\]
Controlling positive coefficients or adjacent ratios therefore does
not automatically control all Toeplitz minors or all Jensen
polynomials.  This is the smallest present proof obstruction.

## 6. Exact finite evidence and the continued fraction

The verifier constructs \(p_r,q_r,A_r,h_r,G_r\) by exact rational
arithmetic and proves:

- recurrence (11) through the requested finite rank;
- \(G_q>0\) through \(q=120\);
- the first seven leading Hankel determinants of
  \((G_{q+1})_{q\ge0}\) are positive; and
- the first twelve coefficients of the Stieltjes continued fraction
  for
  \[
  \frac{\mathcal G(z)}{G_1z}
  =\sum_{q\ge0}\frac{G_{q+1}}{G_1}z^q
  \tag{19}
  \]
  are positive.

The continued-fraction coefficients begin
\[
\frac{31}{72},\quad
\frac{10891}{147312},\quad
\frac{270549241}{8021874960},\quad\ldots
\]
They are positive but do not presently exhibit a simple rational
formula in their index.  Proving that all of them are positive would
show that \((G_{q+1})\) is a Stieltjes moment sequence, a sufficient
condition stronger than the desired coefficient positivity.

The Hankel and continued-fraction checks are deliberately not called
an all-rank proof.  The publishable rigorous part is the
hypergeometric representation (3)--(6), the differential equation
(8), the all-rank recurrence (11), the entire-order bound (13), and
the exact reductions (14)--(18).

## 7. Reproduction

```bash
python3 verify_long_recurrence_leading_log_derivative.py \
  --maximum-rank 120 --continued-fraction-depth 12

pytest -q test_verify_long_recurrence_leading_log_derivative.py
```
