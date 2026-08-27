# Same-model cross-audit: free-multiplier bilinear counting

## Verdict: PASS

This is a cross-reconstruction by a separate Codex agent in the same
model/tool ecosystem.  It is neither a human review nor an externally
independent audit.  I did not modify
`evidence/free_multiplier_bilinear_counting_audit.md`.  All stated identities,
energy scales, counterexamples, and delimited no-go conclusions survive; no
mandatory mathematical correction was found.

## Additive Fourier reconstruction

- Regrouping by `s=ut` gives (3) exactly with the truncated divisor weight
  `d_{U,H}`.  No uniform-product expectation is inserted.
- With `beta_p` normalized by `1/b`, local inversion contributes the density
  `b/p`.  CRT decomposition by the set of nonzero local coordinates gives
  (5), and primitive `a mod P_S` indexes each exact conductor once.  Reducing
  `a mod q` by `gcd(a,q)` proves (7); zero local coordinates are not charged
  to the full conductor.
- The complete `p x p` product count is
  `(2p-1)+(b-1)(p-1)=p+(p-1)b`, verifying (8).  Restricting one variable to
  units removes this zero-product bias but leaves the interval sieve noted in
  (9).
- Orthogonality gives (10).  Decomposing `U=vM+r` and then the incomplete
  `t` range proves (11); if both lengths are multiples of `M`, the surviving
  zero-product line is `UH/M`, as in (12).  The incomplete `r x h` rectangle
  has the standard geometric-kernel bound `O(M(1+log M))`, yielding (13).

## Second moments and energy

The residue-class multiplicities of `1<=t<=H` are `w+1` in `h` classes and
`w` in the other `M-h`, so (14) is exact.  Parseval over one complete `u`
period gives `M E_M(H)`; Cauchy over at most `floor(U/M)+1` periods gives
(15), and for `U,H<=M` this reduces exactly to
`min(UH,sqrt(UHM))`.  Frequency Parseval gives

```text
sum_{a mod M} |B_M(a)|^2 = M E_M(U,H),
```

with congruence energy (18).  The warning that primitive-frequency
restriction instead introduces Ramanujan sums is necessary and correct.

For the global additive transform, the author's convention is unnormalized:
`sum |Fhat|^2=P^2D`, while the bilinear kernel has norm `P E_P`.  Removing
zero frequency and using `UH<P/2` gives (23).  Dividing the separated
Cauchy--Schwarz ledger by `DUH` reproduces exactly

```text
sqrt((1-D)P/(2DUH)).
```

Since `log P=Theta(k)`, `-log D=o(k)`, and `log(UH)=o(k)`, its size is
`exp(Theta(k))`.  This is correctly described only as the size of the
separated `L^2` upper-bound ledger, not a lower bound on the signed error.

## Coherent high-conductor character

If `M>=12UH`, then `0<2 pi ut/M<=pi/6` throughout the rectangle, so every
summand of `B_M(1)` has real part at least `cos(pi/6)`.  Equation (19), and
its restriction to any subset of multipliers, are therefore exact.  PNT
gives

```text
log product_{k+A<p<2k} p = (1+o(1))k,
```

so every affordable `UH=exp(o(k))` lies in this coherent regime for the full
support.  The CRT character `a=1` has a nonzero local coordinate at every
prime.  A proper arithmetic interval of length `0<b<p` has no zero nontrivial
additive Fourier coefficient, so this is a genuine 451 character.  It
refutes conductor-only pointwise cancellation but says nothing by itself
about the signed coefficient sum.

The local Parseval identity (21) follows from the `1/b` normalization.  On a
fixed bulk interval `3k/2<p<2k`, the normalized Dirichlet-kernel `L^1` norm is
`Omega(log k)`; multiplying over `Theta(k/log k)` primes gives the stated
triangle envelope

```text
exp(Omega(k loglog(k)/log(k))),
```

which is subexponential and is correctly not promoted to `exp(Omega(k))`.

## Multiplicative unit-group reconstruction

- On `G=(Z/PZ)^*`, the normalization
  `c_chi=phi(P)^(-1) sum 1_A(x) conjugate(chi(x))` gives inversion
  `1_A(x)=sum c_chi chi(x)`, hence (32) with no missing `phi(P)` factor.
  The principal coefficient is exactly `delta^times`.
- The ratio
  `delta_p^times/(b/p)=1-k/[b(p-1)]` proves (30).  For
  `b>=A=k/log^2 k`, a dyadic block contains `O(B/log k)` primes by the
  standard Brun--Titchmarsh upper bound, so the total logarithmic loss is
  `O(loglog k/log k)=o(1)`.  This named input should be kept explicit when
  the argument is reused.
- Inclusion--exclusion over `P/f` gives (35) exactly because `P` is squarefree
  and divisors of `P/f` are coprime to the inducing conductor `f`.  Thus the
  outer principal-unit sieve really prevents a free complete-period
  reduction.
- Character orthogonality proves (36).  Since `UH<P`, congruence of the two
  positive products is equality, giving the displayed multiplicative energy.
  Normalized group Parseval gives (37).  The diagonal energy and
  `UH=o(phi(P))` yield (38), and division by the principal contribution gives
  precisely (39), of size `exp(Theta(k))`.

The Burgess observation is at the right strength: the squarefree full
conductor is `exp(Theta(k))`, while every permitted interval is
`exp(o(k))`, far below `P^(1/4+epsilon)`.

## Scope conclusion

Equations (19), (24), (26), and (39) rule out only conductor-only pointwise
decay, separated absolute `L^2`, and characterwise triangle summation.  They
do not rule out the signed additive coupling (27) or its multiplicative
analogue.  The author's `closes=[]` and surviving-interface description are
therefore accurate.

No mandatory corrections.  One nonblocking dependency clarification is to
name Brun--Titchmarsh explicitly at (30); PNT alone does not supply the
uniform `O(B/log k)` bound for the shortest dyadic offset blocks.
