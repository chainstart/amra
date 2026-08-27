# Round 3 P776-A: actual-orbit upstream coupling

This round uses only the true zero-seed orbit and the recurrence

\[
 B_2(V)=V+\operatorname{KK}_3(Z_3(V)).                 \tag{1}
\]

It does not use arbitrary endpoint pairs, does not enlarge a finite cutoff,
and does not use the other multiscale survivor.  The outcome is a sharp exact
reduction and a refutation of the stronger two-Lipschitz conjecture;
`Delta B_2<=3` remains conditional.

## 1. Actual residual chain

Put `N=V-25` and let

\[
 E_{V-26}=0,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q).
\]

On the separated ranks five and four define

\[
\begin{aligned}
 Z_3(V)&=E_5-{N-1\choose5}-{N-2\choose4},\\
 B_2(V)&=E_4-{N-1\choose4}-{N-2\choose3}.
\end{aligned}                                           \tag{2}
\]

One canonical shadow step gives the actual identity (1), and the rank-14
normal form is

\[
 W_{14}(V)=27+\operatorname{KK}_2(B_2(V)).              \tag{3}
\]

No synthetic state is used in (1)--(3).

## 2. Exact target at rank three

The proposed theorem

\[
 \Delta B_2:=B_2(V+1)-B_2(V)\le3                       \tag{4}
\]

is exactly

\[
 \operatorname{KK}_3(Z_3(V+1))
 -\operatorname{KK}_3(Z_3(V))\le2.                    \tag{5}
\]

Let `U_2` be the rank-two Macaulay upper adjoint.  Galois adjunction turns
(5) into the single actual-orbit capacity

\[
 \boxed{
 Z_3(V+1)
 \le U_2(\operatorname{KK}_3(Z_3(V))+2).}               \tag{6}
\]

Thus (6), with the true adjacent `Z_3` states, is a strict sufficient route
to H2.  It imports upstream coupling and is not an endpoint-capacity
restatement.

Equivalently, with the aligned diagonal loss

\[
 G_5(V)=S_2(B_2(V))-Z_3(V+1),
\]

condition (6) is

\[
 G_5(V)\ge
 S_2(B_2(V))-U_2(B_2(V)-V+2).                          \tag{7}
\]

Equation (7) identifies the exact information missing from scalar
subadditivity: a lower bound on the actual shadow lost across the adjacent
diagonal.

## 3. A proved all-parameter conditional implication

Write

\[
 \Delta_+Z_3=\max(0,Z_3(V+1)-Z_3(V)),\qquad
 k(V)=\operatorname{KK}_2(B_2(V)).
\]

The one-sided carry inequality gives

\[
 B_2(V+1)-B_2(V)
 \le1+3\Delta_+Z_3.                                   \tag{8}
\]

Since `B_2(V)<=binom(k(V),2)`, the all-parameter implication

\[
 \boxed{1+3\Delta_+Z_3\le k(V)}
 \quad\Longrightarrow\quad
 \Delta W_{14}\le1                                   \tag{9}
\]

follows by

\[
 B_2(V+1)\le {k(V)\choose2}+k(V)={k(V)+1\choose2}.
\]

This is the actual-orbit triangular-slack lemma already present in the
read-only `FIRST_ATTACK.md`, Section 8; round 3 rederives and scopes it rather
than claiming novelty.  Since `B_2>=V`, one has

\[
 k(V)\ge\left\lceil\frac{1+\sqrt{1+8V}}2\right\rceil.
\]

Consequently any all-parameter `o(sqrt(V))` upper bound on the positive
adjacent jump of the true `Z_3` orbit would prove H2 for all sufficiently
large `V`, after a finite base.  No such bound is proved here.

## 4. Sharp actual obstruction to a stronger theorem

The true zero-seed orbit at `V=300 -> 301` has

\[
\begin{array}{c|ccc}
V&Z_3&B_2&W_{14}\\ \hline
300&4494&765&67\\
301&4496&768&67.
\end{array}
\]

Hence

\[
 \Delta Z_3=2,qquad \Delta B_2=3,qquad\Delta W_{14}=0. \tag{10}
\]

This one exact actual parameter refutes the stronger universal claim
`Delta B_2<=2`.  It also attains equality in (4) and (6), so a proof of (4)
cannot demand a spare unit at every carry wall.

At this wall the sufficient inequality (9) is comfortably valid:
`1+3*2=7<=40=k(300)`.  Thus the obstruction does not refute the proposed
three-Lipschitz theorem.

## 5. Status

- **Proved:** identities (1)--(3); equivalences (4)--(7); conditional
  implication (9); exact actual counterexample (10) to `Delta B_2<=2`.
- **Conditional/open:** (4), equivalently (6) or (7), for every `V>=125`.
- **Not claimed:** any inference from the existing bounded data, any
  all-parameter bound on `Delta Z_3`, or closure of the rank-eight entry.

The legitimate next step on M01 is now unique: prove an all-parameter lower
bound (7) for the **actual** diagonal loss, or prove a sub-square-root bound
on the positive adjacent jump of the actual `Z_3` orbit.  Endpoint capacity
and synthetic pairs contain insufficient information.
