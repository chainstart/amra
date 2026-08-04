# Newton-Gram face at the second `q3:RLP` intersection corner

## 1. Scope

`RLP_ROOT_GRAM_CERTIFICATE.md` proves the normalized `q0`-chart polynomial
nonnegative on a local part of the blow-up `x=B*v*t*y`.  This note studies
the common boundary

```text
y=1, equivalently x=B*v*t,
```

where numerical subdivision next accumulates.  It proves the exact Newton
principal at the remaining double-direction corner, but not the higher-order
remainder and not the full activity chamber.

Put `A=1-a`.  On `y=1`, the 3,618-term normalized polynomial becomes a
1,743-term polynomial in `(A,B,z,v,t)`.  Its total `(A,B)` degree ranges from
4 through 9.  The issue is the common corner `A=B=0`.

## 2. Degree-four face

The exact degree-four homogeneous face has 201 terms and factors as

```text
Face[4] = L*H(z),
L = A*(1+t*v)+B*t*v >= 0,                              (2.1)
```

where `H=h0+h1*z+h2*z^2` has 114 terms.  Define

```text
S = A*(1-v+v^2+2*t*v+t^2*v)+B*t*v*(t+v).              (2.2)
```

The verifier reconstructs the following two identities without symbolic
factorization:

```text
h0 = (A+B)*S^2,

h0*h2-h1^2/4
   = A*B*(1-v)^2*(A*(1+v)+B*v)*L*S^2.                 (2.3)
```

Every factor on the right of (2.3) is nonnegative on the closed unit box.
Where `h0>0`, (2.3) implies `h2>=0`, so

```text
[[h0,h1/2],
 [h1/2,h2]]
```

is positive semidefinite.  The same conclusion holds on `h0=0` by
continuity, since the positive-semidefinite cone is closed and the set
`h0>0` is dense in the relevant direction simplex.  Thus `H(z)>=0` for
every real `z`, and (2.1) proves the full degree-four face nonnegative.

## 3. Reproduction and consequence

Run from the campaign directory:

```sh
python3 evidence/verify_rlp_intersection_newton_gram.py \
  | diff -u evidence/rlp_intersection_newton_gram.json -
```

The verifier uses only the Python standard library.  It reconstructs the
original forest polynomial, the projective and small-direction charts, the
`y=1` intersection, the exact homogeneous face, and both Gram identities.
No per-process virtual-memory limit is needed; the WSL total-memory cap is
the sole memory ceiling.

This removes the observed `(A,B)->(0,0)` leading face as a source of a
negative asymptotic direction.  The five higher `(A,B)` degrees still need a
uniform Gram, Bernstein tree, or another blow-up.  Coverage therefore
remains 63 of 81 negative-page chambers; the generic sign of `Delta_b`, the
marked-host theorem, and OPG-1757 remain open.
