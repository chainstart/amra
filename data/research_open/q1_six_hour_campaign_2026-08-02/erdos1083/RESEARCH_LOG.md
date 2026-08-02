# Erdős #1083 live research log

Campaign window: 2026-08-02 10:34:51--16:34:51 HKT

## 10:35--10:55: baseline freeze

- Baseline commit: `669bbad1908e7ab7d8382a8b508e67757006e90c`.
- Read in full the inherited README, claim ledger, phase-one freeze,
  bounded-cycle and many-cycle theorems, coherent-theta theorem,
  defect-transition trichotomy, every red-team/audit file in the
  workstream, the 1,742-line verifier, and its 272-line test suite.
- Replayed the inherited standalone verifier: pass.
- Replayed the inherited regression suite: 21/21 pass.
- Exact unresolved interface: selected network records must be
  converted using the full \(T_i\)-partitions into either
  \(|\Delta(P)|>t^3\) or a power-large ruled/commensurate family.
- Dangerous quantifier identified: a lower bound for *paths* is not a
  lower bound for distinct endpoint tangents, target points, or
  distance labels.  The frozen \(t^{1/20}\) exponent is below \(U\),
  so endpoint tangent pigeonholing is unavailable.
- First falsifier mechanism: an arbitrary-width genuine Euclidean
  coherent theta with fixed lifted endpoints, fixed tangent records,
  and a single common anchor-distance label.  This targets the local
  closure implication only; the full exact block remains outside the
  construction.

## 10:55--11:15: coherent-theta closure refuted

- Proved an all-parameter construction for every \(S\ge2\) and
  \(K\le S-1\).  It gives \(K\) internally disjoint coherent
  two-edge arms on potentials \(2,1,2\), fixed word \((+,-)\), and
  fixed tangent difference one.
- Strengthened the adversarial interface: every endpoint record uses
  tangent \(a\), every internal record uses \(a+1\), and all edges
  share the actual squared-distance label \(a+3\).
- Proved adjacent transversality from
  \(W_z=z\mathbb Q\) and the irrationality of
  \((-x+\sqrt{1+x^2})/\sqrt2\) for nonzero rational \(x\).
- Realized all records by explicit points in \(\mathbb R^3\) and
  included every source--source, source--target, and target--target
  distance.  The full local set has at most \(2S^2+S\) labels.
- Exact radical verifier: pass.  Focused regression: 5/5 pass.
- Claim firewall: this refutes theta-only closure, not #1083; the
  construction deliberately lacks the \(U\)-cell identical-spectrum
  partitions.

## 11:15--11:18: full-partition star conversion

- Reinserted the inherited torsion-free direct-tiling rank theorem.
  Since \(S^3>SU\), no three exact-block row spaces can be pairwise
  transverse.  The whole transverse graph is triangle-free.
- Combined this with the inherited fixed-nonzero-difference graph.
  Its \(t^{8/9}\) ordered edges give one \(t^{1/6}\)-leaf star;
  triangle-freeness makes every two leaves nontransverse.
- Rewrote the conclusion exactly as a pairwise quotient clique in
  \((W\setminus0)/(W\setminus0)\), where
  \(W=\operatorname{span}_{\mathbb Q}(X-X)\).
- Proved the rank-two linear-algebra classification: a pairwise
  intersecting family of 2-spaces either shares a line or lies in one
  3-space.  Rank one is a rational commensurability class.
- New exact/symbolic verifier: pass.  New focused regression: 4/4
  pass, including exhaustive triangle-free graphs through six
  vertices (33,867 graphs scanned; 6,228 triangle-free).
- Remaining boundary: high-dimensional \(W\).  Pairwise intersections
  alone do not produce a common vector, bounded denominator, or a
  global distance gain.

## 11:18--11:24: fixed-tangent amplification and mask-factor inverse theorem

- Re-averaged the full transverse incidence mass over row--tangent
  slots rather than over rows alone.  From
  \(P_\perp=t^{19/9+o(1)}\) and
  \(qU=t^{14/9+o(1)}\), obtained one centre row and one literal tangent
  with \(t^{5/9+o(1)}\) transverse leaf rows.  All corresponding
  target points lie on one tangent line.
- Applied the triangle firewall only to leaf pairs.  It makes their
  row spaces pairwise nontransverse; it does **not** make their total
  intersection nonzero.  Recorded explicit rank-two examples for
  both the common-line and three-dimensional-top alternatives.
