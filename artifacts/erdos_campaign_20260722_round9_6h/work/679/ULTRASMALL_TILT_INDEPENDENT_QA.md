# #679 ultra-small-tilt window: independent adversarial QA

Date: 2026-07-22 (Asia/Hong_Kong)

Verdict: **PASS_PARAMETER_THEOREM / INTERVAL TRANSFER OPEN**.

This audit independently recomputes the scales in
`ultrasmall_tilt_window.md`.  It certifies only the complete-period
large-deviation and Fourier-energy statements.  It does not certify the
missing signed high-conductor tail, an interval estimate, or Erdős #679.

## 1. Parameter separation and Mertens term

Write \(L_j=\log_jX\), let \(B\to\infty\), \(B=o(L_3)\), and put

\[
 H=e^{BL_2+o(1)},\qquad z=e^{L_1/L_2},\qquad
 L=\sum_{H<p\le z}p^{-1}.
\]

Then

\[
 \log\log z=L_2-L_3,
 \qquad \log\log H=L_3+\log B+o(1),
\]

and therefore

\[
 L=L_2-2L_3-\log B+o(1)\sim L_2.
\]

Moreover \(BL_2=o(L_1/L_2)\), so \(H<z\); hence every selected prime is
larger than the number of consecutive shifts and the local forbidden
residues are distinct.

## 2. Threshold loss

For shifts of size \(O(H)\), the original threshold satisfies, uniformly,

\[
 r(k)\le (1+\varepsilon+o(1))
 {BL_2\over L_3+\log B}.
\]

With \(a=CL_1/(HL)\) and \(R=\sum_{j<H}r(K+j)\),

\[
 HaL=CL_1,
\]

whereas

\[
 R\log(1/(1-a))
 \le (C+o(1))L_1{B\over L_3+\log B}=o(L_1).
\]

Thus the claimed complete-period estimate
\(\delta\le X^{-C+o(1)}\) has the correct sign, ceiling treatment and
uniform scale.  The assumption \(B=o(L_3)\), not merely \(B=O(L_3)\), is
essential here.

## 3. Second moment and conductor activation

The exact local identity, with \(x=H/p\), is

\[
 {1-x(1-t^2)\over(1-x(1-t))^2}
 =1+{xa^2(1-x)\over(1-xa)^2},\qquad t=1-a.
\]

Since \(p>H\), summing logarithms gives

\[
 \log(M_2/\mu^2)=O(Ha^2L)
 =O\!\left({C^2L_1^2\over HL}\right).
\]

Its logarithm is
\(-(B-2+o(1))L_2\), so this error, denoted \(\varepsilon_X\), tends to
zero.  The exact Bernoulli conductor formula similarly gives
\(\sum_p\beta_p=O(\varepsilon_X)\), and hence

\[
 M_2/\mu^2=1+O(\varepsilon_X),\qquad
 \mathbb P_2(C(h)>1)=O(\varepsilon_X).
\]

These are relative complete-period Fourier-energy statements; they are not
pointwise Fourier bounds.

## 4. Growing moment

On the good event, \(W^q\ge t^{qR}\), so
\(1_{\rm good}\le t^{-qR}W^q\).  Uniformly whenever \(qa=o(1)\),

\[
 1-t^q=qa\{1+O(qa)\}.
\]

Recomputing the local mean and threshold loss yields

\[
 -\log\{t^{-qR}\mathbb E W^q\}
 \ge qCL_1\left(1-O(qa)-O\left({B\over L_3}\right)\right).
\]

Thus \(\delta\le X^{-qC(1-o(1))}\) is valid for a moving \(q\), provided
the displayed two errors tend to zero.  If also
\(q^2\varepsilon_X=o(1)\), repeating the local second-moment calculation
for \(t^q\) gives nonzero relative energy \(O(q^2\varepsilon_X)=o(1)\).
The admissible range is nonempty and growing; for example one may take
\(q=\exp((B-3)L_2/4)\) after restricting to sufficiently large \(X\).

## 5. Fatal boundary of the inference

The full modulus has

\[
 \log Q=(1+o(1))z=\exp(L_1/L_2+o(1)).
\]

Consequently the generic interval Parseval loss \(Q/X\) overwhelms
\(q^2\varepsilon_X\) throughout the admissible moment range.  Concentration
of normalized Fourier energy at conductor one therefore does **not** imply
that an \(X\)-interval average is close to the zero mode.  The stopping-line
identity reduces the missing part to signed frontier--suffix correlations,
but supplies no inequality for their aggregate.

Final QA status:

- complete-period zero-mode theorem: **PASS**;
- growing-moment complete-period theorem: **PASS with the stated moving-\(q\)
  hypotheses**;
- vanishing relative nonzero energy: **PASS**;
- interval transfer / one-sided signed tail: **UNPROVED**;
- original Erdős #679: **OPEN**;
- SCI-Q2 stopping gate: **NOT MET**.
