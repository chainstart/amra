# Independent audit of the near-logarithmic top-window theorem

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

The improvement
\[
\|R_{\ell,h}\|_1
\le \exp(O(\ell\log(\ell+2)))
\]
is valid.  No stage of the exact profile construction reintroduces an
\(\ell^2\log\ell\) exponent.

The decisive point is that in Newton's partition formula the norm
costs of the power-sum factors add according to the sizes of the
parts:
\[
\sum_i\lambda_i=u.
\]
They must not be bounded by taking the worst \(u\log u\) cost for
every factor.  With the part-sensitive bound retained, the complete
ledger is:

\[
\begin{array}{c|c}
\text{operation}&\log\text{ coefficient-norm cost}\\ \hline
\text{one power sum }S_v&O(v\log(v+2))\\
\text{one Newton partition of }u&O(u\log(u+2))\\
\text{sum over all partitions}&O(u\log(u+2))\\
\text{two Stirling basis changes}&O(u\log(u+2))\\
\text{outer/D/exceptional convolution}&O(\ell\log(\ell+2))\\
\text{determinant convolution}&O(L\log(L+2))\\
\text{mixed moment and final basis change}&O(L\log(L+2)).
\end{array}
\]

The final hypothesis
\[
(d+5)\log(d+5)=o(\log k)
\]
does force the relative error to zero.  The explicit window
\[
d\le \frac{\log k}{(\log\log k)^2}
\]
satisfies that hypothesis uniformly.

No mathematical repair is required.  One harmless indentation defect
in the finite verifier and two presentation improvements are recorded
in Section 8.

## 1. Power-sum coefficient norm

For \(0\le\beta\le5\), define
\[
S_v(t,r)
=\sum_{a=0}^{t-1}(\beta+r+a)^v.
\]
Expanding first in \(a\) gives
\[
S_v(t,r)
=\sum_{q=0}^{v}
\binom vq(\beta+r)^{v-q}
\sum_{a=0}^{t-1}a^q.
\]

The shifted factor satisfies
\[
\|(\beta+r)^w\|_1=(\beta+1)^w\le6^w.
\]
Faulhaber's formula writes the second factor using Bernoulli numbers
of order at most \(q\).  From
\[
|B_j|\le\frac{4j!}{(2\pi)^j}
\]
and the binomial coefficients in Faulhaber's formula, there is an
absolute \(c\) such that
\[
\left\|\sum_{a=0}^{t-1}a^q\right\|_1
\le\exp(c(q+1)\log(q+2)).
\]
The outer binomial sum contributes at most another \(2^v\) factor.
Consequently
\[
\boxed{
\|S_v\|_{\mathbb Q[t,r],1}
\le
\exp(c_1(v+1)\log(v+2))
}
\tag{A}
\]
with a single absolute \(c_1\), uniformly in \(v\) and the six
allowed values of \(\beta\).

This step has no hidden multiplication by \(u\): the bound in (A)
depends on the actual power-sum order \(v\), not on a later total loss
\(u\).

## 2. Newton partition formula

The exact formula
\[
e_u
=\sum_{\lambda\vdash u}
\frac{(-1)^{u-\ell(\lambda)}}{z_\lambda}
\prod_iS_{\lambda_i}
\]
and submultiplicativity of coefficient \(\ell^1\)-norm give, for a
fixed partition,
\[
\log\left\|\prod_iS_{\lambda_i}\right\|_1
\le
c_1\sum_i
(\lambda_i+1)\log(\lambda_i+2).
\]
Since every part is positive,
\[
\lambda_i+1\le2\lambda_i,
\qquad
\log(\lambda_i+2)\le\log(u+2),
\]
and therefore
\[
\sum_i(\lambda_i+1)\log(\lambda_i+2)
\le2u\log(u+2).
\tag{B}
\]

The coefficient \(1/z_\lambda\) is at most one in absolute value.
The number of partitions satisfies
\[
p(u)=\exp(O(\sqrt u)),
\]
which is smaller than \(\exp(O(u\log(u+2)))\).  Summing all partition
terms in (B) proves
\[
\boxed{
\|P_{\beta,u}(t,r)\|_1
\le
\exp(C_0(u+1)\log(u+2)).
}
\tag{C}
\]

This is exactly where the earlier square exponent can be removed.
The invalid coarse route would bound every factor by
\(\exp(O(u\log u))\) and then raise that to as many as \(u\) factors.
The revised proof does not make that substitution.

