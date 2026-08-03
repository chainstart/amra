# Exact transverse expansion ledger

## Coordinates and reconstruction

Use independent activities on the eight deletion edges and write

```text
w01=a+u,  w02=a-u,
w13=d+v,  w23=d-v,
w14=e+q,  w24=e-q,
w04=b,    w12=c.
```

An exact standard-library enumeration reconstructs 128 deletion forests and
58 forests connecting the marked endpoints `0,3`.  After the substitution it
has 155 nonzero terms for `P` and 38 for `xi`, grouped into respectively 10
and 8 transverse monomial classes.

The only graph symmetry is the simultaneous vertex swap `1<->2`, which sends

```text
(u,v,q) -> (-u,-v,-q).
```

Accordingly every transverse monomial has even **total** degree.  Individual
evenness in `u`, `v`, or `q` is false: mixed terms survive.  This is the first
exact obstruction to treating the full polynomial as three independent
symmetric polarizations of the five-variable theorem.

## Positive-anchor transverse fibre

At `a=b=c=d=e=1`, exact expansion gives

```text
P = 128
    -48u^2-38v^2-48q^2-6uq
    +14u^2v^2+14u^2q^2+14v^2q^2+2uv^2q
    -4u^2v^2q^2,

xi = 58
     -10u^2-20q^2+8uv-4uq+2vq
     -4uvq^2-2u^2vq.
```

The transverse Hessians at the anchor are

```text
H_P  = [[-96,  0, -6], [ 0,-76, 0], [-6,0,-96]],
H_xi = [[-20,  8, -4], [ 8,  0, 2], [-4,2,-40]].
```

`H_P` has eigenvalues `-102,-90,-76`, while `H_xi` is indefinite.  Thus `P`
has a strict local transverse maximum, but neither coordinatewise transverse
concavity nor a common Hessian-sign proof is available for `xi`.

## Exact ray reduction and near-contact wall

For a direction `(U,V,Q)` and `s=t^2`, write `P=-2B_P(s)` and
`xi=-2B_xi(s)`.  Exact substitution gives

```text
B_P = 2Q^2U^2V^2 s^3
    +(-7Q^2U^2-7Q^2V^2-QUV^2-7U^2V^2)s^2
    +(24Q^2+3QU+24U^2+19V^2)s-64,

B_xi = (2Q^2UV+QU^2V)s^2
      +(10Q^2+2QU-QV+5U^2-4UV)s-29.
```

On the symmetric direction `(U,V,Q)=(1,1,k)`, the verifier independently
checks

```text
Res_s(B_P,B_xi)
 =-4k(6k^2+k-14)^2(224k^3+148k^2-73k-42).
```

The squared factor, especially

```text
k=(-1-sqrt(337))/12,
```

explains the near-zero wall gap seen by numerical routing.  It is an exact
common-wall contact, not a transverse counterexample.

A discovery-only scan of 100,000,000 random directions found no direction in
which the first `xi` zero preceded the first `P` zero.  It repeatedly
approached the squared symmetric factor above.  This scan is finite routing
evidence only and is not used as proof or as a component certificate.

## Status

- Exact eight-variable reconstruction and transverse expansion: proved by
  enumeration.
- Independent-pair polarization route: obstructed by the displayed mixed
  terms.
- Pure Hessian-sign route: obstructed by the indefinite `xi` Hessian.
- Complete anchor-ray order: suggested, not proved.
- Full transverse component domination or counterexample: open.
- OPG-1757: unchanged.

Reproduce the exact ledger with only Python's standard library:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_transverse_expansion.py
```
