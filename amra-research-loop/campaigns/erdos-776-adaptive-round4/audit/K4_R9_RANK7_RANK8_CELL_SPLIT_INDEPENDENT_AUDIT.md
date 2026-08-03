# Independent audit: K4,r9 rank-7/rank-8 canonical cells

## Verdict

The corrected canonical-cell split reconstructs independently from the raw
Macaulay recurrence.  The quadratic rank-7 formula is exact only at `j=33`.
For every tested actual odd member from `j=35` onward, the stable rank-7 word
gives

```text
gamma7 = 378864136937404017548365 - 4q,
```

which first becomes negative at `j=73`.  The rank-8 word changes once more:
the displayed `j=73` word is a one-member cell, while the stable word from
`j=75` gives

```text
gamma8 = 71769096623329310875999415996803170658344870942 - 4q,
```

which is positive at `j=147` and negative at `j=149`.

This independently validates the corrected author evidence and refutes the
earlier uniform rank-7 recovery interpretation.  It does not prove that this
family remains negative at every later rank.

## Independent reconstruction

The checker starts from

```text
h = 112*2^(j-1),  q = (2h+4)/3,  b = q+4,
n = C(q,2)+9,     H = C(b,2)+1,  tau = H-n,
```

constructs the two initial values, greedily recomputes every canonical
Macaulay word, and advances the orbit through ranks 3 to 8.  It does not
import the author verifier or its word constructors.

Symbolic normalization gives the genuine stable rank-5 words

```text
A = [(q-6,5),(q-11,4),(q-16,3),(q-20,2),(647801944,1)],
B = [(q-5,5),(q-10,4),(q-15,3),(q-19,2),(870476130358,1)].
```

The proposed `j=33` B word differs from the actual stable B value by exactly

```text
B_actual - B_j33_word = -2*(q-q33),
q33 = 320690891436.
```

Thus its equality at `q33` cannot be promoted along the dyadic progression.
The strict last-digit ordering thresholds are `q>647801964` for A and
`q>870476130377` for B, consistent with the transition to the stable B cell
at `j=35`.

At rank 8 the stable C word is

```text
[(q-6,6),(q-11,5),(q-16,4),(q-21,3),(q-25,2),
 (209823679001188505,1)],
```

and the eventual stable D word is

```text
[(q-5,6),(q-10,5),(q-15,4),(q-20,3),(q-24,2),
 (378864346761083666538815,1)].
```

The `j=73` D word differs from the actual eventual value by exactly

```text
D_actual - D_j73_word = q73-q,
q73 = 352603364054266842622636.
```

The stable D ordering requires
`q>378864346761083666538839`, first met by the checked progression at `j=75`.

## Sign checks

Direct exact-integer replay and the independently derived symbolic formulas
agree.  In particular,

- `gamma7(j=71)>0` and
  `gamma7(j=73)=-1031549319279663352942179<0`;
- `gamma8(j=147)>0` and
  `gamma8(j=149)=-34798731098715693576352603055425799524900210322<0`.

Both stable surplus polynomials have leading coefficient `-4`.  Positivity
at an isolated earlier cell therefore supplies no eventual recovery theorem.

## Mechanism-state review

The existing kills of `M401`--`M404` are supported exactly by this audit.
`M408-positive-leading-surplus` should also be marked **killed**: this fixed,
legal stable transition has first nonzero leading coefficient `-4` at both
ranks 7 and 8.

`M409-nearby-family-robustness` is untenable in its current wording because
its named base “K4,r9 rank-seven recovery mechanism” does not persist even on
the K4,r9 family itself.  It should be killed or rewritten as a genuinely new
bounded-cell question; it must not remain evidence for robustness.

`M405`, `M406`, and `M410` remain research candidates, not established
theorems.  The observed stable polynomial cells are compatible with `M405`,
but one fixed pair through rank 8 proves neither a finite transducer for every
fixed pair (`M405`), a uniform finite recovery rank (`M406`), nor an all-rank
negative recurrence (`M410`).  `M407`, `M411`, and `M412` lack their claimed
inductive, finite-tree, and composition interfaces and should remain frozen
or candidate rather than promoted.

## Scope and promotion boundary

The result concerns one actual dyadic family with fixed `(k,r)=(4,9)` and
only the explicitly reconstructed ranks.  It proves failure of the proposed
uniform rank-7 recovery route and supplies negative stable-leading-coefficient
examples.  It does not establish infinite all-rank nonrecovery, classify
nearby `(k,r)` pairs, close the adaptive recovery tree, or compose a legal
persistent seed into the public construction.  No public theorem promotion
is justified.

Both the author verifier and the independent checker passed under a 3 GiB
virtual-memory limit and a 180-second timeout.  Lean was not needed for this
exact arithmetic audit.