- Passed from direction spaces to full partition masks in a common
  torsion-free group ring.  Centre--leaf transversality makes source
  masks coprime, hence every leaf mask divides the centre's \(U\)-term
  complement.  Augmentation already forces \(S\mid U\).
- Proved that any two leaf masks share a nonunit irreducible factor:
  otherwise their product divides the complement and forces
  \(S^2\mid U\), contradicting \(0<U<S^2\).
- Pigeonholing the factors of a minimizing leaf gives a common-factor
  sunflower of size
  \(1+\lceil(|L|-1)/r_*\rceil\), with one genuine common Newton
  direction on that subfamily.
- Isolated the precise high-factor residual.  Only
  \(O(\log S)\) irreducible factor occurrences can have augmentation
  magnitude at least two; all remaining proliferation is through
  augmentation-unit factors.  The mask \(1+x^m\) in a saturated
  ambient lattice supplies an exact cyclotomic obstruction to bounding
  those factors by support size.
- New verifier: pass.  New regression suite: 4/4 pass, including the
  16-factor, 15-augmentation-unit example with
  \(m=3\cdot5\cdot7\cdot11\).
- Remaining exact gate: derive geometric rigidity from a shared mask
  factor, or exclude augmentation-unit richness using the tangent
  realization.  Remaining original-problem gate: stability from the
  near-direct endpoint to the literal exact block.

## 11:24--11:39: entropy synchronization and ruled chart

- Used the exact divisibility \(F_j\mid P_{A_0}\) together with the
  much smaller quotient augmentation
  \(C=U/S=t^{1/18+o(1)}\).  The complement mask has at most
  \(\log_2U\) irreducible-factor occurrences of augmentation magnitude
  at least two, while a leaf quotient can omit at most \(\log_2C\) of
  them.
- Counted omitted-heavy-factor patterns by a binomial tail.  Its
  endpoint cost is
  \(t^{(5/6)H_2(1/15)+o(1)}
    =t^{0.2944661125\ldots+o(1)}\).
  Pigeonholing the \(t^{5/9}\) fixed-tangent leaves leaves
  \(t^{0.2610894430\ldots+o(1)}\) rows with the same complete heavy
  skeleton.
- Proved the exact factorization \(F_j=HE_j\), where
  \(|H(1)|=S\), \(|E_j(1)|=1\), and every irreducible factor of
  \(E_j\) has augmentation magnitude one.  This removes the former
  dependence on an a priori bound for the number of source-mask
  factors.
- Converted a fixed nonzero Newton direction \(h\) of \(H\) into the
  explicit height parameterization \(z_j=h/(2\rho w_j)\) and the
  reciprocal parabolic common-tangent chart
  \(\rho^2+\tau_0+h^2/(4\rho^2w_j^2)+(h/w_j)X\).
- Used the fact that every \(F_j\) is a positive scalar copy of one
  source mask: an associate class contains at most the two scalars
  \(\lambda,-\lambda\).  Thus all but at most two residuals \(E_j\)
  are nonunit and power-many distinct associate classes occur.
- Falsified a tempting positivity upgrade.  The signed quotient
  \(x+y-xy+xy^2+x^2y\) becomes a \(0/1\) mask after multiplication
  by either transverse binomial \(1+x\) or \(1+y\).  Algebraic
  divisibility does not imply a third direct-sum factor.
- New verifier: pass.  New focused regression: 4/4 pass.

## 11:39--11:48: unit-switch width atlas

- Put every synchronized residual \(E_j\) inside the single quotient
  \(B=P_{A_0}/H\).  The power-many residual associate classes force
  \(R_{\rm unit}(B)\ge(\beta+o(1))\log_2t\) augmentation-unit factor
  occurrences.
- Used numerical exponent width, which is exactly additive under
  Laurent multiplication even with interior cancellation.  On a
  same-sign leaf subfamily,
  \(|\lambda_j|\operatorname{diam}X
    =\operatorname{wd}(H)+\operatorname{wd}(E_j)\).
  The residual widths are distinct weighted subset sums of the one
  unit-factor multiset.
- Reparameterized the reciprocal variables as
  \(w_j=\sigma h\operatorname{diam}(X)/
  (\operatorname{wd}(H)+\operatorname{wd}(E_j))\), and identified
  common-tangent target distances with squared subset-sum
  differences.  This yields only \(t^{\beta+o(1)}\) distances and is
  not inflated to the global \(t^3\) target.
