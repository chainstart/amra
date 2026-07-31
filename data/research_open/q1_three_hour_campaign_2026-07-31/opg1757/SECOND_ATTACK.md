# OPG-1757 second attack: complete closure of \(B_{2s-7}\)

Date: 2026-07-31

## 1. Main theorem

Put
\[
n=2s-7,\qquad s\ge4.
\]
Then
\[
\boxed{
B_{2s-7}(s,\beta)
=n!\,s^{2s-12}\beta^{4s-14}
\sum_{r=0}^4s^rP_r(s)\beta^r,
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_0(s)
&=2(s-4)(s^3+12s^2+20s-225),\\
P_1(s)
&=\frac83(s-4)(3s^3+20s^2-28s-225),\\
P_2(s)
&=4(s-4)(4s^3+6s^2-85s+72),\\
P_3(s)
&=8(s-4)(2s-5)(s^2-s-8),\\
P_4(s)
&=\frac23(s-4)(s-3)(2s-7)(6s-11).
\end{aligned}
}
\tag{2}
\]
Here the product in (1) is interpreted as the combined exact expression
when \(s=4\).  Every \(P_r(4)=0\), so \(B_1=0\), as required.

For \(s\ge5\), set \(u=s-5\).  Exact expansion gives
\[
\begin{aligned}
P_0(u+5)
&=600+1030u+484u^2+56u^3+2u^4,\\
P_1(u+5)
&=1360+\frac{7256}3u+1232u^2+\frac{544}3u^3+8u^4,\\
P_2(u+5)
&=1188+2288u+1364u^2+280u^3+16u^4,\\
P_3(u+5)
&=480+1032u+736u^2+200u^3+16u^4,\\
P_4(u+5)
&=76+\frac{566}3u+166u^2+\frac{184}3u^3+8u^4.
\end{aligned}
\tag{3}
\]
All coefficients in (3) are strictly positive.  Therefore
\[
\boxed{
B_{2s-7}(s,\beta)>_{\rm coeff}0
\quad\text{for every }s\ge5,
}
\tag{4}
\]
with the structural boundary \(B_1=0\) at \(s=4\).

Together with the first attack, the three deepest pooled layers
\[
B_{2s-5},\qquad B_{2s-6},\qquad B_{2s-7}
\]
are now completely closed.

## 2. Complete hyperforest excess

Let \(\mathbf w=(w_1,\ldots,w_b)\) be a contracted core profile.  For
\(r\ge3\), define the weighted contraction operator
\[
(\mathcal C_rF)(\mathbf w)
=\sum_{\substack{T\subseteq[b]\\|T|=r}}
\left(\prod_{i\in T}w_i\right)F(\mathbf w/T).
\tag{5}
\]
The factor \(\prod_{i\in T}w_i\) expands the choices of one original spoke
endpoint from every selected current component.

Let \(\Phi_{\mathbf w}(x)\) be the ordinary weighted complete-graph forest
polynomial.  Define
\[
\boxed{
\mathcal H_e(\mathbf w;x)
=[z^e]\exp\left(
x\sum_{r\ge3}z^{r-2}\mathcal C_r
\right)\Phi_{\mathbf w}(x).
}
\tag{6}
\]
The exponential has a literal combinatorial meaning.  An ordered list of
\(m\) nonbinary contractions is divided by \(m!\), leaving an unordered set
of nonbinary hyperedges; the remaining binary edges form an ordinary
forest after those hyperedges are contracted.

The first four excess species are
\[
\begin{aligned}
\mathcal H_0&=\Phi,\\
\mathcal H_1&=x\mathcal C_3\Phi,\\
\mathcal H_2&=x\mathcal C_4\Phi
+\frac{x^2}{2}\mathcal C_3^2\Phi,\\
\mathcal H_3&=x\mathcal C_5\Phi
+\frac{x^2}{2}
(\mathcal C_3\mathcal C_4+\mathcal C_4\mathcal C_3)\Phi
+\frac{x^3}{6}\mathcal C_3^3\Phi.
\end{aligned}
\tag{7}
\]
Thus every possible type needed below is present:

- excess \(0\): only binary merges;
- excess \(1\): one ternary merge;
- excess \(2\): one quaternary merge or two ternary merges;
- excess \(3\): one 5-merge, one quaternary plus one ternary merge, or
  three ternary merges.

There is no additional partition of \(e\le3\), so (7) is an exhaustion,
not a selected list of favourable types.

## 3. Ordered-chain identity

Let \(A_{h,j}\) be the \(j\)-th nilpotent page chain from core profile
\(h\).  Expanding every current block weight into the choice of an original
spoke endpoint sends a chain record to a complete hyperforest.  Conversely,
contracting its hyperedges in any order is valid precisely because the
contracted remainder is a forest.  Therefore
\[
\boxed{
[\beta^{2j+e}]A_{h,j}
=j![x^j]\mathcal H_{h,e}(x).
}
\tag{8}
\]
The \(j!\) counts the possible orders of the \(j\) labelled active pages.

The verifier compares (8) directly with the primitive nilpotent transfer
at 146 independent \((s,h,e,c)\) endpoints.  This includes every species in
(7), not only their final determinant combination.

