# Independent audit: exact reduction and carrier-creation boundary

## Verdict

The decisive lemma is a correct **conditional typed reduction**, not a proof
of the public Erdos #809 bound.  The integer rounding equivalence and the
per-cut Hall reduction reconstruct independently.  The exchange-rank exit is
valid only after an actual graph-realizable certificate object has been
constructed with the stated colour, completion, and noncollision semantics.
Neither that construction nor the required rank lower bound is present.

No conclusion about the `1/8` main term changes.

## 1. Integer rounding

For an integer `R` and real `S`, let `k=floor(S)`.  By definition,
`k <= S < k+1`.  If `R<=S`, then the integer `R` cannot be at least `k+1`, so
`R<=k`; the converse follows from `R<=k<=S`.  Hence

`R<=S` if and only if `R<=floor(S)`.

In the audited odd rows,

`S_m = e/2 - binom(|B|,2) - (n/4)sqrt(3)`.

Here odd `n` makes the nonzero rational coefficient of `sqrt(3)` explicit,
so `S_m` is irrational.  The independent checker decides signs of
`p+q sqrt(3)` by exact rational squaring and compares sampled integer residues
directly with `S_m`.  It reconstructs all 122 rows.

The author checker does compute the floors exactly, but its nearby-residue
guard is circular: `gate_by_floor` is defined as `residue <= floor_slack` and
then compared with that same expression.  Thus the author's 122-row assertion
does not itself test integer comparison against the irrational number.  This
is an implementation weakness, repaired by the independent checker; it does
not falsify the elementary theorem.

## 2. Actual exchange-rank direct exit

The valid implication is certificate-conditional.  If `X_G` is already an
actual bipartite exchange graph whose vertices/edges encode distinct owned
low edges and high anchors, legal distinct colours, actual `C7` completions,
and exactly the conflicts excluded by endpoint-disjoint matching, then a
matching of size `ceil(Phi(n,e))` selects that many noncolliding certified
outputs.  This is the ordinary definition of matching applied to a correctly
typed certificate graph.

The dependency does all the substantive work: the campaign does not define a
completed `X_G` construction for every hard graph, prove that matching alone
captures every cross-output collision, or prove
`nu(X_G)>=ceil(Phi(n,e))`.  In particular, the scalar inequality `R_A>S_m`
does not imply the rank bound.  M809R3-05 therefore remains an unproved route,
not a direct-exit theorem about the original graph class.

## 3. Carrier creation, cut by cut

Let `D` be demands, `C` old carriers, and

`delta = max_{T subseteq D} (|T|-|N_C(T)|)`.

If `z` new carriers are added, a maximizing cut can gain at most `z` distinct
neighbours, so every successful augmentation needs `z>=delta`.  Conversely,
`delta` genuinely new **universal** carriers add `delta` neighbours to every
nonempty cut.  Since each old deficit is at most `delta`, every Hall cut then
passes.  Thus `delta=|D|-nu(C_G)` is exactly the minimum number only in the
universal-adjacency augmentation model.

For graph-derived carriers `Z`, after their existence, legality, distinctness,
and ownership have been established, the exact condition is instead

`|N_C(T) union N_Z(T)| >= |T|` for every `T subseteq D`.

The number `|Z|=delta` alone is insufficient.  An independent two-demand
counterexample starts with no old carriers, so `delta=2`, and creates two
distinct carriers both adjacent only to the first demand.  The singleton cut
containing the second demand still has zero neighbours.  Hall can allocate
legal objects already present in the incidence graph; it cannot create a
previously unused actual carrier, prove a conversion arc legal, or supply an
injective ownership map across overlapping circuits.

The author JSON summary's phrase “must produce delta distinct legal actual
carriers” must therefore be read together with its preceding all-cuts
condition.  Read as a count-only sufficient condition, that phrase would be
false.  The decisive lemma and Markdown evidence state the required
neighbourhood condition correctly.

## 4. Finite enumeration audit

The claimed count is correct under the precise interpretation “labelled
bipartite graphs with ordered left and right shore sizes between zero and
four, including empty shores”:

`sum_{l=0}^4 sum_{r=0}^4 2^(lr) = 74,963`.

These are not 74,963 isomorphism classes.  The independent checker enumerates
the same universe with different algorithms: maximum matching uses a
used-right-mask dynamic program, while deficiency and augmentation are tested
by direct Hall-cut enumeration.  It confirms `delta=|D|-nu`, sufficiency of
`delta` universal carriers, failure with `delta-1`, and the nonuniversal
count-only counterexample.  The 122 count is also correct:

`6 + 8 + 12*9 = 122`.

Run command (no Lean):

```sh
ulimit -v 2097152
timeout 120s python3 audit/independent_verify_exact_reduction.py
```

## Scope and promotion

This audit passes the local conditional reduction and its exact finite
guards, subject to the wording qualification above.  It does not close the
frozen global interface: actual exchange-graph construction/rank, actual
carrier creation, all-cut legality, and global nonreuse remain open.  The
public problem, asymptotic order, and coefficient are unchanged.
