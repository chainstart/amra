# Audit and extraction of the abstract theta interface

## Upstream dependency audit

The pinned upstream source is not parameterized globally:

- line 43 defines `theta : ℝ := 21/40`;
- lines 54--55 state `axiom bhp` only with that global `theta`;
- `badSet` at line 118 and `case_small`, `case_medium`,
  `case_mediumlarge`, and `case_large` at lines 3837, 4268, 4041, and 4623
  all mention the global constant in their theorem types;
- the range-specific parameters `lamML` and `lamLarge` are likewise fixed.

The important reusable exception is `konyagin_application` at line 3567: its
exponent is an explicit argument and its hypotheses are `0<theta<1`.
Consequently the existing four range theorems cannot be instantiated at a
variable exponent by rewriting.  A full formalization of the natural theorem
requires a replay/refactor of Sections 2--6, not a new prime axiom.

## Kernel-checked extraction

`formal/ParametricInterface.lean` proves without `bhp`:

- `PrimeIntervalInput ϑ`, an abstract proposition rather than an axiom;
- `dvd_from_far_at`, `exists_far_prime_at`, and `konyagin_finish_at`, the
  general bad-point-count-to-prime-divisor bridge;
- `ParametricRangePackage ϑ c`, the exact four source-paper ranges;
- `source_interval_of_rangePackage` and `main_of_rangePackage`, including the
  eventual shrink from `(k,k+3k^ϑ)` to `(k,2k)` for `ϑ<1`;
- `exists_frontier_parameters_at`, which constructs all strict-margin
  auxiliaries whenever `2/5<ϑ<3/5` and `0<c<(1-ϑ)/3`;
- `parametric_frontier_interface`, whose sole remaining mathematical input is
  `ParametricRangeBuilder ϑ c := PrimeIntervalInput ϑ →
  ParametricRangePackage ϑ c`.

The old fixed results instantiate the package, and
`erdos451_bhp_frontier_via_interface` recovers the full theorem for every real
`0<c<19/120`.

This is an explicit blocker, not an added axiom: constructing
`ParametricRangeBuilder` from `PI(ϑ)` is exactly the unformalized general-
exponent content.  In particular, the existing fixed proof's coarse additive
large-range envelope uses the numerical inequality
`(2-theta)/3 < theta`; the natural proof over the whole interval
`2/5<theta<3/5` instead needs the sharper minimal-order exponent
`(9-2theta)/21 < theta`.  That sharper estimate must be retained in a general
Lean replay rather than copying the fixed coarse bound.

## Guarded replay

```text
command: cd formal && bash verify_guarded.sh
unit: openmath-task-20260826-155406-130263.scope
upstream: wall 3.46 s, max RSS 920172 KiB, swap 0
fixed frontier: wall 19.14 s, max RSS 6656956 KiB, swap 0
parametric interface: wall 17.44 s, max RSS 6624192 KiB, swap 0
```

Axiom audit:

```text
parametric_frontier_interface:
  [propext, Classical.choice, Quot.sound]
erdos451_bhp_frontier_via_interface:
  [bhp, propext, Classical.choice, Quot.sound]
```

There is no `sorryAx`, `admit`, or new unexplained axiom.  The interface source
SHA-256 is
`1e26f0f1d2665e20ad2b5c7c6b7ebe93894e5ec712967104d74630376d451efe`.
