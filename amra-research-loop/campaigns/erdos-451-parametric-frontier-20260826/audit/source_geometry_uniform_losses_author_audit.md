# Author adversarial audit: finite source-geometry map

## Role and verdict

This is an author-side adversarial audit, not an independent audit and not
human peer review.

**Verdict: PASS for the finite kernel interface; CONDITIONAL where a proposed
source grouping must provide fixed raw constants `a,En,ED`.**

No claim about arbitrary subdivisions, all methods, or Erdős 451 is made.

## Reconstruction

1. From `x/k<=1+k^(theta-1)` and `log(1+t)<=t`, the cap
   `r<=(1/2)k^(1-theta)` gives `r log(x/k)<=1/2`. Since `theta<=1` and
   `k>=1`, the extra copy is at most one, giving the exact `3/2` bound.
2. Logging `a*k^(theta-1)/log k<=delta` is legal because `a>0,k>1`.
   The safe loss `C=-log a` need not be nonnegative; no such hidden premise
   is used.
3. Multiplication by `M` preserves inequalities because the map assumes
   `1<log k`, hence `M>0`.
4. Every derivative logarithm has an explicit positivity proof. With order
   at least two and `lambda,W>=1`, `logT1<0` implies the derivative log is
   negative in the required direction.
5. The general order coefficient is `1+En+ED+B`; `B=3/2` yields exactly
   `D=5/2+En+ED`. No block-count or `r` loss is hidden.
6. From `(3D+2)M<=cK`, the right coefficient in the old separation is at
   least `2cK`. With `q>=1,cK>=0`, multiplying by `q` is safe. The remaining
   strict inequality is a separate finite premise; no limit is asserted.
7. `a,En,ED` quantify outside the finite family. The map is uniform in its
   cardinality but cannot manufacture uniformity from per-block informal
   `O(1)` or `asymp` notation.

If `ED=ED(k)` grows, the mapped loss grows too; likewise if the safe lower
factor tends to zero. The earlier one-block examples then evade the endpoint
contradiction. Fixed raw constants are therefore indispensable, not cosmetic.
The pinned source can be instantiated only after its exact comparison is
checked; no general regrouping theorem supplying these constants is present.

## Build audit

All Lean runs used the shared OpenMath guard (`30G` high, `34G` maximum,
`4G` swap, `512` tasks). The successful fresh family build was unit
`openmath-task-20260826-212956-290745.scope`, exit `0`, wall `128.95s`, peak
RSS `7,067,288 KiB`, zero swap. Two failed family attempts were retained:

- `openmath-task-20260826-212531-287497.scope`, peak `7,002,680 KiB`, zero
  swap: coefficient normalization mismatch;
- `openmath-task-20260826-212740-289422.scope`, peak `7,001,888 KiB`, zero
  swap: an over-broad `convert` left a side goal.

These were local proof-term failures, not mathematical counterexamples. The
final replay unit and SHA are recorded in the formal README and machine
evidence.
