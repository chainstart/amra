# Blind audit: full W4 spoke distinguished component

## Verdict

PASS for the exact four-stabilizer-variable marked-spoke instance.  This
does not prove the global fixed-edge/moving-edge statement or OPG-1757.

## Independent reconstruction

The audit starts from the seven edges of `W4-01`, not from the author's
polynomial.  It independently enumerates every edge subset, rejects cycles
with a disjoint-set implementation, and uses the complement-of-forest
monomial defining the `C` polynomial.  It obtains 86 forests and 38 forests
connecting the marked endpoints, hence `P(1)=86` and `xi(1)=38`.

After the shift `x=a+1,y=b+1,z=c+1,w=d+1`, coefficients recovered from
those reconstructed polynomials give

`P=A*z^2-H` and `xi=C*z+E`.

Independent factorization verifies

`H*C^2-A*E^2=4(w-1)^2(x-1)^4(y-1)^2 J`.

No author-side polynomial or factorization is imported by the checker.

## Sign and component audit

On the proposed base `x,w>0`, `r=wx>1`, `y(r+1)>2`, both factors of
`A=(r-1)(y(r+1)-2)` are positive.  With `x=r/w`, the independently reduced
lower-boundary values and slopes are

`J=2(r-w)^2/(r+1)`, `dJ/dy=(w+1)^2`,

`C/2=(r-1)(r-w)^2/(w(r+1))`,
`d(C/2)/dy=(r(w^2+1)-2w)/w`.

The last numerator exceeds `(w-1)^2` by
`(r-1)(w^2+1)`, so `C,J>0` in the open base.  The boundary identity then
gives `H>=0`.  Equality would force `E=0` and one of `w=1,x=1,y=1`; direct
substitution gives respectively `H=A>0`, `H=A>0`, or
`H=(w+x-2)^2>0` (strict because `wx>1`).  Thus `H>0`.

The base is connected in `(log x,log w,y)` coordinates and its `z` fibre
is the interval `z>sqrt(H/A)`, so the proposed set is connected and contains
the shifted all-positive anchor.  Every possible first exit is blocked:

- at `wx=1`, the not-yet-crossed second wall implies `y>=1`, and the exact
  formula for `H` is nonnegative;
- at `y(wx+1)=2`, `H=2(w-1)^2(x-1)^2/(wx+1)>=0`;
- at `z=sqrt(H/A)`, `P=0`, while at `z=0`, `P=-H<0`;
- reaching `x=0` or `w=0` first requires crossing `wx=1`.

Therefore this is exactly the anchor positivity component.

Finally, if `E>=0`, `xi=Cz+E>0`.  If `E<0`, the boundary identity gives
`C*sqrt(H/A)>=-E`, and the component's strict inequality
`z>sqrt(H/A)` again gives `xi>0`.

## Reproduction and scope

The checker runs in under one second with a 3 GiB/180-second bound and no
Lean process:

```sh
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  audit/verify_full_spoke_distinguished_component_independent.py
```

The certificate closes G202 only.  Together with the separately audited rim
certificate it proves both W4 edge orbits in their stabilizer-variable
specializations, but it supplies no fixed edge for an arbitrary graphic
matroid and does not close the campaign contract.
