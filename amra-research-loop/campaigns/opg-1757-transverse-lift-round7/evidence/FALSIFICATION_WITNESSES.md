# Exact falsification witnesses

## Scope

These witnesses attack two proposed lifts of the five-variable fixed-space
theorem.  They do **not** give a point in the distinguished component with
`xi<=0`, and they do not change OPG-1757.

All values below are reconstructed directly from the 128 deletion forests and
58 marked-endpoint-connected forests by a Python standard-library verifier.

## Full-edge derivative floor

For each of the eight deletion edges `e`, exact forest enumeration gives

```text
partial_(E\{e}) P = 1+w_e.
```

The inherited derivative-component nesting theorem therefore implies
`w_e>-1` for every original edge activity throughout the distinguished
component.  In particular `b+1>0`, so the apparent `b=-1` factor in the
`q`-fibre resultant is outside the component rather than an unresolved wall.

## M702: unconditional polarization-correction domination

At the fixed base `a=b=c=d=e=1`, take

```text
(u,v,q)=(-11/10,-4/5,-37/25).
```

Average independently over the three sign flips of `u`, `v`, and `q`.  This
is the unique separately symmetric multiaffine polarization of the fixed-space
restriction.  On the ray from the origin to the displayed point, write
`s=lambda^2`.  The Bernstein coefficients of its deletion polynomial are

```text
128, 122788/1875, 478091/18750, 975607/781250.
```

All four are positive, so the whole polarized anchor segment is certified
positive.  At its endpoint the independently symmetric connectivity margin is

```text
xi_even = 523/250 > 0,
```

but the genuine graph-specific mixed correction is

```text
xi_full-xi_even = -119992/15625,
```

and hence

```text
xi_full = -174609/31250 < 0.
```

Thus the literal claim that the mixed correction is dominated by the
fixed-space/polarized margin throughout the polarized component is false.
This does not exclude a narrower estimate that also imposes inequalities from
the genuine full-`P` distinguished component; indeed full `P` is negative at
this witness.

## M703: first edge-derivative chamber

At the same fixed base, take

```text
(u,v,q)=(59/22,-21/11,29/11).
```

Exact reconstruction gives

```text
P  = 22107148/1771561 > 0,
xi = -256198/14641 < 0.
```

In edge order `01,02,04,12,13,14,23,24`, all first derivatives of `P` are

```text
257492/161051, 570544/161051, 812497/1771561,
55363774/1771561, 32507183/322102, 510341/322102,
755981/322102, 1325911/322102.
```

Every entry is positive.  Therefore `P>0` plus the complete set of eight
first-edge derivative signs cannot by itself force every `xi<0` point out of
the feasible derivative chamber.  This witness does not certify distinguished
component membership and does not rule out a stronger higher-mixed-derivative
nesting certificate.

## Reproduction

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_falsification_witnesses.py
```
