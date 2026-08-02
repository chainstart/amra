# Ten-proofs methodology transfer for Erdős #1083

Date: 2026-08-02, 20:30 checkpoint  
Status: **method note only; Erdős #1083 remains open and no exponent improvement is claimed**

## 1. Sources and audit boundary

This note uses the local extracts

- `/tmp/ten-proofs-method.TRuWZF/paper.txt`, *Ten Advances in Mathematics and Theoretical Computer Science*;
- `/tmp/ten-proofs-method.TRuWZF/reasoning.txt`, *How the Ideas Came Together*;
- the Lean snapshot `/home/biostar/work/projects/ten-proofs` at commit `94bc0fe`, specifically
  `NonSoficGroup.lean`, `ConnesRigidity.lean`, `Permanent.lean`,
  `QuantumParallelRepetition.lean`, and `GapCVP.lean`.

The prose below extracts proof architecture.  It does **not** import any theorem about
Erdős #1083 from those sources.  References to Lean names mean that the corresponding
mechanism has a machine-checked implementation in the source project, not that the
transfer proposed here is formalized.

## 2. Five reusable proof architectures

### A. Explicit algebraic object before asymptotics

The non-sofic construction does not start from an abstract pathological group.  It first
builds one concrete binary Leavitt algebra, realizes prefix cylinders as matrix units,
and puts the property-(T) group, Thompson-type permutations, and two compression maps
inside the same object.  The two actions can therefore be compared without changing
ambient language.  `NonSoficGroup.lean` implements the permutation models, amplification,
table evaluation, matched cores, pruning, and the later diagonal word selection.

The Connes counterexample uses the same discipline in a different category.  The
explicit quadratic Boolean module has

\[
V=\mathbf F_2[t]^4,\qquad T=V\otimes V,\qquad
B=\langle v\otimes v:v\in V\rangle,
\]

and a quadratic carry changes the group law on the same measurable coordinates.  The
measurable action is preserved while order-four torsion changes.  The Lean file exposes
this through `square`, `B`, `diagonal`, `polarization`, `carry`, `CarryGroup`, and
`orderFourElement`.

**Transfer rule.**  For #1083, the correct object is not a list of rowwise quotient
identities.  It is one simultaneous Laurent-group-ring datum carrying, at once,

\[
F_j=GR_j,\quad P_{A_0}=GB,\quad B=R_jQ_j,\quad
P_{A_j}=F_0Q_j,
\]

the scalar-copy embeddings of the single set \(X\), and the Euclidean height/tangent
parameters.  Any reduction that forgets one of these interfaces is vulnerable to the
known tensor and interval countermodels.

### B. Local-to-global amplification by a bounded potential

The non-sofic proof first has many approximate expander components, not one usable
component.  The key potential is bounded and median-normalized,

\[
f(x)=\frac{M(x)}{M(x)+m},
\]

where \(M(x)\) is component size and \(m\) is a median.  Approximate transport makes
this potential almost monotone.  Because transport is a permutation, the signed drift
sums to zero.  Coarea plus expansion then concentrates \(f\), majority intersection
matches components, and a slowly growing diagonal radius selects one component that
passes every finite word test.  Relevant Lean landmarks include
`permutation_small_support_coarea`, `matchedCore`, `exists_pruned_expander`,
`diagonalRadius`, and `finite_union_bad_density_tendsto_zero`.

The permanent circuit proof has an algebraic version of the same pattern.  It turns
columnwise gradient equations into monic reductions modulo finitely many shared power
sums, obtains a finite module and hence a critical-locus dimension bound, then combines
many disjoint matching blocks into one permanent by root-of-unity cancellation.  Lean
landmarks include `criticalLocus`,
`exists_slicedGradient_of_criticalLocus_codimension`,
`rootOfUnity_node_product_algebra`, and
`sourceSeparatedBlockMinorSum_criticalLocusDimension_le`.

