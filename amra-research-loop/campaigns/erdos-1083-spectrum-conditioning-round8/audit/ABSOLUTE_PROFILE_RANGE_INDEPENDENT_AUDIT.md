# Independent audit: natural absolute product-unit profile range

Date: 2026-08-03

Verdict: **the natural-profile theorem passes, with a quantifier firewall on
the nonzero branch and no public promotion**.

## Blind reconstruction

Use the natural order inherited from `Gamma subset R`, and for every actual
positive Laurent mask set

\[
u_-(P_A)=\min A.
\]

If `P_A` and `P_B` are positive masks, every coefficient in their product is
nonnegative and the coefficient at `min A+min B` is positive.  No smaller
exponent can occur.  Hence

\[
u_-(P_AP_B)=\min(A+B)=\min A+\min B.
\]

This proof uses the actual positive products and is independent of choices of
irreducible-factor representatives.

For the exact common-spectrum identities

\[
P_V=P_{A_j}F_j,\qquad F_j=P_{\lambda_jX},
\]

write `v=min V`, `phi_j=min(lambda_j X)`, and `alpha_j=min A_j`.
Multiplicativity gives the exact affine graph

\[
\alpha_j=v-\phi_j.
\]

The centre coordinates are fixed, so

\[
\Pi_j=(\phi_j,\phi_0,v-\phi_j,\alpha_0).
\]

Projection to the first coordinate and the displayed graph map are inverse
on the image.  Therefore, for every leaf subset `I`, not merely for the full
selected family,

\[
|\Pi(I)|=|\phi(I)|
\]

and every individual fibre, hence also the maximum fibre, has exactly the
same cardinality under `Pi` and `phi`.

## Natural-order same-sign dichotomy

Let `x_-=min X` and `x_+=max X`.  Directly from multiplication by a real
scalar,

\[
\phi_j=\lambda_jx_-\quad(\lambda_j>0),\qquad
\phi_j=\lambda_jx_+\quad(\lambda_j<0).
\]

The inherited core supplies a same-sign `J_sigma` of size at least
`ceil(K/2)` whose scalars are distinct.  If its relevant natural endpoint is
zero, all profiles coincide and the range is one.  If that endpoint is
nonzero, multiplication by it is injective, so the profile range is exactly
`|J_sigma|` and every fibre is a singleton.  Conditional on the second branch
inside an actual selected block this is `t^(5/9-o(1))`.

The residual

\[
\delta_j=\alpha_j+\phi_j-v
\]

is identically zero.  It is accurate to call this particular affine residual
entropy-free after the known scalar-copy datum `(lambda_j,X)` is retained.
This is an identity defining the common-spectrum graph; it supplies no new
cross-row rigidity, quotient-shape control, target propagation, or collision
bound.

## Quantifier and normalization firewalls

The dichotomy is unconditional **inside any already obtained power-large
block**.  It does not prove that the nonzero-anchor branch is realized by a
near-extremal Euclidean configuration, and it constructs no new legal
power-large counterfamily.  Thus it does not by itself refute a hypothetical
subpower theorem on a smaller class of realizable near-extremal blocks.  Its
precise negative content is that the current identities alone leave a
power-large injective branch, so a uniform subpower proof must add a theorem
excluding or controlling that branch.

Reversing the order replaces natural minimum support by natural maximum
support and can exchange range-one with injective behaviour.  That is a valid
normalization-section warning only.  It cannot be chosen after observing the
block and cannot be presented as an actual natural-profile counterexample.
Likewise, independently normalized raw factor units remain subject to the
round-seven gauge and cocycles; their range is not this canonical actual-mask
range.

The author evidence and current survivor/decisive statements respect these
two firewalls.  The stale sign-adapted representation has been replaced by
the fixed-natural-order endpoint dichotomy.  The stronger universal
full-fibre and uniform-subpower assertions survive only as the literal
statements of killed mechanisms `M1083S8-07` and `M1083S8-08`, with matching
kill records; neither is a survivor or a dependency of the decisive lemma.
Thus the stale text is resolved and the overclaims are retained only as
falsified tests, not as conclusions.

## Scope

Passed:

- natural min-support multiplicativity for actual positive masks;
- exact affine graph, range equality and fibre equality;
- natural-order zero-anchor/injective dichotomy;
- zero affine residual, with no cross-row-rigidity inference;
- reverse-order normalization firewall.

Not proved:

- which branch occurs in every realizable near-extremal configuration;
- a new legal power-large Euclidean counterfamily;
- unconditional subpower conditioning on all realizable blocks;
- all-target occurrence, distance-fibre saving, or outer stability;
- any improvement of the public dimension-three exponent.

## Reproduction

Author verifier:

```sh
ulimit -v 3145728
timeout 180s python3 evidence/verify_absolute_profile_range.py
```

Independent verifier, which imports no author code:

```sh
ulimit -v 3145728
timeout 180s python3 audit/verify_absolute_profile_range_independent.py
```

Both completed successfully.  The finite checks guard implementations; the
universal result is the order and affine-graph proof above.
