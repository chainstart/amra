# Cross-audit of the adaptive parameter core

## Scope and verdict

This is a same-model, non-author cross-audit of the current uncommitted
adaptive additions in `formal/ParametricRanges.lean` and their claims in
`formal/README.md`, `evidence/lean_parametric_ranges.{md,json}`,
`decisive_lemma.json`, and `decision.json`.  I reconstructed the algebra
from the declarations rather than inheriting an earlier audit or Lean
verdict.  This is not a human review and not an independently implemented
formalization.

**Verdict: PASS.**  The definitions, feasibility equivalence, and every
conjunct of `adaptive_log_selection_budget` match the adaptive natural-proof
parameter algebra.  The evidence consistently calls this a kernel-checked
logarithmic parameter core, not a completed adaptive
`ParametricRangeBuilder` or a new final divisor theorem.

## 1. Definitions

Set `K=log k`, `M=loglog k`, and `logN=log(n r!)`.  The Lean definitions
reconstruct exactly as follows:

```text
adaptiveLogU = (r+1)K - Q(2r-1)M       = log U_r,
adaptiveLogV = (r+theta)K + Q(r-1)M    = log V_r,
adaptiveLogZ = max(logN,adaptiveLogV)  = log max(nr!,V_r),
adaptiveLogT1 = (logZ-(r+1)K)/(2r-1),
adaptiveLogT2 = ((r+theta)K-logZ)/(r-1),
adaptiveLogLambda = (logZ-logN)/r.
```

Thus `adaptiveLogT1` and `adaptiveLogT2` are the logarithms of the first
two Konyagin terms, and `adaptiveLogLambda` is the logarithm of the positive
`r`-th-root scale that remains to be constructed in the final analytic
wrapper.  There is no hidden balanced-scale condition in
`large_card_raw_adaptive_at`: its Lean interface is the pinned Konyagin
bound for arbitrary real `lambda>=1`, natural `r>=2`, and the stated order
admissibility hypothesis.

## 2. Exact feasibility

`AdaptiveFrontierParameters theta c` is exactly

```text
exists Q,a, 1<Q, 0<a, c<a, 3Qa<1-theta.
```

Under the theorem's explicit hypothesis `c>0`, the forward implication gives
`theta<1` and `3c<1-theta`, hence `c<(1-theta)/3`.  Conversely, putting
`f=(1-theta)/3`, choosing `a=(c+f)/2`, and then choosing
`1<Q<f/a` supplies the predicate.  Therefore

```text
AdaptiveFrontierParameters theta c
  iff theta<1 and c<(1-theta)/3
```

is exact under `c>0`.

The predicate itself deliberately does not contain `0<theta`; accordingly
the equivalence theorem is slightly more general.  The advertised natural
window adds `0<theta` in `adaptive_parameter_certificate_wide`.  Its
`_hTheta0` argument is unused because positivity of theta is needed by the
eventual analytic application, not by this strict-margin feasibility fact.
The README and JSON distinguish these two scopes correctly.

## 3. `adaptive_log_selection_budget`

All six conclusions follow with the stated signs and denominators.

1. From `rM<=aK`, `Q,M>=0`, and `3Qa<1-theta`,

   ```text
   Q(3r-2)M <= 3QrM <= 3QaK < (1-theta)K,
   ```

   which is precisely `adaptiveLogV<=adaptiveLogU`.

2. `adaptiveLogV<=adaptiveLogZ` is the right branch of the maximum.

3. `logN<=adaptiveLogU` and `adaptiveLogV<=adaptiveLogU` give
   `adaptiveLogZ<=adaptiveLogU` by the maximum sandwich.

4. The upper sandwich gives

   ```text
   logZ-(r+1)K <= -Q(2r-1)M.
   ```

   Since `r>=2`, division by `2r-1>0` proves
   `adaptiveLogT1<=-QM`.

5. The lower sandwich gives

   ```text
   (r+theta)K-logZ <= -Q(r-1)M.
   ```

   Division by `r-1>0` proves `adaptiveLogT2<=-QM`.

6. The preceding-order lower bound

   ```text
   rK-Q(2r-3)M <= logN
   ```

   implies

   ```text
   adaptiveLogV-logN
     <= theta K+Q(3r-4)M
     <= theta K+3QrM.
   ```

   The other branch `logZ=logN` has zero difference.  Dividing by `r>0`
   yields exactly

   ```text
   adaptiveLogLambda <= (theta/r)K+3QM.
   ```

The non-strict lower hypothesis is legitimately weaker than what the
natural least-order argument supplies: failure at order `r-1` gives a
strict bound for `log(n(r-1)!)`, and passing to `log(nr!)` only adds
`log r>0`.  No order-one Konyagin invocation is hidden when the selected
order is `r=2`.

## 4. Formal/evidence boundary

The current guarded replay reports exit status zero for
`ParametricRanges`, peak RSS `6,997,116 KiB`, and no swap.  The recorded
source hash

```text
72dc11234659507a96650729a3c3026a00f170f66cb6259d8eb56678524e91a4
```

matches the audited `formal/ParametricRanges.lean`; the replay log prints
only `[propext, Classical.choice, Quot.sound]` for the adaptive declarations
and no `sorryAx`.

More importantly, the prose and structured evidence do not overstate what
was checked:

- the complete kernel-checked builder and final conditional divisor theorem
  remain the balanced `9/23<theta<1` results;
- the new full-window formal result is strict-margin feasibility plus the
  abstract logarithmic `U/V/max` sandwich and arbitrary-lambda raw Konyagin
  interface;
- the actual positive-real max scale, existence/minimality of the stopping
  order with factorial/log identities, and uniform third/additive-term
  estimates are still listed as missing;
- `decisive_lemma.json` and `decision.json` leave the earlier promotion basis
  unchanged and do not claim that a `0<theta<1` adaptive
  `ParametricRangeBuilder` has compiled.

Consequently no mandatory mathematical or evidence-scope correction was
found.  The adaptive formal core strengthens the checked parameter algebra,
but by itself neither widens the compiled final theorem nor changes the BHP
constant `19/120`.
