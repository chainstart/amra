# Exact absolute product-unit profile interface

## Scope and canonical observable

Work in the actual power-large exact block

```text
P_V=P_A0 F_0=P_Aj F_j,       F_j=P_{lambda_j X}.
```

The exponents lie in a finitely generated subgroup `Gamma` of the additive
reals.  For an actual positive Laurent mask `P_A`, define its canonical
absolute product unit by

```text
u_-(P_A)=min A.
```

This does not depend on how irreducible factors are normalized.  For positive
masks, `u_-(P_A P_B)=min(A+B)=min A+min B`.

The selected leaf set has `K=t^(5/9-o(1))` rows.  The core supplies a
same-sign class `J_sigma` with `|J_sigma|>=ceil(K/2)` and distinct scalars.

## 1. Exact one-coordinate counting interface

Put

```text
v=min V,       phi_j=min(lambda_j X),       alpha_j=min A_j.
```

Positivity and the literal common spectrum give

```text
alpha_j+phi_j=v.
```

The centre values `phi_0` and `alpha_0` are fixed.  Hence the complete four
product-observable profile is

```text
Pi_j=(u_-(F_j),u_-(F_0),u_-(P_Aj),u_-(P_A0))
    =(phi_j,phi_0,v-phi_j,alpha_0).
```

Projection to the first coordinate is a bijection from `Pi(I)` to `phi(I)`
for every leaf set `I`, and it preserves every fibre exactly.  Therefore

```text
|Pi(I)|=|{min(lambda_j X):j in I}|,
max_p |Pi^{-1}(p)|=max_a |{j:phi_j=a}|.
```

This is the exact counting interface missing in round seven.  The two centre
observables contribute no leaf entropy, and the complement unit is forced by
the source unit and common total.  The four rows do not give four independent
leaf-varying coordinates.

There is also an entropy-free **residual** profile.  Since `(lambda_j,X)` is
already part of the scalar-copy row data, define

```text
delta_j=alpha_j+phi_j-v.
```

Then `delta_j=0` on every actual leaf.  Thus conditioning the literal right
sides and solving after subtracting the known scalar-source contribution are
different operations: the latter residual range is identically one.

## 2. Exact zero-anchor/injective dichotomy

Let `x_-=min X`, `x_+=max X`.  Under the fixed natural order,

```text
phi_j=lambda_j*x_-   if lambda_j>0,
phi_j=lambda_j*x_+   if lambda_j<0.
```

On the selected same-sign class exactly one of the following occurs.

1. **Zero anchor.**  The relevant endpoint is zero.  Every literal `Pi_j` is
   equal, its range is one and conditioning retains all of `J_sigma`.
2. **Nonzero anchor.**  The relevant endpoint is nonzero.  Distinct scalars
   give distinct `phi_j`, so `Pi` is injective.  Its range is exactly
   `|J_sigma|` and every literal constant-profile fibre has size one.

At the power-large endpoint, branch 2 has

```text
|Pi(J_sigma)|=|J_sigma|>=K/2=t^(5/9-o(1)).
```

Consequently no unconditional `t^o(1)` range theorem for the literal complete
profile follows from the existing hypotheses.  Literal profile pigeonholing
is all-or-nothing on the same-sign class: zero cost in branch 1 and loss of
the entire selected-row exponent in branch 2.  This is conditional on the
already selected actual power-large block; it is not a newly constructed
power-large Euclidean counterfamily and it does not prove which branch every
near-extremal configuration occupies.

## 3. Normalization firewall

The theorem above uses actual positive masks and their natural minimum
support, not independently normalized factor representatives.  If a factor
unit profile is used instead, its normalization section and affine cocycles
must first be fixed.  Such raw factor units can move along the round-seven
gauge without changing any actual product mask.

Reversing the exponent order or translating `X` can change which endpoint
appears and can exchange the two range branches.  That observation is only a
normalization/coordinate warning.  It is not permission to reverse the order
after seeing the data in order to claim an actual natural-profile
counterexample.  A zero-anchor hypothesis must be proved in the actual
geometric coordinate system.

## 4. Exact conclusion and remaining gaps

Proved:

- the exact complete-profile count and fibre formula;
- the zero-anchor range-one theorem;
- the nonzero-anchor power-large injectivity theorem;
- the identically zero residual profile after subtracting known scalar-copy
  data;
- the normalization firewall between actual positive-product units and raw
  factor gauges.

Not proved:

- an unconditional choice between the two branches;
- a new legal power-large Euclidean counterfamily in the nonzero branch;
- that residualization alone supplies the cross-row rigidity needed later;
- all-target occurrence mass, collision-fibre saving or outer stability;
- any improvement to the public dimension-three `3/5` exponent.

## 5. Bounded reproduction

```text
ulimit -v 3145728; timeout 180s python3 evidence/verify_absolute_profile_range.py
```

The checker verifies the affine fibre identity, minimum-support product rule,
both natural-order sign branches and the residual identity.  The universal
claims follow from the proof above, not finite extrapolation.
