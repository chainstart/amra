# Erdős #686: a uniform 2-adic obstruction for `k = 2l`, `l` odd

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous structural theorem; it does not close `N=4` or the original
problem.  Its fixed-`k` finiteness consequence is weaker than the known
fixed-`k` finiteness theorem, but it turns the formerly empirical `k=6`
phenomenon into an infinite-family statement.

## 1. Statement

For `l >= 1`, put

\[
 P_l(x)=\prod_{i=1}^{2l}(x+i)
\]

and let `A_l(x)` be the polynomial part at infinity of `sqrt(P_l(x))`.
If `l` is odd, then for every integer `x`,

\[
 \boxed{v_2(A_l(x))=-l-v_2(l!).}                 \tag{1}
\]

Equivalently,

\[
 2^{l+v_2(l!)}A_l(x)\quad\hbox{is an odd integer}. \tag{2}
\]

Consequently, for each fixed `k=2l` with `l` odd, the equation

\[
 P_l(m)=4P_l(n)                                  \tag{3}
\]

has no solutions with `min(m,n)` sufficiently large.  In particular, the
polynomial-part obstruction previously known at `k=6` works for every
`k congruent to 2 (mod 4)`.

## 2. Centering and the square-root coefficients

Write

\[
 w=2x+2l+1,
 \qquad
 R_l(w)=\prod_{j=1}^l\bigl(w^2-(2j-1)^2\bigr).
\]

Then `P_l(x)=2^{-2l}R_l(w)`.  Define rational numbers `q_j` by

\[
 \sqrt{R_l(w)}
 =w^l\sum_{j\ge0}q_jw^{-2j}
\]

as a formal Laurent series at infinity.  Hence

\[
 A_l(x)=2^{-l}Q_l(w),\qquad
 Q_l(w)=\sum_{0\le j\le(l-1)/2}q_jw^{l-2j}       \tag{4}
\]

when `l` is odd.

We prove the coefficient valuation

\[
 \boxed{v_2(q_j)=-v_2((2j)!)}
 \quad(0\le j\le(l-1)/2).                        \tag{5}
\]

## 3. Proof of the coefficient valuation

Put `t=w^{-2}` and

\[
 F_l(t)=\prod_{j=1}^l(1-(2j-1)^2t).
\]

Every odd square is congruent to `1 modulo 8`, coefficientwise giving

\[
 F_l(t)\equiv(1-t)^l\pmod {8\,\mathbb Z_2[t]}.   \tag{6}
\]

Since `(1-t)^l` is a unit in `Z_2[[t]]`, write

\[
 {F_l(t)\over(1-t)^l}=1+8H(t),\qquad
 H(t)\in t\mathbb Z_2[[t]].
\]

The binomial series is 2-adically legitimate here and gives

\[
 (1+8H(t))^{1/2}=1+4C(t),
 \qquad C(t)\in t\mathbb Z_2[[t]].               \tag{7}
\]

Therefore

\[
 \sqrt{F_l(t)}=(1-t)^{l/2}(1+4C(t)).             \tag{8}
\]

Let

\[
 b_j=(-1)^j\binom{l/2}{j}.
\]

Because `l` is odd,

\[
 b_j=(-1)^j{l(l-2)\cdots(l-2j+2)\over2^j j!},
\]

whose numerator is odd.  Legendre's formula gives

\[
 j+v_2(j!)=v_2((2j)!),
\]

and hence

\[
 v_2(b_j)=-v_2((2j)!).                            \tag{9}
\]

The coefficient of `t^j` in the correction term
`4C(t)(1-t)^{l/2}` is a sum of terms `4c_h b_{j-h}` with `h>=1` and
`c_h in Z_2`.  Each such term has valuation at least

\[
 2-v_2((2j-2h)!)>-v_2((2j)!).                    \tag{10}
\]

Thus it cannot cancel the leading 2-adic part of `b_j`.  Equations
(8)--(10) prove (5).

## 4. Evaluation at integers

For integer `x`, the centered variable `w=2x+2l+1` is odd.  Multiplication
by `w^{l-2j}` does not change a term's 2-adic valuation.  The values in (5)
strictly decrease as `j` increases, since `(2j+2)!/(2j)!` is even.  Hence the
last term in (4), `j=(l-1)/2`, is the unique term of minimum valuation.  It
follows that

\[
 v_2(Q_l(w))=-v_2((l-1)!)=-v_2(l!),
\]

where the last equality uses odd `l`.  Combining this with (4) proves
(1)--(2).

## 5. Consequence for the quotient equation

For fixed `l`, Laurent expansion at infinity gives

\[
 \sqrt{P_l(x)}=A_l(x)+E_l(x),\qquad E_l(x)\to0.
\]

If (3) holds for nonnegative `m,n`, positivity gives

\[
 A_l(m)-2A_l(n)=2E_l(n)-E_l(m).                  \tag{11}
\]

By (2), the left side is `2^{-l-v_2(l!)}` times an odd integer: an odd
integer minus twice an odd integer is odd.  It is therefore nonzero and has
absolute value at least `2^{-l-v_2(l!)}`.  The right side tends to zero as
`min(m,n)` tends to infinity.  This contradiction proves the asserted
fixed-`k` finiteness.

## 6. Boundary

The proof does not give a useful uniform cutoff in `l`, and it says nothing
about `l` even (`k divisible by 4`).  Even after an explicit cutoff, checking
infinitely many `k` would remain.  Thus this theorem is a real route advance
but not a Q2-level stopping result and not a resolution of #686.

The official discussion thread already contains the isolated `k=6`
polynomial-part expansion (posted in March 2026), and cites the stronger
known fact that fixed `N` and fixed `k>2` admit only finitely many solutions.
The campaign-new content here is the uniform coefficient valuation for every
`k congruent to 2 (mod 4)`, not fixed-`k` finiteness itself.  This is only a
targeted priority check, not an exhaustive novelty certification.
