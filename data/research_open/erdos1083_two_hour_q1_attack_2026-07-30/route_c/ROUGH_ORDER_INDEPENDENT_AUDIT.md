# Independent red-team audit: rough-order cyclotomic fibre escape

Date: 2026-07-30

Audited target:
`ROUGH_ORDER_CYCLOTOMIC_FIBRE_ESCAPE_THEOREM.md`

## 0. Verdict

\[
\boxed{\texttt{PASS}}
\]

The Mann-theorem extension is stated with the correct coefficient field
and arithmetic hypothesis.  The five-term rigidity lemma, selected-label
injection, Kneser lower bound, least-prime equal-fibre constant, sharpness
example, aperiodic and complete-fibre corollaries, and scope boundary all
pass independent audit.

In particular, the note does not claim that Mann's theorem is new, does
not extend its rational-coefficient argument to an arbitrary field, and
does not claim an unconditional improvement for Erdős #1083.

## 1. Mann short-relation lemma

Let
\[
\sum_{j=1}^{s}c_j\omega_j=0,\qquad c_j\in\mathbb Q^\times,
\]
be an irreducible relation among roots of unity.  The version of Mann's
theorem used in the manuscript says that every quotient
\(\omega_i/\omega_j\) has order dividing
\[
P_s=\prod_{\substack{q\le s\\q\ {\rm prime}}}q.
\]

Suppose a nonempty rational relation among distinct powers of a
primitive \(m\)-th root has at most five terms.  A minimal vanishing
subsum is irreducible and still has distinct roots, with \(2\le s\le5\).
Mann gives
\[
\operatorname{ord}(\omega_i/\omega_j)\mid P_s\mid30.
\]
The quotient is also an \(m\)-th root, so its order divides \(m\).
Under \(\gcd(m,30)=1\), the quotient therefore has order one.  This says
two distinct roots in the minimal subsum are equal, a contradiction.
Hence no such nonzero relation exists.

This argument correctly handles signed coefficients: signs belong to
the rational coefficients \(c_j\), not to the roots.  No additional
factor beyond \(30\) is needed.

The cited primary source is H. B. Mann, *On linear relations between
roots of unity*, Mathematika **12** (1965), 107--117,
doi:10.1112/S0025579300005210.

## 2. Distance-label injection

An equality of two selected labels expands to a rational relation
supported on
\[
\{0,d,-d,e,-e\}\pmod m.
\]
After equal exponents are collected, the remaining exponents are
distinct and the support has cardinality at most five.  Section 1
therefore forces the coefficient vector to vanish.

The canonical representatives
\[
1\le d,e\le(m-1)/2
\]
give disjoint sign pairs unless \(d=e\).  If \(d\ne e\), the
coefficient of \(\zeta^d\) is \(-r^2\ne0\), impossible.  Thus \(d=e\);
the same coefficient gives equality of the positive radii.  Equality
of the anchored height squares then gives equality of heights because
both offsets are nonnegative.  This proves injection across sign
classes, radii, and heights exactly as claimed.

The hypothesis \(\gcd(m,30)=1\) implies that \(m\) is odd, so every
nonzero unoriented class \(\{d,-d\}\) has two elements.  There is no
unhandled order-two angular class.

## 3. Kneser and the least-prime constant

Let \(\ell\) be the least prime divisor of \(m\), and let
\(H\) be the stabilizer of one anchored difference set.  Kneser's
theorem gives
\[
|A-B|\ge |A+H|+|B+H|-|H|.
\]
If \(H\) is trivial and both fibres have size \(S\), then
\[
q\ge S-1\ge\frac{\ell-1}{2\ell}S.
\]

If \(H\) is nontrivial, its order \(h\) divides \(m\), hence
\(h\ge\ell\).  With \(c=\lceil S/h\rceil\),
\[
L\ge(2c-1)h,\qquad S\le ch.
\]
Therefore
\[
\frac qS
\ge
\frac{(2c-1)h-1}{2ch}
\ge
\frac{h-1}{2h}
\ge
\frac{\ell-1}{2\ell}.
\]
The middle inequality differs by
\((c-1)(h+1)/(2ch)\ge0\), so no ceiling or parity case is hidden.

The cyclic group has a unique subgroup of order \(\ell\).  Taking one
fibre supported on it gives a regular \(\ell\)-gon with exactly
\((\ell-1)/2\) nonzero distances, establishing sharpness of the uniform
constant over this family.

The aperiodic and complete-fibre corollaries then follow identically to
the prime-power case.

## 4. Boundary and coefficient field

If \(2\), \(3\), or \(5\) divides \(m\), an embedded regular
\(p\)-gon supplies a rational relation with at most five terms, so the
Mann argument no longer proves rigidity.  The manuscript correctly
describes this as a boundary of the method, not as a counterexample to
distance injection for every excluded order.

The order-eight identity
\[
a_2=2,\qquad a_4=4
\]
does give a genuine cross-radius collision, so failures among excluded
orders are real.

The note also correctly withholds the prime-power base-field extension.
For a general composite \(m\), irreducibility of \(\Phi_m\) over a
larger field does not by itself provide the disjoint sparse-block
description used for \(p^a\), while the invoked Mann theorem is a
rational-coefficient result.

## 5. Reproduction record

The exact verifier and regression tests were rerun:

```text
PYTHONDONTWRITEBYTECODE=1 python3 verify_rough_order_cyclotomic_escape.py
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider \
  test_verify_rough_order_cyclotomic_escape.py
```

Result:

```text
5 passed in 0.40s
```

The finite certificates cover non-prime-power orders
\(77,91,143\), prime-power quotient compatibility at order \(49\),
least-prime subgroup sharpness at order \(77\), and the five-term
boundary at order \(35\).  These calculations check the exact algebra
and indexing; the unbounded short-relation assertion rests on Mann's
theorem and the proof audited in Section 1.

## 6. Scope verdict

The result materially broadens the structured-family exclusion from
prime powers to all angular orders with no prime factor below seven.
It remains conditional on the anchored coaxial model and rational
radii/height squares.  Without an extraction theorem placing arbitrary
critical configurations into that model, it is not a standalone
solution of Erdős #1083 and is unlikely to support a top-quartile paper
by itself.
