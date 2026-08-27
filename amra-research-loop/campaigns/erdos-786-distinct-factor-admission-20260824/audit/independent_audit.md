# Independent audit: Erdős 786 distinct-factor admission

## Verdict

The decisive lemma is mathematically correct.  I recommend promotion under
the frozen success condition `standalone_decisive_lemma`, and under no
stronger condition.  The promoted statement must be limited to the explicit
all-`N` fractional transversal of cost `(1+o(1))N/log N` and the supporting
bounded-length and circuit facts.

Neither the integral finite density-one assertion nor the infinite
natural-density assertion is proved.  In particular this audit does **not**
recommend `original_problem_closed`, `main_term_improved`, or
`global_interface_closed` for either public assertion.

## Blind protocol

Before reading any author file in `evidence/` or the author verifier, I read
only `campaign_state.json`, `closure_contract.json`, and the statement and
dependency fields of `decisive_lemma.json`.  I then wrote
`audit/blind_reconstruction.md` and fixed its SHA-256 as

```text
b73a8c3717dfa7693d927ca0f290b43eddd4d8e03d7fbf5ac8c8c14174b22ac0
```

Only after that hash was recorded did I inspect the author proof notes and
verifier.  The blind reconstruction contains an independent proof of every
promoted mathematical claim.

## Claim-by-claim audit

### 1. Variant, cancellation, and exceptional elements: passed

The frozen problem is the Finset/distinct-factor variant.  If two positive
Finsets `S,T` have equal product, cancellation of `S intersect T` produces
disjoint shores `S\T,T\S`, preserves equal products, and preserves the
cardinality difference.  Thus a hyperedge support counts each surviving
integer once; it is not a multiset support.

The integer `1` cannot be admitted because `{1}` and the empty Finset have
equal product and unequal cardinality.  If naturals include `0`, then any
positive-density admissible set cannot contain `0`: together with any other
admitted integer `m`, the Finsets `{0}` and `{0,m}` violate the property.
The decisive finite hypergraph correctly works on `{2,...,N}`.

### 2. Fractional vertex cover: passed for every `N>=2`

Let a disjoint bad relation be oriented with `k=|S|>|T|=l` and common
product `P`.  Since every element of the smaller shore is at most `N`,
`P<=N^l`.  Therefore

\[
\sum_{n\in S\cup T}\frac{\log(N/n)}{\log N}
=\frac{(k+l)\log N-2\log P}{\log N}
\ge k-l\ge1.
\]

This directly proves the cover constraint with support counted once.  It
also verifies the author's alternative identity
`sum_S w_N-sum_T w_N=k-l`: nonnegativity of the `T`-weight then gives
`sum_(S union T) w_N>=sum_S w_N>=1`.  No repeated-factor or additive
functional argument is used.

At `N=2` the only weight is zero, but the bad-support hypergraph is empty,
so the assertion remains valid vacuously.

### 3. Exact total weight and Stirling: passed

The exact sum over the actual vertex set is

\[
\sum_{n=2}^N w_N(n)
=\frac{(N-1)\log N-\log(N!)}{\log N}
=\frac{N\log N-\log(N!)}{\log N}-1.
\]

Using
`log(N!)=N log N-N+(1/2)log(2 pi N)+O(1/N)` gives

\[
\sum_{n=2}^N w_N(n)
=\frac N{\log N}-\frac{\log(2\pi N)}{2\log N}-1
+O\!\left(\frac1{N\log N}\right)
=(1+o(1))\frac N{\log N}.
\]

This is a feasible fractional-cover cost, hence an upper bound on the
fractional optimum.  Neither the author nor this audit claims equality with
the optimum.

### 4. High-tail bounded-length theorem: passed

For integer `L>=2`, retain only `n>N^(1-1/L)`.  If a bad relation has larger
shore size `k<=L` and smaller size `l<=k-1`, then strictness of the cutoff
gives

\[
\prod S>N^{k(1-1/L)}\ge N^{k-1}\ge N^l\ge\prod T,
\]

a contradiction.  If `L=o(log N)`, the deleted proportion is at most
`N^(-1/L)=exp(-log N/L)=o(1)`.  All quantifiers and the strict lower cutoff
are correct.  This proves only the bounded-larger-shore variant.

### 5. `K_(s+1,s)` edge-prime circuit: passed, with one author-proof repair

Give each edge of `K_(s+1,s)` a distinct prime and assign to a graph vertex
the product of its incident edge primes.  The `s+1` left products and `s`
right products are distinct and squarefree, and both shore products equal
the product of all edge primes.

