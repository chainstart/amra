# Independent audit: finite-menu and canonical one-step seed switches

## Verdict

Two strictly scoped no-go statements reconstruct independently.

First, every fixed finite collection of q-independent lower-tail profiles
through a fixed rank `R`, retaining the K4,r9 `H/q` staircase, is defeated
simultaneously by one sufficiently late actual odd strip.  This includes a
fixed finite-state controller only when its reachable outputs and reset times
through `R` form such a finite q-independent profile collection.

Second, even arbitrary q-dependent lower digits cannot produce a nonnegative
surplus at a step `4<=n<=42` if that choice retains all of:

```text
the same H/q leading staircase and surplus identity,
B_(n+1)=C(B_n,2)-(20n-52),
and a canonical next word.
```

This second result is pointwise, so a growing menu does not evade it.  It
does not cover a leading-block change, a different bottom transfer, or a
terminal positive word for which canonical continuation is not required.

## Blind stable-word reconstruction

I reconstructed the full generic rank-n stable words rather than importing
either author verifier.  Their aligned Macaulay upper-shadow cancellation
was checked symbolically at generic ranks 4 through 9 and gives

```text
gamma_n=C(B_n,2)-C(A_n+1,2)+2-4q.              (1)
```

The rank does not occur in the coefficient of q.  The two bottom Pascal
identities independently give

```text
A_(n+1)=C(A_n,2)-(20n-49),
B_(n+1)=C(B_n,2)-(20n-52).                     (2)
```

These identities require the fixed leading staircase; (2) alone does not
justify (1) after an arbitrary leading-block switch.

## Finite-menu quantifier

For a q-independent profile and fixed rank, the non-q part of (1) is one
fixed integer.  Its canonical digit-order requirements are finitely many
strict lower bounds on q.  For a finite menu and fixed `R`, the union of all
profile/rank requirements is still finite.  Taking one maximum `Q`, then an
actual odd K4,r9 parameter with `q_j>Q`, makes every retained menu word
canonical and every corresponding surplus negative simultaneously.

The exact quantifiers are

```text
for every fixed R and every fixed finite q-independent menu S,
there exists one actual odd j=j(R,S) defeating every choice in S through R.
```

They do not address a menu whose values depend on q.  A finite-state
controller corollary is valid only if, after unrolling through fixed `R`, it
has finitely many q-independent lower-tail profiles and retains the same
staircase.  Controller decisions may depend on the observed state: the one
chosen q defeats every reachable option simultaneously.

## Arbitrary q-dependent one-step choice

Let `A_n(q),B_n(q)` be arbitrary legal lower digits.  Since a canonical
lower digit has `C(A_n+1,2)>=0`, (1) gives

```text
gamma_n <= C(B_n,2)+2-4q
        = B_(n+1)+20n-50-4q.
```

Canonical ordering in the next word requires

```text
B_(n+1)<q-(5n-11).
```

Therefore, pointwise for every such choice,

```text
gamma_n < -3q+15n-39.                           (3)
```

For `q>=5n-13`, the right side is at most zero, so the strict inequality
gives `gamma_n<0`.  Actual K4,r9 odd strips have `q>=q_3=300`; throughout
`n<=42`, `5n-13<=197`.  Hence (3) applies to every actual pre-rank-42 step.

No finiteness, regularity, or q-independence of the choice was used.  This is
why a q-dependent or growing menu is killed only after specifying that every
choice remains inside this same one-step lower-tail interface.

## Mechanism wording review

The original M505 and M512 wording mentioned the bottom recurrence and a
canonical next word but did not literally state preservation of the `H/q`
leading staircase/surplus identity.  That omission would make their kills
too broad: changing a leading block can invalidate (1).  Their decisive
claims have therefore been narrowed explicitly.

After narrowing, both kills are strict:

- `M505` asserts one q-dependent same-interface choice with `gamma_n>=0`
  for some `4<=n<=42`, directly contradicting (3);
- `M512` asserts that a growing menu contains such a choice, but (3) holds
  pointwise for every member, independently of menu cardinality.

M509 and M511 were likewise scoped to q-independent lower-tail profiles and
the unchanged leading staircase.  Their finite-menu kills then follow from
the simultaneous-maximum quantifier.  M506 correctly survives because a
leading-block or bottom-transfer change lies outside both no-go statements.
M510 remains frozen because no local seed persistence or public suffix
composition theorem is supplied.

## Machine reproduction and scope

The independent checker passed under

```text
ulimit -v 3145728; timeout 180s python3 audit/verify_seed_switch_no_go_independent.py
```

Its SHA-256 is
`e362c80379f1adcd4bdd07d65618ca1ddf0348d94b5f13dfa4d44c218cef0c2c`.
The bounded finite-profile replay is only a cross-check; the universal
statements follow from the symbolic identities and finite-maximum argument.
Lean was not needed.

These are exact route obstructions.  They do not analyze leading-block
switches, prove suffix persistence, improve the public main term/exponent,
or close Erdos-776.  No public promotion is justified, and external
priority remains uncertain.
