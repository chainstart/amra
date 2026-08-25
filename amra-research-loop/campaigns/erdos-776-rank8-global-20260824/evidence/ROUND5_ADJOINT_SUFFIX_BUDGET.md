# Round 5: adjoint suffix-budget ladder for LTJ

## Status and scope

This note gives a new all-parameter **conditional reduction** for the sole
surviving `M776G-01` route.  It replaces linear estimates such as
`KK_s(h)<=s h` by the exact Macaulay upper adjoint at every rank.  It does not
prove the remaining actual-orbit hypothesis and therefore does not prove LTJ,
H1--H2, the rank-eight entry, or Erdős #776.

There are three exact outcomes.

1. An actual adjacent suffix bound at any fixed rank carrying its explicit
   adaptive budget is sufficient for LTJ.
2. The rank-five and rank-six versions are false on actual zero-seed orbits:
   exact counterexamples occur at `V=1435` and `V=845`, respectively.
3. Rank-seven deferral already fails at `V=186`. A different later wall,
   `V=1471`, happens to satisfy the rank-five and rank-six conditions, showing
   why selected-wall evidence alone was misleading.

Thus every fixed-rank deferral tested from five through seven is frozen. The
only single-rank budget variants left by this round are rank three and rank
four; alternatively one needs a genuinely joint multirank carry invariant.

## 1. Residual recurrence

On the separated shortened zero-seed chart, retain the Round 3 notation

\[
 Z_{s-1}(V)=V+\operatorname{KK}_s(Z_s(V)),
 \qquad
 \delta_s=Z_s(V+1)-Z_s(V).
 \tag{R5.1}
\]

For nonnegative residuals, numerical-shadow subadditivity and monotonicity
give the exact one-sided estimate

\[
 \delta_{s-1}
 \le 1+\operatorname{KK}_s\bigl((\delta_s)_+\bigr).
 \tag{R5.2}
\]

This is strictly sharper than the earlier linear majorant
`1+s(delta_s)_+`.  It retains the rank of the actual suffix increment and
therefore includes unavoidable canonical carry compression.

## 2. Adjoint budget ladder

Write

\[
 B_2(V)=\binom a2+b,\qquad 0\le b<a,
 \tag{R5.3}
\]

and let `U_r` be the Macaulay upper adjoint, so

\[
 \operatorname{KK}_{r+1}(x)\le t
 \quad\Longleftrightarrow\quad
 x\le U_r(t).
 \tag{R5.4}
\]

Define the adaptive budgets

\[
 A_3=U_2(a-1),\qquad
 A_s=U_{s-1}(A_{s-1}-1)\quad(s\ge4)
 \tag{R5.5}
\]

as long as `A_(s-1)>0`.

**Adjoint suffix-budget lemma.**  Fix `m>=3`.  Suppose (R5.1) is valid with
nonnegative residuals from ranks `m` down to `2`, every budget in (R5.5)
through `A_m` is defined, and

\[
                 (\delta_m)_+\le A_m.                 \tag{R5.6}
\]

Then

\[
                 \delta_2\le a,                       \tag{R5.7}
\]

which is the actual leading-top jump condition.

Indeed, adjunction gives

\[
 \operatorname{KK}_s(A_s)\le A_{s-1}-1.
\]

Starting from (R5.6), (R5.2) descends to
`delta_(s-1)<=A_(s-1)` at every step.  At the final step,

\[
 \delta_2
 \le1+\operatorname{KK}_3(A_3)
 \le a.
\]

No finite extrapolation, common-prefix assumption, or desired LTJ cap is
used in this implication.

## 3. The single-rank targets

At rank three the sufficient condition is

\[
 (\delta_3)_+\le U_2(a-1).                            \tag{R5.8}
\]

At rank four it is

\[
 (\delta_4)_+\le U_3\!\left(U_2(a-1)-1\right).        \tag{R5.9}
\]

Either condition proves LTJ by the lemma. Applying further upper adjoints
defines honest rank-five, rank-six, and rank-seven proposals, but the next
section refutes all three on actual adjacent orbits.

These are not restatements of LTJ.  They permit a much larger upstream
integer increment and then charge its *canonical shadow* rather than its raw
magnitude.  They are also not consequences of Round 4 diagonal-gap size;
they impose new information on the actual adjacent suffix.

## 4. Actual counterexamples to ranks five through seven

An exhaustive guarded falsifier on `125<=V<=2000` found the following least
failures in that finite range. Each row was then reconstructed independently
by the lightweight verifier.

| proposed rank | actual wall | `a` | increment | budget | LTJ margin |
|---:|---:|---:|---:|---:|---:|
| 5 | `1435 -> 1436` | 63 | `delta_5=622` | `A_5=484` | 61 |
| 6 | `845 -> 846` | 52 | `delta_6=250` | `A_6=211` | 51 |
| 7 | `186 -> 187` | 36 | `delta_7=14` | `A_7=9` | 35 |

All three walls still satisfy LTJ itself. For example, at `V=1435`,

\[
 (\delta_2,\delta_3,\delta_4,\delta_5,\delta_6,\delta_7)
 =(2,5,90,622,3571,12853),                             \tag{R5.10}
\]

where

\[
 (A_3,A_4,A_5,A_6,A_7)=(186,360,484,469,331).         \tag{R5.11}
\]

Thus rank four still certifies this particular wall, but rank five and every
higher displayed budget fail badly. At the separate `1471 -> 1472` wall,
rank five and rank six happen to pass while rank seven fails. Consequently no
fixed-rank target may be inferred from a few prominent carry walls.

## 5. Fail-closed next action

The rank-five, rank-six, and rank-seven single-coordinate subroutes are
refuted. A legitimate next round must prove or refute the rank-four target
(R5.9), the rank-three target (R5.8), or a materially new joint multirank
invariant that uses compensation between several suffix increments. A larger
LTJ scan does not change the gate. The verifier

```text
python3 evidence/verify_round5_adjoint_suffix_budget.py
```

checks the algebraic inequalities on exact integer cases and reconstructs the
three counterexample walls above. The exhaustive scan summary is retained in
`round5_adjoint_budget_falsifier_125_2000.json`. Finite cases are guards and
kill tests only; the budget lemma itself is proved symbolically above.
