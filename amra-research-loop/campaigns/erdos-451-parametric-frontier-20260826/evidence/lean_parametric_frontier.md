# Lean verification of the BHP frontier

The package in `formal/` proves the theorem `erdos451_bhp_frontier` for an
arbitrary real constant `c` satisfying `0 < c < 19/120`.  It does not freeze a
sample rational constant.  Its conclusion is the full source range and the
final interval `(k,2k)`.

The proof has three parameterized layers:

1. `large_asym_of_margins` converts strict exponents `q₁>1`, `q₃>1` into the
   Konyagin error estimate.
2. `hasLargeMarginCertificate_of_parameters` takes `c<a<b` together with
   `3*q₁*b<1-theta` and `4*q₃*b<1`, constructs
   `r0=ceil(a log(k)/loglog(k))`, and then takes the least admissible `r`.
3. `exists_frontier_parameters` constructs the auxiliary parameters for every
   `c<19/120`, and `erdos451_bhp_frontier` eliminates them.

The clean guarded replay was:

```text
cd formal && bash verify_guarded.sh
OpenMath unit: openmath-task-20260826-152220-123614.scope
upstream: exit 0, wall 3.86 s, max RSS 922316 KiB, swaps 0
frontier: exit 0, wall 18.42 s, max RSS 6684560 KiB, swaps 0
```

Lean reports exactly

```text
'erdos451_bhp_frontier' depends on axioms:
  [bhp, propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`, `admit`, or new unexplained axiom.  `bhp` is the named
short-prime-interval input already present in the pinned upstream development.
The formal result fixes `theta=21/40`; the abstract conditional `PI(theta)`
theorem and the delimited method-class no-go remain independently audited
natural proofs rather than claims of Lean formalization.
