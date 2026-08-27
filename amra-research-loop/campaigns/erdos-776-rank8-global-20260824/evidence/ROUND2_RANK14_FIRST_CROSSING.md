# Round 2: rank-14 first-crossing normal form and its obstruction

This round attacks the conditional high-rank lemma without enlarging the
finite parameter scan.  It independently reconstructs an exact all-parameter
normal form already implicit in `FIRST_ATTACK.md`, Section 8, and produces an
all-parameter synthetic obstruction to the proposed local proof mechanism.
It does **not** prove or refute the actual zero-seed lemma.

## 1. A second-complement identity at ranks 18, 17, and 16

Let

\[
 E_{V-26}=0,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q),
 \qquad N=V-25.                                        \tag{1}
\]

The tail-complement calculation used for the old rank-18 gate gives, on the
chart before its first failed capacity,

\[
 D_{k+13}-P_{k+13}=E_k-{N\choose k},qquad k=5,4,3,    \tag{2}
\]

where

\[
 P_q={V-12\choose q}+{V-13\choose q-1}.               \tag{3}
\]

Thus the observed rank-14 residual is the rank-three terminal excess

\[
 W_{14}=D_{16}-P_{16}=E_3-{N\choose3}.                 \tag{4}
\]

Equation (2) is an identity conditional only on the explicit capacity chart;
it is not inferred from selected values.  The round-2 verifier reconstructs
both zero-seed orbits independently at three selected parameters as a guard.

## 2. Exact rank-two normal form

Put

\[
 J_4={N-1\choose4}+{N-2\choose3},qquad
 B_2=E_4-J_4.                                         \tag{5}
\]

Pascal gives

\[
 {N\choose4}-J_4={N-2\choose2}.                       \tag{6}
\]

Whenever

\[
 0\le B_2\le {N-2\choose2},                           \tag{7}
\]

the two terms in `J_4` and the 2-canonical word of `B_2` form the required
separated chart (with equality in (7) interpreted by the merged Pascal
term).  One exact shadow step gives

\[
\begin{aligned}
 E_3
 &=V+{N-1\choose3}+{N-2\choose2}
   +\operatorname{KK}_2(B_2),\\
 {N\choose3}
 &={N-1\choose3}+{N-2\choose2}+{N-2\choose1}.
\end{aligned}
\]

Since `N-2=V-27`, (4) becomes the all-parameter identity

\[
 \boxed{W_{14}(V)=27+\operatorname{KK}_2(B_2(V)).}     \tag{8}
\]

This explains the small, slowly changing rank-14 residual without assuming
one stable high-rank canonical word.

## 3. Exact form of the Lipschitz clause

Under (7) at adjacent parameters,

\[
 W_{14}(V+1)-W_{14}(V)\le1
\]

is equivalent to

\[
 \operatorname{KK}_2(B_2(V+1))
 \le \operatorname{KK}_2(B_2(V))+1.                   \tag{9}
\]

Rank-two Galois adjunction makes (9) exactly

\[
 \boxed{
 B_2(V+1)
 \le {\operatorname{KK}_2(B_2(V))+1\choose2}.}         \tag{10}
\]

A convenient stronger sufficient inequality is

\[
 B_2(V+1)-B_2(V)\le\operatorname{KK}_2(B_2(V)),        \tag{11}
\]

because `B_2(V)<=binom(KK_2(B_2(V)),2)`.

Equations (8)--(10), not a larger scan, are the round's exact reduction.  The
identity `W=27+KK_2(y)` and a sufficient adjacent lemma were already recorded
in the read-only
`data/research_open/q1_three_hour_campaign_2026-07-31/erdos776/FIRST_ATTACK.md`.
This campaign claims independent reconstruction and sharper scope, not
novelty for that identity.

Indeed, on the next separated chart, if

\[
 Z_3=E_5-{N-1\choose5}-{N-2\choose4},
\]

then

\[
 B_2=V+\operatorname{KK}_3(Z_3).                       \tag{11a}
\]

Writing `Delta_+=max(0,Z_3(V+1)-Z_3(V))` and
`k=KK_2(B_2(V))`, the one-sided carry bound proves the inherited sufficient
condition

