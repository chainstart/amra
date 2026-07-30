# Independent red-team audit of the ordinary top-symbol theorem

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

The revised proof passes the requested strict audit.  In particular:

1. Equations (23a)--(23c) now give an all-orders, coefficientwise
   derivation of \(C(x)\), rather than citing a finite computer check.
2. Equations (26a)--(26b) contain the complete degree-\((L-2)\)
   determinant ledger.
3. Equation (27) now assigns the correct, different powers of
   \(J\) and \(k-J\) to the \(BB\) and \(AC\) terms.

The independent finite verifier is corroborating evidence only.  The
logical all-orders step is the arbitrary-coefficient extraction in
(23a), followed by the formal-series identity (23b), not the
verifier's cutoff.

## 1. Independent extraction

The audit verifier imports no existing OPG verifier or recorded profile
symbol.  It reconstructs \(U_{0,j},U_{1,j},U_{2,j}\) directly from
the finite Lagrange sums (12)--(15), extracts \(R_{\ell,h}\), and uses
redundant values of \(j\) to check the polynomial degree.

Through loss ten it independently obtains
\[
A(x)=\sqrt{1-2x},
\qquad
B(x)=-\frac{2x}{\sqrt{1-2x}},
\qquad
C(x)=-\frac{2x^2}{(1-2x)^{3/2}}.
\]
This confirms the formulas but is intentionally treated only as an
exact coefficient stress test, not the all-orders proof.

## 2. Audit of the all-orders \(C(x)\) derivation

Put
\[
\mathcal P_h(s,x)
=
\frac{2^j j!}{s^{2j}}U_{h,j}(s),
\qquad j=xs.
\]
The marked bidegree theorem gives the formal coefficientwise expansion
\[
\mathcal P_h(s,x)
=A(x)
+\frac{P(x)+hB(x)}s
+\frac{Q(x)+hD(x)+h^2C(x)}{s^2}
+O_{\rm formal}(s^{-3}).                            \tag{A}
\]
Consequently,
\[
\frac{s^2}{2}
\left(\mathcal P_2-2\mathcal P_1+\mathcal P_0\right)
=C(x)+O_{\rm formal}(s^{-1}).                       \tag{B}
\]

The revision now determines this coefficient rather than merely
asserting its value.  It substitutes the exact finite profiles
(12)--(15), expands through \(\varepsilon^2=s^{-2}\), and applies
the exact falling-moment identity (16) to every Lagrange-index term.
For every fixed \(\ell\), only finitely many factors enter and the
complete sum gives
\[
\boxed{
C_\ell
=2(\ell-2)(\ell-3)A_{\ell-2}
\qquad(\ell\ge2).
}                                                     \tag{C}
\]
Equivalently,
\[
\boxed{C(x)=2x^2A''(x).}                            \tag{D}
\]
Since \(A(x)=\sqrt{1-2x}\),
\[
2x^2A''(x)
=-\frac{2x^2}{(1-2x)^{3/2}},
\]
which is (11).

This is an all-orders argument: (23a) is stated for arbitrary
\(\ell\), identifies the finite source expansion and the exact identity
that evaluates its complete sum, and (23b) repackages those coefficient
identities.  It does not infer a formal identity from finitely many
computed coefficients.  The independent verifier additionally checks
(C) exactly through loss ten.

## 3. Complete degree-\((L-2)\) determinant ledger

