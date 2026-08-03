# Independent audit: normalized-unit translation firewall

## Verdict

The decisive finite lemma passes independent reconstruction.  The two
reverse-circle blocks at source translations `0` and `-1/4` have the same
normalized Boolean quotient, factor/root/logarithmic and row-spectrum data,
while their exact target--target squared-distance label counts are respectively
127 and 145.  This strictly refutes determination of collision behaviour by
the stated **unit-blind normalized** data.

The result does not refute a statistic retaining Laurent units, does not bound
the relative unit fibre after one common source `X` is fixed, and supplies no
asymptotic fibre or propagation theorem.  Erdős #1083 and the public `3/5`
exponent are unchanged.

## 1. Independent algebraic reconstruction

Set

```text
G=1+x,                  F0=1+x^2,
R1=1,                   R3=1-x+x^2,
H1=R3,
H2=1+x+x^2,             H3=1-x^2+x^4,
B=1+x^4+x^8.
```

Independent sparse-polynomial multiplication gives

```text
B=H1 H2 H3,
Q1=B=H1 H2 H3,          y1=(1,1,1),
Q3=H2 H3,               y3=(0,1,1),
B=R1 Q1=R3 Q3.
```

It also reconstructs all positive masks used to build the three scalar rows:

```text
supp(G B)   ={0,1,4,5,8,9},
supp(F0 Q1) ={0,2,4,6,8,10},
supp(F0 Q3) ={0,1,2,6,7,8},
G R1=1+x,                G R3=1+x^3.
```

Every displayed mask has coefficient one at its support and zero elsewhere.
Thus the paired-positive identities and normalized quotient vectors pass.

## 2. Units, factors, roots and logarithmic data

For source translation `t`, the reconstructed unit vector is

```text
u(G)=t,      u(F0)=2t,    u(B)=-3t,
u(R1)=0,     u(R3)=2t,    u(Q1)=-3t,    u(Q3)=-5t.
```

Subtracting the minimum Laurent exponent and normalizing the first coefficient
returns exactly the same seven normalized polynomials at `t=0` and `t=-1/4`.
Consequently their nonzero roots and multiplicities agree.  The independent
checker also forms every normalized rational logarithmic derivative `P'/P`;
its numerator and denominator are identical in the two blocks.

This agreement is specifically normalized agreement.  For a Laurent
associate `x^u P`, the full logarithmic derivative contains the additional
term `u/x`, so a unit-aware statistic distinguishes the two blocks.

## 3. Common-X scalar copies and the 12 labels

For `X_t={t,t+1}`, row `lambda` uses scalar source
`lambda X_t` and a complement shifted by `-lambda t`.  The independently
reconstructed starting masks are

```text
lambda=1: supp(F0 Q1),
lambda=2: supp(G B),
lambda=3: supp(F0 Q3).
```

For both translations, the Minkowski sum of each scalar source with its
complement is exactly `{0,...,11}`.  After adding 100, every row therefore has
the identical 12-element source--target squared-distance spectrum
`{100,...,111}`.

This checks both common-X use and the fact that the agreement holds row by
row, not only after taking a union over the three scalars.

## 4. Genuine reverse-circle geometry and exact label counts

The Euclidean realization can be reconstructed explicitly.  For
`x in X_t`, scalar `lambda`, `z=lambda/2`, and a positive tangent square
`tau`, take

```text
p_x=(0,sqrt(1-x^2),x),
q=(sqrt(tau),0,-z).
```

Then

```text
||p_x-q||^2=tau+1+z^2+lambda*x.
```

Choosing

```text
tau=100+s-lambda*t-(1+z^2)
```

for each row start `s` gives distances `100+s` and
`100+s+lambda`.  Both source pairs lie in `[-1,1]`, and every reconstructed
`tau` is positive, so both are genuine configurations in `R^3`.

For two targets `(tau,z)` and `(sigma,w)`, exact subtraction gives

```text
tau+sigma+(z-w)^2-2 sqrt(tau*sigma).
```

The audit canonicalizes each rational square root into a rational coefficient
and squarefree radicand.  Among the 153 unordered pairs of 18 targets it finds:

```text
t=0       : 127 distinct labels,
t=-1/4    : 145 distinct labels.
```

Thus normalized data and common row spectra do not determine the collision
partition.  The arithmetic is exact; no floating-point comparison is used.

## 5. Exact scope of the kill

The pair directly kills `M1083M4-08` and `M1083M4-09` in their unit-blind
forms.  More generally it kills an inference only when the sufficient
statistic is invariant under Laurent associates but the conclusion asserts
determination of the target collision behaviour.

It does **not** show any of the following:

- that a Laurent-unit-aware root, Fourier or moment theorem fails;
- that the number of relative unit vectors is large after fixing one common
  source `X`;
- that no lower bound can hold uniformly across every unit fibre;
- that an all-target fibre theorem or selected-row propagation is impossible.

This is why `M1083M4-07` legitimately survives.  The adversarial pair varies
the common source translation itself and is separated by the retained unit
vector.  It supplies no many-unit family inside one fixed common-X fibre.

The other round-four killed mechanisms are correctly described only as
scoped failures of their current unit-blind, incidence-only, or
missing-interface proof patterns.  The translation pair is not a
counterexample satisfying every stronger future hypothesis stated in those
mechanisms.

## 6. Capacity and fibre dependency

The inherited exponents are

```text
q=13/18,       U=5/6,       q+U=14/9.
```

Hence the all-target unordered-pair capacity has exponent

```text
2(q+U)=28/9,
```

which exceeds 3 by exactly `1/9`.  On an actual all-target pair occurrence
domain of size `t^(28/9-o(1))`, a maximum-fibre bound

```text
t^(1/9-epsilon+o(1))
```

would yield at least `t^(3+epsilon-o(1))` labels by division.  An appropriate
energy/average-fibre statement needs the analogous mass inequality on the
same domain.

There is an important dependency precision: `|targets|<=qU` gives only an
upper capacity.  A future fibre argument must also retain an actual occurrence
domain of size `t^(28/9-o(1))`, or an equivalent weighted mass lower bound.
An upper capacity plus a small-fibre assertion alone cannot force many labels.
The selected-row information must additionally be propagated to this same
all-target domain.

## Reproduction

The independent checker uses only the Python standard library and does not
import or execute the author checker.

```sh
env AMRA_MEMORY_KIB=2097152 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-1083-moment-round4/audit/independent_verify_unit_translation_firewall.py
```

It completed in under one second.  No Lean process was used.  SHA-256:

- independent script: `0c8afdcc437f20c3680687a9071a9f3da4856b2f286408d4888ab9db234bc742`
- independent JSON: `9cca019aa0bd06d3572e21a9e9a3d818eba88143c7f368b64562521a6dc2d686`

## Promotion decision

Reject promotion.  The audited result is an exact finite information-loss
firewall, but the closure contract requires a rigorous dimension-three
exponent strictly greater than `3/5`.  Relative-unit control, common-X
Fourier structure, full-target propagation, occurrence-domain mass, fibre
control below `1/9-epsilon`, and outer stability all remain open.

