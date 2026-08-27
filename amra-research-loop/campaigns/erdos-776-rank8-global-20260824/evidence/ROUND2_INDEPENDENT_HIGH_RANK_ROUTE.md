# Round 2 independent high-rank route

## Outcome

**No new actual-orbit all-parameter result was obtained.**  In particular,
this round neither proves nor refutes

\[
 W_{14}(V+1)-W_{14}(V)\le1\qquad(V\ge125),             \tag{H2}
\]

and it does not prove the rank-7--14 separator statement H1.  Bounded orbit
calculations were used only to discover and stress candidate state languages;
they are not promoted.

The useful output is two exact conditional reductions which isolate what an
actual-orbit upstream coupling would have to prove.  The first differs from
an arbitrary capacity argument: a three-unit upper bound for the *generated*
rank-two tail is enough to exclude the known synthetic two-unit shadow jump.
The second shows that a very weak linear bound at rank 14 would close every
lower H1 separator.

## 1. Independent consistency with the rank-two tail formula

At rank 17, the observed stable canonical language has a long forced prefix
and a two-canonical tail.  If that language is established for all relevant
parameters, write its tail as \(B_2(V)\).  Shadowing the prefix and adding
the tax gives

\[
 W_{14}(V)=27+\operatorname{KK}_2(B_2(V)).             \tag{1}
\]

This agrees independently with the formula obtained on the separate
`erdos_404` route.  It is recorded here only as consistency, not as a new
claim of priority or closure.  This round did not prove the stable rank-17
prefix for every \(V\).

The actual tail is not an arbitrary capacity variable.  The next observed
upstream suffix \(B_3(V)\) satisfies, whenever the displayed stable prefix is
legally separated,

\[
 B_2(V)=V+\operatorname{KK}_3(B_3(V)).                 \tag{2}
\]

More generally the candidate stable language at rank \(s+15\) gives

\[
 B_{s-1}(V)=V+\operatorname{KK}_s(B_s(V)).             \tag{3}
\]

The finite states satisfy (2)--(3), but this round found no all-parameter
separator invariant that starts (3) upstream.  Consequently (2)--(3) are a
candidate actual-orbit coupling architecture, not a proved universal orbit
description.

## 2. A proved three-unit actual-tail criterion for H2

The following elementary statement is all-parameter.

### Lemma

Let \(x,y\) be nonnegative integers, let the leading upper index in the
2-canonical expansion of \(x\) be at least three, and suppose

\[
 y-x\le3.
\]

Then

\[
 \operatorname{KK}_2(y)-\operatorname{KK}_2(x)\le1.   \tag{4}
\]

### Proof

Write

\[
 x=\binom a2+b,qquad 0\le b<a,qquad a\ge3.
\]

If \(b=0\), then \(\operatorname{KK}_2(x)=a\), while
\(x+3\le\binom{a+1}2\); hence every \(y\le x+3\) has shadow at most
\(a+1\).

If \(b>0\), then \(\operatorname{KK}_2(x)=a+1\).  Since

\[
 \binom{a+2}2-x
 =2a+1-b\ge a+2>3,
\]

one has \(y<\binom{a+2}2\), and therefore
\(\operatorname{KK}_2(y)\le a+2\).  This proves (4).  Negative jumps are
already included because the only assumption is the one-sided bound
\(y-x\le3\).  \(\square\)

Combining (1) and (4) gives the exact sufficient actual-orbit target

\[
 B_2(V+1)-B_2(V)\le3
 \quad\Longrightarrow\quad \text{H2},                 \tag{5}
\]

once the rank-17 tail identity and the harmless top-index lower bound are
proved.  Thus the capacity-only synthetic shadow jump of two does not by
itself refute the actual orbit: it can occur only through a tail transition
which violates the generated three-unit coupling or the stable-prefix
interface.

Finite exploration found maximum \(B_2\) increment three for
\(125\le V\le500\) and found the triangular tail states to advance safely.
This is only a falsifier observation.  No proof of (5)'s premise for
unbounded \(V\) was found.

## 3. A proved linear rank-14 criterion for all of H1

There is also a simple exact reduction of all eight H1 separators to a weak
rank-14 estimate.

### Lemma

Assume \(V\ge125\) and

\[
 0\le W_{14}(V)\le V.                                 \tag{6}
\]

Then

\[
 0\le W_r(V)<\binom{V-13}{r}qquad(7\le r\le14).      \tag{7}
\]

### Proof

The rank-14 separator follows immediately from (6), since
\(V<\binom{V-13}{14}\) at \(V=125\) and the right side grows faster.
Whenever the rank-\(r\) separator holds, exact prefix cancellation gives

\[
 W_{r-1}(V)=V+\operatorname{KK}_r(W_r(V)).             \tag{8}
\]

Using \(\operatorname{KK}_r(x)\le rx\), define
\(A_{14}=1\), \(A_{r-1}=1+rA_r\).  Induction from (6) gives
\(0\le W_r(V)\le A_rV\), with

\[
\begin{array}{c|rrrrrrrr}
r&14&13&12&11&10&9&8&7\\ \hline
A_r&1&15&196&2353&25884&258841&2329570&18636561.
\end{array}
\]

At \(V=125\), each \(A_rV\) is strictly below
\(\binom{112}{r}\); the smallest relative check is still

\[
 18636561\cdot125=2329570125
 <\binom{112}{7}=36227890512.
\]

For each fixed \(r\ge7\), \(\binom{V-13}{r}/V\) is increasing for
\(V\ge125\).  Therefore the same strict comparisons hold for every larger
\(V\), permitting (8) successively down to rank seven.  \(\square\)

Hence the entire H1 package would follow from the much simpler actual-orbit
claim \(0\le W_{14}(V)\le V\).  This round did not prove that claim.  H2 and
the base value give the upper half \(W_{14}(V)\le V\), but H2 alone does not
prevent a negative downward jump, so nonnegativity remains an independent
obligation.

## 4. Computational boundary and final status

Exploration used the existing exact compressed orbit engine and separately
inspected canonical runs at ranks 17--22.  It observed a low-dimensional
tail and no H2 failure, but runtime-limited or enlarged cutoffs would add no
mathematical evidence.  No new verifier is persisted because no new
all-parameter actual-orbit assertion was proved that requires executable
support; the two lemmas above are direct symbolic arguments.

Final classification:

* rank-two three-unit lemma (4): **proved**;
* linear rank-14 criterion (6) \(\Rightarrow\) H1: **proved**;
* stable upstream language (1)--(3): **conditional/observed**, independently
  consistent with the other route;
* actual generated-tail bound \(B_2(V+1)-B_2(V)\le3\): **open**;
* H2: **open**;
* H1: **open**;
* all-\(V\) rank-8 entry and original Erdős #776: **unchanged**.

The next noncosmetic action is not a larger scan.  It is an all-parameter
separator theorem for the rank-17 upstream prefix together with a generated
tail invariant proving the three-unit bound in (5), or an infinite actual-
orbit family violating that bound.
