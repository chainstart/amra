# Same-model cross-audit: weighted multiplicative characters

## Verdict: PASS

This is a fresh reconstruction by a separate Codex agent in the same
model/tool ecosystem.  It is not a human review or externally independent
audit.  I did not modify
`evidence/weighted_multiplicative_character_deepening.md`.  The exact
normalizations, low-conductor theorem, energy scales, and scoped no-go
conclusions survive; no mandatory mathematical correction was found.

## Exact transform and local moments

For squarefree `P`, a character is a tuple of local characters and every
nonprincipal character modulo a prime is primitive.  Hence its exact
primitive conductor is the product of its nonprincipal coordinates.  With
group Fourier normalized by `1/phi(P)`, the local principal density is
`delta_p=d_p/(p-1)` and the relative coefficient is the interval average
`rho`; this reconstructs `c_chi=delta product rho` with no missing
`phi(P)` factor.

Möbius inversion over the primes outside the conductor gives (5) because
those divisors are coprime to the primitive conductor.  Multiplicative
orthogonality gives

```text
sum_psi |rho_p,psi|^2=(p-1)/d_p,
sum_{psi ne 1}|rho_p,psi|^2=k/d_p,
```

since `p-1-d_p=k`; the higher-moment multiplicative energy formula is exact
for the same normalization.  The absorber contributes only the phase
`psi(-Q_0)`, so it correctly disappears from absolute moments.

On a bulk offset block, Polya--Vinogradov bounds the largest nonprincipal
`rho` by `O(log(k)/sqrt(k))`, while its square mass is bounded below.
Therefore `L_p` is between `c sqrt(k)/log(k)` and `C sqrt(k)`, confirming
the genuine `f_S^(1/2+o(1))` absolute coefficient entropy.

## Low-conductor aggregate

Every divisor in the outer unit sieve below `X` uses at most
`J_X=floor(log(X)/log(k))` remaining primes.  With
`log X=gamma k/log(k)`, the binomial divisor count has logarithm
`O(k loglog(k)/log(k)^2)=o(log X)`.  Polya--Vinogradov applied inside the
exact sieve formula therefore yields the uniform bound (16).

For `f<=X^(4/3-eta)`, support rank is at most `R=log(Y)/log(k)`.  Bounding
`P_S` by `(2k)^r` and the coefficient ledger by
`(C sqrt(k) log(k))^r` gives exponent

```text
(3/2) R log(k) <= (2-3 eta/2) log(X),
```

while the divisor and support-count entropies are `o(log X)`.  After the
`X^-2` normalization the decay is `exp(-(3 eta/2)log X+o(log X))`.
Thus (18) is genuinely unconditional for every fixed `0<eta<4/3`.

The Burgess ledger is also correct: combining the true coefficient entropy
with the `nu`-th pointwise estimate allows decay only below
`log f/log X < 4nu/(nu^2+nu+1)`, whose maximum over positive integers is
`4/3` at `nu=1`.

## High-conductor energy and random walk

Summing over characters nonprincipal at every local prime gives the kernel
`p-2` on a congruent pair and `-1` otherwise.  Identical multiset indices
contribute `N product(p-2)`.  For distinct represented integers below `T`,
the product of the exceptional primes divides their nonzero difference and
is at most `T`; unequal-pair mass is therefore `N^2T=exp(o(k))`.  Equal
values at different indices add with the positive diagonal sign.  This
reconstructs (28).

The full-support coefficient square mass is exactly

```text
product delta_p(1-delta_p),
```

and differs from one only by `exp(-Theta(k/log k))`.  Consequently the
*numerical separated Cauchy--Schwarz ledger*, divided by the density main
term, is `exp((1/2+o(1))k)`.  This is correctly not claimed as a lower bound
on the signed error.

For a word walk on primes at most `k`, all letters are units modulo `P`.
When `k^L<P`, character orthogonality plus unique factorization gives the
exact moment with `g^L<=E_L(G)<=L!g^L`.  Applying the same full-support
diagonal shows that separated Hilbert-space mixing needs
`N>=P^(1-o(1))`, hence `L log(k)>=(1-o(1))k`; this exhausts the affordable
value budget.  Collisions only strengthen the diagonal.

## Centered inverse transform and scope

The inverse transform (37)--(38) has the correct conjugation convention and
keeps the `Q_0` phase inside the actual local sets.  The even/odd parity
halves of the half-density cube are identical on every proper centered
support but opposite on the full support, while a two-violation singleton
has the same full-product sign as the all-allowed singleton.  These are
valid kill tests for generic bounded-cumulant and violation-parity closure,
not models of the 451 product multiset.

Accordingly the note closes only the low-conductor aggregate and kills
three explicitly delimited absolute/separated handoffs.  The signed
high-conductor coupling (40) remains open, and `closes=[]` is accurate.

Nonblocking dependency clarification: retain the named short-interval prime
upper bound (for example Brun--Titchmarsh) in the dyadic estimate used for
`-log(delta)`; PNT alone is not uniform at the smallest offset scale.