Full support-minimality requires checking arbitrary new shores, not only a
subproduct of original-left vertices against a subproduct of original-right
vertices.  Give every constructed integer a signed coefficient
`c_x in {-1,0,1}` in an arbitrary cancelled subrelation.  At the prime on
edge `xy`, equality of valuations is exactly `c_x+c_y=0`.  Connectivity
forces all left coefficients to be one common value `t` and all right
coefficients to be `-t`.  Hence `t=0` gives the empty relation and
`t=+/-1` gives the full circuit, up to reversing shores.  This supplies the
minor step omitted by the narrower membership-indicator wording in
`OBSTRUCTION_ANALYSIS.md`.

The statement for every `s>=2` is valid; in fact the construction already
works for `s=1`.  Placement with comparable edge primes uses only the
standard fact that, for fixed `s`, sufficiently large dyadic prime intervals
contain the required finite number of primes.  This placement is supporting
obstruction evidence, not a dependency of the fractional-cover theorem.

### 6. Fixed-`N` hypergraph and ILP: passed, finite scope only

After disjointization, an admitted subset of `{2,...,N}` has the desired
property exactly when it contains no bad support.  Its complement is
therefore a transversal of the finite bad-support hypergraph.  Inclusion-
minimal supports suffice by finite descent, so the displayed binary hitting-
set ILP is exact at each fixed `N`.

The author enumeration is complete for each printed cutoff through `N=18`:
it groups all `2^(N-1)` subsets by exact integer product, takes symmetric
differences of unequal-cardinality collisions, minimizes the resulting
supports, and exhausts every admission mask.  An independently written
direct subset-product check through `N=12` agreed with the hypergraph
predicate and optimum at every cutoff.

There is one documentary overclaim in `MECHANISM_FALSIFICATION.md`: the
verifier does **not** “replay every maximizing set.”  It retains one
`best_mask` per cutoff and directly replays that one witness.  This does not
invalidate the optimum, since every candidate mask is covered by the exact
bad-support independence test, but the sentence should say “one maximizing
witness at each cutoff.”  No bounded computation is an all-`N` asymptotic
certificate.

## Statement and boundary audit

The decisive-lemma statement matches the proved theorem exactly: all
`N>=2`, Finset products, disjoint bad supports after valid cancellation, and
the stated total weight.  It explicitly says integral rounding and the
infinite construction remain unresolved.

The local Lean source phrases its finite interval as `Set.Icc 1 (N+1)`
while the prose and frozen closure contract use `[N]={1,...,N}`.  This is an
off-by-one formalization boundary, asymptotically harmless but worth keeping
distinct.  The audited standalone lemma uses `{2,...,N}` and is unaffected.

The finite and infinite public parts are still open:

* A fractional transversal of cost `o(N)` does not imply an integral
  transversal of cost `o(N)`.  A generic loss of order `log N` would erase
  the saving; a problem-specific `o(log N)` loss or another mechanism is
  still needed.
* Independently optimized finite sets do not supply a single coherent
  infinite set with a natural-density limit.  Cross-block multiplicative
  relations and stabilization remain uncontrolled.

## Dependency audit

The decisive theorem depends only on cancellation in positive integers,
the logarithm of an equal product, elementary finite hypergraph dual
terminology, and Stirling's formula.  All are used correctly and no
unproved campaign survivor is imported.  The high-tail and edge-prime
circuit results are independently reconstructed above.  The remaining
integral-rounding and natural-density statements are listed as gaps rather
than silently assumed.  Dependency check therefore passes.

## Machine replay

The author verifier has SHA-256

```text
54e089a1f37b0b1332b1de738318900744f4837f6f62ff4b8a8e3355e0724996
```

and reproduced with

```text
python3 evidence/verify_distinct_factor_obstructions.py
```

Result: `PASS`; exact finite cutoff `N=18`; 86 minimal bad supports and
optimum 11 at the final cutoff; fractional-cover checks for `6<=N<=18`;
edge-prime circuits for `2<=s<=6`.  These loops are finite replays only; the
universal conclusions come from the symbolic proofs above.

The AMRA checks also reproduced:

```text
python3 scripts/research_loop.py validate \
  --campaign campaigns/erdos-786-distinct-factor-admission-20260824
# valid: true, errors: []

python3 -m unittest discover -s tests -v
# Ran 5 tests: OK
```

## Novelty and promotion recommendation

No public exact-solution search was performed, as required.  A targeted
search of the local AMRA/openmath/ara-paper-writing repositories found no
earlier copy of the log-defect theorem outside this campaign.  That is not a
primary-literature priority determination, so `novelty_check` is
`priority_uncertain`.

Subject to that publication-priority caveat, the theorem is exact,
all-parameter, independently reconstructed, and closes the entire
fractional feasibility interface at `o(N)` cost.  I therefore recommend:

```text
outcome: promote
success_condition: standalone_decisive_lemma
```

The promotion reason must say explicitly that original Erdős #786, its
finite integral density-one part, and its infinite natural-density part all
remain unsolved.
