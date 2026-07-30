# Independent audit of the fixed-depth asymptotic theorem

Date: 2026-07-30

Audited sources, left unchanged:

- `../FIXED_DEPTH_ASYMPTOTIC_THEOREM.md`
- `../verify_fixed_depth_asymptotic.py`

## Verdict

**Literal-document verdict: NEEDS MINOR CORRECTION.**

**Corrected theorem-level verdict: PASS.**  The leading constant,
parity bookkeeping, determinant asymptotic, and fixed-depth positivity
argument are mathematically correct after three local corrections:

1. Equation (2) is missing a plus sign between its main term and its
   \(O_r\)-term.  As printed, it is not a valid asymptotic equality.
2. The sentence “Capacity gives” before (18) is false at the last
   below-support evaluation for even \(k\).  The required vanishing is
   true, but it uses the exact determinant cancellation
   \(W_{1,1}^2-W_{0,1}W_{2,1}=0\).
3. “The cases \(r=0,1\) strengthen to all \(k\)” needs the qualification
   \(r=0\) for \(k\ge2\), and \(r=1\) for \(k\ge3\).  At \(k=2\),
   \(c_2=1\), so \(a_{2,1}=0\) and there is no second active layer.

Equation (20) omits the constant \(e^{-2\ell}\) only in the sense that
it states a coarse big-\(O\) bound.  The bound is correct because
\(\ell\le r\) is fixed.  Any asymptotic equivalence or next-order
expansion must include this constant.

## 1. Independent \(W_0\) and \(A\) expansions

Put \(\rho=c-1\), \(u=1/n\), and
\[
g_\rho=\frac1{2^\rho\rho!}.
\]
Expanding each finite product in (5) gives
\[
\frac{W_{0,c}}{n^{n-2}}
=g_\rho\left[
1+5\rho u+\frac{\rho(35\rho-47)}2u^2+O_c(u^3)
\right].                                             \tag{A1}
\]
An independent coefficient calculation from (6), whose product begins
at \(3\), gives
\[
\frac{A_c}{n^{n-4}}
=g_\rho\left[
3+11\rho u+\frac{5\rho(13\rho-37)}2u^2+O_c(u^3)
\right].                                             \tag{A2}
\]

The independent verifier expands the products directly, rather than
calling the source verifier, for \(1\le c\le15\).  All 30 comparisons
through \(u^2\) agree with (A1)--(A2).

## 2. Independent \(W_1\) and \(W_2\) expansions

From edge transitivity,
\[
\frac{W_{1,c}}{g_\rho n^{n-3}}
=2\frac{1-(\rho+1)u}{1-u}
\frac{W_{0,c}}{g_\rho n^{n-2}}.
\]
Explicitly expanding this product yields
\[
\frac{W_{1,c}}{n^{n-3}}
=g_\rho\left[
2+8\rho u+\rho(25\rho-49)u^2+O_c(u^3)
\right].                                             \tag{A3}
\]

For \(W_2\), divide the pair-orbit identity by \(n^{n-4}\).  The two
rational prefactors are
\[
\frac{\binom{n-c}{2}n^2}{N_{\rm dis}}
=4\frac{(1-(\rho+1)u)(1-(\rho+2)u)}
        {(1-u)(1-2u)(1-3u)}
\]
and
\[
\frac{N_{\rm adj}}{N_{\rm dis}}
=\frac{4u}{1-3u}.
\]
Consequently
\[
\begin{aligned}
\frac{W_{2,c}}{g_\rho n^{n-4}}
={}&4\frac{(1-(\rho+1)u)(1-(\rho+2)u)}
          {(1-u)(1-2u)(1-3u)}
  \frac{W_{0,c}}{g_\rho n^{n-2}}\\
&-\frac{4u}{1-3u}\frac{A_c}{g_\rho n^{n-4}}.
\end{aligned}
\]
Substitution of (A1)--(A2) gives
\[
\frac{W_{2,c}}{n^{n-4}}
=g_\rho\left[
4+12\rho u+2\rho(17\rho-57)u^2+O_c(u^3)
\right].                                             \tag{A4}
\]
Thus both lines of source equation (12) are correct.  The source
verifier checked only the \(W_0/A\) prefixes directly; the independent
verifier additionally checks the rational transformations leading to
\(W_1/W_2\).

## 3. Ordered and symmetrized determinant coefficient

Suppress \(g_\rho g_\sigma n^{2n-6}\).  Substituting
(A1), (A3), and (A4), the ordered summand has \(u\)-coefficient
\[
-4(\rho-\sigma),
\]
as in (13).  Its ordered \(u^2\)-coefficient is
\[
-20\rho^2-4\rho+16\sigma^2+16\sigma+4\rho\sigma.
\]
Adding the reversed order and dividing by two gives
\[
\boxed{
2\left(3(\rho+\sigma)-(\rho-\sigma)^2\right).
}                                                     \tag{A5}
\]
Thus equation (14) is correct provided “symmetrized” means the average
of the two orders.  Equation (15) uses precisely that convention; there
is no factor-of-two error.

## 4. Binomial variance and the leading constant

