# OPG-1757: fixed-layer obstruction for the odd transport bulk kernel

Date: 2026-08-02

Status: **PROVED ROUTE OBSTRUCTION; TRANSPORT RECURRENCE OPEN**.

## 1. The recurrence route

Let `L_s^o(beta)` be the sufficient odd bulk kernel constructed in
`THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md`, and clear its positive
denominator by putting

\[
 W_s(\beta)=12s\beta^8L_s^{\rm o}(\beta).
\tag{1}
\]

Finite exact data suggest

\[
 L_{s+1}^{\rm o}-u_6^2L_s^{\rm o}>_{\rm coeff}0.
\tag{2}
\]

After clearing denominators, (2) is equivalent to positivity of

\[
 Q_s=sW_{s+1}-(s+1)u_6^2W_s.
\tag{3}
\]

An exact differentiation of the five exponential terms in `F6`, the
three in `F4`, and the elementary bottom majorant gives

\[
 \boxed{
 Q_s=\sum_{a=2}^6u_a^{2s-15}E_{a,s}(\beta),
 }
\tag{4}
\]

where all `E_(a,s)` have fixed beta degree.  The executable verifier
reconstructs both (1) and (4) directly from the frozen fixed-page
kernels.

## 2. Expansion around `u_2`

Since

\[
 u_6=u_2+4\beta,\quad u_5=u_2+3\beta,\quad
 u_4=u_2+2\beta,\quad u_3=u_2+\beta,
\]

the `r`-th binomial layer outside the `u_2` term has fixed kernel

\[
 R_{s,r}=4^rE_{6,s}+3^rE_{5,s}+2^rE_{4,s}+E_{3,s}.
\tag{5}
\]

Merging the first `R` layers and then proving every remaining layer
coefficientwise nonnegative would require

\[
 R_{s,r}\ge_{\rm coeff}0\qquad(r\ge R).
\tag{6}
\]

That requirement is impossible for every fixed `R`.

## 3. Exact negative coefficient

The beta-linear coefficients of the five recurrence kernels are

\[
\begin{array}{c|c}
a&[\beta]E_{a,s}\\ \hline
6&408\\
5&-16(2s+87)\\
4&96(s+18)\\
3&-48(2s+19)\\
2&8(4s+21).
\end{array}
\tag{7}
\]

Consequently

\[
\begin{aligned}
[\beta]R_{s,r}
={}&408\,4^r-16(2s+87)3^r
 +96(s+18)2^r-48(2s+19)\\
={}&-32(3^r-3\cdot2^r+3)s
 +408\,4^r-1392\,3^r+1728\,2^r-912.
\end{aligned}
\tag{8}
\]

For `r>=3`,

\[
 3^r-3\cdot2^r+3>0.
\tag{9}
\]

Indeed it equals `6` at `r=3`, and its value at `r+1` minus twice its
value at `r` is `3^r-3>0`.  Thus for every fixed `r>=3`, (8) is negative
for all sufficiently large `s`.

The first particularly small witness is

\[
 [\beta]R_{s,4}=-1152(s-16),
\tag{10}
\]

so

\[
 \boxed{[\beta]R_{17,4}=-1152.}
\tag{11}
\]

For merge depth at most three, the still-unmerged layer `r=3` already
has

\[
 [\beta]R_{s,3}=-96(2s-15)<0\qquad(s\ge8).
\tag{12}
\]

For any fixed merge depth `R>=4`, choose `s` large enough in (8) with
`r=R`.  Hence no fixed-depth termwise-positive `u_2` layer proof of (2)
can work.

## 4. Boundary

This calculation does **not** refute (2), and it does not produce a
negative coefficient of either proposed third-active transport.  It
only refutes a specific proof architecture: merge a fixed number of
initial `u_2` layers and require all later layer kernels separately to
be coefficientwise nonnegative.

A successful proof of the growing middle must instead retain
cancellation across a number of layers growing with `s`, use a
two-parameter `d/s` inequality (for example a Bernstein subdivision),
or choose a different positive decomposition.

Run

```bash
PYTHONDONTWRITEBYTECODE=1 python3 third_active_transport_recurrence_attack.py
```

The verifier checks 150 coefficients in six direct reconstructions of
the odd/even sufficient kernels, reconstructs (4) at three parameters,
verifies every identity in (7), and checks the exact witness (11).  The
actual recurrence and both full transports remain open.
