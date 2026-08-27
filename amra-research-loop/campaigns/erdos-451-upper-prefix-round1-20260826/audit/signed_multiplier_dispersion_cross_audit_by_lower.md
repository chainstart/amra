# Same-model cross-audit: signed multiplier dispersion

## Role, scope, and verdict

This is a read-only mathematical reconstruction by the lower-frontier agent,
which did not author the audited B-line evidence. It is an independent-agent
check inside the same Codex model/tool environment, not human peer review.
I did not modify the author evidence, structured JSON, or A-line files.

**Verdict: PASS for the exact identities, conditional endpoint transfer, and
the stated universal-damping/separated-energy no-go. No mandatory correction
was found.**

The verdict is deliberately method-scoped. The evidence does not prove a
lower bound for the coefficient-weighted signed aggregate
`mathcal H_a`, does not rule out joint cancellation among its three factors,
and does not improve Erdős 451.

Audited SHA-256 values:

```text
ef3fea613955c1e619c7ed10b3186819508a6bed4c68cfa135395788826b0a63  evidence/signed_multiplier_dispersion_no_go.md
ac588d3fe8ba8f951e5ee811f7cf8a1153477ca056139b6b1e74e44c9d3cadd1  decisive_lemma.json
d73f572919f2bc59c19881e123f028df56522571a79835821cc559fdd64b7739  information_loss_map.json
14bdd905a2918d80d9b9b99198faeaad30d1c4a3caf274e1979274b18ffbadd1  kill_tests.json
4dbb5003ab9f2b21f58d1fe0d83bcd562c0de8f81ea40f572a2f10392d5d3e26  mechanisms.json
```

## 1. Endpoint coefficient, phase, and conjugations

With the convention

```text
F(y)=sum_chi c_chi chi(y),
```

the local allowed residues are `-j*Q_0^(-1)`, `1<=j<=d_p`. Therefore

```text
1/(p-1) sum_(allowed y) conjugate(chi_p(y))
 = 1/(p-1) chi_p(-Q_0)
     sum_(j<=d_p) conjugate(chi_p(j)).
```

The sign and conjugation are correct because
`conjugate(chi_p(-Q_0^(-1)))=chi_p(-Q_0)`. Multiplication over primes gives
exactly

```text
c_chi=phi(P)^(-1) chi(-Q_0)
      product_p sum_(j<=d_p) conjugate(chi_p(j)),
```

where a principal local component contributes `d_p`. This agrees with the
prior full-modulus endpoint formula.

Replacing `y=ut` by `y=gut` contributes `chi(g)` with no conjugate. Hence

```text
C_X(g)=sum_chi c_chi chi(g) (S_X^P(chi))^2,
Z_a=sum_chi c_chi A_a(chi) (S_X^P(chi))^2.
```

The square is the complex square because `u` and `t` are summed with the
same character, not conjugate characters. Also

```text
chi(-Q_0) A_a(chi)=sum_g a_g chi(-Q_0 g),
```

so the absorber phase is translated rather than discarded. Equations
(2), (6)--(8) preserve every phase and conjugation.

## 2. Principal normalization and signed positivity

For the principal character, `A_a(1)=sum_g a_g`. Thus normalization
`sum_g a_g=1` leaves the principal term exactly `delta*N`.

Each physical `C_X(g)` is a nonnegative integer count, whereas the real
weights may have either sign. The spectral total equals the real physical
quantity `Z_a=sum_g a_g C_X(g)`. If the low- and high-conductor errors are
both `o(delta*N)`, then

```text
Z_a=delta*N+o(delta*N)>0.
```

If all supported physical counts vanished, `Z_a` would be zero. Therefore
some supported `g` has `C_X(g)>0` (indeed some positive-weight term must).
This is the only positivity transfer used; it does not incorrectly infer
positivity of every term.

For its allowed pair, `n=Q_0*g*u*t` is valid: `g` is a unit modulo `P`,
`F(gut)=1` handles every remaining prime, and the absorbed primes divide
`Q_0`. Eventually `Q_0>2k`, while

```text
log n <= log Q_0+log G+2log X.
```

Thus `log G=o(k)` gives `n=exp(o(k))`, and
`log G=O(k/log k)` gives the sharper `exp(O(k/log k))` statement. The
strict lower endpoint is also valid.

## 3. Low-conductor `L` budget

The prior low-conductor theorem supplies the quantitative relative bound

```text
sum_(1<f_chi<=Y) |c_chi| |S_X^P(chi)|^2 /(delta*X^2)
 <= exp(-(3*eta/2)log X+o(log X))
```

for fixed `gamma>0`, `0<eta<4/3`, and
`log X=gamma*k/log k`. Since `|A_a(chi)|<=L`, the same aggregate after
inserting the multiplier is bounded by `L` times this expression. The
assumption