The same argument covers
\[
[s^{r-u}](s-\alpha)_{\underline r},
\]
either directly or by specializing the bivariate falling-product
formula.  Thus both inner and outer falling products obey (C).

## 3. Normalized Lagrange summation

At loss \(u\), \(P_{\beta,u}(t,r)\) has total degree at most \(2u\).
Write it as
\[
\sum_{a+b\le2u}c_{a,b}t^ar^b.
\]
The conversion
\[
t^a=\sum_v{a\brace v}(t)_{\underline v}
\]
has row norm equal to the \(a\)-th Bell number, and hence at most
\[
\exp(O(a\log(a+2)))
\le\exp(O(u\log(u+2))).
\]
Applying
\[
\sum_{t=0}^r
\binom rt2^{r-t}(-1)^t(t)_{\underline v}
=(-1)^v(r)_{\underline v}
\]
introduces no norm cost depending on \(r\).

Finally,
\[
(r)_{\underline v}
=\sum_q s(v,q)r^q
\]
has coefficient \(\ell^1\)-norm \(v!\), because the absolute
first-kind Stirling coefficients sum to the number of permutations.
Thus this conversion costs
\[
v!\le(2u)^{2u}
=\exp(O(u\log(u+2))).
\]

The number of monomials of total degree at most \(2u\) is only
\(O(u^2)\), already absorbable in the same exponent.  Combining this
with (C) gives
\[
\boxed{
\|\text{normalized \(E\)-profile at loss }u\|_1
\le
\exp(C_1(u+1)\log(u+2)).
}
\tag{D}
\]

Both Stirling changes are therefore linear-exponent operations.
There is no multiplication of two \(u\log u\) exponents and no
iteration through \(u\) separate basis changes.

## 4. Consecutive, outer, and exceptional profiles

The exact normalized consecutive difference is
\[
\widehat D_{\beta,r}
=\widehat E_{\beta,r}
-2rs^{-1}\widehat E_{\beta+1,r-1}.
\]
Multiplication by \(2r\) changes coefficient norm by a fixed factor
two and raises polynomial degree by one; it does not create a
factorial norm.

The exceptional \(h=2\) term is
\[
8rs^{-2}
\widehat F_{4,r-1}\widehat E_{4,r-1}.
\]
It similarly contributes a fixed factor eight, one factor \(r\), and
two units of loss.

For a coefficient at total loss \(\ell\), every product has a fixed
number of factors and losses satisfying
\[
u_1+\cdots+u_q=\ell+O(1),
\qquad q\le3.
\]
Using \(u_i\le\ell+O(1)\),
\[
\sum_i(u_i+1)\log(u_i+2)
\le
O((\ell+1)\log(\ell+2)).
\]
There are at most polynomially many truncated convolution terms
(\(O(\ell^2)\) is a safe bound).  Their number contributes only
\(O(\log\ell)\) to the logarithm of the norm.  Hence
\[
\boxed{
\|R_{\ell,h}\|_1
\le
\exp(C_2(\ell+1)\log(\ell+2)),
\qquad h=0,1,2.
}
\tag{E}
\]

The marked total-degree lemma is used only to improve polynomial
degree:
\[
\deg_r[h^v]R_{\ell,h}\le\ell-v.
\]
The exact algebra above already bounds the coefficients.  Removing
the higher-degree coefficients that vanish by the marked lemma cannot
increase the coefficient \(\ell^1\)-norm.

## 5. Determinant and moment conversion

At total determinant loss \(L\), each product of two profile symbols
has norm at most
\[
\exp\!\left(
C_2\ell\log(\ell+2)
+C_2(L-\ell)\log(L-\ell+2)
\right)
\le
\exp(O(L\log(L+2))).
\]
Summing over \(0\le\ell\le L\) preserves this order.

The marked degree assertion yields the same two cancellations as in
the previously audited growing-window theorem:

1. degree \(L\) cancels pointwise;
2. the mark-independent part of degree \(L-1\) cancels pointwise;
3. the remaining mark-linear degree-\((L-1)\) convolution is
   antisymmetric under
   \((J,\ell)\leftrightarrow(k-J,L-\ell)\) and has zero expectation.

Thus the averaged numerator has degree at most \(L-2\).

