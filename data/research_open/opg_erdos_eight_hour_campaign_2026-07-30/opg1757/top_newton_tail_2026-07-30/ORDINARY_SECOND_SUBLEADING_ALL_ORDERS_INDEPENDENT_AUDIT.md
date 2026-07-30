# OPG-1757 ordinary second-subleading symbol: independent red-team audit

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

No mathematical or implementation error was found in
`ORDINARY_SECOND_SUBLEADING_SYMBOL_THEOREM.md` or
`verify_ordinary_second_subleading_all_orders.py`.

The audit did not import the new verifier.  It independently started from
the finite normalized Lagrange sums, reconstructed the exact profile
polynomials, formed the determinant by a generic convolution, and formed
the ordinary polynomials by an exact binomial average.

## 1. Rank-four saddle and exceptional shift

At saddle rank \(r\), an amplitude derivative of order \(m\) pairs with
\(E_{2r-m}\).  Rank four therefore uses
\[
0\le m\le8,\qquad E_0,\ldots,E_8.
\]
Since \(E_8\) contains the phase term indexed by \(p=8\), the required
phase derivatives are exactly
\[
\phi^{(2)},\ldots,\phi^{(10)}.
\]
The Gamma logarithm is required through \(s^{-4}\), and exponentiating it
requires \(\Gamma_0,\ldots,\Gamma_4\).  These are precisely the ranges in
the verifier.

For the exceptional profile, the exact normalized finite expression is
\[
8j\,s^{-2}\widehat F_{4,j-1}\widehat E_{4,j-1}.
\]
After \(j=xs\), it has an external factor \(8x/s\).  Consequently its
contribution to the overall \(s^{-4}\) symbol is the internal rank-three
coefficient, not internal rank four.  The code correctly uses
`exceptional_profile(..., MAXIMUM_RANK - 1)` and adds
`exceptional[3]` to `primary[4][4]`.

The Gamma arguments also match the exact integrals:
\[
\begin{array}{c|ccc}
 &\Gamma(xs+1)&\Gamma(s-3)&
\Gamma((1-x)s-2)^{-1}\\ \hline
\text{exceptional}&(x,1)&(1,-3)&-(1-x,-2).
\end{array}
\]

As a redundant check, the independent program extracted the fourth
subdegree directly from exact profiles through loss \(16\), with all
\(3(16-3)=39\) comparisons passing.  It also separately confirmed that
the exceptional fourth-subdegree contribution is nonzero.

## 2. The \(G_4\) convolution

The independent program did not transcribe equation (12).  It built
\(G_r\) generically as
\[
G_r=\sum_{a+b=r}
\left(F_{1,a}(x)F_{1,b}(1-x)
-F_{0,a}(x)F_{2,b}(1-x)\right).
\]
The resulting \(G_4\) agrees coefficientwise with the claimed \(H_4\)
through the audited loss.  This independently checks all nine terms and
their signs in (12).

## 3. Central binomial contribution

The rank-zero kernel vanishes.  The reconstructed rank-one kernel obeys
the exact identity
\[
G_1(1-x,t)=-G_1(x,t).
\]
Since \(J/k-1/2\) has a symmetric distribution, its binomial expectation
is exactly zero, to every order.  Thus no \(G_1\) derivative contributes.

For the other ranks, the complete order ledger through \(k^{-4}\) is
\[
\begin{array}{c|c|c}
\text{kernel}&\text{Taylor derivative}&
\text{total inverse-}k\text{ order}\\ \hline
G_2&0,2,4&2,3,4\\
G_3&0,2&3,4\\
G_4&0&4.
\end{array}
\]
Using
\[
\mathbb E\delta^2=\frac1{4k},\qquad
\mathbb E\delta^4=\frac3{16k^2}+O(k^{-3}),
\]
the fourth-order coefficient is therefore exactly
\[
G_4(1/2)+\frac18G_3''(1/2)+\frac1{128}G_2''''(1/2).
\]
The sixth moment is \(O(k^{-3})\); multiplied by the leading
\(k^{-2}G_2\), it first appears at \(k^{-5}\).  No sixth-moment term is
missing.

## 4. Division by \(2k(k-1)\)

Writing \(L=d+4\), the three numerator terms relevant to \(k^{d-2}\)
are
\[
k^{L-2}H_2,\qquad k^{L-3}H_3,\qquad k^{L-4}H_4.
\]
The expansion
\[
\frac1{2k(k-1)}
=\frac1{2k^2}(1+k^{-1}+k^{-2}+\cdots)
\]
therefore contributes respectively \(H_2/2,H_3/2,H_4/2\).  Hence
\[
C_d=\frac12[t^{d+4}](H_2+H_3+H_4)
\]
is correct.

Exact independently reconstructed ordinary polynomials through depth
\(10\) agree with this formula and with the stated degree-six polynomial.

## 5. Boundary

The restriction \(d\ge2\) is essential because \(k^{d-2}\) is not a
polynomial coefficient for \(d=0,1\).  Consistently, the formal
continuation satisfies
\[
[t^4](H_2+H_3+H_4)
=[t^5](H_2+H_3+H_4)=0.
\]
Depth \(d=2\) is included and gives the exact constant coefficient
\[
C_2=42.
\]

## Verification

```bash
python3 independent_verify_ordinary_second_subleading_all_orders.py
pytest -q test_independent_verify_ordinary_second_subleading_all_orders.py
```
