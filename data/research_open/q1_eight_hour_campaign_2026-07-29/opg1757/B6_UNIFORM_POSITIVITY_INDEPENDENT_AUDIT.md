# Independent audit of the \(B_6\) uniform-positivity proof

Date: 2026-07-30

## Verdict

The argument in `B6_UNIFORM_POSITIVITY.md` proves the stated result:
\[
  F_s^{(6)}\ge_{\mathrm{coeff}}0\qquad(s\ge7),
\]
and the separately derived \(s=6\) boundary is positive.  Consequently the
six-page Newton layer \(B_6\) is coefficientwise nonnegative for every
admissible core size.

This is an unbounded theorem, not an inference from the scan through
\(s=200\).

## Algebraic audit

Write
\[
 F=A-4B+6C-4D+E,\qquad G=A-4B.
\]
The decomposition
\[
 F=G+3(C-2D+E)+2(D-E)+3C
\]
is exact.  The first two parenthesized terms are respectively the already
proved \(B_4\) and \(B_3\) brackets after multiplication by monomials with
nonnegative coefficients.  Thus it is legitimate to prove the low degrees
directly for \(F\), while proving only the high-degree tail of \(G\).

For
\[
 \Delta_s=K_{s+1}^{(6)}-K_s^{(6)},\quad
 H_s=u_6^2\lambda_s^2K_s^{(5)}
     -u_5^2\lambda_{s+1}^2K_{s+1}^{(5)},\quad
 M=2s-12,
\]
direct subtraction gives
\[
 G_{s+1}-u_6^2G_s=u_6^M\Delta_s+4u_5^MH_s.
\]
Expanding \(u_6^M=(u_5+\beta)^M\), isolating \(r=0,1,2\), and factoring
\(u_5^{M-2}\) gives exactly the displayed three-layer recurrence.  No
inequality is used in this identity.

The certificate checks that \(\Delta_s\) is coefficientwise nonnegative
and that the merged polynomial \(I_s/\beta^2\) has 17 beta layers, every
coefficient being a positive polynomial in \(s-15\).  Hence
\[
 G_{s+1}-u_6^2G_s\ge_{\mathrm{coeff}}0
\]
for \(s\ge15\).

## Truncation audit

Let \(T_s\) retain degrees at least 20 from \(G_s\).  Since
\[
 u_6^2=1+12\beta+36\beta^2,
\]
discarded degrees at most 19 can affect only degrees 20 and 21 after one
transport step.  Therefore:

- for \(d\ge22\), the truncated difference equals the corresponding
  coefficient of the full positive recurrence;
- at \(d=20\), the correct difference is
  \(g_{s+1,20}-g_{s,20}\);
- at \(d=21\), it is
  \(g_{s+1,21}-g_{s,21}-12g_{s,20}\).

These are exactly the two expressions certified in the verifier.  Their
factorizations are positive for \(s\ge15\).  The 13 coefficients of
\(T_{15}\), in degrees 20 through 32, are strictly positive, so induction
is valid.  The early cases \(7\le s\le14\) are checked separately from the
exact coefficient formula.

## Low-degree audit

Degrees below 8 vanish identically.  For degrees 8 through 19 the verifier
derives the coefficients from the original five-term formula rather than
from the recurrence.

The only sign-sensitive displayed factors are:

- \(n(2n-1)\) at degree 18;
- \(n(n-1)(2n-1)\) at degree 19,

where \(n=s-7\).  At the potentially negative integer values, the zero
factors make the entire coefficient zero: \(n=0\) for degree 18 and
\(n=0,1\) for degree 19.  For the remaining integers all factors and all
coefficients of the quotient polynomials are positive.  Thus there is no
gap from treating positivity over integers rather than over all real
\(n\ge0\).

## Reproduction and independent spot checks

Regenerating the static certificate produced a byte-identical file with
SHA-256

```text
f1cd7be72392ebc57c433f317d8f1924b78353c82173b8cfeae62369b0e96fe7
```

Direct integer-convolution checks at
\[
s=7,8,14,15,16,37,201,500,1000
\]
found no negative coefficient in \(F_s^{(6)}\) or in the candidate full
recurrence remainder.  These checks are regressions only; the proof is the
symbolic low-degree and truncated-tail certificate above.

## Scope firewall

The result proves one complete page-Newton layer for the disjoint
core-edge orbit in the two-activity complete-split-graph model.  Together
with the earlier work it establishes uniform positivity of
\(B_2,\ldots,B_6\).  It does **not** prove:

- all remaining Newton layers \(B_n\);
- all edge-pair orbits for arbitrary core size;
- independent edge activities; or
- the full Grimmett--Winkler/Pemantle random-forest conjecture.

Those distinctions must remain explicit in any publication assessment.
