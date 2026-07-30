# OPG-1757: all-rank positivity of the leading long-recurrence layer

Date: 2026-07-30

## 0. Theorem

Retain the polynomial extensions from
`ORDINARY_ALL_RANK_FALLING_TRIANGLE_COROLLARY.md`:
\[
\mathfrak h_j(d),\qquad
\mathfrak g_q(d)=\gamma_{d,q}\quad(d\ge2q+1).
\]
Then, for every \(q\ge0\),
\[
\boxed{
\deg\mathfrak g_q=3q+2,\qquad
[d^{3q+2}]\mathfrak g_q(d)>0.
}
\tag{1}
\]
For \(q\ge1\), the already proved boundary factor therefore has the
sharpened form
\[
\boxed{
\mathfrak g_q(d)=(d-2q)S_q(d),\qquad
\deg S_q=3q+1,\qquad
[d^{3q+1}]S_q(d)>0.
}
\tag{2}
\]
In particular, every fixed long-recurrence band is eventually
positive:
\[
\boxed{
\text{for each fixed }q,\quad
\gamma_{d,q}>0\text{ for all sufficiently large }d.
}
\tag{3}
\]
The threshold in (3) is not claimed to be uniform in \(q\), and this
theorem does not prove \(\gamma_{d,q}>0\) at every admissible pair.

## 1. Exact logarithmic reduction