**Transfer rule.**  Do not union-bound all bad rows or all quotient factors.  First choose
a bounded row potential whose drift has an exact conservation law, then use a coarea or
rank inequality to select one power-large coherent core.  Natural candidates are a
normalized signed-resolvent energy and a truncated moment/Hankel rank.  Both remain
bounded under rare bad rows, unlike raw support size or raw coefficient height.

### C. Tensor repetition only after preserving the correct mass

Quantum parallel repetition explains why independent repetition alone is not an upper
bound: losses can be fully correlated, and conditioning on a rare success branch creates
a fatal \(1/p\) factor.  The successful object is the resolvent purification

\[
[\Gamma(F)v](u)=F(F+uI)^{-1}v,
\qquad \Gamma(F)^*\Gamma(F)=F.
\]

It preserves Born mass exactly, controls singular eigenvalue scales without a minimum
eigenvalue, and telescopes along a live-coordinate martingale.  Probability weighting
cancels the normalization denominator before averaging; greedy conditioning then turns
the one-coordinate gap into exponential repetition.  Lean landmarks include
`failureMass`, `exists_greedy_stopping`,
`noncommutative_resolvent_identity`,
`scalar_resolvent_purification_integral`,
`spectralPurificationFilter_eq_resolvent`, and the purification entropy/Jensen lemmas.

The permanent block construction supplies a complementary warning: a product of blocks
creates unwanted critical components, whereas a root-of-unity engineered **sum** has
additive critical codimension.  Tensorization is useful only after mixed terms have been
cancelled and every desired block retains nonzero weight.

**Transfer rule.**  The \(2^k\) signed-switch cube is not itself an amplifier.  Before
repeating switch coordinates, preserve an exact positive mass (augmentation, finite-
quotient shadow, or a positive quadratic energy) and prove that conditioning/projection
does not divide by a tiny spectral quantity.  Otherwise the multidirectional tensor
barrier is an example, not a contradiction.

### D. A complexity potential that survives cancellation

For permanent formulas, coefficient count is replaced by transcendence degree.  Pruning
to the marked skeleton charges only genuine branching nodes; long unary chains collapse
to affine maps, or to projective \(2\times2\) wrappers when valid division is allowed.
A logarithmic matching then controls \(m^2\) algebraically independent coefficients via
two binary encodings and a tensor-product Vandermonde Jacobian.  Entry-disjoint matching
blocks let the charges add.  Lean landmarks include the contracted rational skeleton,
`matchingPolynomial`, `matchingPolynomial_natDegree`, and
`matchingPolynomialEvaluationMatrix_det_ne_zero`.

GapCVP replaces a failed positivity argument for signed histograms by another
cancellation-stable potential: moments and Hankel rank.  Low Hamming weight gives
type-dependent good fibres; Hankel/Vandermonde reconstruction recovers a small separable
root set; shifted moments and a common splitting field/valuation force one global root to
satisfy all clauses.  A parity-lift lattice finally converts table weight exactly to
Euclidean distance.

**Transfer rule.**  Coefficientwise signs of \(Q_j\) are the wrong invariant.  Candidate
potentials are:

1. the rank of \(H_j=(m_{a+b}(Q_j))_{0\le a,b<h}\);
2. transcendence degree of the scalar-copy coefficient family over the shared centre;
3. an \(L^2\) resolvent energy after passing to a finite abelian shadow.

Each can be small only for a structurally reconstructible family.  In particular, signed
cancellation should be handled by reconstruction, not by asserting latent positivity.

### E. Counterexample first, and test the exact remembered interface

The Connes proof begins by asking what the crossed product remembers: the measurable
action, not the hidden compact group law.  It then deliberately changes an invariant
outside that remembered interface.  The quantum walkthrough similarly records holonomy
and rare-branch constructions that kill tempting proof steps even though they do not
refute the theorem.  The permanent chapters compare determinant witnesses to establish
that the successful invariant is genuinely permanent-specific.  GapCVP explicitly
keeps the signed-histogram failure before switching to binary reconstruction.