For \(R=\rho+\sigma=t-2\),
\[
g_\rho g_\sigma
=\frac1{R!}\frac{\binom R\rho}{2^R}.
\]
If \(X\sim\operatorname{Bin}(R,1/2)\), then
\[
\rho-\sigma=2X-R,\qquad
\mathbb E(2X-R)^2=4\operatorname{Var}(X)=R.
\]
It follows exactly that
\[
\sum_{\rho+\sigma=R}g_\rho g_\sigma=\frac1{R!},
\]
\[
\sum_{\rho+\sigma=R}g_\rho g_\sigma
(\rho-\sigma)^2=\frac R{R!}.
\]
Applying (A5) gives
\[
\frac{2(3R-R)}{R!}
=\frac4{(R-1)!}
=\frac4{(t-3)!}.
\]
The common unnormalized power is \(n^{2n-6}\), and the first surviving
coefficient is \(u^2\), so Lemma 2 has the correct power
\(n^{2n-8}\).  Since \(t\) is fixed, the finitely many \(O_c(u^3)\)
remainders sum to \(O_t(n^{2n-9})\).

## 5. Newton inversion and the missing exponential constant

At depth \(q_0+r\), the surviving evaluations are
\(n_0+j\), \(0\le j\le r\).  Their coefficient in the forward
difference is
\[
(-1)^{r-j}\binom{q_0+r}{r-j},
\]
so equation (18) has the correct sign and binomial normalization.

Write \(n=n_r\) and \(j=r-\ell\).  A direct logarithmic expansion gives
the refinement of (20):
\[
\boxed{
(n-\ell)^{2(n-\ell)-8}
=e^{-2\ell}n^{2n-8-2\ell}
\left[
1+\frac{\ell^2+8\ell}{n}+O_r(n^{-2})
\right].
}                                                     \tag{A6}
\]
Also, because \(q_0+r=n-4\),
\[
\binom{n-4}{\ell}
=\frac{n^\ell}{\ell!}
\left[
1-\frac{\ell(\ell+7)}{2n}+O_r(n^{-2})
\right].                                             \tag{A7}
\]
Combining (A6)--(A7),
\[
\binom{n-4}{\ell}
\frac{(n-\ell)^{2(n-\ell)-8}}{n^{2n-8}}
=\frac{e^{-2\ell}}{\ell!}n^{-\ell}
\left[
1+\frac{\ell^2+9\ell}{2n}+O_r(n^{-2})
\right].                                             \tag{A8}
\]

In particular, after including the determinant leading constants, the
ratio of the \(j=r-\ell\) term to the \(j=r\) leading term is
\[
(-1)^\ell
\frac{(t_r-3)!}{(t_r-2\ell-3)!}
\frac{e^{-2\ell}}{\ell!}n^{-\ell}
\left(1+O_r(n^{-1})\right).                          \tag{A9}
\]
The \(\ell=1\) term is \(O_r(n^{-1})\), and every earlier term is
smaller.  Hence the source proof's claimed error
\(O_r(n^{2n-9})\) is correct.  The factor \(e^{-2\ell}\) is absorbed by
big-\(O\), but (A6)--(A9) show exactly where it would enter a
next-order theorem.

## 6. Capacity boundary and parity

For odd \(k\), every evaluation below \(q_0\) has total component count
at most \(1\), so ordinary capacity is sufficient.

For even \(k=2m+2\), the final evaluation below support is
\[
i=q_0-1=m-1,\qquad n=m+3.
\]
Its total component count is \(2\), not below the component capacity.
The only term is
\[
\begin{aligned}
\mathcal C_2(n)
&=W_{1,1}^2-W_{0,1}W_{2,1}\\
&=(2n^{n-3})^2-(n^{n-2})(4n^{n-4})\\
&=0.
\end{aligned}
\]
Therefore the vanishing used in (18) is correct, but attributing it
solely to capacity is not.

The parity definitions
\[
t_0=3\quad(k\text{ odd}),\qquad
t_0=4\quad(k\text{ even})
\]
and \(t_r=t_0+2r\) are correct.  Multiplying the determinant leading
term \(4/(t_r-3)!\) by the normalization \((k-2)!/2\) gives
\[
\frac{2(k-2)!}{(t_r-3)!},
\]
so no parity-dependent factor or normalization is missing.

## 7. Required source corrections

The displayed asymptotic should read
\[
\boxed{
a_{k,q_0+r}
=\frac{2(k-2)!}{(t_r-3)!}n_r^{2n_r-8}
+O_r\!\left((k-2)!\,n_r^{2n_r-9}\right).
}
\]

The proof before (18) should replace “Capacity gives” with:

> Capacity gives the vanishing except at the last below-support
> evaluation for even \(k\); there it follows from
> \(W_{1,1}^2-W_{0,1}W_{2,1}=0\).

The all-\(k\) sentence should read:

> The case \(r=0\) is positive for every \(k\ge2\), and \(r=1\) is
> positive for every \(k\ge3\); at \(k=2\) no second active layer
> exists.

## 8. Independent verification

`independent_verify_fixed_depth.py` performs:

- 30 direct finite-product checks of (A1)--(A2);
- symbolic rational expansion of (A3)--(A4);
- independent ordered/symmetrized \(u^2\) calculation;
- exact binomial moment checks through \(R=30\);
- exact even-capacity cancellation checks through \(n=30\); and
- an exact symbolic series proof that the first correction in (A6) is
  \(\ell^2+8\ell\), followed by 80-digit Decimal convergence checks for
  (A6)--(A8), \(1\le\ell\le5\).

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/fixed_depth_independent_audit
pytest -q test_independent_verify_fixed_depth.py
python3 independent_verify_fixed_depth.py
```
