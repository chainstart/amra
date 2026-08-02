# Method atlas extracted from `openai/ten-proofs`

Date: 2026-08-02

Snapshot: `94bc0feb6a9ff12c7d31d6de640a725c9d43d2b6`

Sources inspected:

- the 249-page collection *Ten Advances in Mathematics and Theoretical
  Computer Science*;
- the 62-page *How the Ideas Came Together* discovery notes;
- all ten theorem-facing Lean modules and the Comparator challenge layout.

Status: **METHOD MAP, NOT A TRANSFER THEOREM**

## 1. Result-by-result discovery mechanisms

| Result | Decisive move | Reusable proof pattern | Principal warning |
|---|---|---|---|
| Sphere packing | Balance the origin so the packing LP becomes a Fourier sign-uncertainty problem; Mellin transform turns radial Fourier action into reflection; a small remote positive shell repairs the global tail. | Normalize until a hidden involution appears; prove a universal dual lower bound; construct a near-extremal local witness; add a much smaller global correction whose sole job is sign control. | A locally sharp ansatz may fail only at remote scales.  Increasing local accuracy does not repair a global sign tail. |
| Binary/spherical codes | Replace a false one-variable recurrence by moving projections with an explicit positive remainder; use constant-weight shells and a hierarchy of harmonics. | When one certificate is overconstrained, introduce a moving fibre and preserve the discarded positive remainder.  Optimize a hierarchy rather than one improved polynomial. | Dropping the remainder or freezing the projection can reverse the claimed sign.  The right comparison benchmark matters. |
| Non-sofic group | Put expanders and self-similar compressions in one explicit ring; use median concentration and component matching to find one component passing every finite word test. | Build the obstruction and approximation mechanism inside one algebraic host; aggregate many local tests, then select one globally coherent component by a bounded statistic. | Passing each test on some component is not the same as one component passing all tests. |
| Connes rigidity | Ask what the von Neumann algebra forgets, then encode an equivariant Boolean carry which changes torsion while preserving the factor; shift the carry to obtain an infinite fibre. | Identify the invariant's blind coordinate and vary exactly that coordinate while freezing everything the invariant sees. | Equal coarse invariants do not give the needed group properties automatically; ICC and relative property `(T)` require separate gates. |
| Permanent circuits | Replace global Newton-volume arguments by critical cones and matching faces; use columnwise inclusion--exclusion and root-of-unity filters to isolate many blocks. | Localize a global complexity measure to a rigid combinatorial face, and build an exact character filter which cancels every unwanted contribution. | Global volume can hide exponential concentration on one critical face. |
| Permanent formulas | Track matching coefficients through a tree and make division/reuse explicit; convert local matching capacity into a global leaf lower bound. | Put a conserved combinatorial resource on every node and prove an additive/submultiplicative recursion that survives the actual computation model. | A circuit argument need not survive formula unfolding or division.  The computational model is part of the theorem. |
| Quantum repetition | Preserve Born weight while resolving incompatible eigenvalue scales; replace an oscillatory coherent gauge by finite resolvent purification and telescope the resulting energy loss. | If one square root cannot serve all scales, split into scale-resolved positive pieces.  Seek a bounded energy whose loss accumulates under repetition. | Tensoring local error bounds coherently can fail because of holonomy and noncommuting scales. |
| GapCVP | Encode clauses by signed histograms, reconstruct binary bits through separable polynomial identities, then synchronize parity, characteristic, and valuations. | Recover a discrete object one coordinate family at a time; use several independent arithmetic invariants so spurious signed solutions cannot satisfy all interfaces. | One invariant reconstructs only a relaxation.  Sign, parity, and valuation compatibility must meet on the same assignment. |
| Ehrhart volume | Abandon harmonic symmetrization; pass an arbitrary body to a toric potential and compare two exact slopes of a convex functional. | Change category until the conjectured constant is the meeting point of two geometries; obtain lower and upper derivatives independently and close by convexity. | The sharp inequality does not automatically classify equality.  Rank-one kernel convexity cannot be replaced by an averaged finite partition. |
| Multicolor Ramsey | Fixed products cannot make the exponential base grow; introduce a stronger inductive invariant—bounded chromatic labels per colour—then glue separated palettes with one saturated matrix fixed in advance. | Strengthen the invariant just enough to recurse; compress all bad pairs into a bounded exceptional list; pack separated parameter blocks; interpolate between sparse construction scales. | An existential choice made after seeing a block pair is tautological.  The deterministic map/certificate must be fixed before every pair. |
| Compactness counterexample | Use two complementary forbidden templates: one bounds concentrated extension sets, the other turns the remaining bad vertices into an edge cover; use different finite geometries for different singleton witnesses. | Split a global obstruction into two mechanisms which cover opposite failure modes.  Track the exact quantifier allowing different witnesses for different forbidden members. | One witness need not avoid the whole family.  Confusing `for every H exists G_H` with `exists G for every H` destroys the counterexample. |
| Two-degenerate counterexample | Stop trying to embed every pattern; construct one alternating pattern in a thinned Hamming host.  A corrected entropy inequality forces a bounded layer potential to rise by a fixed amount. | Search for a small positive exponent window, retain dependence corrections, then repeat a fixed local gadget until a potential in `[0,1]` is exhausted. | The useful window is only about `0.0037`; ignoring without-replacement dependence or a mixed parent type erases it. |