- Built the sharp cyclotomic boundary: for prime \(S\), the positive
  arithmetic-progression masks \(P_{mX}\), \(m\mid M\), give
  \(2^{\omega(M)}\) scalar switches inside one positive common
  complement, all with augmentation-one residuals.  Source/common-
  complement positivity alone cannot bound the atlas.
- New verifier: pass.  New focused regression: 4/4 pass.

## 11:48--12:00: near-full heavy-factor hub

- Observed that complete heavy-skeleton synchronization is not needed
  for one common direction.  Every leaf mask has augmentation
  \(S>1\), so it contains a heavy irreducible factor; the centre
  complement has at most \(\lfloor\log_2U\rfloor\) heavy factor
  occurrences in total.
- Pigeonholing gives one normalized heavy irreducible factor on
  \(|L|/\log_2U=t^{5/9-o(1)}\) leaves.  Content one excludes a
  constant prime, so this factor has a nonzero Newton direction.
- Upgraded the denominator-free reciprocal ruled chart from the
  entropy exponent \(0.261089\ldots\) to the almost-full fixed-tangent
  exponent \(5/9-o(1)\).  The smaller entropy family still records
  the stronger complete-skeleton/unit-switch data.
- Independent audit confirmed the UFD, multiplicity, content, and
  exponent interfaces.  New verifier: pass; focused regression: 3/3.

## 12:00--12:06: simultaneous-positive-complement no-go

- Tested the strongest natural two-row positivity upgrade.  For every
  \(S\ge4\), the signed polynomial
  \(Q_S=x+y-xy+xy^S+x^Sy\) has augmentation \(3<S\), while
  \(P_S(y)Q_S\), \(P_S(x)Q_S\), and
  \(P_S(x)P_S(y)Q_S\) are all \(0/1\) masks of sizes
  \(3S,3S,3S^2\).
- This gives two transverse exact tilings of one spectrum with both
  complements positive and \(U=3S<S^2\), yet the switching quotient
  remains signed.  It is a full counterexample to any pairwise
  positive-quotient lemma.
- Chose explicit irrational real exponent steps, a source set inside
  the unit interval, and two heights so that the complements become
  positive tangent sets sharing one literal tangent.  The exact masks
  are realized by actual source and target points in \(\mathbb R^3\).
- The model has only two transverse rows, so it respects the triangle
  firewall and is not a public-problem counterexample.  It proves that
  the remaining positive input must be simultaneous control of a
  power-large leaf family.
- New exact/symbolic verifier: pass.  New focused regression: 3/3.

## 12:06--12:30: power-large simultaneous-switch core

- Cancelled the common heavy factor on the almost-full
  \(t^{5/9-o(1)}\) hub and obtained the uniform identities
  \(F_j=GR_j\), \(P_{A_0}=GB\), \(B=R_jQ_j\), and
  \(P_{A_j}=F_0Q_j\), with the small exact augmentation
  \(Q_j(1)=C=U/S<S\).
- Proved that residual associate classes contain at most two scalar
  rows.  Their divisor classes force
  \(\Omega(B)\ge\log_2\lceil K/2\rceil=(5/9-o(1))\log_2t\), and
  numerical width gives an almost-full weighted subset-sum atlas.
- Proved the clean-quotient lemma: if the quotient direction is
  transverse to the centre direction, support-sum injectivity forces
  the quotient itself to be a \(C\)-term mask and both factorizations
  to be direct.  Thus every signed switch is direction-contaminated.
- First tested the support-only case of the same-line cyclotomic
  construction: an omitted prime \(p\) forces a \(\Phi_{Sp}\) divisor
  and hence \(C\ge\min\{S,p\}\).  This was only the first-power case;
  the valuation-complete statement is recorded in the Red Team I
  repair below.
- New verifier: pass.  New focused regression: 5/5 pass.

## 13:00--13:15: Red Team I repairs of the simultaneous core

- Corrected the frozen source exponent from the unrelated
  fixed-difference-star exponent \(1/6\) to \(S=t^{7/9+o(1)}\).
  The endpoint certificate now independently asserts
  \((S,U,C)=(7/9,5/6,1/18)\) at exponent level and \(U-S=C\).
- Upgraded the cyclotomic obstruction from prime support to exact
  valuations: if \(a=v_p(m)<v_p(M)\), then
  \(\Phi_{S p^{a+1}}\mid F_M/F_m\), so \(p>C\) cannot vary.  Added
  the smallest missed boundary \(P_3(y^4)/P_3(y^2)=\Phi_{12}(y)\)
  and two gaps larger than one / opposite prime-order regimes.
