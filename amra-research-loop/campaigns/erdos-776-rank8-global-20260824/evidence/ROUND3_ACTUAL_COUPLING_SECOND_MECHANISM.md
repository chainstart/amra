# Round 3 actual coupling, second mechanism

## Scope and independence

This route attacks only the actual zero-seed `M776G-01` survivor. It was
developed from the recurrence and the campaign's round-2 definitions. The
prohibited `erdos_404/ROUND3_ACTUAL_B2_COUPLING.md` was not read.

There are two exact outcomes:

1. the previously proposed actual-tail condition
   `B_2(V+1)-B_2(V)<=3` is refuted by the real orbit at
   `V=1471 -> 1472`;
2. a materially weaker, all-parameter leading-top jump criterion is proved.
   It survives the counterexample and supplies a new possible mechanism for
   H2, but its actual-orbit hypothesis remains open.

Thus H2 and M776G-01 remain unproved. This note does not enlarge a finite scan
or infer an unbounded statement from computation.

## Definitions

Put `N=V-25` and use the second zero-seed orbit

\[
E_{V-26}=0,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q).
\]

On the separated low-rank chart, define

\[
\begin{aligned}
 Z_s(V)&=E_{s+2}(V)-{N-1\choose s+2}-{N-2\choose s+1},\\
 B_2(V)&=Z_2(V).
\end{aligned}
\]

Then the true generated-tail recurrence is

\[
Z_{s-1}(V)=V+\operatorname{KK}_s(Z_s(V)),             \tag{1}
\]

and in particular

\[
B_2(V)=V+\operatorname{KK}_3(Z_3(V)),\qquad
W_{14}(V)=27+\operatorname{KK}_2(B_2(V)).             \tag{2}
\]

Equation (2) is used only where the exact displayed words below certify the
separator directly.

## Exact actual-orbit falsifier to the three-unit target

The compressed zero-seed recurrence gives the following exact integer rows.

| quantity | `V=1471` | `V=1472` |
|---|---:|---:|
| `E_4` | 181407790321 | 181910654663 |
| rank-4 baseline | 181407788289 | 181910652625 |
| `B_2` | 2032 | 2038 |
| `E_5` | 52317805836268 | 52499213624571 |
| rank-5 baseline | 52317805830290 | 52499213618579 |
| `Z_3` | 5978 | 5992 |
| `E_6` | 12564932898197124 | 12617250704027442 |
| rank-6 baseline | 12564932898165648 | 12617250703995938 |
| `Z_4` | 31476 | 31504 |

The relevant canonical words are

\[
\begin{aligned}
B_2(1471)&={64\choose2}+{16\choose1},\\
B_2(1472)&={64\choose2}+{22\choose1},                \tag{3}\\
Z_3(1471)&={33\choose3}+{32\choose2}+{26\choose1},\\
Z_3(1472)&={34\choose3}+{4\choose2}+{2\choose1}.    \tag{4}
\end{aligned}
\]

Also

\[
\operatorname{KK}_3(Z_3(1471))=561,qquad
\operatorname{KK}_3(Z_3(1472))=566,
\]

so (2) independently reconstructs `2032=1471+561` and
`2038=1472+566`. Therefore

\[
B_2(1472)-B_2(1471)=6>3.                              \tag{5}
\]

This exact real-orbit row kills the universal three-unit submechanism; it is
not a synthetic capacity pair. It does **not** refute H2. Indeed, (3) gives

\[
\operatorname{KK}_2(B_2(1471))
=\operatorname{KK}_2(B_2(1472))=65,                  \tag{6}
\]

so the corresponding `W_14` jump is zero. The reason is structural: a
six-unit move inside one positive rank-2 tail costs no new shadow unit.

## New mechanism: leading-top positive-jump budget

The failure of a constant jump bound suggests charging an actual positive
jump to the current leading rank-2 index rather than to a fixed constant.

### Lemma (all parameters)

Let

\[
x={a\choose2}+b,qquad 0\le b<a,quad a\ge2,
\]

and let `y` be a nonnegative integer. If

\[
y-x\le a,                                             \tag{7}
\]

then

\[
\operatorname{KK}_2(y)-\operatorname{KK}_2(x)\le1.   \tag{8}
\]

### Proof

If `y<=x`, (8) follows from monotonicity. Suppose `y>x`.

If `b=0`, then `KK_2(x)=a` and

\[
y\le {a\choose2}+a={a+1\choose2},
\]

so `KK_2(y)<=a+1`.

If `b>0`, then `KK_2(x)=a+1`. Since `b<=a-1`, (7) gives

\[
y\le {a\choose2}+2a-1<{a+2\choose2}.
\]

Thus `KK_2(y)<=a+2`. This proves (8) in both cases. QED.

For the actual tail, write `a(V)` for the leading upper index of the
2-canonical word of `B_2(V)`. The new sufficient mechanism is

\[
\boxed{\bigl(B_2(V+1)-B_2(V)\bigr)_+\le a(V).}        \tag{LTJ}
\]

Because `a(V)` is of order `sqrt(B_2(V))`, LTJ is a sub-square-root positive
jump target. It is not the Galois-equivalent H2 target. When the tail
`b>0`, exact H2 permits jumps as large as
`2a+1-b`, whereas LTJ uses the uniform smaller budget `a`. Thus LTJ has
genuine slack and can in principle be established without solving the exact
rank-2 endpoint inequality.

The real counterexample (5) passes LTJ with wide margin: `6<=64`.

## Actual diagonal-loss formulation and remaining gap

For adjacent actual tails put

\[
\delta_s=Z_s(V+1)-Z_s(V)
\]

and define the exact one-sided carry loss

\[
L_s=s\max(0,\delta_s)
-\left(\operatorname{KK}_s(Z_s(V+1))
       -\operatorname{KK}_s(Z_s(V))\right)\ge0.       \tag{9}
\]

Whenever `delta_s>=0`, (1) gives the exact diagonal identity

\[
\delta_{s-1}=1+s\delta_s-L_s.                         \tag{10}
\]

For a consecutive positive chain, (10) telescopes with factorial weights;
for example

\[
\delta_2=4+12\delta_4-3L_4-L_3.                      \tag{11}
\]

If some upstream `delta_s` is negative, monotonicity instead immediately
gives `delta_(s-1)<=1`. This identifies the genuinely new information an
actual proof would need: either an upstream nonpositive reset, or enough
weighted carry loss in (10) to prove LTJ. Arbitrary endpoint capacities do
not control these losses.

At `1471 -> 1472`, the tail jumps are

\[
\delta_4=28,qquad\delta_3=14,qquad\delta_2=6.
\]

The large upstream jump is compressed by real canonical losses and remains
far inside the LTJ budget. However, this campaign has no all-`V` lower bound
on the weighted losses in (10), and no proof of LTJ. Merely defining `L_s`
does not close the mechanism.

## Classification

- `B_2(V+1)-B_2(V)<=3` on the actual orbit: **refuted**, exact at
  `V=1471`.
- Leading-top lemma (7)--(8): **proved**, all parameters.
- LTJ on the actual zero-seed orbit: **conditional/open**.
- Telescoping loss identity (9)--(11): **proved as an identity**, but the
  needed all-parameter lower bound on accumulated loss is open.
- H2, H1, the all-`V` rank-eight entry, and the original Erdős 776 problem:
  **unchanged**.

The noncosmetic next step, if this survivor is continued, is an actual-orbit
invariant that pays the weighted losses in (10). Another Galois restatement
or a larger scan is not progress.