## 2. Cross-cutting workflow

The twelve narratives repeatedly use the following sequence.

1. **Write the strongest literal interface.**  Replace prose such as
   "structured", "coherent", or "many" by a finite object, exact map,
   conserved mass, or typed incidence relation.
2. **Falsify the first natural route.**  Search not only for a counterexample
   to the theorem, but for a minimal counterexample to the proposed bridge.
   Preserve it as a theorem about the method's scope.
3. **Locate the missing invariant.**  The winning invariant is often
   strictly stronger than the target: colour-graph chromatic labels,
   matching coefficients, Born-weight energy, or a layer entropy.
4. **Separate local sharpness from global repair.**  First optimize the core
   object.  Then add a remote shell, exceptional-list handler, interpolation,
   or padding step whose only task is global quantifier control.
5. **Turn a tiny gap into a bounded potential contradiction.**  Exact
   corrections matter more than a large numerical margin; once a uniform
   positive increment is proved, repeat a fixed gadget sufficiently often.
6. **Interpolate construction scales.**  Prime powers, recursion stages, or
   calibrated dimensions establish only a subsequence.  Monotonicity and
   safe padding are explicit proof steps.
7. **Formalize interfaces, not analogies.**  The main Lean files contain no
   `sorry`; definitions expose admissibility, positivity, labels, and model
   assumptions before algebraic automation is used.  Comparator files leave
   selected holes only as independent proof-checking challenges.

## 3. Four-lane transfer map

### OPG-1757

Highest-value transfers:

- treat the exact first 31 columns as the locally sharp core and search for
  a positive "remote shell" supported near the logarithmic boundary;
- replace one fixed transport certificate by a moving projection or
  scale-resolved hierarchy, retaining an explicit positive remainder;
- formulate a dual coefficient functional which certifies the whole gap at
  once rather than proving each coefficient termwise;
- separate eventual `s>=S` control from finite-`s` interpolation.

The existing fixed-depth negative layer is analogous to the failed local
Gaussian ansatz: it rules out one architecture and positively motivates a
small global correction or unbounded-depth hierarchy.

**Transfer outcome.**  Assembling every equal-height base before taking a
sign, rather than bounding bases separately, produced the positive core
`e^(2x)-(1+x)^2`.  It closes the entire logarithmic third-active gap
eventually.  A second, independent source-pinned audit extracted the finite
constant hidden in the inherited remote theorem.  Consequently the same
explicit 117-digit threshold which controls the gap also controls both
complete third-active transports for every larger `s`.  This is an effective
eventual theorem, not universal finite-`s` positivity.

### Erdős #1083

Highest-value transfers:

- use exact character/root-of-unity filters to project signed residuals onto
  a rigid matching or fibre coordinate;
- seek several independent reconstruction invariants—augmentation, Newton
  width, valuation, and common-`X` scaling—whose intersection forces a
  literal set mask;