For the norm calculation, retain \(J\) and \(k-J\) as two variables.
Convert their ordinary powers separately to falling powers.  At
orders at most \(L\), the two Bell-number costs are
\(\exp(O(L\log L))\).  The mixed identity
\[
\mathbb E\!\left[
(J)_{\underline a}(k-J)_{\underline b}
\right]
=\frac{(k)_{\underline{a+b}}}{2^{a+b}}
\]
then replaces each mixed monomial by one falling power of order at
most \(L\).  Expanding it into ordinary \(k\)-powers costs at most
\[
(a+b)!\le L!=\exp(O(L\log L)).
\]

Consequently the degree-\((L-2)\) numerator has coefficient norm
\[
\exp(O(L\log(L+2))).
\]
With \(L=j+4\), evaluation at \(k\) and division by \(2k(k-1)\)
give
\[
\boxed{
|b_{k,j}|
\le
\exp(C_3(j+5)\log(j+5))k^j
}
\]
for \(k\ge2(j+5)\).  This final conversion does not require an
\(\exp(O(L^2\log L))\) allowance.

## 6. Relative-error condition

The already verified \(4\)-Stirling comparison gives
\[
\left|\frac{p_{k,d}}{T_{m,d}}-1\right|
\le
16^dd\,
\exp(C(d+5)\log(d+5))\frac d k.
\]
For \(d\ge1\), the logarithm of the right-hand side is
\[
-\log k
+C(d+5)\log(d+5)
+d\log16
+2\log d.
\]
The hypothesis
\[
(d+5)\log(d+5)=o(\log k)
\]
also implies
\[
d=o(\log k),
\qquad
\log d=o(\log k).
\]
Therefore the logarithm is
\[
-(1-o(1))\log k\longrightarrow-\infty.
\]
The case \(d=0\) is exactly the monic term and needs no error sum.
Thus the relative error tends to zero under the claimed condition.

The condition also implies \(d/k<1\) and \(m\ge4d\) for sufficiently
large \(k\), validating the two elementary inequalities used before
the final bound.

## 7. Explicit near-logarithmic window

Let
\[
D(k)=\frac{\log k}{(\log\log k)^2}.
\]
The function \(x\mapsto(x+5)\log(x+5)\) is increasing for
nonnegative \(x\).  Uniformly for \(0\le d\le D(k)\),
\[
\begin{aligned}
(d+5)\log(d+5)
&\le(D(k)+5)\log(D(k)+5)\\
&=O\!\left(\frac{\log k}{\log\log k}\right)\\
&=o(\log k).
\end{aligned}
\]
Hence the explicit window is a valid corollary.

The main manuscript writes the intermediate estimate with
\(d\log(d+5)\).  The omitted additive
\(5\log(d+5)\) is also
\(O(\log\log k)\) throughout this window and does not affect the
conclusion.  Writing \((d+5)\log(d+5)\) there would make the
connection to hypothesis (1) completely literal.

## 8. Verifier and test audit

The supplied test passes:

```text
1 passed in 0.44s
```

Running the verifier at its full default scope gives:

```text
maximum loss:             64
partition checks:         12,308,138
largest partition ratio:  1.0
maximum Stirling n:       96
Stirling ratio checks:    9,500
status:                   finite_checks_passed
```

The five displayed clean-window scale ratios decrease from about
\(1.87\times10^{-2}\) to \(1.38\times10^{-3}\).

These computations are appropriate regression checks, but the
uniform theorem is certified by Sections 1--7, not by finite
enumeration.  The verifier imports `four_stirling_table` from the
earlier growing-window verifier, so its Stirling portion is exact but
not implementation-independent.

There is one harmless indentation defect:

```python
    for n in range(4, maximum_n + 1):
        ...
        scale_rows = []
```

`scale_rows` is reset once per outer \(n\)-iteration and the final
empty list is then populated after the loop.  For every supported
run with `maximum_n >= 4`, the output is nevertheless correct.  The
minimal cleanup is to dedent `scale_rows = []` to the same level as
the `for n` statement.  This is a code-quality repair, not a theorem
failure.

## 9. Final assessment

The sharpened coefficient-norm proof has correctly replaced every
previous square-exponent allowance by a part-sensitive
\(\exp(O(\ell\log\ell))\) estimate.  The Lagrange sum, exceptional
profile, determinant convolution, and mixed-moment conversion all
fit that same order.

The theorem, its condition \(d\log d=o(\log k)\) in shifted form, and
the explicit \(\log k/(\log\log k)^2\) window pass this independent
audit.
