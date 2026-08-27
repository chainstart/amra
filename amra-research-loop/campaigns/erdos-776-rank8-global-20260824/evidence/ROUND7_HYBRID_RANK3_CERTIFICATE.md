# Round 7: hybrid rank-three certificate

## Status and verdict

This round proves a new all-parameter **conditional certificate** for the
surviving `M776G-01` route.  It combines canonical position and increment
size instead of imposing either datum at every wall.  The actual-orbit
premise remains open, so the result does not prove LTJ, H1--H2, the rank-eight
entry, or Erdős #776.

The bounded kill test on `125 <= V <= 2000` found that every actual wall
satisfies the new disjunction.  This finite result is not extrapolated.  An
exact synthetic counterexample also proves that the disjunction, and even the
older rank-three budget, do not follow from the known low-rank recurrences and
Round 4 diagonal domination alone.  Genuine upstream actual-orbit coupling is
still required.

## 1. Notation

Retain the separated residual recurrence

\[
 Z_{s-1}(V)=V+\partial_s Z_s(V),
 \qquad \partial_s=\operatorname{KK}_s,
\]

and put

\[
 X=Z_4(V),\quad Y=Z_4(V+1),\quad
 \delta_4=Y-X,
\]

\[
 Z=Z_3(V),\quad Z'=Z_3(V+1),\quad
 \delta_3=Z'-Z.
\]

Write

\[
 B_2(V)=\binom a2+b,\qquad 0\le b<a,
\]

and set

\[
 C_4(a)=U_3(a-1),\qquad A_3(a)=U_2(a-1).
\]

The exact adjacent recurrence is

\[
 \delta_3=1+\partial_4(Y)-\partial_4(X).       \tag{R7.1}
\]

## 2. The rank-four top lies below the LTJ top

Let `c` be the leading upper index of the 4-canonical word of `X`.  Then

\[
                         c\le a.                       \tag{R7.2}
\]

Indeed, `X >= binom(c,4)` gives
`partial_4(X) >= binom(c,3)`, hence

\[
 Z=V+\partial_4(X)\ge\binom c3,
 \qquad
 B_2(V)=V+\partial_3(Z)>\binom c2.
\]

But the definition of `a` gives `B_2(V)<binom(a+1,2)`.  If `c>=a+1`, these
two inequalities contradict each other, proving (R7.2).

## 3. Hybrid certificate

**Hybrid rank-three lemma.**  Fix an actual adjacent wall with `V>=125`.
Suppose at least one of the following holds.

1. The 4-canonical words of `X` and `Y` share their first two terms.
2. The positive increment satisfies
   `(delta_4)_+ <= C_4(a)=U_3(a-1)`.

Then

\[
                         \delta_3\le a\le A_3(a),       \tag{R7.3}
\]

so the Round 5 rank-three budget holds and LTJ follows.

For the first branch, write the common prefix as

\[
 \binom c4+\binom d3,\qquad c>d.
\]

After cancelling this prefix, each remaining suffix has ranks at most two
and all its upper indices are below `d`.  Its 4-shadow contribution therefore
lies between `0` and `d`: a suffix
`binom(e,2)+binom(f,1)` contributes at most `e+1<=d`.
Consequently

\[
 \partial_4(Y)-\partial_4(X)\le d,
 \qquad
 \delta_3\le d+1\le c\le a.                           \tag{R7.4}
\]

For the second branch, shadow subadditivity and adjunction give

\[
 \delta_3
 \le1+\partial_4((\delta_4)_+)
 \le1+\partial_4(U_3(a-1))
 \le a.                                                \tag{R7.5}
\]

Finally `B_2(V)>=V>=125` implies `a>=16`.  For every `a>=15`,
`partial_3(a)<=a-1`: the five-top cases `15<=a<=19` are immediate, while
for canonical top at least six the leading binomial contributes at least
five more units to the integer than to its shadow and the rank-two suffix can
lose at most one unit.  Adjunction therefore gives
`a<=U_2(a-1)=A_3(a)`, completing (R7.3).

This is a genuine joint certificate.  The rank-four amplitude branch alone
is false at the actual wall `V=1435`, where `delta_4=90>U_3(62)=74`; that
wall is instead certified by two common leading terms.

## 4. Bounded actual-orbit kill test

The guarded verifier checked every adjacent wall `125 <= V <= 2000` without
increasing the previous cutoff.  Of 1,876 walls:

- 1,838 satisfied the two-prefix branch;
- 1,875 satisfied the amplitude branch;
- 1,837 satisfied both;
- all 38 walls with fewer than two common terms satisfied the amplitude
  branch; and
- the only amplitude exception was `V=1435`, certified by the prefix branch.

Thus the union had no uncovered wall in this finite range.  The 38 prefix
exceptions exhibit 23 different higher-rank prefix profiles (24 profiles
when the `V=1435` amplitude exception is included), so this diagnostic does
not support replacing the disjunction by one fixed higher-rank reset pattern.

The reproducer is

```text
python3 evidence/verify_round7_hybrid_rank3.py --start 125 --end 2000 --workers 16
```

and was run under the OpenMath 30/34 GiB memory guard.

## 5. Exact low-information no-go

The already proved low-rank recurrence and diagonal domination do not imply
the new premise.  At synthetic parameter `V=125`, take

\[
 X=27404
  =\binom{29}4+\binom{28}3+\binom{27}2+\binom{26}1,
\]

\[
 Y=27616
  =\binom{30}4+\binom{11}3+\binom{10}2+\binom{1}{1}.
\]

The low-rank recurrence gives

\[
 Z=4185,\quad Z'=4252,\quad B_2=577,\quad B'_2=582.
\]

Here `a=34`, `A_3=66`, and `C_4(a)=28`, but

\[
 \operatorname{prefix}_4(X,Y)=0,
 \quad \delta_4=212>28,
 \quad \delta_3=67>66.                                \tag{R7.6}
\]

Nevertheless both known diagonal caps hold:

\[
 Y=27616\le S_3(Z)=32160,
 \qquad
 Z'=4252\le S_2(B_2)=6681.                            \tag{R7.7}
\]

This is not an actual zero-seed orbit row.  Its exact scope is to refute any
proof of the hybrid premise or rank-three budget using only the displayed
low-rank recurrences and diagonal capacities.  It does not refute LTJ; in
fact its synthetic `B_2` jump is only `5<=a`.

## 6. Gate result

The new decisive missing claim is the actual-orbit carry dichotomy

\[
 \boxed{
 \operatorname{prefix}_4(Z_4(V),Z_4(V+1))\ge2
 \quad\text{or}\quad
 (\delta_4)_+\le U_3(a(V)-1).}                         \tag{R7.H}
\]

Proving (R7.H) for every `V>=125` would prove LTJ through the hybrid lemma.
The finite kill test does not prove it, and the synthetic no-go shows that a
proof must use higher-rank actual-orbit coupling not yet captured by the
campaign.  This candidate merits bounded symbolic continuation, but no larger
ordinary scan and no promotion.
