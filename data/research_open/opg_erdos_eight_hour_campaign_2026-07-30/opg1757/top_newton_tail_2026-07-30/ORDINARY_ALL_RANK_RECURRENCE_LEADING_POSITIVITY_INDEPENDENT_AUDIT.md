# Independent audit: all-rank recurrence-leading positivity

Date: 2026-07-30

## 0. Verdict

\[
\boxed{\text{PASS}}
\]

The proof in
`ORDINARY_ALL_RANK_RECURRENCE_LEADING_POSITIVITY_THEOREM.md`
correctly establishes
\[
G_q=[d^{3q+2}]\mathfrak g_q(d)>0
\qquad(q\ge0).
\]
The coefficient majorant, Rouché localization, Jensen estimate,
zero-power-sum dominance, and exact finite prefix have compatible
indices and leave no uncovered rank.

## 1. Independent check of the coefficient majorant

For
\[
p_r=\frac{(6r-3)!!}{9^r(2r)!},
\]
direct cancellation gives
\[
\frac{p_{r+1}}{p_r}
=\frac{36r^2-1}{6(r+1)}<6r.
\]
Since \(p_1=1/6\), induction yields the sharper bound
\[
p_r\le6^{r-2}(r-1)!\qquad(r\ge1).
\]
Moreover,
\[
q_1=1,\qquad q_r=(6r-7)p_{r-1}
\le6^{r-1}(r-1)!\qquad(r\ge2).
\]
For \(n\ge2\),
\[
\begin{aligned}
[z^n]Q^2
&\le6^{n-2}
\sum_{i=1}^{n-1}(i-1)!(n-i-1)!\\
&\le6^{n-2}(n-1)!.
\end{aligned}
\]
The last inequality follows because each summand is at most
\((n-2)!\), and there are \(n-1\) summands.  Also
\[
6(n-1)p_{n-1}\le6^{n-2}(n-1)!.
\]
Dropping the negative \(P^2\) term from the exact highest-layer
identity therefore gives
\[
S_n\le2\cdot6^{n-2}(n-1)!.
\]
With \(n=r+2\), this is exactly
\[
\lambda_r=\frac{S_{r+2}}{2(3r)!}
\le\frac{6^r(r+1)!}{(3r)!}=b_r.
\]
Thus the majorant used in the complex-analytic argument includes
the small case \(r=0\) and has the stated constant.

The further estimate
\[
b_r\le\frac{12^r}{(r!)^2}
\]
is valid: \((3r)!\ge(r!)^3\) gives the intermediate factor
\(6^r(r+1)/(r!)^2\), and \(r+1\le2^r\) for \(r\ge0\).
Consequently
\[
M_H(x)\le\sum_{r\ge0}\frac{(12x)^r}{(r!)^2}
\le e^{2\sqrt{12x}},
\]
so \(H\) has order at most \(1/2\).

## 2. Independent check of the Rouché certificate

Set \(R=21/10\).  For \(u_r=b_rR^r\),
\[
\frac{u_{r+1}}{u_r}
=\frac{6R(r+2)}
{(3r+1)(3r+2)(3r+3)}.
\]
This ratio decreases for \(r\ge4\), and its first value is
\[
\frac{u_5}{u_4}=\frac9{325}.
\]
Exact rational arithmetic gives
\[
\lambda_2R^2+\lambda_3R^3+
\frac{b_4R^4}{1-9/325}
=\frac{14448059591}{54058752000},
\]
while
\[
\lambda_1R-1=\frac{17}{60}.
\]
Their strict difference is
\[
\frac{868586809}{54058752000}>0.
\]
Hence Rouché's theorem does give exactly one zero, counted with
multiplicity, in \(|z|<R\), and no zero on \(|z|=R\).

At \(x=2\), the corresponding tail ratio starts at \(12/455\).
Keeping the terms through degree three and replacing the remaining
signed tail by its absolute majorant gives
\[
H(2)\le-\frac{11562637}{1023096096}<0.
\]
Since \(H(0)=1\), there is a positive real zero \(\rho\in(0,2)\).
The Rouché count makes it the unique zero in \(|z|<R\) and proves
that it is simple.  All remaining zeros have modulus strictly
greater than \(R\).

## 3. Independent check of Jensen and zero dominance

Because the order is strictly below one and \(H(0)=1\), Hadamard
factorization has no nonconstant exponential factor and uses genus
zero.  In particular,
\[
H(z)=\prod_k(1-z/\rho_k),\qquad
\sum_k|\rho_k|^{-1}<\infty,
\]
so logarithmic differentiation and coefficient extraction are
justified near the origin.

Jensen's formula at radius \(2s\) gives
\[
N(s)\log2\le\log M_H(2s)\le2\sqrt{24s}.
\]
The elementary inequalities \(\log2>2/3\) and
\(\sqrt{24}<5\) imply
\[
N(s)<15\sqrt s.
\]
For \(n\ge2\), grouping all zeros other than \(\rho\) in the
annuli \(R2^j<|\rho_k|\le R2^{j+1}\) therefore gives
\[
\sum_{k\ne1}|\rho_k|^{-n}
<
\frac{15\sqrt{2R}}{1-2^{1/2-n}}R^{-n}
<63R^{-n}.
\]
The last inequality follows from \(\sqrt{2R}<R\) and
\(1-2^{1/2-n}>1/2\).

Since \(\rho<2\), its contribution is greater than \(2^{-n}\).
Finally, the first five binomial terms already give
\[
\left(\frac{21}{20}\right)^{100}
>
\sum_{j=0}^4\binom{100}{j}20^{-j}
=\frac{403809}{6400}>63.
\]
Thus, for every \(n\ge100\),
\[
\sum_k\rho_k^{-n}
>
2^{-n}-63R^{-n}>0.
\]
The logarithmic identity then proves \(G_{n-1}>0\) for the entire
infinite tail \(n\ge100\).

## 4. Finite-prefix scope and sign convention

`verify_all_rank_recurrence_leading_positivity.py` calls
`falling_leading_coefficients(99)`, which returns the 100 values
\(L_0,\ldots,L_{99}\).  The triangular logarithmic recurrence then
returns exactly
\[
G_0,\ldots,G_{98}.
\]
It checks all 99 values with exact `Fraction` arithmetic.  These are
precisely the missing power-sum indices \(n=1,\ldots,99\); the
analytic argument begins at \(n=100\).

The verifier uses the alternating original series
\[
H(z)=\sum_r(-1)^r\lambda_rz^r,
\]
not the sign-normalized positive series \(H_+(z)\).  Its first
values
\[
G_0=\frac{11}{6},\quad
G_1=\frac{341}{432},\quad
G_2=\frac{74317}{186624}
\]
confirm the sign convention.  Therefore the finite and infinite
parts prove positivity for every \(q\ge0\), rather than merely
providing a finite search.
