# Erdős #686: conjectural extension of the 2-adic polynomial-part law

Date: 2026-07-22 (Asia/Hong_Kong)

Status: exact finite evidence and a concrete next lemma; **not proved**.

Let

\[
 P_l(x)=\prod_{i=1}^{2l}(x+i)
\]

and let `A_l(x)` be the polynomial part of `sqrt(P_l(x))` at infinity.  The
companion note proves, for odd `l`,

\[
 v_2(A_l(x))=-l-v_2(l!)\qquad(x\in\mathbb Z).         \tag{1}
\]

Exact calculation exposes a different but equally rigid law when `l` is
even.  Write `s=oddpart(l)`.  The conjectural identity is

\[
 \boxed{v_2(A_l(x))=l-2s-v_2(s!)}
 \qquad(l\text{ even},\ x\in\mathbb Z).              \tag{2}
\]

For example, as `l=2,4,6,8,10,12,16`, the predicted valuations are

\[
 0,2,-1,6,-3,5,14.
\]

The exact script `probe_even_half_length_pattern.py` checked (2) for every
even `2<=l<=64` and every `0<=x<=127`, a total of 4096 rational evaluations,
with no failure.  This is only finite conjecture generation.

## Why this is a plausible proof target

With `w=2x+2l+1`, put

\[
 F_l(t)=\prod_{j=1}^l(1-(2j-1)^2t),\qquad
 \sqrt{F_l(t)}=\sum_{j\ge0}q_jt^j.
\]

Then

\[
 A_l(x)=2^{-l}\sum_{0\le j\le l/2}q_jw^{l-2j}.
\]

For `l=2^a s`, pairing the odd numbers `u` and `4m-u` in the passage
`l=2m` gives

\[
 (4m-u)^2-u^2\equiv0\pmod {2^{3+v_2(m)}}.            \tag{3}
\]

Thus `F_{2m}` is a high 2-adic approximation to a square built from
`F_m`.  Iterating this pairing until the odd core `s` is reached is the
natural source of the `oddpart(l)` in (2).  What is still missing is a
coefficientwise square-root/truncation lemma strong enough to retain the
*exact* valuation after evaluation at every odd `w`; a coarse congruence
from (3) loses precisely the powers needed for equality.

An equivalent integer-valued-polynomial target is often cleaner.  If

\[
 V(l)=l-2\operatorname{oddpart}(l)
      -v_2(\operatorname{oddpart}(l)!),
\]

then it would suffice to prove that the Mahler expansion of
`2^{-V(l)}A_l(x)` has odd constant coefficient and all positive finite-
difference coefficients even.  The finite data have exactly this pattern.

## Consequence if proved, and its limit

Equation (2) would imply that `A_l(m)-2A_l(n)` always lies in a fixed
nonzero 2-adic lattice coset.  The Laurent-tail argument from the odd-`l`
theorem would then rule out

\[
 P_l(m)=4P_l(n)
\]

for sufficiently large `min(m,n)` for **every fixed even block length
`k=2l`**, not only `k congruent to 2 (mod 4)`.  However, fixed-`k`
finiteness is already known more generally, and the original problem lets
`k` vary.  Even a proof of (2) would therefore be a structural component,
not a solution or by itself a Q2-level main theorem.