Refine each profile symbol by
\[
\begin{aligned}
R_{\ell,h}(j)
={}&A_\ell j^\ell
+(P_\ell+hB_\ell)j^{\ell-1}\\
&+(Q_\ell+hD_\ell+h^2C_\ell)j^{\ell-2}
+O(j^{\ell-3}).
\end{aligned}                                       \tag{E}
\]
Put \(r=L-\ell\).  In
\[
R_{\ell,1}(J)R_{r,1}(k-J)
-R_{\ell,0}(J)R_{r,2}(k-J),
\]
the complete degree-\((L-2)\) ledger, including the associated
monomials, is
\[
\begin{aligned}
BB:\;&B_\ell B_rJ^{\ell-1}(k-J)^{r-1},\\
DA-AD:\;&D_\ell A_rJ^{\ell-2}(k-J)^r
         -A_\ell D_rJ^\ell(k-J)^{r-2},\\
BP-PB:\;&B_\ell P_rJ^{\ell-1}(k-J)^{r-1}
         -P_\ell B_rJ^{\ell-1}(k-J)^{r-1},\\
CA-3AC:\;&C_\ell A_rJ^{\ell-2}(k-J)^r
         -3A_\ell C_rJ^\ell(k-J)^{r-2}.
\end{aligned}                                       \tag{F}
\]

There are no further degree-\((L-2)\) sources: the \(Q\)-terms cancel,
products involving a degree at most \(\ell-3\) are too low, and the
marked degree bound excludes an \(h^q\) term from degree above
\(\ell-q\).

After summing over \(\ell\):

- \(DA-AD\) is antisymmetric under
  \((\ell,J)\leftrightarrow(r,k-J)\);
- \(BP-PB\) is antisymmetric under the same involution; and
- the \(C_\ell A_r\) sum equals the \(A_\ell C_r\) sum after that
  involution, so \(CA-3AC\) becomes \(-2AC\).

Thus, after binomial symmetrization, the sole contribution is exactly
\[
\boxed{BB-2AC.}
\]
The statement is deliberately made after expectation; pointwise
symmetry is neither asserted nor needed.  The independent verifier
reconstructs the full kernels for \(L=4,\ldots,8\), checks the complete
homogeneous component, removes the antisymmetric part, and finds exact
agreement with \(BB-2AC\).

## 4. Audit of the repaired moment formula

The revised equation (27) correctly reads
\[
\begin{aligned}
\sum_{\ell=0}^L\Bigl\{&
B_\ell B_{L-\ell}\,
\mathbb E\!\left[
J^{\ell-1}(k-J)^{L-\ell-1}
\right]_{\rm lead}\\
&-2A_\ell C_{L-\ell}\,
\mathbb E\!\left[
J^\ell(k-J)^{L-\ell-2}
\right]_{\rm lead}
\Bigr\}.                                             \tag{H}
\end{aligned}
\]
Terms with negative exponents are zero.  Both moments have total
degree \(L-2\), and
\[
\mathbb E[J^a(k-J)^b]
=2^{-(a+b)}k^{a+b}+O(k^{a+b-1}).
\]
Hence both receive the same leading factor
\(2^{-(L-2)}k^{L-2}\), so (H) leads literally to (29).

## 5. Generating function and prefactor

Using the correct center factor,
\[
\begin{aligned}
B(z/2)^2
&=\frac{z^2}{1-z},\\
-2A(z/2)C(z/2)
&=\frac{z^2}{1-z}.
\end{aligned}
\]
Therefore the coefficient at every \(z^{L-2}\), \(L\ge4\), is \(2\).
The determinant numerator is consequently
\[
2k^{L-2}+O_L(k^{L-3}).
\]
Finally,
\[
\frac{2k^{L-2}+O(k^{L-3})}{2k(k-1)}
=k^{L-4}+O(k^{L-5}).
\]
With \(L=d+4\),
\[
\boxed{[k^d]b_{k,d}=1.}
\]

## 6. Final assessment

The two defects recorded in the previous audit have been repaired.
No omitted degree-\((L-2)\) determinant term remains, and the
all-orders \(C(x)\) identity is now supported by an arbitrary-
coefficient argument using the exact source profiles and identity
(16).  The theorem, determinant numerator leading coefficient \(2\),
and final ordinary-power leading coefficient \(1\) therefore receive
an unconditional PASS under the requested audit standard.

## 7. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/top_newton_tail_2026-07-30
pytest -q test_independent_verify_ordinary_top_symbol.py
python3 independent_verify_ordinary_top_symbol.py
```
