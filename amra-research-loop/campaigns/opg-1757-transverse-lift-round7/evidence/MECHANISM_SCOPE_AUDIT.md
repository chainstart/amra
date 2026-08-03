# Mechanism closure and falsifiability audit

## Audit rule

A mechanism survives this campaign only if its stated claim, by itself or by
dependencies already named in the mechanism, can satisfy the frozen closure
contract and has a finite first kill test.  Rejecting a mechanism for scope or
specification does not assert that its mathematical subclaim is false.

## M704: one fixed anchor is underquantified

M704 quantifies rays only from `a=b=c=d=e=1`.  The closure contract quantifies
all eight activities in the distinguished component, including every point of
the five-dimensional fixed base.  Even a proof of first-wall order on every
ray from this single anchor would leave all other base fibres untouched.  The
closure contract already records that a complete anchor-ray theorem alone is
not the eight-variable component statement.

**Disposition:** kill the mechanism for closure mismatch.  The anchor-ray
claim remains open and may still be useful as routing evidence.

## M705: anchor-fibre star-shapedness has the same mismatch

M705 can at most combine with M704 to turn ray order into domination on the
single transverse fibre over `a=b=c=d=e=1`.  It supplies no transport between
different fixed-base points.  Therefore its stated closure effect cannot meet
the frozen all-base quantifier.

**Disposition:** kill the mechanism for closure mismatch.  No claim is made
about whether the distinguished anchor fibre is star-shaped.

## M707: “low degree” has no finite complement

The decisive claim and kill test do not freeze a multiplier degree, monomial
support, denominator class, or Positivstellensatz ansatz.  Failure of any
bounded search would therefore leave the stated existential untouched.  This
violates the fail-closed requirement that a first kill test be finite rather
than promised.

**Disposition:** kill the current mechanism specification.  A replacement may
be opened after fixing an exact degree and multiplier ansatz.

## M708: a P-positive retraction does not transport xi sign

The claimed retraction provides a path inside `P>0` from a point to the fixed
space.  Fixed-space positivity of `xi` at the endpoint does not imply
positivity at the starting point: a second continuous polynomial may cross
zero along a path on which `P` never vanishes.  M708 names no monotonicity,
nonvanishing, winding, or boundary-barrier invariant for `xi`.

**Disposition:** kill the stated closure mechanism as a conditional bridge.
The topological retraction claim itself may still be true.

## M711: the CAD promise is not yet a bounded mechanism

M711 freezes neither a projection order nor a projection operator, degree/cell
budget, exceptional-section policy, or a completeness certificate identifying
the distinguished component.  The exact symmetric-ray resultant already has
a squared common-wall factor, so singular sections cannot simply be discarded.
“Run a bounded CAD and inspect what remains” is a representation-search action,
not yet a decisive finite claim with a falsifiable complement.

**Disposition:** kill the current mechanism specification.  A concrete CAD
certificate schema with frozen bounds can be proposed as a new mechanism.

## Survivors after this audit

- `M706`: all-base quadratic-fibre wall order.
- `M709`: exact asymmetric counterexample plus component path.
- `M712`: mixed-channel factorization with higher derivative nesting.

These are mutually distinct proof, refutation, and algebraic-factorization
routes.  None is proved, and OPG-1757 is unchanged.