```text
log L=o(k/log k)=o(log X)
```

is exactly sufficient. Moreover `N=M_X^2~X^2`, so changing the denominator
from `delta*X^2` to `delta*N` costs `1+o(1)`. The conditional lemma and the
structured summary use this correct budget. Merely assuming `log L=o(k)`
would not suffice; the evidence does not use that weaker statement in its
closure lemma.

## 4. Sparse quadratic annihilator

For each support value `g_i`, the condition `chi_epsilon(g_i)=1` is one
linear equation on `epsilon in F_2^m`; `chi_epsilon(-Q_0)=1` is one more.
Because every prime in `mathcal P` exceeds `k+A`, `-Q_0` is a unit at every
coordinate. The common kernel has dimension at least `m-s-1`.

If this dimension is `d>0`, its active-coordinate set has size at least
`d`. Every active coordinate is one on half the kernel, so averaging Hamming
weight produces a vector of weight at least `d/2`. For `s=o(m)`, its
conductor obeys

```text
log f_chi >= (d/2)log k=(1/2-o(1))*k >> log Y.
```

On this character `A_a(chi)=sum a_g=1` and `chi(-Q_0)=1`. This refutes
uniform damping for sublinear support, but correctly says nothing about the
corresponding interval coefficient or the whole signed aggregate.

## 5. Exact full-support energy and off-diagonal bound

Summing `|A_a(chi)|^2` over characters nonprincipal at every local prime
uses the exact local identity

```text
sum_(psi mod p, psi nonprincipal) psi(g) conjugate(psi(h))
 = p-2  if g=h (mod p),
 = -1   otherwise.
```

After equal residue classes are aggregated, distinct positive support values
are distinct modulo `P` because `G<P` eventually. The diagonal contribution
is

```text
sum_g |a_g|^2 product_p(p-2)
 >= S^(-1) product_p(p-2),
```

using `sum a_g=1` and Cauchy--Schwarz.

For `g!=h`, the magnitude of the local product is

```text
product_(p divides g-h)(p-2)
 <= product_(p divides g-h)p
 <= |g-h| <= G.
```

Consequently the entire off-diagonal has absolute value at most
`L^2*G`. Under `S,L,G=exp(o(k))`, this is `exp(o(k))`, whereas the diagonal
is `exp((1+o(1))k)/S`. Subtracting the off-diagonal magnitude proves

```text
sum_(supp chi=mathcal P)|A_a(chi)|^2
 >= (1-o(1))*S^(-1)*product_p(p-2).
```

There are `product_p(p-2)` full-support characters, so some such character
has `|A_a(chi)|>=exp(-o(k))`; its conductor is `P>Y`. The exact assumptions
`sum a_g=1`, `S,L,G=exp(o(k))`, and unit support are indispensable and are
present in the evidence.

## 6. Universal damping versus the coefficient-weighted endpoint

The preceding energy is multiplier-only:

```text
sum_(full support)|A_a(chi)|^2.
```

It is neither

```text
sum |c_chi A_a(chi)|^2
```

nor a lower bound for

```text
H_a=sum_(f_chi>Y)c_chi A_a(chi)(S_X^P(chi))^2.
```

The interval coefficient `c_chi` may vanish or be small, the complex square
may be small, and distinct character terms may cancel. Thus (31) kills only
the promised uniform pointwise damping and factor-separated energy handoff.
Likewise the reciprocal bound for an inverse filter kills “uniform damping
plus stable recovery”, but a direct proof of the joint signed `H_a` would
not invert the filter.

The author evidence states these exclusions repeatedly, and the structured
diffs preserve them: they call the coefficient-aware high-conductor estimate
conditional/open, retain `closes=[]`, and do not report an Erdős-451 bound.
The sparse wording in summaries must be read with the evidence's exact
condition `s=o(m)`, and the general energy statement with assumptions (28);
under those stated meanings there is no scope overreach.

## 7. Nonblocking background note

The Burgess paragraph following (34) is only a consistency check and is not
used in any exact result above. If its “positive interval multiplier” is
read literally inside the earlier unit-supported class for intervals longer
than `k`, it should be unit-sieved or described simply as the unsieved
character-sum comparison. This wording does not affect equations (2)--(33),
(35)--(36), the conditional endpoint lemma, or the universal-damping no-go,
so it is not a mandatory correction to the audited result.

## Final classification

- Exact phase/conjugation identities: **PASS**.
- Signed positivity and endpoint/value transfer: **PASS**.
- Low-conductor `L` budget: **PASS**.
- Full-support energy and off-diagonal estimate: **PASS**.
- Universal-versus-coefficient-weighted scope: **PASS**.
- Public problem/main term/main exponent: unchanged.
- Campaign phase: remains `survivor_deepening`; no promotion gate moved.