Put
\[
L_j=[d^{3j}]\mathfrak h_j(d),\qquad
G_q=[d^{3q+2}]\mathfrak g_q(d),
\]
and
\[
H(z)=\sum_{j\ge0}L_jz^j.
\]
The leading triangular identity proved in
`ORDINARY_LONG_RECURRENCE_LEADING_REDUCTION_LEMMA.md` is
\[
\boxed{
\sum_{q\ge0}G_qz^{q+1}
=-3z\frac{H'(z)}{H(z)}.
}
\tag{4}
\]
The all-rank ordinary-symbol theorem gives
\[
L_j=(-1)^j\lambda_j,\qquad \lambda_j>0.
\tag{5}
\]
It remains to prove that every nonconstant coefficient on the
right-hand side of (4) is positive.

## 2. A global coefficient bound

Use the positive highest-Laurent-layer sequences
\[
p_r=\frac{(6r-3)!!}{9^r(2r)!},\qquad
q_r=\frac{6r}{6r-5}p_r
\quad(r\ge1).
\]
If \(S_n=(-1)^nA_n>0\), equation (30) of
`ALL_RANK_ORDINARY_SYMBOL_DEGREE_THEOREM.md` says
\[
S_n=[z^n]Q(z)^2+6(n-1)p_{n-1}
-3(n-1)[z^{n-1}]P(z)^2.
\tag{6}
\]
Consequently
\[
S_n\le [z^n]Q(z)^2+6(n-1)p_{n-1}.
\tag{7}
\]

The exact ratios give
\[
\frac{p_{r+1}}{p_r}
=\frac{6(r-\frac16)(r+\frac16)}{r+1}<6r,
\]
and hence
\[
p_r\le6^{r-2}(r-1)!\quad(r\ge1).
\tag{8}
\]
Also \(q_1=1\), while
\[
q_r=(6r-7)p_{r-1}
\le6^{r-1}(r-1)!\quad(r\ge2).
\tag{9}
\]
Since \(a!b!\le(a+b)!\), equations (7)--(9) give
\[
[z^n]Q^2
\le6^{n-2}\sum_{i=1}^{n-1}(i-1)!(n-i-1)!
\le6^{n-2}(n-1)!,
\]
and the second term in (7) satisfies the same bound.  Since
\[
\lambda_r=\frac{S_{r+2}}{2(3r)!},
\]
we obtain, for every \(r\ge0\),
\[
\boxed{
0<\lambda_r\le
b_r:=\frac{6^r(r+1)!}{(3r)!}.
}
\tag{10}
\]

This already proves that \(H\) is entire of order at most \(1/2\).
Indeed,
\[
b_r\le\frac{6^r(r+1)}{(r!)^2}
\le\frac{12^r}{(r!)^2},
\]
so its maximum modulus satisfies
\[
\boxed{
M_H(x)\le
\sum_{r\ge0}\frac{(12x)^r}{(r!)^2}
\le e^{2\sqrt{12x}}.
}
\tag{11}
\]
For the last inequality, use
\(\binom{2r}{r}\le4^r\) and compare the series with
\(\cosh(2\sqrt{12x})\).

## 3. A unique dominant positive zero

The first coefficients are
\[
\lambda_0=1,\quad
\lambda_1=\frac{11}{18},\quad
\lambda_2=\frac{143}{2592},\quad
\lambda_3=\frac{3169}{1679616}.
\tag{12}
\]
Set \(R=21/10\).  For
\[
u_r=b_rR^r
\]
the ratio
\[
\frac{u_{r+1}}{u_r}
=
\frac{6R(r+2)}
{(3r+1)(3r+2)(3r+3)}
\]
is decreasing for \(r\ge4\), and its value at \(r=4\) is \(9/325\).
Therefore
\[
\begin{aligned}
\left|\sum_{r\ge2}L_rz^r\right|
&\le
\lambda_2R^2+\lambda_3R^3
+\frac{b_4R^4}{1-9/325}\\
&=
\frac{14448059591}{54058752000}
<
\frac{17}{60}
=\frac{11R}{18}-1
\end{aligned}
\tag{13}
\]
on \(|z|=R\).  Rouché's theorem applied to
\[
H(z)=1-\frac{11}{18}z+\sum_{r\ge2}L_rz^r
\]
shows that \(H\) has exactly one zero in \(|z|<R\), counted with
multiplicity.

This zero is real and positive.  It is real because nonreal zeros
occur in conjugate pairs, and it cannot be negative because
\[
H(-x)=\sum_{r\ge0}\lambda_rx^r>0\qquad(x\ge0).
\]
The same tail estimate at \(x=2\), keeping the first four exact
terms, gives
\[
H(2)
\le
-\frac{11562637}{1023096096}<0.
\tag{14}
\]
Since \(H(0)=1\), the unique zero, denoted by \(\rho\), satisfies
\[
\boxed{0<\rho<2,}
\tag{15}
\]
and every other zero \(\rho_k\) satisfies
\[
\boxed{|\rho_k|>R=21/10.}
\tag{16}
\]

## 4. Jensen bound and dominance of the first zero

Because \(H\) has order below one and \(H(0)=1\), Hadamard
factorization has genus zero:
\[
H(z)=\prod_k(1-z/\rho_k).
\tag{17}
\]
Thus, as a formal power series at the origin,
\[
-3z\frac{H'(z)}{H(z)}
=3\sum_{n\ge1}
\left(\sum_k\rho_k^{-n}\right)z^n.
\tag{18}
\]

Let \(N(s)\) count zeros in \(|z|\le s\), with multiplicity.
Applying Jensen's formula at radius \(2s\) and using (11) gives
\[
N(s)\log2
\le\log M_H(2s)
\le2\sqrt{24s},
\]
and hence
\[
\boxed{N(s)<15\sqrt s.}
\tag{19}
\]
Here \(\log2>2/3\) and \(\sqrt{24}<5\) suffice for the last constant.

Partition all zeros other than \(\rho\) into the annuli
\[
R2^j<|\rho_k|\le R2^{j+1}\qquad(j\ge0).
\]
For \(n\ge2\), equations (16) and (19) give
\[
\begin{aligned}
\sum_{k\ne1}|\rho_k|^{-n}
&<
15\sqrt{2R}\,R^{-n}
\sum_{j\ge0}2^{-j(n-1/2)}\\
&<63R^{-n}.
\end{aligned}
\tag{20}
\]
On the other hand, (15) gives \(\rho^{-n}>2^{-n}\).  Finally,
\[
\left(\frac{21}{20}\right)^{100}
>
\sum_{j=0}^{4}\binom{100}{j}20^{-j}
=\frac{403809}{6400}
>63.
\tag{21}
\]
Therefore, for every \(n\ge100\),
\[
\sum_k\rho_k^{-n}
>
2^{-n}-63R^{-n}>0.
\tag{22}
\]
Equations (18) and (22) prove \(G_{n-1}>0\) for every \(n\ge100\).

## 5. Closing the finite prefix

The exact rational verifier
`verify_all_rank_recurrence_leading_positivity.py` checks
\[
G_q>0\qquad(0\le q\le98)
\tag{23}
\]
directly from the all-rank formulas for \(c_r,d_r,e_r,A_r,L_r\);
it does not use floating-point roots.  Together, (22)--(23) prove
\(G_q>0\) for every \(q\ge0\), and hence (1)--(3).

Reproduction:

```bash
python3 verify_all_rank_recurrence_leading_positivity.py
pytest -q test_verify_all_rank_recurrence_leading_positivity.py
```

The finite verifier closes only the explicitly bounded prefix.  The
unbounded tail is proved by the coefficient bound, Rouché theorem,
Hadamard factorization, and Jensen estimate above.
