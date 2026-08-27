# Independent cross-audit: source geometry to uniform losses

## Verdict

**PASS, with the source and quantifier scope stated below.  No mandatory
correction found.**

This is an independent read-only reconstruction by the upper-bound agent.  It
does not rely on `audit/source_geometry_uniform_losses_author_audit.md`, does
not modify the author evidence or Lean sources, and does not claim an
independent Lean replay.  The audited result is a finite implication from the
explicit `SourceGeometrySubdivisionAt` predicate to the already delimited
location-blind certificate class.  It is not a theorem that arbitrary shifted
or regrouped source decompositions satisfy that predicate.

## 1. Exact interface

`SourceGeometrySubdivisionAt theta c a En ED k q H s block` assumes:

1. `s` is a nonempty `Finset`, `H>0`, every block weight is positive, and the
   weights sum exactly to `H`;
2. every order is at least two, every source position lies in
   `[k,k+k^theta]`, and
   `r <= (1/2) k^(1-theta)`;
3. the same displayed parameters `a>0`, `En>=0`, and `ED>=0` give, for every
   block, the safe-tail lower bound, endpoint-scale lower bound, and
   derivative-scale lower comparison;
4. `factorialScale`, `lambda`, and `W` are at least one; and
5. the positive first-two-term ledger, summed with the block weights, is at
   most `H exp(-loglog(k)-q)`.

Under `0<=theta<=1`, `k>1`, and `log(k)>1`,
`sourceGeometrySubdivision_to_locationBlind` concludes exactly

```text
LocationBlindTermwiseSubdivisionAt
  theta c log(k) loglog(k) (-log a) (5/2+En+ED) q H s ...
```

The source predicate contains no assumed
`c log(k)-(5/2+En+ED)loglog(k) <= r loglog(k)` inequality.  That conditional
order bound is proved in the map.

## 2. Window and safe-tail losses

Put `K=log(k)` and `M=log(K)`.  From
`x in [k,k+k^theta]`, `0<=theta<=1`, and
`r <= (1/2)k^(1-theta)`, the elementary `log(1+t)<=t` argument gives

```text
r log(x/k) <= 1/2,
(r+1)(log x-K) <= 3/2.
```

The second constant is the sum of the first `1/2` and the valid bound
`log(x/k)<=1`, since `k^theta<=k`.  No asymptotic or family-cardinality term
is used.

The raw lower bound

```text
a k^(theta-1)/log(k) <= delta
```

with `a>0` gives

```text
-(1-theta)K-M-(-log a) <= log(delta).
```

Because `W>=1`, adding `4 log W` preserves the inequality.  Thus the safe
loss is exactly `C=-log a`.  Neither the formal target nor the endpoint
theorem requires `C` itself to be nonnegative, so allowing `a>1` creates no
sign gap.

## 3. Reconstruction of `D=5/2+En+ED`

The endpoint comparison gives

```text
c K^2-En M <= log(nScale) M.                       (A)
```

If the first Konyagin log term is negative, `r>=2`, `lambda>=1`, and `W>=1`
force `log(derivativeScale)<0`.  Combining this with the derivative lower
comparison and `factorialScale>=1` yields

```text
log(nScale) < (r+1)log(x)+ED
            <= (r+1)K+3/2+ED.                    (B)
```

Equations (A)--(B) imply

```text
c K^2 < ((r+1)K+3/2+ED+En) M.
```

Here `K>=1`, `M>0`, and `En,ED>=0`.  Replacing the fixed additive loss by its
larger multiple by `K` and dividing by positive `K` gives

```text
c K-(1+3/2+En+ED)M <= r M.
```

Therefore `D=5/2+En+ED` is arithmetically correct: `3/2` is the shifted-base
loss and the additional `1` converts `r+1` to `r`.  No block-count loss is
hidden.  The estimate is deliberately coarse but valid.

The endpoint lower bound on `nScale` and the derivative comparison are real
source hypotheses.  They are not the desired order conclusion in disguise,
but an application to a new shifted or regrouped construction must prove
them with suitable common losses; the theorem does not derive them from PI
input or from partition geometry alone.

## 4. Finite separation wrapper

Write `C=-log a` and `D=5/2+En+ED`.  The wrapper assumes

```text
q >= 1,
c K >= 0,
(3D+2)M <= cK,
((3D+3)M+C)M < 2cK.
```

The coefficient inequality gives

```text
2cK <= 3cK-(3D+2)M.
```

The right side is nonnegative, and `q>=1` then gives

```text
3cK-(3D+2)M <= (3cK-(3D+2)M)q.
```

Together with the strict left inequality this is exactly the separation
hypothesis of `locationBlindTermwiseSubdivision_endpoint_no_go`.  The signs,
strictness, and coefficient constants all agree.  At
`c >= (1-theta)/3` the resulting contradiction is therefore valid for the
explicit source predicate.

The Lean wrapper does not prove that these finite scale inequalities hold
eventually.  For fixed `a,En,ED` and fixed positive `c`, that external step
uses `K/M^2 -> infinity`; the author evidence explicitly records that this
limit is not packaged as a Lean sequence theorem.

## 5. Finite and growing-family quantifiers

The theorem is uniform in an arbitrary finite index type and `Finset s`; no
upper bound on `s.card` or lower bound on an individual positive weight
appears.  Hence it can be instantiated pointwise when a block count grows
with `k`, provided each family is finite and all displayed hypotheses hold.

It is not an infinite-family theorem, and Lean does not bind `a,En,ED`
across different values of `k`: they are ordinary parameters of each finite
invocation.  Therefore the asymptotic phrase “growing family with fixed
losses” requires an external assertion that common losses can be chosen (or
that the two explicit separation inequalities still hold).  The frozen
evidence and structured summaries state this limitation rather than
promoting the pointwise theorem to arbitrary regroupings.

## 6. Frozen build evidence and hashes

Read-only hashing of the audited checkout gives:

```text
ParametricRanges.lean
  8793c3a76f46ce7e4985e7619bb53eb91ce481391ac52bce343dfc9232f4f7b5
ParametricInterface.lean
  1e26f0f1d2665e20ad2b5c7c6b7ebe93894e5ec712967104d74630376d451efe
verify_inside_guard.sh
  7013bf9d3f86cf75daa19ba401f3596a775d477f8601c680f75e7d0516c6c38c
lakefile.toml
  2ab8618c84e5370963d53afe5e63736e8289edc3e471897564283aab06f6ad7c
lake-manifest.json
  4f88144c9db6bab6b1e0a7447a9e58bf4627b340fcc2fd9ef102a0925410cd0b
```

All five equal both `evidence/lean_parametric_ranges.json` and
`formal/logs/final-sha256.txt`.  The frozen replay log records guard unit
`openmath-task-20260826-213317-292367.scope`, exit status zero, maximum RSS
`7075568 KiB`, and zero swaps.  Its axiom print for both source-geometry
theorems is exactly `[propext, Classical.choice, Quot.sound]`; a read-only
scan found no `sorry` or `admit` in `ParametricRanges.lean` or
`ParametricInterface.lean`.

No new Lean build was run for this audit.  The mathematical reconstruction,
current-source hashes, and frozen replay metadata are mutually consistent.

## Final scope finding

The finite source-to-location-blind map and finite endpoint wrapper pass.
They prove a no-go only for source families satisfying the explicit common
raw comparisons and positive termwise ledger.  They do not rule out
prime-location-adaptive covers, cross-block cancellation, variable losses
that defeat separation, infinite families, or arbitrary shifted/regrouped
sources.  No Erdos-451 conclusion is enlarged by this interface.
