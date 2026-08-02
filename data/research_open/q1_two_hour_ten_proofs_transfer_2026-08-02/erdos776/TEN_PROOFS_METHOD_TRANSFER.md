# Ten-proofs method transfer for Erdős #776

Date: 2026-08-02 HKT

Status: **METHOD NOTE ONLY; NO NEW #776 THEOREM IS CLAIMED HERE**.

## 1. Audited sources and scope

This note extracts reusable proof architecture from the local
`ten-proofs` snapshot `94bc0fe` and the accompanying reasoning
walkthrough.  The principal sources were:

- `MulticolorTriangleRamsey.lean`, especially separated palettes,
  saturated matrices, exceptional columns, the palette-block certificate,
  and the recursive growth theorem;
- `CompactnessAndDegeneracy.lean`, especially maximum-cut/minimum-degree
  reduction, admissible quotient templates, heavy-fibre compression, the
  pair-generated graph, Hamming thinning, and the bounded entropy
  potential;
- `MetricCodes.lean`, especially the rejected guessed recurrence, the
  corrected moving projections, the complete positive Gram remainder,
  finite spectral certificates, and shell localization;
- `GapCVP.lean`, especially typewise sparse-fibre reduction, finite
  reconstruction, exact encoding/decoding interfaces, strict YES/NO
  promises, and the final `Comparator` wrapper.

The target remains the adaptive diagonal-seed theorem behind Erdős #776.
The actual dyadic family already found in the previous campaign refutes the
fixed rank-five bridge only.  It recovers at rank six and is **not** a
counterexample to Erdős #776.

## 2. Five transferable proof patterns

### 2.1 Random existence first, deterministic interface second

The Ramsey proof samples a saturated matrix and proves that the union of
all bad column-set events has probability below one.  It then forgets the
random experiment: the recursive construction uses one fixed matrix and
two deterministic covering maps.  The degeneracy proof similarly thins a
Hamming host randomly, but the theorem retains one concrete realization
outside a finite union of failure events.

Transfer to #776: use computation or probabilistic sampling only to
discover a finite *wall template* or a separating statistic.  The final
lemma must quantify over an explicitly fixed template and prove its
transition rule arithmetically.  In particular, a large scan of dyadic
strips cannot be the proof of cap recovery, but it can identify the finite
carry signatures that the proof must cover.

### 2.2 Compress bad events before taking a union bound

Three examples are especially relevant.

1. Ramsey saturation groups all row failures by a missing alphabet symbol;
   the cost is `H` missing-symbol classes rather than one event for every
   row value.
2. Hamming thinning groups child arrays by their coordinatewise
   `(00,11,01)` count profiles.  Repetitions are allowed in the counting
   upper bound and distinctness is imposed only when the independent
   retention factor is used.
3. GapCVP discards heavy fibres separately for each table type.  Requiring
   a common good set would multiply the exceptional-set loss by the number
   of types and destroy the parameter budget.

Transfer to #776: do not union over raw pairs `(h,b)` or full canonical
words.  Compress them by the finite data actually seen by a transition:

\[
  (\text{promotion count},\ \text{borrow depths},\
    \text{leading-index gaps},\ \text{cap remainders}).
\]

Different low blocks may use different good parameter ranges.  Only the
final surplus comparison needs their simultaneous intersection.  This is
the direct analogue of typewise good fibres in GapCVP and avoids paying an
artificial factor for every wall.

### 2.3 Prove a finite template, then amplify it

The Ramsey `PaletteBlockCertificate` isolates exactly five local facts;
once they hold, triangle-freeness and the next-stage colouring invariant
follow without reopening the construction.  The compactness proof closes
template overlap by taking every admissible colour-preserving quotient of
two marked finite graphs.  The degeneracy counterexample chooses a huge
but fixed pair-generated graph and amplifies a small positive entropy gap
through many layers.

Transfer to #776: define a finite cap-transition certificate whose fields
are:

- the legal canonical decomposition before the wall;
- the normalized word after each permitted borrow;
- the exact surplus identity;
- a monotone lower bound or a bounded potential increment;
- the exit condition (seed, next template, or explicit exceptional base).

Then prove one composition lemma for certificates.  A wall can overlap
the next wall, just as two graph templates can overlap; the safe closure is
to include every admissible quotient/signature produced by identifying
equal leading indices, rather than assuming disjoint carries.  A fixed
template library may then be iterated to an adaptive rank of order
`log log h` without asserting that any fixed rank works.

### 2.4 Let a small counterexample diagnose the missing term

The first MetricCodes recurrence was rejected by the eight-bit even-parity
code.  The counterexample showed that the error was structural: guessed
associated-recurrence coefficients were not induced by actual orthogonal
maps.  The repair kept both coordinate channels and the full positive Gram
remainder.  Likewise, the #776 rank-five counterfamily diagnoses the term
lost by a pure-superadditivity bridge; retaining the full leading-block
loss already closes five neighbouring chambers.

Transfer protocol:

1. search for the lexicographically first failing canonical signature;
2. freeze the exact integer certificate;
3. solve its equality/inequality pattern symbolically for a low-dimensional
   parameter family such as fixed `(K,r)`;
4. impose the original dyadic congruence only after the symbolic family is
   obtained;
5. compute the first recovery rank and search for a monotone recovery
   invariant.

This protocol must classify every output as either a counterexample to a
named bridge, a route obstruction, or a public-problem counterexample.  No
current output belongs to the last class.

