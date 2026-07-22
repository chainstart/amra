# #679: fixed-exponent refinement of the vanishing-energy window

Date: 2026-07-22

The hypothesis \(B\to\infty\) in ultrasmall_tilt_window.md is stronger than
needed. A particularly clean choice is

\[
 H=\lfloor(\log X)^2\rfloor,\qquad
 z=\exp(L_1/L_2),\qquad
 L=\sum_{H<p\le z}{1\over p},
\]

\[
 a={C L_1\over HL},\qquad t=1-a,                       \tag{1}
\]

where \(C>1\) is fixed. This retains the complete-period exponent, makes the
relative Fourier variance tend to zero, and permits a growing Markov moment.
It still does not give interval transfer.

## 1. Prime mass and threshold loss

Here

\[
 \log\log H=L_3+\log 2+o(1),
\]

so Mertens gives

\[
 L=L_2-2L_3-\log2+o(1)\sim L_2.                       \tag{2}
\]

Every selected prime exceeds the number \(H\) of consecutive shifts. Thus
the local forbidden classes are distinct. Uniformly over those shifts,

\[
 r(k)\le (2+o_\varepsilon(1)){L_2\over L_3}.           \tag{3}
\]

If \(R\) is the sum of the \(H\) integer thresholds, then

\[
 HaL=C L_1,\qquad
 R\log(1/t)\le (2C+o_\varepsilon(1)){L_1\over L_3}
              =o(L_1).                                \tag{4}
\]

Consequently the same Markov argument proves, for the complete CRT period,

\[
 \delta\le X^{-C+o(1)}.                                \tag{5}
\]

## 2. Vanishing relative energy

The exact local second-moment identity gives

\[
 \log{M_2\over\mu^2}
 =O(Ha^2L)
 =O\!\left({C^2L_1^2\over HL}\right)
 =O_C(1/L_2).                                         \tag{6}
\]

Likewise, under normalized Fourier energy,

\[
 \sum_p\beta_p=O_C(1/L_2),\qquad
 \mathbb P_2(C(h)>1)=O_C(1/L_2).                       \tag{7}
\]

For a typical prime away from the lower endpoint,

\[
 p\beta_p=(1+o(1))Ha^2
 ={C^2+o(1)\over L_2^2}.                              \tag{8}
\]

Thus \(B=2\), not a moving \(B\), already eliminates the round-8
single-full-conductor energy artefact.

## 3. An explicit growing moment

Take

\[
 q=\lfloor L_3\rfloor.
\]

Then \(qa=o(1)\) and \(q^2/L_2=o(1)\). Put
\(b=1-t^q=qa\{1+O(qa)\}\). On the same good event,
\(1_{\rm good}\le t^{-qR}W^q\), and the local mean calculation gives

\[
 -\log\{t^{-qR}\mathbb E_Q W^q\}
 \ge qCL_1
 \left(1-O(qa)-O_\varepsilon(1/L_3)\right).            \tag{9}
\]

Therefore

\[
 \boxed{\delta\le X^{-C L_3(1-o(1))}},                 \tag{10}
\]

while the relative nonzero Fourier energy of \(W^q\) is

\[
 O(Hb^2L)=O_C(L_3^2/L_2)=o(1).                         \tag{11}
\]

More generally, any integer \(q\to\infty\) with
\(q=o(\sqrt{L_2})\) works; the condition \(qa=o(1)\) is then automatic.

## 4. Independent boundary checks

* Formula (3) uses \(\log H=2L_2+o(1)\) and
  \(\log\log H=L_3+\log2+o(1)\); the ceiling contributes only \(O(1)\).
* The threshold term in (9) is multiplied by the same \(q\) as its main
  exponent. Hence the relative loss remains \(O(1/L_3)\), not
  \(O(q/L_3)\).
* Equation (11) is relative complete-period energy. It is not a pointwise
  bound for Fourier coefficients.
* The full modulus still has
  \(\log Q=(1+o(1))z=\exp(L_1/L_2+o(1))\). Generic interval Parseval
  therefore still loses an uncontrollable factor \(Q/X\).
* The polynomial-level denominator audit remains adverse at \(B=2\):
  a modulus \(d\le X^\theta\) contains at most
  \((\theta/2+o(1))L_1/L_2\) selected primes, and its canonical soft
  Selberg denominator has logarithm \(o(qL_1)\), versus the required
  \(qCL_1\).

Strict status: **cleaner and stronger complete-period parameter theorem;
signed interval transfer unproved; Erdős #679 open; no publication gate
claimed**.