\[
 1+3\Delta_+\le k\quad\Longrightarrow\quad
 W_{14}(V+1)-W_{14}(V)\le1.                            \tag{11b}
\]

Thus the actual upstream gap is an all-parameter adjacent bound on `Z_3`,
not further rank-two algebra.

## 4. Why the natural capacity proof does not simplify the old gate

The upper half of (7) is `E_4<=binom(N,4)`.  By (2), this is
`D_17<=P_17`.  But the comparison with `P` cannot recover after failure:

\[
 D_{18}\ge P_{18}
 \Longrightarrow
 D_{17}=V+\operatorname{KK}_{18}(D_{18})
 \ge V+P_{17}>P_{17}.                                 \tag{12}
\]

Hence

\[
 E_4\le{N\choose4}
 \Longrightarrow D_{17}\le P_{17}
 \Longrightarrow D_{18}<P_{18}.                       \tag{13}
\]

The last statement is the already known zero-slack closing gate.  Therefore
proving the rank-14 separator by first proving the full capacity (7) is
noncircular logically, but it is not a weaker route: it silently proves an
earlier closing interface.

## 5. Full-parameter obstruction: local separator does not pay Lipschitz

Even the much stronger local seed bounds `0<=W_14(V)<=V` at adjacent
parameters do not imply the Lipschitz clause.  For every integer `V>=125`,
define the synthetic local pair

\[
 B_2(V)={V-30\choose2},\qquad
 \widetilde B_2(V+1)={V-28\choose2}.                  \tag{14}
\]

Both obey their exact capacities:

\[
 0\le B_2(V)\le{V-27\choose2},\qquad
 0\le\widetilde B_2(V+1)\le{V-26\choose2}.            \tag{15}
\]

Yet (8) gives

\[
 W_{14}(V)=V-3,qquad
 \widetilde W_{14}(V+1)=V-1,                          \tag{16}
\]

so the jump is `2`.  This is a genuine all-parameter counterfamily to the
inference “separation/capacity alone implies one-Lipschitz”.  Its exact scope
is local: the synthetic pair is not asserted to be generated by the common
zero-seed orbit.  It proves that any successful H2 proof must retain an
upstream adjacent coupling, not just the two endpoint capacities.

## 6. Consequence for H1 and the remaining actual theorem

If (7) holds, (8) gives `0<=W_14<=V`.  Starting from this bound and using
`KK_r(x)<=rx`, the exact coefficients

\[
 b_{14}=1,qquad b_{r-1}=1+rb_r
\]

give `W_r<=b_r V`.  At `V=125`, all inequalities

\[
 b_rV<{V-13\choose r}\qquad(7\le r\le14)              \tag{17}
\]

hold, and their binomial-to-linear ratios increase with `V`.  Thus the one
rank-four capacity (7) implies the entire H1 separator chain.  However,
(13) shows why this route does not simplify the prior closure gate.

After round 2, the unresolved actual-orbit statement is the adjacent rank-two
inequality (10), together with a way to reach its chart that is genuinely
weaker than `D_18<P_18`.  No finite table proves either condition.

## 7. Pivot to the independent multiscale survivor

The inference "local capacity alone pays H2" has therefore been frozen.  The
full M01 survivor is not refuted because an actual upstream `Z_3` coupling
could still prove (11b).  The distinct M02 survivor is also retained: the
global rank-six carry-height construction.  A precise next
structural target, stronger than a list of checked parameters, is:

> Let `T(V)` be the top upper index in the nonempty six-canonical word of
> `W_6(V)`.  After the exact base `40<=V<=125`, every new record wall
> `T=a+1>=20` can occur only at a parameter at least twice the first parameter
> of the preceding record wall `T=a`.

Such dyadic record spacing would imply
`T(V)<=ceil(log_2 V)+13`, while using information genuinely different from
the rank-18/17 capacity chart.  It remains unproved; the next legitimate
work is an all-parameter injection from each new record carry to a disjoint
doubling interval.  Enlarging the finite scan is not evidence for it.
