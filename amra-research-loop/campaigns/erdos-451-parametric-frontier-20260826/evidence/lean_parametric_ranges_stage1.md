# Variable-theta range-builder stage-1 checkpoint

## Compiled result

For every real `theta` with `0 < theta < 1`, and every abstract
`PrimeIntervalInput theta`, `formal/ParametricRanges.lean` proves the first
three fields of `ParametricRangePackage theta c`:

1. `ParametricSmall.case_small` for
   `2k < n <= (1/2) k^(2-theta)`;
2. `ParametricMed.case_medium` for
   `(1/2) k^(2-theta) < n <= k^2/log^2(k)`;
3. `ParametricML.case_mediumlarge` for
   `k^2/log^2(k) < n <= (1/2) k^(2+theta)`.

Each conclusion is `SourceIntervalConclusion theta k n`: there is a prime
`p` with `k < p < k + 3 k^theta` dividing `Pprod k n`.  The three final
theorems depend only on `[propext, Classical.choice, Quot.sound]`; in
particular they do not depend on the fixed `bhp` axiom.

## Dependency audit by source range

| Class | Upstream lemmas / constructions | Result |
|---|---|---|
| Directly parameterized | `konyagin_application`, `poly_log_lt`, `poly_log_lt_eq`, `card_int_abs_sub_lt_le`, `primeCard_le_add`, `exists_prime_of_primeCard_pos`, `Pprod` divisibility lemmas | Already expose the needed exponent, or are exponent-free; reused without changing their statements. |
| Only numerical constants were fixed | medium-large `lamML`, `lamUB`, `gML` and the `r=2` count; small-window excess/count argument; medium `medWindow`, `medFiber`, `medJ`, fiber/card/RHS estimates | Rebuilt with variable `theta`; every formerly numerical inequality follows from `0<theta<1`. |
| Genuinely global-theta dependent | `bhp`; fixed `badSet`/finish bridge; `E1exp`, `lamLarge`, `large_card_raw`, `large_asym`, `large_r0_bounds`, `large_r0_P`, `large_r_data` | `bhp` is replaced by `PrimeIntervalInput theta`, and the bad-set bridge was already parameterized in `ParametricInterface`.  The large-range chain remains the sole builder blocker. |

## Exact large-range blocker

The upstream lemma `lamLarge_lt` discards `E1 >= 0` and obtains the coarse
uniform estimate `lambda < k^((2-theta)/r)`, hence at `r=3` the additive term
has exponent `(2-theta)/3`.  Comparing it with `k^theta/log(k)` requires
`theta>1/2`, so this cannot establish the intended full interval
`2/5<theta<3/5`.

The required replay must retain

```text
E1(theta,r) = (1-theta)(2r-1)/(3r-2),
a(theta,r)  = (2-theta-E1(theta,r))/r
            = ((4-theta)r+theta-3)/(r(3r-2)).
```

For `r>=3`, `0<theta<1`, direct algebra gives

```text
a(theta,r) <= a(theta,3) = (9-2theta)/21.
```

Indeed the difference after clearing the positive denominator is

```text
(r-3) * (r(27-6theta)+7theta-21) >= 0.
```

Moreover `(9-2theta)/21 < theta` is equivalent to `theta>9/23`, and is
therefore strict throughout `theta>2/5`.  Thus the asymptotic additive term
can be handed to `poly_log_lt` as

```text
2 k^((9-2theta)/21) log(k) = o(k^theta/log(k)).
```

This algebra is a proved natural handoff, not part of the final Lean
checkpoint: three guarded attempts to formalize its first rational identity
did not close, and the experimental namespace was removed rather than leaving
`sorryAx`.  The substantive remaining Lean work is to parameterize
`E1exp`/`lamLarge`, retain this exact exponent in the minimality estimate, and
then replay `large_card_raw` plus the `r0`/least-order construction.  No finite
experiment is used as a theorem.

## Reproduction and safety

Run `cd formal && bash verify_guarded.sh`.  That script performs the complete
upstream/frontier/interface/ranges replay inside the shared OpenMath memory
slice, checks the exact axiom lists, rejects `sorryAx`, and records SHA-256
hashes.  Failed guarded attempt metadata is retained in
`formal/logs/ranges-attempts-20260826.md`; the authoritative successful output
is `formal/logs/ranges-build.log`.