- Restricted the width-distance identity to one sign class
  \(J_\sigma\).  Added the literal three-row exact-block witness with
  \(X=\{\pm1/2\}\), \(\rho^2=\sqrt2\), and
  \(\lambda_0=1+2\sqrt2\): it has one common positive tangent and
  zero leaf residual widths, but the mixed-sign targets are separated
  by squared distance \(1/\rho^2\).
- Made both pigeonholes explicit.  Clean/contaminated is a rowwise
  direction partition with a \(\lceil K/2\rceil\) majority; a
  contaminated quotient need not be signed.  Mask/signed is a
  different partition with the same majority guarantee, and signed
  rows are necessarily contaminated.
- Repaired verifier: pass.  Expanded focused regression: 7/7 pass;
  32,766 finite Boolean branch partitions checked.

## 13:20--13:47: signed same-line family closed

- Removed the unjustified positivity assumption on the cyclotomic
  quotients.  Reducing the positive product \(P_S(x)R\) modulo
  \(x^S=1\) gives a genuinely nonnegative shadow of mass \(C\), and
  preserves every divisor in the independent leaf direction.
- Proved the sharp positive-multiple lemma for
  \(H_{S,a}=P_S(z^a)/P_S(z)\): every nonzero nonnegative multiple has
  mass at least \(\min\{S,a\}\).  The proof uses the union-of-two-axes
  Fourier support on \(\mathbb Z/a\times\mathbb Z/S\) and the resulting
  rectangle identity; both regimes are sharp.
- For every pair \(m,n\), coprimality of the reduced cyclotomic factors
  forces \(m/(m,n),n/(m,n)\le C\).  A Farey count gives the all-family
  bound \(|\mathcal D|\le C^2=t^{1/9+o(1)}\), closing the signed
  same-line model by a \(4/9\) exponent margin.
- Added the exact nonempty divisor family with \(Q=P_M\), showing that
  the local mechanism is real but has only \(\tau(M)=C^{o(1)}\) rows.
  New focused suite: 4/4 pass.

## 13:47--13:57: finite-quotient shadow and aperiodic boundary

- Extended the cyclic shadow to any centre mask which exactly tiles a
  finite abelian quotient.  Multiplication by the finite tiling
  complement makes the projected positive mask constant on the quotient,
  with nonnegative external shadow of exact mass \(C\); external factors
  remain divisors of the shadow.
- Located the smallest aperiodic escape:
  \((1+x+x^4)(1-x^4+x^5+x^7)\) is a six-term mask and the signed quotient
  has augmentation two.  The centre has no root-of-unity zero, hence no
  finite-quotient tiling shadow.  Every two-point centre has such a shadow,
  so three is minimal.
- This is one local row, not a #1083 counterexample.  New focused suite:
  4/4 pass.

## 13:57--14:17: endpoint normal-form barrier and interface correction

- Tensorized \((1+x)(1-x+x^2)=1+x^3\).  The resulting family has
  \(2^k\) divisor patterns, signed contaminated quotients, all displayed
  mask positivities, and exact endpoint calibration
  \((S,C,U,t)=(2^{14\ell},2^\ell,2^{15\ell},2^{18\ell})\).
- Proved that after a positive \(\mathbb Q\)-linearly independent real
  embedding, a homothety class of mixed \(1/3\)-step boxes has at most
  \(k+1\) rows.  Summing edge logs fixes the scaling shift; exponential
  independence then fixes the bit pattern.  The prefix construction over
  \(3^{1/k}\) attains \(k+1\).
- Self-audit caught a second omitted exact-block interface before blind
  review: the construction takes \(F_0=G\), so centre--leaf
  transversality/coprimality fails in addition to common-\(X\)
  scalar-copy.  The manuscript was therefore downgraded from an
  exact-interface obstruction to a positive-multiple normal-form barrier;
  every claim now names both failures.
- New focused suite: 4/4 pass.  The full lane reached 54/54 before this
  documentation-only boundary repair; a fresh full regression follows.

## 14:17--14:31: transverse \(\Phi_6\)-cube fibre rigidity

- Characterized the one-dimensional positive switch exactly. A binary
  coefficient word remains binary after multiplication by
  \(1-z+z^2\) if and only if its zero padding avoids \(010\) and \(101\).
  Thus every nonempty line fibre has at least two terms, with equality
  only for two consecutive terms.
