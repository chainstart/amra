# Survivor first proof attempts

This note records one exact first proof attempt for each of `M809C-05`,
`M809C-08`, and `M809C-11`.  It deliberately separates proved arithmetic or
bookkeeping statements from graph-realizability claims.

## M809C-05: exact unweighted cardinality is refuted

The mechanism asks for a finite unweighted set `Sigma` with cardinality exactly

`S_m = e - binom(|B|,2) - Phi(n,e)`.

At the first edge count above the Turan threshold and odd `n`,

`e = floor(n^2/4)+1` and `e-n^2/4 = 3/4`.

Consequently

`Phi(n,e) = e/2 + n sqrt(3)/4`,

which is irrational.  Since `e-binom(|B|,2)` is integral, `S_m` is irrational.
It therefore cannot be the cardinality of any finite unweighted set.  This
refutes `M809C-05` exactly as stated, independently of carrier provenance.

The old hard-local pair at `n=14`, `e=50`, `|B|=3` has `Phi=32` and `S_m=15`.
It is compatible with integrality, so it remains a useful provenance test, but
it cannot rescue the universal exact-cardinality claim.  A viable repair would
have to use weighted nonnegative atoms of total mass `S_m`, or an integer
floor/ceiling ledger with its rounding error retained explicitly.  Neither
repair is proved here.

## M809C-08: one direct exit is proved, the outer gate remains conditional

The inherited exact ledger is

`R_A = e(G[A_<q*]) + I_mix - N_int`.

For every mixed colour, choose its unique high internal anchor.  The inherited
anchor construction is injective by colour and places these anchors in the
pairwise `C7`-compatible high-edge family.  Hence

`I_mix >= ceil(Phi(n,e))`

is an exact direct exit to the public colour target.

The scalar identity by itself does not force that exit.  At the old `n=14`
scale the integer ledger profile

`Phi=32, S_m=15, e(G[A_<q*])=8, I_mix=8, N_int=0`

has `R_A=16>S_m`, while neither displayed channel reaches `Phi`.  This is only
a logical counterprofile to an inference from the identity and thresholds; it
is **not** asserted to be graph-realizable.  The graph-specific gap is thus a
cross-channel compatibility lemma combining internal-low edges with mixed-high
anchors, or a direct graph proof of `R_A<=S_m`.  Previously established dense
internal-low exits remain available under their own hypotheses.

## M809C-11: Hall bookkeeping is exact but creates no resources

Fix a finite demand set, a finite typed carrier set, and the bipartite graph of
legal demand-to-carrier arcs.  Hall's theorem gives the exact equivalence:
every demand is payable by a distinct legal carrier if and only if every demand
subset `T` satisfies `|N(T)| >= |T|`.  Moreover the maximum number of unpaid
demands is

`max_T (|T|-|N(T)|)`.

The tight three-demand/two-`B`-carrier instance has matching rank two and Hall
deficiency one.  Merely listing three `A` owners changes nothing when no legal
arcs to them have been proved.  Adding one actual owned slack carrier adjacent
to the third demand raises the rank to three and removes the deficiency.

Thus `M809C-11` is a correct conditional host for a proof, but Hall's theorem
does not construct the conversion arcs, slack carriers, or ownership maps that
the graph argument still needs.

## Reproduction and scope

The exact arithmetic and finite matching checks are reproduced by:

```text
AMRA_MEMORY_KIB=5242880 AMRA_TIMEOUT_SECONDS=1800 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-809-conversion-round2/evidence/survivor_first_proof_attempts.py
```

The machine-readable output is `survivor_first_proof_attempts.json`.  No Lean
build or Lean invocation was used.  These attempts do not prove the public
Erdos-809 statement and do not alter its `1/8` main term.
