# Independent audit: universal even second-active Newton row

Date: 2026-08-02

Audit status: PASS

## 1. Audited claim

For every \(m\ge1\) and every \(0\le r\le4m\),

\[
 \Delta_s^{m+1}C_{2m,r}(4)>0.
\tag{1}
\]

Combined with the separately audited odd row, this gives

\[
 \Delta_s^{\lfloor q/2\rfloor+1}C_{q,r}(4)>0
 \qquad(q\ge1,\ 0\le r\le2q).
\tag{2}
\]

The audit reconstructed the proof in
`EVEN_SECOND_ACTIVE_UNIVERSAL_THEOREM.md` from the displayed kernels
and exact certificates.  It did not infer an unbounded theorem from a
finite scan.

## 2. Algebraic decomposition

The comparison polynomial satisfies

\[
 M_s:=3\beta^6\mathcal K_s=Y_s+P_s.
\]

The easy part is exactly

\[
 P_s
 =3\lambda_s^4u_3^{2s-8}K_s^{(3)}
  -\lambda_s^6u_2^{2s-6}
 =\lambda_s^4
  \left(2u_3^{2s-8}K_s^{(3)}+J_s\right).
\]

Both summands in the last parenthesis are coefficientwise
nonnegative by the proved \(B_3\) theorem and the explicit positive
kernel.  Thus no cancellation estimate is hidden in \(P_s\).

For the hard part, direct binomial expansion of the four bases gives

\[
\begin{aligned}
Y_{s+1}-u_5^2Y_s
={}&u_2^{L-4}I_s\\
&+\sum_{r=4}^{L}
 \binom Lr\beta^ru_2^{L-r}R_{s,r},
\qquad L=2s-10.
\end{aligned}
\tag{3}
\]

The audit caught and repaired an earlier transcription in which the
plus sign before the sum was omitted.  Equation (3) is the identity
used by the verifier and by the proof.

## 3. Uniform positivity of all layers

After writing \(s=n+8\), every nonzero monomial coefficient in each
of

\[
 E_{5,s},\qquad
 R_{s,4}=81E_{5,s}+16E_{4,s}+E_{3,s},
\]

\[
 81E_{5,s}+8E_{4,s},\qquad I_s
\]

is strictly positive.  The exact counts are respectively

\[
 36,\qquad59,\qquad52,\qquad112.
\]

These are fixed polynomial identities in \(n,\beta\), so positivity
holds for every integer \(s\ge8\).

For \(r\ge4\),

\[
\begin{aligned}
R_{s,r+1}-R_{s,r}
&=2^r\left(E_{4,s}+2(3/2)^rE_{5,s}\right)\\
&\ge
\frac{2^r}{8}\left(8E_{4,s}+81E_{5,s}\right)
\ge_{\rm coeff}0.
\end{aligned}
\]

The inequality is directionally valid even though \(E_{4,s}\) need
not be nonnegative: the separately certified positivity of
\(E_{5,s}\) absorbs the excess
\(2(3/2)^r-81/8\).  Since \(R_{s,4}\ge0\), every omitted layer in
(3) is nonnegative.  Hence

\[
 Y_{s+1}-u_5^2Y_s\ge_{\rm coeff}0
 \qquad(s\ge8).
\tag{4}
\]

## 4. Audit of the moving top boundary

The recurrence (4) alone would not justify positivity at the two new
degrees introduced when \(s\) increases.  The proof supplies exactly
the required boundary data:

- \([\beta^{14}]Y_s>0\) and \([\beta^{15}]Y_s>0\) are positive
  shifted polynomials for every \(s\ge8\);
- \(Y_8\) is positive at degrees \(14,15,16\);
- \(Y_7\) is positive at its top degree \(14\).

If \(Y_s\) is positive on \(14\le d\le2s\), then

\[
[\beta^d]Y_{s+1}
=[\beta^d]Y_s
+10[\beta^{d-1}]Y_s
+25[\beta^{d-2}]Y_s
+[\beta^d]Q_s,
\]

where \(Q_s\ge0\).  At degrees \(2s+1\) and \(2s+2\), the last two
shifted terms use the already positive top coefficients of \(Y_s\).
The two fixed bottom degrees are supplied independently.  This closes
the full moving-support induction without a missing diagonal.

## 5. Splice back to the Newton row

- Degrees \(6\le d\le13\) of \(M_s\) are covered by eight universal
  comparison columns, certified by 84 positive shifted monomials.
- Degrees \(d\ge14\) are positive because \(Y_s>0\) and \(P_s\ge0\).
- Division by \(3\beta^6\) proves the whole comparison kernel.
- Exact homogenization then proves the reduced row through degree
  \(2s-12\), using the already proved \(G_d(s)\ge0\).
- The independently certified six reverse coefficients cover exactly
  \(2s-11,\ldots,2s-6\).
- The direct \(s=6\) boundary is strictly positive.

The ranges are adjacent and exhaust the support.  The parameter change
\(s=m+5\) maps \(s=6\) to \(q=2\), proving (1).

## 6. Reproduction and firewall

The audit reran

```bash
python3 verify_even_second_active_universal.py
pytest -q test_even_second_active_universal.py \
  test_even_second_active_partial.py test_odd_second_active.py
```

The universal verifier passed all 259 recurrence-certificate
monomials, 31 moving-boundary monomials, four exact bases, 105 direct
recurrence coefficients, 84 low-column monomials, 72 reverse-ratio
monomials, and all exceptional values.

What is proved is one complete Newton order.  The third and later
active rows, full base-four Newton positivity, the arbitrary-host
passage, and OPG-1757 remain open.
