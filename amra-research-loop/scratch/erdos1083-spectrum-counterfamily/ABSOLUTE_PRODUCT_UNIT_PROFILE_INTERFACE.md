# Exact absolute product-unit profile interface

## Scope

This note reads the frozen `erdos-1083-unit-matrix-round7` campaign without
modifying it.  It makes one particular meaning of **absolute product unit**
canonical: if a nonzero positive Laurent mask is

\[
P=\sum_{a\in A}[a]\in \mathbb Z[\Gamma],\qquad \Gamma\subset\mathbb R,
\]

put

\[
u_-(P):=\min A.
\]

This is invariant under how irreducible factors are normalized, and
`u_-(PQ)=u_-(P)+u_-(Q)` whenever `P,Q` are positive masks.  Thus it is an
observable unit of the actual positive product, rather than a raw factor
unit or an associate gauge coordinate.

## Exact one-coordinate reduction

Let a centre-leaf exact block satisfy

\[
P_V=P_{A_0}F_0=P_{A_j}F_j,qquad F_j=P_{\lambda_jX}.
\]

Write

\[
v=\min V,\quad \phi_j=\min(\lambda_jX),\quad
\alpha_j=\min A_j.
\]

All factors in these two displayed products are positive masks.  Therefore

\[
\alpha_j+\phi_j=v
\]

for every leaf.  Since the centre entries `phi_0` and `alpha_0` are fixed,
the four-observable profile

\[
\Pi_j=(u_-(F_j),u_-(F_0),u_-(P_{A_j}),u_-(P_{A_0}))
      =(\phi_j,\phi_0,v-\phi_j,\alpha_0)
\]

is in bijection with the single coordinate `phi_j`.  Consequently, for
every leaf set `I`,

\[
\boxed{|\{\Pi_j:j\in I\}|=|\{\min(\lambda_jX):j\in I\}|.}
\]

This is the exact counting interface missing from the frozen wording.  The
two centre observables contribute no profile entropy, and the complement
observable is forced by the common-spectrum identity.

There are consequently two different conditioning questions which must not
be conflated.  Requiring the **literal four-vector** `Pi_j` to be constant
also requires the deterministic scalar-source unit `phi_j` to be constant.
By contrast, after recording the already known pair `(lambda_j,X)`, its
residual affine datum is

\[
\delta_j:=\alpha_j+\phi_j-v,
\]

and `delta_j=0` identically.  Under this canonical positive-mask section the
residual profile range is one on every leaf, even when the literal profile
range is power-large.  Therefore a future unit-matrix argument should state
whether it conditions the literal right sides or only the right sides after
subtracting the known scalar-copy contribution.  The latter is the relevant
entropy-free interface for solving a row-dependent affine system.

## Same-sign zero-anchor/injective dichotomy

Let `x_- = min X`, `x_+ = max X`, and restrict to a fixed sign
`sigma in {+,-}`.  Then

\[
\phi_j=
\begin{cases}
\lambda_jx_-,&\lambda_j>0,\\
\lambda_jx_+,&\lambda_j<0.
\end{cases}
\]

The power-large core proves that after restriction to one sign there is a
class `J_sigma` of at least `ceil(K/2)` leaves and its scalar magnitudes are
distinct.  Hence exactly one of the following holds.

1. **Zero anchor.**  `x_-=0` on the positive class, or `x_+=0` on the
   negative class.  Every `Pi_j` is identical.  Conditioning costs exactly
   one profile and retains all `|J_sigma| >= ceil(K/2)` rows.
2. **Nonzero anchor.**  The relevant endpoint is nonzero.  The map
   `j -> Pi_j` is injective.  The profile range has exactly `|J_sigma|`
   elements and every constant-profile fibre has size one.

At the frozen endpoint `K=t^(5/9-o(1))`, the second branch has

\[
|\{\Pi_j:j\in J_\sigma\}|=t^{5/9-o(1)}.
\]

Thus there is no unconditional `t^o(1)` profile-range theorem at the level
of these hypotheses.  A profile pigeonhole is either entropy-free or loses
the entire selected-row exponent; there is no intermediate loss on a
same-sign class.

## Normalization firewall

The theorem is about actual positive masks under the canonical minimum
support section.  If “unit profile” instead means units of independently
normalized irreducible factors, its range is not well-defined until the
normalization section and its affine cocycles are fixed.  Raw factor-unit
profiles may be inflated along the gauge found in rounds five through seven
without changing any actual product mask.

The minimum-support profile is also coordinate-origin sensitive.  Translating
the common set `X` changes the endpoint and can exchange the two branches at
the additive exact-block level, while leaving difference spaces and
normalized factor shapes unchanged.  Therefore the zero-anchor hypothesis
must be proved in the actual geometric coordinate system; it cannot be
silently imposed as an associate normalization.

## What this proves and does not prove

It proves a rigorous subpower conditioning theorem in the exact zero-anchor
range (indeed range one), and a rigorous power-large obstruction in the
nonzero-anchor range, conditional on the already selected power-large block.
It does **not** construct a new legal power-large Euclidean counterfamily,
prove that either branch occurs in every near-extremal point configuration,
control target-target distance fibres, or improve the public exponent.

The previously stored interval multirow family illustrates the zero-anchor
branch but has fewer than `sqrt(C)=t^(1/36+o(1))` leaves, so it must not be
reported as a power-large counterfamily.

## Bounded reproduction

```sh
ulimit -v 3145728
timeout 180s python3 \
  amra-research-loop/scratch/erdos1083-spectrum-counterfamily/verify_absolute_product_unit_profile.py
```

The verifier exhausts small direct tilings and checks the exact profile
identity and both branches.  Universality follows from the displayed minimum
and direct-product identities, not from the finite run.
