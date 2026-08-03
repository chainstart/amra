# Independent audit: gauge-invariant width profile

Verdict: **pass as an exact local profile/no-go theorem; no distance-exponent
promotion**.

## Blind reconstruction

Let all Laurent exponents lie in the common additive group `Gamma` inside
the naturally ordered reals.  For a nonempty finite actual mask `A`, write
`e(A)=(min A,max A)` and `wd(A)=max A-min A`.

1. The diagonal monomial action is
   `(l,r)->(l+c,r+c)`, `c in Gamma`.  Equal widths imply the unique
   translation `c=l'-l in Gamma`, and translation preserves width.  Thus
   width completely classifies the endpoint orbit; no coordinate reversal
   or data-dependent order choice is involved.
2. For positive masks, support of the product is the Minkowski sum at both
   extremes, so its endpoints and width add.  Applying this only to the
   actual positive masks avoids any choice of associates for signed factors.
3. Put `D=wd(X)>0`, `W=wd(V)`, and `d_j=wd(lambda_j X)=|lambda_j|D`.
   The two actual identities `P_V=P_Aj F_j=P_A0 F_0` give

   ```text
   Psi_j=(d_j,d_0,W-d_j,W-d_0).
   ```

   This is a one-dimensional affine graph: only `d_j` varies.

The inherited power-large core supplies distinct nonzero row scalars and,
after one sign pigeonhole, a fixed-sign class `J_sigma` of size at least
`ceil(K/2)=t^(5/9-o(1))`.  On one fixed sign, distinct scalars have distinct
absolute values.  Since `D>0`, `d_j` and hence `Psi_j` are injective on this
*already selected actual block*.  Its exact literal range is `|J_sigma|`
and every literal fibre is a singleton.

## Four fixed-natural-order branches

Let `x_-=min X`, `x_+=max X`.

```text
lambda>0: phi=lambda*x_-, d=lambda*D;
lambda<0: phi=lambda*x_+, d=-lambda*D.
```

For positive rows with `x_-=0`, and negative rows with `x_+=0`, `phi` is
constant while `d` is injective.  In the other two cases the relevant
endpoint is nonzero and `d` is respectively `(D/x_-)*phi` or
`(-D/x_+)*phi`.  Thus width repairs exactly the zero-anchor loss and is a
fixed nonzero multiple of the round-8 coordinate otherwise.  These are
exhaustive sign/anchor branches in the fixed natural order.

## Residual and divisor checks

Once the row datum `(lambda_j,X)` and common `W` are retained, all four
residuals are identically zero:

```text
wd(F_j)-d_j,
wd(F_0)-d_0,
wd(P_Aj)+d_j-W,
wd(P_A0)+d_0-W.
```

Also `F_j=G R_j` gives `a+b_j=wd(F_j)=|lambda_j|D`.  The divisor atlas and
first width coordinate are therefore the same coordinate up to the fixed
summand `a`, not independent information.

## Ten audit checks

- endpoint orbit quotient: passed in the common exponent group;
- positive-mask endpoint/width additivity: passed;
- four-width affine graph: passed;
- positive zero-anchor branch: passed;
- positive nonzero-anchor branch: passed;
- negative zero-anchor branch: passed;
- negative nonzero-anchor branch: passed;
- residual range one and `a+b_j` identification: passed;
- fixed natural order and actual power-large-block quantifiers: passed;
- statement/dependency/promotion firewall: passed.

The author's theorem matches this reconstruction.  One wording nuance is
important: the result is unconditional only *inside an already obtained
power-large simultaneous-switch block*.  It neither constructs such a block
in every near-extremal configuration nor turns widths into new target-target
Euclidean distances.

## Scope and decision

No all-target occurrence, target-distance collision saving, or outer
stability inequality is present.  Literal injectivity is conditioning cost,
while the known-source residual is zero.  Consequently the public
dimension-three `3/5` exponent is unchanged.  External novelty/priority is
not established; classify it as `priority_uncertain` and freeze the campaign
as a scoped local no-go/diagnostic theorem.

Independent bounded reproduction (imports no author code):

```sh
ulimit -v 3145728
timeout 180s python3 audit/verify_width_profile_independent.py
```
