# The fourth active base-four Newton layer is positive for every \(k\)

Date: 2026-07-30

## 1. Statement

Let
\[
C_k(s)=[x^k]\bigl(\Phi_1(x)^2-\Phi_0(x)\Phi_2(x)\bigr),
\qquad
c_k(s)=\frac{(k-2)!}{2}C_k(s),
\]
and write
\[
c_k(s)=\sum_q a_{k,q}\binom{s-4}{q},
\qquad
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

### Theorem

For every \(k\ge4\),
\[
\boxed{a_{k,q_0+3}>0.}                               \tag{1}
\]
For \(k=3\), \(q_0+3=3\) exceeds the degree \(2k-4=2\), so there is no
fourth active layer.

Define
\[
P_5(x)=x^3+12x^2+20x-225,
\]
\[
Q_6(x)=x^5+16x^4+52x^3-587x^2-3063x+12240,
\]
\[
P_7(x)=x^6+25x^5+229x^4+211x^3
       -10101x^2-36081x+183330,
\]
\[
\begin{aligned}
P_8(x)={}&x^8+29x^7+321x^6+459x^5-23239x^4\\
         &-161291x^3+565356x^2+5972364x-18174240,
\end{aligned}
\]
\[
\begin{aligned}
P_9(x)={}&x^9+39x^8+667x^7+5064x^6-10918x^5\\
         &-512106x^4-2462113x^3+15195399x^2\\
         &+108066951x-385491960,
\end{aligned}
\]
and
\[
\begin{aligned}
P_{10}(x)={}&x^{11}+43x^{10}+823x^9+7078x^8-20797x^7\\
&-1100827x^6-7668142x^5+39507308x^4\\
&+663343272x^3-563146065x^2\\
&-23775670800x+61440120000.
\end{aligned}
\]

For odd \(k\), put \(n=(k+11)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+3}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)
\Bigl[
\frac{P_9(n)}{180}n^{2n-20}\\
&-\frac{P_7(n-1)}6(n-1)^{2n-18}\\
&+P_5(n-2)(n-2)^{2n-16}\\
&-\frac23(n-3)^{2n-14}
\Bigr].
\end{aligned}}                                       \tag{2}
\]

For even \(k\), put \(n=(k+12)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+3}
={}&\frac{(k-2)!}{2}(n-4)(n-5)(n-6)
\Bigl[
\frac{P_{10}(n)}{1260}n^{2n-22}\\
&-\frac{P_8(n-1)}{30}(n-1)^{2n-20}\\
&+\frac13Q_6(n-2)(n-2)^{2n-18}\\
&-\frac23(n^2-2n-27)(n-3)^{2n-16}
\Bigr].
\end{aligned}}                                       \tag{3}
\]

## 2. Uniform component-total source

For completeness, define
\[
F_h^{(n)}(y)=\sum_cW_{h,c}(n)y^c,
\qquad
A^{(n)}(y)=\sum_cA_c(n)y^c.
\]
If \(T=ze^T\), \(U=T-T^2/2\), and
\(\vartheta=y\,d/dy\), then
\[
F_0^{(n)}(y)=n![z^n]e^{yU},                          \tag{4}
\]
\[
F_1^{(n)}(y)
=(n-2)![z^{n-2}]\,y e^{2T}e^{yU}
=\frac{2(n-\vartheta)}{n(n-1)}F_0^{(n)}(y),           \tag{5}
\]
\[
A^{(n)}(y)=(n-3)![z^{n-3}]\,y e^{3T}e^{yU},           \tag{6}
\]
and
\[
F_2^{(n)}(y)
=\frac{
\frac12(n-\vartheta)(n-\vartheta-1)F_0^{(n)}(y)
-N_{\rm adj}A^{(n)}(y)
}{N_{\rm dis}}.                                      \tag{7}
\]
Thus all component-total layers come from
\[
\mathcal C_t(n)
=[y^t]\left(F_1^{(n)}(y)^2-F_0^{(n)}(y)F_2^{(n)}(y)\right). \tag{8}
\]

Equivalently, Lagrange inversion gives the finite formulas
\[
W_{0,c}(n)
=n^{n-c-1}(n-1)!
\sum_j
\frac{(-1/(2n))^j(c+j)}
 {j!(c-j-1)!(n-c-j)!},                               \tag{9}
\]
\[
A_c(n)
=\sum_j
\frac{(-1)^j(c+j+2)(n-3)!n^{n-c-j-3}}
 {2^jj!(c-j-1)!(n-c-j-2)!}.                          \tag{10}
\]
Together with edge transitivity and the adjacent/disjoint edge-pair
identity, these determine every summand in (8).

## 3. New exact determinant layers

Substitution of (9)--(10) into (8), followed by collection of powers of
\(n\), gives
\[
\boxed{
\mathcal C_9(n)
=\frac{(n-4)(n-5)(n-6)}{180}
P_9(n)n^{2n-20},
}                                                       \tag{11}
\]
\[
\boxed{
\mathcal C_{10}(n)
=\frac{(n-4)(n-5)(n-6)}{1260}
P_{10}(n)n^{2n-22}.
}                                                       \tag{12}
\]
After the displayed common factors are removed, (11)--(12) are
ordinary polynomial identities of degrees nine and eleven.  Hence
their verification is finite exact algebra, not an asymptotic or
numerical inference.

## 4. Four-point Newton difference

