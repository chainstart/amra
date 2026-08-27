# Same-model cross-audit: high-support centered mechanisms

## Verdict: PASS

This is a fresh reconstruction by a separate Codex agent in the same
model/tool ecosystem.  It is neither human peer review nor an externally
independent audit.  I did not modify
`evidence/high_support_centered_mechanisms.md`.  Both exact mechanism
identities and both scoped obstruction claims survive; no mandatory
mathematical correction was found.

## Local multiplier correlations

For `p=k+b` and `d=b-1`, the unit density is `delta=d/(p-1)` and the
centered covariance is overlap density minus `delta^2`.  Since
`2d<p` for every remaining `p<2k`, the interval and its negative are
disjoint.  Hence

```text
R_p(-1)/(delta(1-delta))=-d/k.
```

For multiplication by `2`, absence of wrap gives overlap `floor(d/2)` and
the numerator in (8).  If `d` is even the normalized value is exactly
`(k-d)/(2k)`; if `d` is odd its numerator is
`(d(k-d-1)-k)/2`.  Thus fixed positive small multipliers are not universal
coordinatewise reversals, whereas the representative of `-1 mod P` is
`P-1=exp((1+o(1))k)` and is unaffordable.

The fixed-generator resonance lemma is exact linear algebra over
`F_2`: `s` generator constraints leave dimension at least `m-s`; the set of
active coordinates has size at least that dimension; averaging Hamming
weight in the kernel produces a vector of weight at least `(m-s)/2`.
The resulting quadratic character is trivial on the generated subgroup and
has genuinely high conductor.  The note correctly warns that its interval
coefficient may vanish, so this is not a signed-error lower bound.

## Prefix transport

For positive support below `T` and `gT<P`, the test
`phi(x)=log(x)/log(gT)` lies in `[0,1]` on both supports.  Push-forward by
`g` shifts its expectation by exactly `log(g)/log(gT)`, proving the total
variation lower bound.  Since `log T=O(k/log k)`, its minimum over integers
`g>=2` is `Omega(log k/k)`, exponentially larger than the target density
`exp(-Theta(k/log k))`.  The maximum-element argument also rules out exact
finite positive invariance without wrap.  These facts kill only a handoff
that pays unmatched boundary mass absolutely; signed boundary telescoping
is expressly left open.

## Block-full energy

Local nonprincipal-character orthogonality gives `p-2` when two units agree
modulo `p` and `-1` otherwise, proving (14).  Identical multiset indices
contribute `M product(p-2)`.  For unequal represented values below `T`, the
product of block primes selecting the large factor divides their difference
and is at most `T`; all unequal pairs cost at most `M^2T`.  Equal values at
different indices add positively.  Therefore the condition
`product(p-2)>2MT` implies the block diagonal lemma exactly.

For the bulk block `3k/2<p<2k`, PNT gives block size
`Theta(k/log k)` and `log P_block=(1/2+o(1))k`.  Every nonempty conditioned
submultiset has `M,T=exp(O(k/log k))`, so the diagonal lemma applies with an
exponential margin.  The block-full coefficient square mass is
`product delta_p(1-delta_p)=exp(-Theta(k/log k))`.  Dividing the numerical
separated Cauchy--Schwarz ledger by the block density main scale gives

```text
(2M)^(-1/2) product sqrt((p-2)(1-delta_p)/delta_p)
  = exp((1/4+o(1))k).
```

Conditioning decreases `M` and therefore cannot improve this separated
handoff.  As stated by the author, this is a lower bound on the size of the
*method's norm ledger*, not on the actual signed full-order remainder.

## Scope conclusion

The evidence rigorously kills (i) fixed-generator uniform spectral
contraction, (ii) transport of the short positive prefix with absolute
boundary payment, and (iii) a block-cumulant scheme that hands its
macroscopic full-order remainder to separate coefficient and energy norms.
It does not kill position-dependent multipliers, a signed dilation-boundary
identity, direct coefficient--kernel coupling, or cancellation between
full-order block remainders.  The surviving high-conductor centered
correlation is therefore stated at the correct strength, and `closes=[]`
is accurate.