**Transfer rule.**  Every proposed #1083 lemma must be tested against four nested models:

1. rowwise positive-multiple identities only;
2. all simultaneous divisor identities;
3. the common-\(X\) scalar-copy interface;
4. the full Euclidean exact block, and finally the outer near-extremal geometry.

A counterexample at level \(r\) refutes only lemmas using information through level \(r\).
The existing interval multirow construction is therefore a scope counterexample, not a
counterexample to Erdős #1083.

## 3. Four-gate transfer matrix

| #1083 gate | Imported mechanism | Concrete next lemma | Failure certificate to seek first |
|---|---|---|---|
| arbitrary aperiodic \(X\) | explicit common object; resolvent purification | finite-shadow convolution inverse with an exact \(L^2\) mass identity, parameterized by the smallest Fourier singular value of \(P_X\) | aperiodic \(0/1\) masks whose singular value is too small for a uniform bound |
| signed residuals \(Q_j\) | Hankel reconstruction; projective wrappers | bounded moment rank implies a common finite signed support/reconstruction field; high rank must spend the common quotient's complexity | two multipliers making the same signed residual positive while all low moments cancel |
| common-\(X\) | two binary encodings; root-of-unity cancellation | a Jacobian/transcendence lower bound for many scalar copies \(F_0Q_j=P_{\lambda_j X}\), charged against factors of the single \(B\) | simultaneous masks satisfying all divisibilities but arising from different source sets |
| outer stability | median/coarea; live-coordinate martingale; diagonal radius | select one exact-like power-large core while charging discarded cells to the original \(t^{o(1)}\) defect budget | near-equality examples in which each row is good but no common row core survives |

## 4. Immediate research decision

The most testable first transfer is the **finite-shadow resolvent energy lemma**.  It is
fully rigorous finite Fourier analysis, applies to signed \(Q\), and cleanly separates the
arbitrary-centre difficulty into one measurable condition number.  It will not by itself
close #1083: a second theorem must either lower-bound that condition number on a selected
shadow, or replace it with a moment-rank reconstruction that does not pay a small divisor.
The next work product should therefore contain both the exact lemma and an adversarial
search for small-divisor aperiodic centres.

## 5. Result of the first transfer

The resolvent idea became stronger after retaining integrality.  Instead of paying the
smallest Fourier singular value, `SIGNED_RESIDUAL_FACTORIAL_ENERGY.md` uses

\[
 \delta(q)=\frac12\sum_gq(g)(q(g)-1).
\]

A sufficiently large elementary prime quotient makes **every** \(S\)-term source
Fourier-invertible, and Parseval identifies \(2\sum_j\delta(q_j)\) exactly with a
common-mask reciprocal-frame excess.  In physical space the same quantity is an exact
negative autocorrelation debt.  Positive/negative overlap then forces a popular source
difference, while the nonexact norm identity supplies the requested stable outer-error
ledger.  This realizes four transfer principles at once: explicit algebraic object,
integral cancellation-stable potential, mass-preserving Fourier resolution, and counterexample-first
scope testing.  It still leaves the power-large excess upper bound and geometric
extraction open.

The adversarial half also succeeded.  `APERIODIC_SMALL_DIVISOR_NO_GO.md` proves
that the irreducible five-term mask \(1+x+x^3+x^5+x^6\) has no torsion zero but
does have non-torsion unit-circle zeros, so its finite cyclic minimum singular
value is positive yet at most \(15\pi/n\).  Therefore “aperiodic” separates
invertibility from conditioning exactly as the quantum walkthrough separates
probability preservation from division by a rare-branch weight.
The same mask admits the signed augmentation-two quotient
\(1-x^5+x^8+x^{10}-x^{13}+x^{18}\), whose product is a ten-term mask, so the
conditioning failure occurs on an actual signed-residual centre rather than an
extraneous polynomial.