- replace one coherent quotient by scale-resolved positive pieces, with a
  bounded energy measuring signed cancellation across scales;
- aggregate rowwise alternatives through a bounded median/potential before
  selecting one common family.

The main firewall is unchanged: a model obstruction becomes relevant to
#1083 only after exact-block extraction and outer stability.

**Transfer outcome.**  The signed residual now has an exact integer
factorial energy which simultaneously measures autocorrelation debt and edit
distance to a mask.  A fixed aperiodic five-term centre proves that
torsion-point invertibility does not imply uniform conditioning, while an
explicit signed positive quotient shows the obstruction occurs on the actual
residual interface.  Galois pair-flips upgrade the former finite search to an
unbounded fixed-source theorem:
`gcd(P(x^r),P(x^s))=1` for all distinct positive `r,s`, where
`P=1+x+x^3+x^5+x^6`.  Hence this escape cannot support a second row at a
different absolute scale when the complement has augmentation `5C`,
`1<=C<5`.  The source is fixed; power-large synchronization and outer
geometric extraction remain open.

### Erdős #776

Highest-value transfers:

- search small exact Macaulay states for the minimal obstruction, then lift
  its binary/carry word to a parametric family;
- attach a conserved "cap loss" or "promotion entropy" to each adaptive
  rank and prove it cannot rise indefinitely;
- split complementary no-borrow points into two templates, one controlling
  concentrated cap crossings and one converting the residue into a bounded
  delay;
- interpolate sparse dyadic families only through a legal monotonicity or
  padding operation.

The current rank-five counterfamily is a route refutation, exactly the kind
of negative result the ten-proofs workflow uses to reveal the missing
adaptive invariant.

**Transfer outcome.**  Exact finite types and retained canonical remainders
give an 85,278-state positive atlas, an unbounded multi-cap inequality, and
eventual positivity for every fixed promotion count `c>=3`.  A possible bad
fixed-`c=2` sequence is forced into `r/q->1, u/q->0`, then into
`k=q-r=O(q^(1/3))`, `u=O(q^(2/3))`, `k+u->infinity`, with normalized limit
points in the compact parabolic cap `2K+U^2<=3^(2/3)`.  Exact least-cap-depth
coordinates then reduce a bad sequence to `k=1` and two correction phases,
both of which have positive normalized surplus.  Thus every fixed `c>=2` is
eventually positive.  Growing `c` and the adaptive bridge remain open.

### Erdős #809

Highest-value transfers:

- strengthen rainbow-`C_7` compatibility to a recursive per-colour label or
  palette invariant which survives block/gluing operations;
- use two complementary templates: one limits concentrated repeated-colour
  extension sets, the other turns all remaining hard edges into a vertex or
  reserve cover;
- build an alternating chain of coherent stars and search for a bounded
  synchronization/defect potential with a positive increment at every hard
  step;
- treat the sharp cyclic degree-spread graphs as equality cores and ask for
  a stability theorem forcing every near-sharp configuration into the
  already reserve-paid branch.

The Hamming-host counterexample method is not itself a #809 construction:
the rainbow colouring and global reserve provenance are extra interfaces.

**Transfer test outcome.**  The first bullet is too weak when read only as
colourability: under the standing `L_4(2)`, minimum-degree, rainbow-`C_7`
hypotheses, every entire colour graph is already an induced matching and
hence two-colourable.  The sharp parity cores even realize noninjective
`2K_2` colour classes while paying their full defect by actual reserve.  The
literal analogue of the Ramsey construction must therefore keep the part
which is stronger than colourability: endpoint-label agreement fixed before
the deficient family is chosen, coupled to the existing reserve--Hall token
sets.  A label chosen after observing the Hall obstruction is tautological.

## 4. Admission rules for this campaign

- A transferred theorem must name the exact ten-proofs mechanism and prove
  its AMRA hypotheses from existing lane definitions.
- A numerical probe may select a candidate invariant but cannot prove an
  unbounded statement.
- A counterexample to a bridge is not a counterexample to the public problem.
- An author-written executable check is not an independent audit.
- Every result entering the final ledger must survive an author swap before
  21:50 HKT.
