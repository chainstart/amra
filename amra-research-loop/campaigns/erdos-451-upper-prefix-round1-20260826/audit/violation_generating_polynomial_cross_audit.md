# Same-model cross-audit of the violation generating polynomial

## Verdict

**PASS.**  I
independently reconstructed equations (5)--(13), the proper-degree cube
dual, the two proper-marginal witnesses, the contour norm, and the
conditional high-conductor implication.  The mathematical evidence file is
correct in its current form and explicitly keeps the full-modulus estimate
open.  The initially missing structured quantifier on the cutoff has now
been corrected: all seven structured occurrences explicitly say fixed
`0<eta<4/3`.  No mandatory correction remains.

This is a read-only cross-audit by another Codex agent in the same model and
tool environment.  It is not an independent human review.  I did not modify
the author evidence or any structured artifact.  The audited evidence
SHA-256 was
`5bbf9070715921e6c497937da09b1f3d8915166bc9155280208275f7e50a2382`.

## 1. Generating identity: (5)--(8)

For one point,

```text
z^V = product_p (I_p+z J_p)
    = product_p (z+(1-z)I_p).
```

Selecting the `I_p` factor exactly on `T` gives
`z^(m-|T|)(1-z)^|T|`.  Summation over the product multiset therefore gives
(5), with no sign or multiplicity loss.  Substitution
`N_(P_T)=delta_T N+E_(P_T)` factors the principal subset sum into

```text
product_p (q_p z+delta_p),
```

which proves (6).  At `z=0`, only `T=mathcal P` remains, so (7) is exactly
`F_X(0)=N_P(X)`, not a Bonferroni approximation.

Differentiating `z^V` at one gives
`F_X^(j)(1)/j!=sum_x binom(V(x),j)`.  Expanding the binomial coefficient as
the number of `j`-subsets of violated coordinates proves (8).  Thus the
proper jet really contains exactly proper-rank failure intersections.

## 2. Character normalization and the `Q_0` phase: (9)--(13)

On the unit group modulo `p`, the local function is
`z+(1-z)1_(A_p)`, with

```text
A_p={-Q_0^(-1)j:1<=j<=d_p}.
```

Fourier normalization by `1/(p-1)` gives the principal coefficient

```text
z+(1-z)d_p/(p-1)=delta_p+q_p z.
```

For a nonprincipal `psi`, the constant `z` has zero coefficient and

```text
(1-z)/(p-1) sum_(a in A_p) conjugate(psi(a))
 = (1-z)delta_p psi(-Q_0)/d_p
     sum_(j<=d_p) conjugate(psi(j)).
```

The phase sign is correct because
`conjugate(psi(-Q_0^(-1)))=psi(-Q_0)`.  Multiplying local coefficients gives
(11).  Summing `chi(ut)` over independent `u,t` produces the complex square
`(S_X^P(chi))^2`; replacing it by an absolute square would be false.

At `z=0`, every local coefficient is

```text
1/(p-1) * psi_p(-Q_0)
  * sum_(j<=d_p) conjugate(psi_p(j)),
```

where a principal local character has inner sum `d_p`.  Their product is
exactly (13), including `1/phi(P)`, the global phase `chi(-Q_0)`, and the
outside principal densities.  All supports and primitive conductors are
present.

## 3. Proper-degree cube dual: (14)--(18)

The top multilinear coefficient is

```text
sum_S (-1)^(m-|S|) Q(1_S).
```

It vanishes when the total degree is less than `m`, and solving for the empty
vertex gives the sign in (17):

```text
Q(0)=sum_(S nonempty) (-1)^(|S|+1)Q(1_S).
```

After substitution in the expectation, the coefficient of `Q(1_S)` is
`mu(S)+(-1)^(|S|+1)mu_0`.  It is positive for odd support.  For even support
it is `mu(S)-mu_0>=0`, since

```text
mu(S)/mu_0=product_(i in S) q_i/delta_i >= 1.
```

Every nonempty vertex value is nonpositive, so the expectation is
nonpositive.  The theorem therefore kills every proper-degree *pointwise
one-sided* multilinear separator, including nonsymmetric ones.  It does not
kill arbitrary signed arithmetic estimates of proper-degree terms.

