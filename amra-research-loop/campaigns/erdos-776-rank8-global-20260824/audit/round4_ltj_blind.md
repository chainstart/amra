# Blind reconstruction: Round 4 LTJ diagonal loss

## Blind boundary

Before freezing this reconstruction I read only `closure_contract.json` and
the updated `decisive_lemma.json` from the campaign.  In particular I did not
read `evidence/ROUND4_LTJ_DIAGONAL_LOSS.md`, its verifier, or any other Round 4
author evidence.

The two permitted JSON files do not define the symbols
`E_q^V,S_q,U_q,B,a,L_q,T_q,P_q`.  Accordingly, the reconstruction below fixes
the exact invariant-level claims recoverable from those files and derives the
canonical-plateau obstruction independently.  It does not silently choose
definitions for the missing symbols.  Unblinding must check that the author
uses one consistent definition and that every displayed identity is
well-typed under it.

## Public and local scope

The public target is the exact threshold `n_0(r)` for every multiplicity `r`,
including existence for every larger `n`, sharp nonexistence at the boundary,
and all exceptional small `r`.  The local orbit is

\[
 D^{[V]}_{V-12}=0,
 \qquad
 D^{[V]}_{q-1}=V+KK_q(D^{[V]}_q),                         \tag{B.1}
\]

and the still-conditional high-rank target consists of H1

\[
 0\leq W_r(V)<\binom{V-13}{r}\quad(7\leq r\leq14)         \tag{B.2}
\]

and H2

\[
 W_{14}(V+1)-W_{14}(V)\leq1                              \tag{B.3}
\]

for all `V>=125`.  Round 4 can at most prove an actual-orbit comparison or
refute a proposed way of proving the leading-top jump.  It cannot by itself
prove H1, H2, LTJ, the rank-eight entry, the inherited parameter map, or exact
`n_0(r)`.

## Canonical background used independently

For a nonnegative integer `x`, its rank-`q` Macaulay representation has the
form

\[
 x=\binom{c_q}{q}+\binom{c_{q-1}}{q-1}+\cdots,
 \qquad c_q>c_{q-1}>\cdots,                               \tag{B.4}
\]

and the lower-shadow operator is

\[
 KK_q(x)=\binom{c_q}{q-1}+\binom{c_{q-1}}{q-2}+\cdots.    \tag{B.5}
\]

Only uniqueness of (B.4), monotonicity of the shadow, and the explicit
plateaus below are used in this blind reconstruction.

## Reconstructed aligned-loss identity

Compare the actual zero-seed orbit for `V` with the diagonally aligned orbit
for `V+1`.  At a rank-`q` recurrence step, let `L_{q-1}` denote the total loss
between the shadow allowed by the aligned upper data and the actual next
lower residual.  The Round 4 status asserts the exact decomposition

\[
                         L_{q-1}=T_q+P_q.                 \tag{B.6}
\]

The two summands have different sources and must not be conflated:

- `T_q` is the tax supplied by the additive `V` versus `V+1` term in the two
  recurrences.  Its claimed all-parameter lower bound is

  \[
               T_q\geq \lfloor V/q\rfloor-1.             \tag{B.7}
  \]

  Thus it is nonnegative on the advertised range whenever `V>=q`.  The
  unblinded proof must state the exact admissible range of `q`; (B.7) alone is
  not nonnegative for arbitrary positive `q,V`.
- `P_q` is the loss propagated through the canonical shadow step.  Its claimed
  sign is

  \[
                            P_q\geq0.                     \tag{B.8}
  \]

  This must follow from a monotonicity or canonical-prefix comparison, not
  from the desired LTJ cap.

Equations (B.6)--(B.8) imply

\[
 L_{q-1}\geq \lfloor V/q\rfloor-1\geq0.                  \tag{B.9}
\]

The decisive JSON records the consequent diagonal domination as

\[
 E^{[V+1]}_{q+1}\leq S_q(E^{[V]}_q).                     \tag{B.10}
\]

The logical direction matters: nonnegative diagonal loss gives (B.10).
Nothing in (B.10) alone supplies a strictly positive propagated loss, an
upper bound for the adjacent `B_2` jump, or H1/H2.

## Exact rank-four LTJ interface

Write the actual rank-two value in the usual leading-top form

\[
 B=\binom{a}{2}+b,\qquad 0\leq b<a,                       \tag{B.11}
\]

so the leading-top jump condition is the actual adjacent-orbit claim that a
positive jump of `B` is at most `a`.  Round 4 asserts that, after exact replay
of the aligned recurrence through rank four, this condition is equivalent to

\[
 L_4\ \geq\ S_2(B)-U_2(B-V+a-1).                         \tag{B.12}
\]

This is an **exact threshold**, not a proved inequality.  An audit must check
both implications, all `b=0` and plateau-end cases, and that the argument does
not replace the actual `B(V+1)` by an extremal value without justification.
In particular, diagonal domination only yields `L_4>=0`; it proves LTJ only
where the right side of (B.12) is nonpositive.  Any positive right side needs
additional actual suffix or canonical-position information.

Because `S_2` and `U_2` are undefined in the permitted JSON, (B.12) cannot be
independently type-checked before unblinding.  The author evidence must define
both operators and derive (B.12) without an off-by-one at `B-V+a-1`.

## Independent arbitrary-plateau obstruction

Canonical shadows have arbitrarily long flat pieces.  Fix `q>=2` and an
integer `A>q`.  For

\[
 x_b=\binom{A}{q}+\binom{b}{1}
     =\binom{A}{q}+b,
 \qquad 1\leq b<A,                                       \tag{B.13}
\]

the representation is canonical and

\[
 KK_q(x_b)=\binom{A}{q-1}+\binom{b}{0}
          =\binom{A}{q-1}+1,                              \tag{B.14}
\]

independent of `b`.  Hence there are canonical plateaus of length `A-1`, and
that length is unbounded.

Take two distinct points on one such plateau.  Their input gap is positive,
but the propagated shadow difference is zero.  Therefore any proposed
universal estimate of the form

\[
 P_q\geq f(q,L_q)>0\quad\hbox{whenever }L_q>0             \tag{B.15}
\]

which uses only the size of the gap and ignores canonical position is false.
In the author's notation this must appear as an admissible plateau with
`P_q=0`.  The obstruction does not show that the actual zero-seed orbit stays
on the bad portion of a plateau; it only proves that gap magnitude alone
cannot make it escape.

## Blind preliminary classification

Subject to exact definitions and quantifier checks after unblinding:

- (B.6)--(B.10) would be an all-parameter supporting theorem about the actual
  aligned orbit.
- (B.13)--(B.15) would be a standalone scoped no-go theorem killing every
  gap-only positive propagated-loss estimate.
- (B.12) would be a conditional exact reformulation of LTJ, not LTJ itself.
- H1, H2, the rank-eight entry, the `r`-to-`(V,n)` map, the sharp lower
  boundary, and exact `n_0(r)` would all remain open.

The decisive question for unblinding is whether the author proves the identity
and signs for all actual aligned orbit parameters without assuming a separator
or LTJ, and whether the plateau family is valid for the exact definition of
`P_q`, rather than merely for an unrelated scalar shadow.
