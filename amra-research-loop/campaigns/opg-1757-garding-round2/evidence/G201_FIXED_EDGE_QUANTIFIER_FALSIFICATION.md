# G201 fixed-edge quantifier: exact finite falsification attempt

## Exact formulation

For an ordinary edge `e` of a connected graphic matroid, put

\[
 P_e=C_{M\setminus e},\qquad Q_e=\xi_e=C_{M\setminus e}-C_{M/e},
\]

and let `C_e` be the distinguished positivity component of `P_e`.  Define

\[
 E_{\rm global}(G)=\{e:Q_e(p)>0\text{ for every }p\in C_e\}.
\]

The precise G201 fixed-edge claim is `E_global(G)` nonempty for every graph
remaining after the separate loop/coloop reductions.  A fixed edge may change
after deletion in the recursive induction, but it may not depend on the point
`p` inside one deletion component.

On a common activity domain where every restriction `p_-e` lies in `C_e`, set

\[
 E(p)=\{e:Q_e(p)>0\}.
\]

The pointwise statement `E(p)` nonempty for every `p` is only a cover.  G201
requires one edge in the intersection over the whole domain.  Consequently
two exact component-valid points with `E(p_1) intersect E(p_2)` empty would
strictly refute G201 for that graph.  More generally it suffices to give, for
every edge, some point in its own `C_e` where `Q_e<=0`.

For a coloop, `Q_e` is identically zero and Fang--Ma uses the exceptional
coloop recursion.  The convention `0 triangleleft P_e` means a tree is not a
legitimate strict-positivity quantifier counterexample.  The search therefore
uses connected bridgeless graphs only.

## Exact one-coordinate search

All connected bridgeless labelled simple graphs on at most five vertices were
enumerated: 264 graphs.  For each varied edge `f`, set its activity to a
rational `t` and all other activities to one.  Exact forest enumeration gives,
for every marked edge `e`,

\[
 P_e(t)=A_{ef}t+B_{ef},\qquad Q_e(t)=C_{ef}t+D_{ef}
\]

with nonnegative integer coefficients.

The common component-valid interval is

\[
 t>\rho_f:=\max_{e:A_{ef}>0}(-B_{ef}/A_{ef}).
\]

For such `t`, every `P_e(t)>0`; because `P_e` is affine and is also positive
at `t=1`, the complete line segment from `t` to one stays in `P_e>0`.  This is
an explicit simultaneous path to the positive orthant, not a positivity
sample or mesh inference.

The search evaluated rational representatives of every interval cut out by
the exact roots of all `Q_e`, including the roots themselves.  It certified
1,781 rational points before good-set deduplication.

## Result

No edge became nonpositive on any certified one-coordinate point.  Every
tested graph had exactly one good-edge profile after deduplication: its full
edge set.  Thus:

- no two-point incompatible-edge certificate was found;
- no finite intersection shrinkage was found at all;
- the minimum common intersection was three, attained only because the
  triangle is the smallest tested bridgeless graph and all three edges remain
  good.

This is a finite absence result, not evidence that G201 is true.  The search
sees only coordinate lines through the all-ones point.  The distinguished
components are multidimensional; a sign change may require two or more
activities to move together, and no continuity/convexity theorem reduces the
full component to these lines.  Even a larger finite rational grid would not
repair that missing reduction.

The next legitimate falsifier is an exact multicoordinate path—preferably two
points in a common component-valid domain—with an empty intersection of good
edge sets.  Any such path must certify `P_e>0` continuously (for example by
exact Bernstein positivity, Sturm isolation, or a semialgebraic path), not
only at its endpoints.

The script ran under 2 GiB and a 120-second timeout in 0.8 seconds, with no
Lean.  SHA-256:
`881a8abc645bc047440aead1e9a82d955ff7afe9d4e8e8cd513aaef8e6a5eaa1`.
No public OPG conclusion changes.