### 2.5 Comparator formalization is part of the mathematics

The GapCVP formalization separates rich mathematical instances from their
binary records.  It proves encoding injectivity, decoding equivalence,
well-formedness, strict YES/NO disjointness, and only then exports the
comparator theorem.  MetricCodes makes the analogous conceptual move:
the spectral comparison is accepted only after the proposed Jacobi matrix
is realized by actual incidence maps and its discarded remainder is proved
to be a Gram kernel.

The #776 comparator should therefore expose four independent predicates:

1. `on_original_lattice(h,b)` (including the dyadic strip and range);
2. `canonical_signature(state, signature)` (no hidden wall crossing);
3. `exact_transition(state,next_state,gamma)`;
4. `claimed_exit(signature,gamma)`.

Two implementations of Macaulay raising should agree, but agreement alone
is not the theorem.  Universal rows need a symbolic certificate; finite
rows need a frozen exhaustive domain; and discovery-only scans must be
labelled as such.  The final report should state the strongest exported
implication in the same way the GapCVP comparator states its promise.

## 3. Immediate attack plan for the complementary no-borrow lattice

The previous one-promotion/two-one-wall chart is a useful template, not an
exhaustive classification.  The next attack should avoid a global case
split by raw `K=b-q`.

1. Write

   \[
   n=\binom q2+r,\qquad n+b-1=\binom{q+c}{2}+u,
   \]

   and treat the promotion count `c` as the first compressed type.  Derive
   the exact original-lattice equation and the inequalities cutting out
   each `c`.
2. For every actual no-borrow antecedent, normalize the two rank-four low
   blocks and record the borrow-depth pair, not merely its signs.  Search
   for the smallest signature outside the old `(c=1, depth<=1)` chart.
3. Close all signatures whose leading gap is at least two by a generalized
   full-block-loss inequality.  Keep the adjacent orientation `D<E` as a
   separate exceptional template; the known `(K,r)=(6,10)` family shows
   why it cannot be forced positive at rank five.
4. On every negative adjacent template, compute one further exact row.  The
   candidate potential is the ordered pair

   \[
     (\text{borrow depth},\ \text{normalized deficit}/\text{leading gap}),
   \]

   ordered lexicographically.  The desired statement is not fixed-rank
   positivity, but either immediate positivity or a strict potential
   improvement while the leading index remains below the rank-42 cap.
5. As in the Ramsey exceptional-column argument, isolate a bounded
   exceptional signature list and inject it into distinct future ranks.
   If the list has size `O(log log h)`, an adaptive seed follows without a
   false uniform-rank bridge.

The first two steps are exact classification tasks.  Steps 3--5 are proof
targets, not results of this note.

## 4. Immediate attack plan for positive-side cap transitions

The inherited fixed-offset recurrence shows that the slow pre-cap wall is
the offset `k=5`, but moving offsets can meet a cap earlier.  The negative
double-borrow proof suggests the correct template:

1. freeze the last canonical row before the first positive-side cap;
2. bound the amount by which each low block can cross the next wall from
   previous-row canonicality;
3. enumerate the resulting finite quotient/signature types;
4. prove sign on each type using the exact full-block loss, retaining every
   leading term;
5. if a type can be negative, prove recovery or strict potential increase
   at the next row instead of forcing a false immediate sign.

The key test imported from MetricCodes is: every proposed scalar
inequality must be realized by the actual canonical transition.  If a
remainder has no manifest monotonicity, superadditivity, or Gram/counting
interpretation, a small exact counterexample search is mandatory before it
is used in an induction.

## 5. Transfer to Erdős #809

Several graph-theoretic devices transfer almost verbatim to the #809
normal form.

- **Admissible quotient closure.**  When two zero-shore stars or rectangle
  witnesses overlap, quotient the marked finite template by equal host
  images while preserving injectivity on each marked star.  This prevents
  a proof from silently assuming disjoint local witnesses.
- **Maximum-cut plus sharp pruning.**  Convert a global dense obstruction
  to a supported bipartite, minimum-degree subgraph before applying local
  zero-shore counting.  The pruning invariant must track the colour defect
  and reserve, not just edges.
- **Heavy-fibre compression.**  Split common-coordinate or repeated-colour
  fibres at a threshold; discard the light mass and take a convex moment of
  the heavy fibres.  This is a promising way to turn many local stars into
  one bounded family of high-multiplicity templates.
- **Two-template logic.**  One template should bound concentrated
  extensions; a second should force the residual bad vertices/colours to
  cover every surviving edge.  This mirrors the `J/K` division in the
  compactness proof and is more realistic than asking one local inequality
  to close every reserve branch.
- **Pair-layer potential.**  A fixed pair-generated witness can alternate
  between the two shores.  If every embedded layer either spends reserve
  or increases a normalized defect potential in `[0,1]`, sufficiently many
  fixed layers give a contradiction.  Independence/repetition must be
  handled in the same order as in Hamming thinning: overcount profiles
  first, invoke distinct-edge resources only afterward.

These are method transfers only.  They do not strengthen the current #809
claim ledger without new proofs.

## 6. Firewall

- Exact scans are discovery tools and finite certificates only.
- The one-promotion/two-one-wall chart is conditional and not yet known to
  exhaust the complementary no-borrow lattice.
- The `(K,r)=(6,10)` dyadic family refutes the rank-five bridge and recovers
  at rank six; it does not refute Erdős #776.
- Positive-side moving cap transitions and the global adaptive seed remain
  open.