- Iterated this automaton by slicing in independent switch directions.
  If all \(2^k\) subset-switch states are masks, every nonempty switch-
  lattice fibre has at least \(2^k\) terms. Equality forces, inductively,
  a monomial translate of \(\prod_i(1+z_i)\); torsion-freeness and
  \(\mathbb Z\)-independence of the switch directions are explicit.
- Added the transverse quotient consequence. If \(A=F_0H\), the
  \(S\)-term centre is transverse to the switch span, and the **additional
  hypothesis** \(\pi_W(H)\ge0\) holds, the quotient is torsion-free and a
  sumset bound gives at least \(S\) occupied fibres. Fibre mass then gives
  \(SC\ge S2^k\), hence \(2^k\le C\).
- This closes only the no-cancellation transverse repair of the tensor
  model. A repair with strong signed compression after quotienting by all
  switch directions remains open, as does common-\(X\) scalar-copy.
- New verifier exhausts 8,178 nonempty one-dimensional words, all 511
  masks in a \(3\times3\) rank-two grid, equality models through rank six,
  and the sharp projection model. Focused suite: 4/4 pass.
- Froze `SIGNED_SWITCH_RESULT_DEPENDENCY_MAP.md`: the cyclotomic \(C^2\)
  bound, finite-quotient shadow, and transverse fibre theorem now have
  separate hypothesis ledgers, with their non-overlapping escape routes
  stated explicitly.
- Full lane after integration: 58/58 tests pass in 32.67 seconds; all
  verifier and test modules compile.

## 14:31--14:47: signed transverse binary-box switch bound

- Replaced the extra condition \(\pi_W(H)\ge0\) in the binary-box case by
  a tailored finite shadow. Rational dual functionals to the centre
  directions, vanishing on the transverse leaf span, are cleared by a
  denominator \(D\) and reduced modulo \(2D\). The centre maps to the
  subgroup \(\{0,D\}^k\), which tiles \((\mathbb Z/2D)^k\), while the
  combined quotient retains all leaf directions injectively.
- Verified that multiplying the projected positive complement by the
  quotient tiling set produces a nonnegative shadow of mass **exactly**
  \(C\). Every factor supported in the leaf span remains a divisor of
  that shadow, even when the original quotient is signed.
- Proved the Newton-zonotope mass lemma: a nonnegative integral multiple
  of \(d\) independent factors \(1-z_i+z_i^2\) has mass at least \(2^d\).
  Newton polytopes add without a coefficient-sign assumption on the other
  multiplier; nonnegativity is used only to charge at least one unit of
  mass to each of the \(2^d\) zonotope vertex cones. The bound is sharp.
- For every two tensor patterns, Euclid cancellation and the shadow give
  both one-sided Hamming bounds at most \(\lfloor\log_2C\rfloor\). Thus an
  endpoint family lies in a Hamming ball of radius \(k/7\) and has size at
  most \(S^{H_2(1/7)}=t^{0.4601899388\ldots}\), a
  \(0.0953656167\ldots\) exponent margin below \(5/9\).
- The uniform endpoint masks \(X\) and \(3X\) are actual scalar copies;
  they would require \(C\ge2^k=S\), contradicting \(C<S\). Hence the
  signed transverse binary-box repair is closed. Arbitrary \(X\) and
  arbitrary residual divisors remain open.
- New finite verifier: pass after correcting one nonmathematical test
  threshold (6,604 rather than 10,000 quotient elements were enumerated).
  It also checks all 256 ordered pattern-pair cancellations at rank four
  and four sharp exact common-product models; the shadow certificate now
  starts from a genuinely signed quotient. Focused suite: 6/6 pass.
- Full lane after the binary-box integration: 64/64 tests pass in 34.39
  seconds; every Python module compiles.

## 15:35--15:50: blind cross-audit II

- A fresh implementation reconstructed the cyclotomic mass/Farey bound,
  finite quotient shadows and aperiodic escape, all-subset `Phi_6` fibres,
  tailored binary-box shadows, Hamming/entropy constants, and the
  `X -> 3X` endpoint contradiction.
- Verdict: all four theorem families pass after three minimal repairs:
  explicitly restore prime `S` in the finite-shadow cyclotomic corollary,
  correct the final decimal digit of the exponent margin, and replace an
  ambiguous dependency-map row reference.  The `C=0` firewall passes.
- The independent verifier passes, its pytest wrapper reports 2/2, and the
  five affected author modules report 22/22.  Arbitrary residual divisors,
  general common-`X`, and outer exact-block stability remain open.