## 4. Active-page overlap becomes differentiation

The exact pooled coefficient is
\[
B_n
=\sum_{\substack{j,q,\ell\\j+q-\ell=n}}
\frac{n!}{\ell!(j-\ell)!(q-\ell)!}
\lambda^{2s-4-j-q}
\left(A_{1,j}A_{1,q}-A_{0,j}A_{2,q}\right).
\tag{9}
\]
At \(n=2s-7\), an overlap of size \(\ell\) leaves
\[
\lambda^{2s-4-j-q}=\lambda^{3-\ell}.
\tag{10}
\]
After inserting (8), the factorial in (9) becomes
\[
\frac{n!}{\ell!}(j)_\ell(q)_\ell.
\]
The two falling factorials are exactly the coefficients created by
\(\ell\)-fold differentiation.  Consequently, for \(0\le r\le3\),
\[
\boxed{
\begin{aligned}
\frac{[\beta^{2n+r}]B_n}{n!}
={}&
\sum_{\ell=0}^{\lfloor r/2\rfloor}\frac1{\ell!}
\sum_{\substack{e+f+a=r-2\ell}}
\binom{3-\ell}{a}s^a\\
&\times[x^{n-\ell}]
\left(
\mathcal H_{1,e}^{(\ell)}
\mathcal H_{1,f}^{(\ell)}
-
\mathcal H_{0,e}^{(\ell)}
\mathcal H_{2,f}^{(\ell)}
\right).
\end{aligned}
}
\tag{11}
\]
In (11), superscript \((\ell)\) means the \(\ell\)-th derivative in \(x\).

Equation (11) accounts for active-page overlap exactly:

- \(r=0,1\) force \(\ell=0\);
- \(r=2,3\) allow \(\ell=1\);
- no larger overlap can occur below the already proved top coefficient
  \(r=4\).

The fifth coefficient \(r=4\) is supplied independently by the all-depth
Stirling top-face theorem, so no unproved excess-four classification is
being suppressed.

## 5. All-\(s\) endpoint reduction

Let
\[
H_{h,e,c}
=[x^{s-h-c-e}]\mathcal H_{h,e}(x).
\]
The component lemma proved and tabulated in
`SECOND_DEFICIT_COMPONENT_TABLE.md` is
\[
\boxed{
H_{h,e,c}
=2^hs^{s-h-2c-e}P_{h,e,c}(s),\qquad
\deg P_{h,e,c}\le2c+2e-2.
}
\tag{12}
\]
Only 30 endpoint polynomials occur:
\[
\begin{array}{c|c}
e&c\\ \hline
0&1,2,3,4\\
1&1,2,3\\
2&1,2\\
3&1.
\end{array}
\]

The exponent in (12) makes every term of (11) share the factor
\[
s^{2s-12+r}.
\]
Indeed, if the two hyperforests have \(c,d\) components, their degrees
force
\[
c+d+e+f=5-\ell,
\]
and hence the product exponent, including the \(s^a\) from \(\lambda\), is
exactly \(2s-12+r\).

Substituting the 30 exact endpoint polynomials into (11) and simplifying
gives \(P_0,\ldots,P_3\) in (2).  For \(P_4\), the first-attack formula
\[
4\left(
{2s-5\brace 2s-7}-{2s-6\brace2s-7}
\right)
=\frac23(s-4)(s-3)(2s-7)(6s-11)
\tag{13}
\]
gives the last line of (2).  Equations (11)--(13) prove (1).

## 6. Denominator-aware Abel proof and exact reconstruction

The independent audit correctly identified that the earlier three-line
argument for
\[
\deg P_{h,e,c}\le2c+2e-2
\]
did not prove its contraction step.  That strong bound is no longer used
as an interpolation premise.

The replacement is proved step by step in
`ABEL_EXCEPTIONAL_PROFILE_LEMMA.md`.  For a fixed exceptional profile
\[
\mathbf w=(1^{s-\sum v_i},v_1,\ldots,v_p)
\]
the weighted Abel lemma gives
\[
\mathcal F_c(\mathbf w)
=\left(\prod_i v_i\right)s^{|\mathbf w|-2c}
Q_{\mathbf v,c}(s),
\qquad
\deg Q_{\mathbf v,c}\le2c-2.
\tag{14}
\]
Its proof uses:

1. the exact exceptional-component EGF
   \[
   \frac{\prod_{i\in J}v_i}{a_J}
   (a_J+D)^{|J|-1}e^{a_JT};
   \]
2. the full set-partition sum over exceptional components;
3. Lagrange inversion;
4. the coefficient-preserving pole reduction
   \[
   \Lambda\!\left(
   tf'-(s(1-t)-a)f
   \right)=0.
   \]

