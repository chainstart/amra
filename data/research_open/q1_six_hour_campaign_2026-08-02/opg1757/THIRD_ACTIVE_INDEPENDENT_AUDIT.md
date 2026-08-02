# Independent hostile audit of the third-active OPG reduction

Date: 2026-08-02

Status: `EXACT_REDUCTION_PASS__TRANSPORT_SIGN_OPEN`

Audited source: `THIRD_ACTIVE_EXACT_REDUCTION.md`

The executable audit is
`verify_third_active_independent_audit.py`.  It does not import the new
third-active workbench: finite rows are reconstructed from the original
pooled Newton enumerator, while the symbolic endpoint identities are
reconstructed from the frozen \(K_6,K_7\) kernels.

## 1. Forward-difference support

Put \(m=\lfloor q/2\rfloor\) and \(j=m+2\).  With the standard forward
difference convention,

\[
 \Delta_s^j C_q(4,z)=
 \sum_{i=0}^j(-1)^{j-i}\binom ji C_q(4+i,z).
\]

The frozen boundary vanishing leaves \(i=m,m+1,m+2\).  Their binomial
coefficients, including signs, are

\[
 \binom{m+2}{2},\qquad -(m+2),\qquad 1.
\]

Reversing their order gives exactly equation (1) of the source note.
No fourth boundary value is present.

For \(p=2t-5-q\), the three surviving page orders are

\[
 (6,4,2)\quad(q=2m+1),
 \qquad
 (7,5,3)\quad(q=2m).
\]

This independently confirms both parity labels.

## 2. Constants and powers in the odd branch

Let \(s=m+6\).  For the top \(B_6\) term, the factor
\(60\beta^{12}\) divided by \(6!z^{12}\) gives \(1/12\), while
\(s^{2s-2}\beta^{12}/z^{12}=s^{2s-14}\).  This is the first term
of (4).

For the middle \(B_4\) term, \(24/4!=1\), the forward coefficient is
\(-(s-4)\), and the residual scale is
\((s-1)^{2s-12}\).  Its lambda exponent exceeds the common
\(2s-16\) by two, producing \((1+z)^2\).

For the bottom \(B_2\) term,

\[
 \binom{s-4}{2}\frac4{2!}=(s-4)(s-5).
\]

The remaining scale and lambda difference give
\((s-2+2z)^{2s-10}(1+z)^4\).  Thus every constant, sign, exponent,
and common factor in (3)--(4) is reproduced.

The stable top formula begins at \(s=8\), so the two earlier odd rows
are genuinely finite bases rather than silently extrapolated stable
cases.

## 3. Constants and powers in the even branch

The same computation gives

\[
 \frac{84}{7!}=\frac1{60},\qquad
 -(s-4)\frac{40}{5!}=-\frac{s-4}{3},
\]

and

\[
 \binom{s-4}{2}\frac{12}{3!}=(s-4)(s-5).
\]

The residual scales are respectively

\[
 s^{2s-16},\quad (s-1)^{2s-14},\quad (s-2)^{2s-12},
\]

and the lambda differences from the common exponent \(2s-18\) are
\(0,2,4\).  This reproduces (5)--(6).  The stable range starts at
\(s=9\), leaving exactly two even pre-stable bases.

## 4. Maximal common factor

At \(z=-1\), the middle and bottom reduced terms vanish.  Direct
substitution in the original kernels gives

\[
 K_s^{(6)}(-1/s)=
 \frac{(s-7)(s-6)(s-5)^2(s-4)^2(s-3)(s-2)}{s^8}>0
\]

for \(s\ge8\), and

\[
 K_s^{(7)}(-1/s)=
 \frac{(s-8)(s-7)(s-6)^2(s-5)^2(s-4)^2(s-3)(s-2)}{s^{10}}>0
\]

for \(s\ge9\).  Hence the displayed powers of \(1+z\) are maximal
on the full stable ranges.  The source note correctly refrains from
turning this into an unproved exact assertion about the top \(z\)-degree.

## 5. Independent finite guards

The old pooled-state enumerator, with no call into the new workbench,
reproduces all six displayed base vectors exactly.  It also checks:

- the full forward sum equals the collapsed three-term sum for
  \(1\le q\le20\);
- all 440 coefficients in those independently reconstructed rows are
  positive; and
- all 637 coefficients in the two proposed transports through
  \(s=20\) are strictly positive.

These are regression and falsification guards only.  They do not prove
the transports for unbounded \(s\).

## 6. Conditional implication and verdict

If the odd transport (13) holds, positivity of \(H_8^{\rm o}\) propagates
to every stable odd row because multiplication by \((s+6z)^2\) preserves
strict coefficient positivity.  The even statement is identical from
\(H_9^{\rm e}\).  The four pre-stable rows are already among the exact
positive bases.  Thus the two transports are sufficient for the full
third-active theorem, with no missing base gate.

Verdict: `PASS` for the all-parameter reduction, page normalization,
stable ranges, maximal common factors, finite bases, and conditional
induction interface.  `OPEN` for the two strict transport signs.  The
audit makes no claim about later Newton rows or the arbitrary-host
OPG-1757 proposition.
