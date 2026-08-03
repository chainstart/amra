# Exact `c=0` q-fibre containment theorem

## Theorem

Write the eight deletion-edge activities as

```text
w01=a+u,  w02=a-u,  w04=b,  w12=c,
w13=d+v,  w23=d-v,  w14=e+q,  w24=e-q.
```

Let `(a,b,0,d,e,u,v)` be in the projection of the distinguished Gårding
component `C_P`.  Then the nonempty q-fibre

```text
I={q:P(a,b,0,d,e,u,v,q)>0}
```

is a single open interval and

```text
xi_03(a,b,0,d,e,u,v,q)>0
```

for every `q` in `I`.

This discharges the `c=0` exceptional wall in the round-7 quadratic-fibre
route.  It does not classify `u=0`, the remaining linear-factor walls, or
the general resultant chambers.

## 1. Three component signs from fifth derivatives

Put

```text
A0=w01*w02+w01+w02,
D0=w13*w23+w13+w23,
E0=w14*w24+w14+w24.
```

A fresh graph-level enumeration gives, after setting `c=0`,

```text
partial_(04,13,14,23,24) P = A0,
partial_(01,02,04,14,24) P = D0,
partial_(01,02,04,13,23) P = E0.
```

Each displayed derivative is nonzero and positive at the all-one anchor.
The inherited derivative-component nesting theorem therefore makes all
three positive at every point of `C_P` on this wall.  The full-edge floor
from `FALSIFICATION_WITNESSES.md` also gives `1+w_ij>0`.

For example,

```text
A0=(1+w01)(1+w02)-1>0.
```

Both shifted factors are positive and have product greater than one.  Their
arithmetic mean is therefore greater than one, so

```text
a=(w01+w02)/2>0.
```

The identical argument applied to `D0` and `E0` gives

```text
a>0,  d>0,  e>0.                              (1.1)
```

For `e`, it is enough to use any one q-value witnessing that the base lies in
the projection of `C_P`, because the mean of `w14=e+q` and `w24=e-q` is the
base coordinate `e`.

## 2. Boundary sign

On `c=0`, both q-linear coefficients vanish:

```text
P=P2*q^2+P0,  xi=X2*q^2+X0.
```

The exact coefficient identities are

```text
X2=-4*a*d*(b+1),

Delta0=P2*X0-X2*P0
      =-4*d*e*(a^2-u^2)^2*(b+1)*(d^2+2*d-v^2).
```

The last factor is precisely

```text
d^2+2*d-v^2=D0>0.
```

Together with (1.1), the edge floor `b+1>0`, and the square factor, this
proves

```text
X2<0,  Delta0<=0.                              (2.1)
```

The inherited q-fibre derivative identity gives `P2<0` throughout `C_P`.
Because the base is in the projection, `P>0` for at least one q-value; hence
the even, strictly concave P-quadratic has two distinct roots `q_-<q_+` and
`I=(q_-,q_+)`.  At either root,

```text
xi(q_-)=xi(q_+)=X0-X2*P0/P2=Delta0/P2>=0.      (2.2)
```

## 3. Strict interior positivity

By (2.1), `xi` is a strictly concave q-quadratic.  It lies strictly above the
chord joining its values at the two distinct endpoints of `I`; both endpoint
values are nonnegative by (2.2).  Therefore `xi>0` at every interior point.

The whole interval is also in `C_P`: it contains the projected-component
witness, and every other point of `I` is joined to it by the q-line segment
on which `P` stays positive.  No global convexity of a Gårding component is
used.

## Reproduction and scope

The verifier reconstructs the 128 deletion forests and 58 marked-connected
forests directly in the eight original edge variables, independently repeats
the transverse substitution, and checks every displayed polynomial identity
using only Python's standard library:

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_c_zero_fibre.py
```

Mathematical status: author-verified exact algebra plus the named Fang--Ma
Gårding/derivative-nesting dependency inherited from round 6.  Independent
reconstruction and novelty review have not started.  The full eight-variable
host theorem and OPG-1757 remain open.
