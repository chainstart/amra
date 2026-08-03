# AMRA four-problem mechanism-first round — 2026-08-03

## Operating contract

- Persistent wall-clock budget: four hours, continued from the recorded
  `round-2026-08-03` checkpoint.
- Four problem lanes ran in parallel with author-swapped reconstruction where
  a scoped theorem survived.
- Python probes used a 3 GiB virtual-memory ceiling and 180-second timeout for
  heavy checks.  No Lean rebuild was performed.  The exact identities in this
  round were small enough for integer/SymPy reconstruction, so Lean was not
  needed merely to duplicate those checks.
- No result below is promoted to a public AMRA theorem unless its original
  closure contract was met.  None of the four public contracts was met.

## OPG-1757

The main campaign accumulated independently audited component theorems for
W4, K3,3, two triangular-prism reductions, and the K5-e high-triangle slice.
The new marked-cross-edge campaign reconstructs five fixed-space orbits.  On
the natural `a=d=e=1` slice,

```text
P  = 54bc+27b+32c+15,
xi = 2(11bc+6b+8c+4).
```

With `x=54b+32`, `y=c+1/2`, the distinguished component is
`x>0,y>0,xy>1`, and

```text
54xi = 22xy+x+160y-32
     > x+160/x-10
     = (x-5)^2/x+135/x > 0.
```

An independent graph-definition enumeration reproduced 128 forests and 58
endpoint-connected forests.  The five-variable fixed space, three transverse
directions, G201 and OPG-1757 remain open.

A second natural cross-edge slice, `a=c=d=1`, was also closed.  Its anchor
component is the epigraph above the upper `A(e)` wall, and the identity
`A xi/2=D P+Q` has `disc(Q)=-9552`, with `D,Q>0` throughout that component.
The independent audit caught and repaired one reversed integer comparison in
the author text before certifying the theorem.

A third natural slice, `c=d=e=1`, has the parallel exact certificate
`A xi/2=D P+a^2(120a^2+48a+5)`.  The quadratic discriminant is `-96`, and a
fresh graph-level audit again reproduces the 128/58 forest counts.  These
three cross-edge slice theorems sharpen the fixed-space map but still do not
control its remaining variables or transverse directions.

## Erdos-776

The complete legal `(++ -> ++)` gamma4-negative branch now has an audited
rank-five recovery theorem.  The adjacent-sum kernel was proved analytically
for the high and asymptotic low regions and exactly for all 1,434,006 remaining
low-region pairs.

A different actual K4,r9 family then refuted the uniform fixed-rank waiting
route: for every fixed `R>=4`, some later odd member has negative surplus at
every rank `3,...,R`.  The quantifier is `forall R exists j_R`, not one member
for all ranks.

The follow-up reset analysis proves two route obstructions.  A fixed finite
menu of q-independent constant tails can be defeated simultaneously through
any fixed rank.  More strongly, any q-dependent reset that retains the same
bottom recurrence and has a canonical next word satisfies

```text
gamma_n < -3q+15n-39,
```

and is negative for `q>=5n-13`.  Thus a viable persistent seed must change a
leading block or the bottom recurrence.  Adaptive switching, suffix
persistence and the public antichain interface remain open.

For the one remaining leading-block/bottom-recurrence interface, an affine
slope ledger gives the necessary budget `alpha+delta>=3`.  A leading-only
switch therefore needs slope improvement at least three; a bottom-only
switch needs transfer slope at least three.  Equality is not sufficient, and
no legal Macaulay switch at that budget was constructed.

## Erdos-809

The output-expansion campaigns proved a fixed-graph joint-legality lemma and
an explicit two-output matching certificate, then exhausted the bounded
mode-2 and mode-3 models.  Mode 2 covered `3,876 x 496` cases and mode 3
covered `969 x 4,960`; neither produced an unprotected candidate.  The unique
unprotected base configuration has 93 traces, 21 singleton traces and exact
transversal number 21.

The final short campaign explains the number 21 structurally.  The singleton
kernel is the disjoint union

```text
R x (P union U union W),  P x Q,  U x W,  K2(W),
```

with block sizes 12, 4, 4 and 1.  An author-swapped enumeration of every
canonical seven-cycle reproduced 68,508 present cycles, 93 traces and exact
transversal number 21.  These remain finite-model facts: the missing interface
is a structural lift to arbitrary legal exchanges and the public asymptotic
main term.

## Erdos-1083

The unit-matrix campaigns realized the actual common-X aggregate matrix and
its gauge/spectrum kernels.  In the natural minimum-support normalization,
the four-coordinate profile is an affine graph over

```text
phi_j = min(lambda_j X),
```

so it has exactly the same range and fibres as `phi_j`.  On a power-large
same-sign class there is a sharp dichotomy: a zero relevant endpoint gives
literal range one, while a nonzero endpoint makes the profile injective with
range at least `K/2=t^(5/9-o(1))`.  The residual after scalar-copy subtraction
is identically zero, so it supplies no cross-row rigidity.  No unconditional
branch choice, all-target fibre theorem, counterfamily or exponent gain was
obtained.

## Research-loop conclusion

The strongest transferable lesson is negative but operational: bounded-rank
waiting and same-interface reset menus for Erdos-776 are now closed by exact
coefficient arguments; profile enrichment for Erdos-1083 must add information
not already affine-determined by one minimum coordinate; and OPG stabilizer
positivity must next confront transverse directions rather than accumulating
more equalized slices.  For Erdos-809, further finite census work has sharply
diminishing value until the trace obstruction is expressed as an arbitrary-
size structural lemma.

All campaign packages retain their exact scope, machine evidence, independent
audit status, and freeze decision.  There was no public theorem promotion.

## Concrete next attempts

1. **OPG-1757:** stop treating further unit slices as the main route.  Write
   the full five-variable cross-edge pair as `P=A_b b+C_b` and
   `xi=D_b b+E_b`; compute the four-variable determinant
   `A_b E_b-D_b C_b`.  The closing exploratory probe already finds
   `2a^2 R(a,c,d,e)`, where `R` has total degree 10, 41 terms and all-positive
   coefficients, and all three audited certificates are its restrictions.
   The next task is to classify every `A_b=0` anchor barrier and decide whether
   the complete real anchor component stays in a sign chamber where this
   determinant is positive.  Only after that should transverse perturbations
   be added one at a time.
2. **Erdos-776:** enumerate exact legal Macaulay transitions starting at the
   newly proved budget boundary `alpha+delta>=3`.  Reject a candidate as soon
   as a digit order or canonical-next-word inequality fails; demand a suffix
   persistence identity before treating any terminal positive surplus as a
   seed.
3. **Erdos-809:** replace additional locked-instance censuses by a quantified
   block-kernel lemma.  The first falsification target is whether every hard
   natural-switch branch forces a singleton kernel analogous to the
   `12+4+4+1` decomposition; one exact counter-branch would redirect the
   route immediately.
4. **Erdos-1083:** any new conditioning observable must not be an affine graph
   over `min(lambda_j X)`.  Test gauge-invariant two-endpoint information
   (for example a fixed-order support width together with one endpoint) and
   require a theorem controlling both the zero-anchor and injective branches,
   rather than selecting a normalization after seeing the block.
