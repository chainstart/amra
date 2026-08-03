# Initial falsification of typed conversion mechanisms

Date: 2026-08-03  
Status: **nine current mechanisms killed; three bounded survivors; no closure**

## Evidence boundary

The exact finite guard is `minimal_conversion_falsification.py`, with output
`minimal_conversion_falsification.json`.  It was run under the campaign's
5 GiB / 1800 second Python limit and exited `0` in under one second.  No Lean
process was started.

The three-colour/two-token data are inherited from the independently audited
`ab4b524` fourteen-vertex graph:

```text
D_B=3
full common B reserve={bc,cz}
M_B=rho_B=2
distinct owned A atoms={x1y1,x2y2,x3y3}
no missing-B atom outside the full reserve
```

Other tests below are exact typed-incidence countermodels.  They kill claims
made from the current data alone.  They do not refute a strengthened theorem
that introduces new graph-specific conversion adjacency or a proved slack
atomization.

## Killed typed-injection mechanisms

### `M809C-01`: killed

The tight circuit needs one additional B carrier.  Its complete B reserve
already consists of the only two missing B edges, so the right side of the
claimed new-B conversion graph is empty.  Its matching number is zero rather
than `|T|-rho_B(T)=1`.  The three distinct A owners cannot manufacture a
third B edge.

### `M809C-02`: killed in its coherence-only form

For every `t`, take distinct owner atoms `a_1,...,a_t` and give each the same
singleton typed target `{q}`.  Every total map has congestion `t`.  The Python
guard checks `2<=t<=12`; the displayed construction is all-parameter.  Thus
coherence, distinct ownership and a carrier relation alone do not give an
absolute congestion bound.  A future hard-graph theorem that proves expansion
of the target neighbourhood is not refuted.

### `M809C-03`: killed as a closure mechanism

The conditional matching statement is true: an actual unused target reached
by an alternating path augments a matching.  The tight graph has neither an
unused B carrier nor a proved conversion arc, so the condition does not fire
on the first unresolved circuit.  It cannot be the decisive payment mechanism
without separately proving one of the surviving conversion theorems.

### `M809C-04`: killed

On the tight graph there is no new-B transversal, while the merged whole
rectangle has the actual endpoint `M_B=2<D_B=3`.  The scalar rectangle
transference cannot be applied a second time to turn the three diagonal A
atoms into an extra B edge.  Hence the proposed transversal-or-merge
dichotomy misses its first exact circuit.

## Killed slack and outer-charge mechanisms

### `M809C-06` and `M809C-07`: killed without new slack geometry

Take two uncancelled outer demands with the same sole proposed slack carrier.
Both singleton tests have rank one, but

```text
rho_S({u1,u2})=1<2
maximum matching size=1.
```

The inherited colourwise cancellation identity supplies no theorem excluding
this owner pattern.  Thus neither disjoint per-colour injections nor the
universal Hall inequality follows from that ledger.  Both mechanisms could
be reconsidered only after `M809C-05` constructs graph-specific carriers and
owner neighbourhoods.

### `M809C-09`: killed in its direct-charge form

An owned diagonal is a **missing** A edge.  The term
`e(G[A_<q*])` consists of **present** internal-low edges.  These are disjoint
carrier types; placing both endpoints below `q*` does not define an injection
between them.  The mixed-high identity likewise supplies an anchor count, not
a map from missing diagonals to anchors.  This version repeats the forbidden
scalar conversion at a finer coordinate.

### `M809C-10`: killed from the current normal form

The exact hardness normal form has an independent Branch-A outer residue.  A
minimal typed blocker may therefore consist of one uncancelled outer demand,
zero available slack carriers, and no repeated-B owned rectangle.  Current
hypotheses do not imply that every blocker contains the proposed rectangle.
This is a route obstruction, not a graph-realizable public counterexample; a
future theorem forcing such a rectangle from the complete hard graph would be
new information.

## Killed recursion

### `M809C-12`: killed as a typed-incidence recursion

Let two tight circuits have colour sets `{c1,c2}` and `{c2,c3}`, and let both
share their only B carrier `q` and their only A owner `a`.  Each has deficit
one.  Their merge has three colours, one B carrier, one distinct A owner, and
deficit two.  No new carrier appears, and counting `a` in both children is
double spending.  Hence the proposed lexicographic ascent is not monotone on
the typed data it names.  Extra graph geometry may still provide a new atom,
but that is precisely the missing decisive lemma.

## Survivors

### `M809C-05`: graph-specific `S_m` atomization

No countermodel was found to a genuinely new decomposition of `S_m` into
nonnegative, carried, pre-owned atoms.  The tight/paid graph pair warns that
the atomization cannot depend only on `(n,e,|B|,rho_A)` and cannot exchange an
A edge for a B edge anonymously.

### `M809C-08`: direct outer-A compatible-edge exit

No example satisfying the complete hard outer-A gate was found with
`R_A>S_m` but without the proposed large compatible-colour family.  The n=14
graph is only hard-local and does not test this claim.  This route survives
because it avoids A-to-B fungibility entirely.

### `M809C-11`: typed min--max after explicit ranks exist

On the tight circuit with no conversion arcs, the sound typed oracle reports
deficit one despite `rho_A+rho_B=5`; it passes the anti-smuggling test.  It is
only a framework: it becomes decisive after an explicit conversion rank and
slack rank are constructed, and cannot itself supply them.

## Disposition

- Killed: `M809C-01,02,03,04,06,07,09,10,12`.
- Surviving: `M809C-05,08,11`.
- Kill ratio among nine non-survivors: `9/9`.
- The survivors are not proved and do not imply one another automatically.
- Erdős #809, the `n^2/8` main term, and the global interface remain open.