Now fix an incidence type with \(m\) nonbinary contractions and total
excess \(e\).  It uses at most \(e+2m\) untouched unit blocks, so its
embedding multiplicity has degree at most \(e+2m\).  Relative to the
normalization in (12), its contribution is
\[
\frac{E_\tau(s)Q_{\tau,c}(s)}{s^m},
\qquad
\deg E_\tau\le e+2m,\quad
\deg Q_{\tau,c}\le2c-2.
\]
Because \(m\le e\), taking the common denominator \(s^e\) proves
\[
\boxed{
\frac{H_{h,e,c}}{2^hs^{s-h-2c-e}}
=\frac{N_{h,e,c}(s)}{s^e},
\qquad
\deg N_{h,e,c}\le2c+3e-2.
}
\tag{15}
\]

Therefore a proposed table identity is proved after checking
\[
2c+3e-1
\tag{16}
\]
distinct positive values of \(s\).  Across the 30 entries this is exactly
180 values.  Both the main aggregated verifier and the independent
direct-position verifier check all 180, starting at \(s=7\) and ending at
\(s=16\).  In particular, the three \(e=3,c=1\) entries now include the
previously missing \(s=16\) value.

After the 30 identities have been proved in this denominator-aware way,
their displayed polynomial forms may of course be substituted into (11).
That exact symbolic simplification gives (2).  Thus the all-\(s\) theorem
is no longer conditional on an assumed polynomial degree bound.

## 7. Previous algebra gap closed

The first attack abbreviated the substitution from its component table to
the two formulas used for \(B_{2s-6}\).  Write
\[
F_{h,c}=2^hs^{s-h-2c}p_{h,c},\qquad
G_{h,c}=2^hs^{s-h-2c-1}q_{h,c},
\]
for the ordinary and one-ternary component endpoints from that table.
Then the exact normalized binary determinant is
\[
\begin{aligned}
\frac{[x^{2s-6}]C}{s^{2s-10}}
=4\big(&2p_{1,1}p_{1,3}+p_{1,2}^2\\
&-p_{0,1}p_{2,3}-p_{0,2}p_{2,2}
-p_{0,3}p_{2,1}\big)\\
=4(s^2+4s-24).
\end{aligned}
\tag{17}
\]
The normalized one-ternary correction is
\[
\begin{aligned}
\frac{[x^{2s-6}]Q}{s^{2s-9}}
=4\big(&2(p_{1,1}q_{1,2}+p_{1,2}q_{1,1})\\
&-(p_{0,1}q_{2,2}+p_{0,2}q_{2,1})\\
&-(q_{0,1}p_{2,2}+q_{0,2}p_{2,1})\big)\\
=-8(5s-16).
\end{aligned}
\tag{18}
\]
Because the linear coefficient of \(\lambda^2\) is \(2s\), factoring the
common \(s^{2s-9}\) leaves
\[
2\cdot4(s^2+4s-24)-8(5s-16)
=8(s^2-s-8),
\tag{19}
\]
which is the middle coefficient in the first-attack formula.  The new
verifier checks (17)--(19) as exact symbolic identities.

The separate one-line boundary proof is also now explicit:
\[
D_0=D_1=0
\Longrightarrow
B_0=P(0)=0,\qquad B_1=P(1)-P(0)=0.
\tag{20}
\]

## 8. Executable audit

Run:

```bash
python3 -m unittest -v test_verify_second_deficit.py
python3 verify_second_deficit.py --minimum-s 4 --maximum-s 16
```

Current certificate:

- 30 exact component identities proved after denominator clearing;
- 180 main-verifier endpoint values and 180 independent direct-position
  endpoint values, including \(s=16\);
- 146 primitive chain/species comparisons;
- all five \(B_{2s-7}\) coefficients checked against the primitive pooled
  transfer for \(s=4,\ldots,16\);
- fixed-deficit finite-reduction bounds checked at \(q=2\);
- certificate digest:
  `6a6547d2adf8bead71f4231549790ac0a43e98eb4f39e7d782689f77bd1824c5`
  under schema `amra.opg1757.second_depth_deficit.v2`;
- eight second-attack tests and all 15 combined first/second-attack tests
  pass.

## 9. Scope and the then-next gap

This attack proves one more unbounded, growing-depth complete-split pooled
layer.  It does **not** prove:

- every \(B_n\ge_{\rm coeff}0\);
- the complete disjoint-core \(\alpha^2\) layer;
- complete-split Rayleigh positivity outside the proved layer;
- arbitrary-host OPG-1757.

At the end of this second attack, the first open depth was
\[
B_{2s-8},
\]
which has seven possible coefficients
\[
4s-16\le\deg_\beta B_{2s-8}\le4s-10.
\]
The master species (6) and overlap formula (11) now give the finite
rational reduction proved in `FIXED_DEFICIT_FINITE_REDUCTION.md`: for
fixed \(q\ge1\), only
\[
\frac{3(q+2)(q+3)}2
\]
endpoint types are needed, with
\[
\frac{(q+2)(q+3)(5q+8)}2
\]
exact endpoint values in the safe certificate.  This is not a positivity
theorem.  The already closed \(q=0\) boundary has the smaller exact counts
6 and 12.  That \(q=3\) target has now been closed in
`FOURTH_ATTACK_Q3.md`: \(B_{2s-8}=0\) at \(s=4\) and is
coefficientwise strictly positive for every integer \(s\ge5\).