Put \(n_0=q_0+4\) and \(n=n_0+3\).  Vanishing below \(q_0\) leaves four
terms:
\[
\boxed{
\begin{aligned}
a_{k,q_0+3}
=\frac{(k-2)!}{2}\Bigl[
&C_k(n)-(n-4)C_k(n-1)\\
&+\binom{n-4}{2}C_k(n-2)\\
&-\binom{n-4}{3}C_k(n-3)
\Bigr].
\end{aligned}}                                       \tag{13}
\]
For odd \(k\), the component totals in (13) are \(9,7,5,3\).
Factoring \((n-4)(n-5)(n-6)\) gives (2).

For even \(k\), the totals are \(10,8,6,4\).  The final translated
quadratic is
\[
(n-3)^2+4(n-3)-24=n^2-2n-27,                         \tag{14}
\]
which gives (3).  Equation (14) is the sign-sensitive translation:
the linear term is \(-2n\), not \(+2n\).

## 5. Odd-\(k\) positivity

The two cases below the stable first-pair exponent range are, by exact
substitution in (2),
\[
a_{5,4}=14088,\qquad a_{7,5}=300069360.              \tag{15}
\]

Let \(n\ge10\) and \(E=2n-20\).  Since \(P_7(n-1)>0\), the first two
terms in (2) are at least
\[
\frac{n^E}{180}
\left(P_9(n)-30P_7(n-1)(n-1)^2\right),               \tag{16}
\]
because \(((n-1)/n)^E\le1\).  With \(n=m+8\), the polynomial in
parentheses is
\[
\begin{aligned}
{}&m^9+81m^8+3037m^7+70532m^6+1120046m^5\\
&+12162282m^4+83300223m^3+309079669m^2\\
&+544745537m+374542080,
\end{aligned}
\]
so it is positive.  The needed auxiliary positivity is also formal:
with \(n-1=v+9\),
\[
\begin{aligned}
P_7(n-1)={}&v^6+79v^5+2569v^4+43285v^3\\
&+387555v^2+1675557v+2704374>0.
\end{aligned}
\]

For the last two terms put \(F=2n-16\).  Already for \(n\ge8\),
\[
\begin{aligned}
&P_5(n-2)(n-2)^F-\frac23(n-3)^{F+2}\\
&\quad\ge
\frac{(n-2)^F}{3}
\left(3P_5(n-2)-2(n-3)^2\right).
\end{aligned}                                        \tag{17}
\]
At \(n=m+8\), the final polynomial is
\[
3m^3+88m^2+796m+1579>0.
\]
Equations (15)--(17) prove the odd case.

## 6. Even-\(k\) positivity

The exact cases below the stable first-pair range are
\[
\begin{aligned}
a_{4,4}&=24,\\
a_{6,5}&=1979520,\\
a_{8,6}&=68886560880.
\end{aligned}                                        \tag{18}
\]

For \(n\ge11\), put \(E=2n-22\).  The first two terms in (3) are at
least
\[
\frac{n^E}{1260}
\left(P_{10}(n)-42P_8(n-1)(n-1)^2\right).            \tag{19}
\]
With \(n=m+8\), the polynomial in parentheses is
\[
\begin{aligned}
{}&m^{11}+89m^{10}+3625m^9+91828m^8+1670445m^7\\
&+23203873m^6+238019538m^5+1606293934m^4\\
&+6068863474m^3+11934197401m^2\\
&+12534603162m+5584273380,
\end{aligned}
\]
which is positive.  Also \(P_8(n-1)>0\), since its shift at \(n-1=10\)
has coefficients
\[
1,109,5151,136619,2196211,21538149,
123423226,374486184,461304000.
\]

For the last pair, \(F=2n-18\ge0\) when \(n\ge9\), and
\(n^2-2n-27>0\).  Therefore it is bounded below by
\[
\frac{(n-2)^F}{3}
\left[
Q_6(n-2)-2(n^2-2n-27)(n-3)^2
\right].                                             \tag{20}
\]
At \(n=m+8\), the bracket is
\[
m^5+44m^4+748m^3+5593m^2+14693m+11424>0.
\]
The remaining value \(n=8\) is already included in (18).  This proves
the even case.

## 7. Formal nature of the finite closure

The all-parameter proof does not infer positivity from a scan up to a
chosen bound:

1. Four positive-coefficient translations certify the infinite
   ranges in (16), (17), (19), and (20).
2. Positive-coefficient translations separately certify
   \(P_7(n-1)>0\) and \(P_8(n-1)>0\) where their signs are used.
3. Exactly five residual parameter values remain, and (15), (18)
   evaluate them symbolically.

Thus no Sturm computation is required.  The finite closure is an exact
five-case calculation plus positive-coefficient polynomial
certificates.

## 8. Verification and proof/computation boundary

The human proof consists of the generating identities (4)--(10), the
finite polynomial identities (11)--(12), the exact difference (13),
and the positive-coefficient certificates in Sections 5--7.

The companion verifier independently:

- reconstructs \(\mathcal C_9,\mathcal C_{10}\) from (9)--(10);
- checks every shifted polynomial coefficient exactly;
- recomputes the fourth difference from component counts for
  \(4\le k\le12\); and
- performs an exact-integer transcription regression through \(k=100\).

The finite regression is not a premise of the theorem.

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/fourth_layer_2026-07-30
pytest -q test_verify_fourth_active_newton.py
python3 verify_fourth_active_newton.py
```