## 4. The two proper-marginal laws: (19)--(21)

Every product atom satisfies `mu(S)>=delta`, because every ratio
`q_i/delta_i` is at least one.  Hence

```text
mu_plus(S)=mu(S)+delta*(-1)^|S|,
mu_minus(S)=mu(S)-delta*(-1)^|S|
```

are nonnegative.  Their perturbations have total mass
`delta*(1-1)^m=0`.  If any proper coordinate set is fixed, summing over one
omitted coordinate cancels the alternating perturbation, so every proper
marginal agrees.  At the empty vertex the masses are `2delta` and zero.
All local probabilities are rational, so clearing one common denominator
does yield exact finite multisets.

The generating-polynomial difference is exactly
`2delta(1-z)^m`; hence every derivative below order `m` agrees at one while
the endpoints differ by `2delta`.  The evidence correctly labels these as
distribution-free witnesses, not actual `{Q_0ut}` product laws.

## 5. Compact-contour norm

On degree-at-most-`m` polynomials with norm
`sup_(|1-z|<=r)|H(z)|`, the test polynomial `(1-z)^m` has norm `r^m` and
endpoint value one.  Thus endpoint evaluation has operator norm at least
`r^(-m)`.  Subexponential conditioning forces `-log r=o(1)`, equivalently
`r=1-o(1)`, leaving only `exp(-o(m))` full-degree damping.  This is exactly a
no-go for universal linear continuation; it does not rule out additional
arithmetic cancellation in a phased contour integrand.

## 6. Conditional high-conductor implication

For fixed `gamma>0` and **`0<eta<4/3`**, one has

```text
X=floor(exp(gamma*k/log k)),
Y=X^(4/3-eta)>1.
```

Because `Y>1`, (13) partitions disjointly into:

1. the principal character, contributing `delta N`;
2. nonprincipal characters with `1<f_chi<=Y`, whose absolute aggregate is
   `o(delta X^2)` by the proved low-conductor theorem (18) of
   `weighted_multiplicative_character_deepening.md`; and
3. the single signed sum `H_X` over `f_chi>Y`.

The coefficients in `H_X` are exactly the endpoint coefficients of (13),
so the inherited theorem applies without a normalization conversion.  The
elementary unit sieve gives

```text
X(1-sum_p 1/p)-m <= M_X <= X,
```

and `sum_(k<p<2k)1/p=o(1)`, hence `N=M_X^2~X^2`.  Assumption
`|H_X|=o(delta N)` then yields `F_X(0)=delta N+o(delta N)>0`.

For a surviving product, `n=Q_0ut`.  Primes in `(k,k+A]` were absorbed by
`Q_0`; `V(ut)=0` handles all remaining primes.  Furthermore

```text
log Q_0 <= A log(e(k+A)/A)=o(k/log k),
ut<=X^2,
```

so `n<=exp((2gamma+o(1))k/log k)`.  Since
`Q_0=binom(k+A,A)>2k` eventually and `u,t>=1`, the strict lower bound
`n>2k` is also valid.

The estimate for `H_X` is an assumption, not a proved full-modulus theorem.
The evidence explicitly says so, keeps `closes=[]`, and does not claim an
unconditional `exp(O(k/log k))` upper bound.

## 7. Resolved structured correction

The evidence file states the required range `0<eta<4/3` at the start of
Section 6.  My initial audit found that the structured cutoff summaries had
omitted it.  The author has now added **fixed `0<eta<4/3`** to all seven
cutoff occurrences:

- the two occurrences in `decisive_lemma.json`;
- the three occurrences in `information_loss_map.json`; and
- the status evidence of `U451-M05` and `U451-M10` in `mechanisms.json`.

I checked both the current files and their diff.  `kill_tests.json`
introduces no cutoff.  The corrected artifacts now exclude `eta>=4/3`, so
`Y=X^(4/3-eta)>1`, the principal conductor remains outside `H_X`, and the
three-part decomposition in Section 6 is valid.  The structured diffs also
preserve the correct method-only scope, open status, `closes=[]`, and
`survivor_deepening` phase.  The prior mandatory correction is resolved.
