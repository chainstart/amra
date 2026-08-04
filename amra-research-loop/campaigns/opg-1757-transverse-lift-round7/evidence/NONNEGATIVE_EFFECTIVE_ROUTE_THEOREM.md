# Complete nonnegative-effective-route theorem

## Theorem

Assume

```text
q0,q3,q4,c>=0
```

and all eight edge floors are positive.  Then the exact `b=w04` Rayleigh
boundary determinant satisfies

```text
Delta_b>=0.                                    (T)
```

Indeed, on a length-two page with positive floors,

```text
(1+xL)*(1+xR)=q+1>=1.
```

Both activities cannot be negative, because then both factors on the left
would lie in `(0,1)` and their product would be below one.  Thus every page
has exactly one of the three sign types

```text
P = both activities nonnegative,
L = only the left activity is negative,
R = only the right activity is negative.
```

The resulting `3^3=27` chambers are partitioned, without overlap, by the
six exact certificates:

| Certificate | New chambers | Count |
|---|---|---:|
| `NONNEGATIVE_ROUTE_CHAMBERS.md` | direct and one-negative nonshared cases | 11 |
| `SHARED_PAGE_DISCRIMINANT.md` | `LPP,RPP` | 2 |
| `NESTED_SHARED_DISCRIMINANT.md` | `LPR,LRP,RLP,RPL` | 4 |
| `OPPOSITE_NONSHARED_CHAMBERS.md` | `PLR,PRL` | 2 |
| `SAME_SIDE_THREE_NEGATIVE.md` | `LLL,RRR` | 2 |
| `MIXED_THREE_NEGATIVE.md` | `LLR,LRL,LRR,RLL,RLR,RRL` | 6 |

The counts sum to 27, proving (T).  Every constituent verifier reconstructs
the 178-term `Delta_b` independently from the forest definitions and uses
exact integer or rational sparse-polynomial arithmetic.

## Aggregate reproduction

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 2097152
timeout 600s python3 evidence/verify_nonnegative_effective_route_theorem.py
```

The aggregate standard-library verifier reruns all six constituent
verifiers, checks their outputs against the frozen JSON evidence, verifies
that their chamber sets are disjoint, and checks equality with the full
Cartesian set `{P,L,R}^3`.

This theorem does not yet cover the four `K>0` matrix chambers with one
negative diagonal route quantity.  Therefore it does not by itself prove
the generic projected-component lemma, the full marked-host theorem, or
OPG-1757.
