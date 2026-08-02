# Erdős #1083 six-hour attack (2026-08-02)

This workstream attacks the exact missing interface left by the
2026-07-31 campaign.  The public problem asks whether, for fixed
\(d\ge3\), every \(N\)-point subset of \(\mathbb R^d\) determines
\(N^{2/d-o(1)}\) distances.  In dimension three the inherited lower
bound is \(N^{3/5-o(1)}\); no improvement of that exponent is claimed
at freeze.

The frozen exact-block branch has

\[
 q=t^{13/18+o(1)},\quad S=t^{7/9+o(1)},\quad
 U=t^{5/6+o(1)},\quad |T_*|\le t^{1+o(1)},
\]

and exact row partitions

\[
 V=(\rho^2+z_i^2+T_i)\oplus(2\rho z_iX),
 \qquad |V|=SU=t^{29/18+o(1)}.
\]

The previous campaign extracts, in its transverse-heavy branch, a
fixed nonzero tangent difference and then a bounded noncoherent cycle,
a sparse height relation, or a coherent theta/lifted-row hub.  The
first unresolved gate is to use the *full* partitions \(T_i\), not just
the local row graph, to force more than \(t^{3+o(1)}\) global distance
labels or a power-large ruled/commensurate configuration.

The first attack is adversarial.  `COHERENT_THETA_EUCLIDEAN_NO_GO.md`
proves that the coherent theta output has no standalone
distance-budget force even after all its selected records are realized
by genuine points in \(\mathbb R^3\).  The construction fixes the
tangent difference, both lifted
endpoints, the orientation word, the endpoint tangent, the internal
tangent, and one common anchor-distance label.  It has \(K\) internally
disjoint coherent arms for every \(K\le S-1\), while its complete local
point set has only \(O(S^2)\) pairwise distances.  This is a sharp
no-go for any closure lemma that consumes only the theta record; it is
not a counterexample to #1083 because
it does not realize the \(U\)-cell common-spectrum partitions.

The exact radical verifier and five focused regression tests pass.

The first positive use of the omitted cells is
`EXACT_BLOCK_TRANSVERSE_STAR_CLUSTER.md`.  Exact direct tiling and
\(U<S^2\) make the transverse row graph triangle-free.  The inherited
fixed-\(\delta\) graph therefore has a \(t^{1/6+o(1)}\)-leaf star
whose leaves are pairwise nontransverse.  Equivalently, every pair of
leaf-height ratios lies in the quotient set of
\(\operatorname{span}_{\mathbb Q}(X-X)\).  In rank one this is a
genuine rationally commensurate family; in rank two it has an exact
common-line/three-dimensional-ambient dichotomy.  The new verifier and
four focused tests pass.

A stronger averaging over row--tangent slots gives, in the
transverse-heavy branch, one *fixed tangent* and
\(t^{5/9+o(1)}\) transverse leaves.  Triangle-freeness makes their
direction spaces pairwise intersecting.  Pairwise intersection does
not by itself imply one common direction, even in rank two; the file
contains explicit common-line and three-dimensional-top boundary
examples so those alternatives are not conflated.

`MASK_FACTOR_SUNFLOWER_INVERSE.md` uses the masks of the full exact
partitions to go beyond this linear-algebra barrier.  Every leaf mask
divides the centre row's \(U\)-term complement mask, so \(S\mid U\),
and every two leaf masks share a nonunit irreducible factor.  If a
leaf has \(r\) distinct irreducible factors, one factor is shared by
at least \(1+\lceil(|L|-1)/r\rceil\) leaves.  Hence the high-rank
residual is now either an almost-full common mask factor/common
Newton direction or a power-large supply of augmentation-unit
factors.  A cyclotomic construction proves that the latter cannot be
excluded from support size alone.  Its verifier and four focused
tests pass.

The surviving exact-block gate is therefore geometric control of
augmentation-unit factors (or a denominator-free escape from the
common-factor chart), followed by stability back to the original
near-extremal point set.

`HEAVY_SKELETON_RULED_CHART.md` sharpens that residual without any
factor-count hypothesis.  Because a leaf quotient has augmentation
\(C=U/S=t^{1/18+o(1)}\), it can omit only \(\log_2 C\) of the
centre complement's at most \(\log_2U\) heavy factor occurrences.
An entropy pigeonhole synchronizes the entire heavy-factor skeleton
on

\[
 t^{\beta+o(1)},\qquad
 \beta=\frac59-\frac56H_2(1/15)
       =0.2610894430\ldots
\]

leaves.  On this family \(F_j=HE_j\), with
\(|H(1)|=S\) and \(|E_j(1)|=1\).  A fixed Newton direction of \(H\)
puts the heights and their common-tangent distance cells in an
explicit denominator-free reciprocal ruled chart.  Exact
\(0/1\)-support and scalar-copy rigidity further force power-many
distinct augmentation-unit switching residuals \(E_j\).  A separate
signed trade shows why the algebraic quotient itself need not be a
positive set mask.  The verifier and four regression tests pass.

The strongest common-direction conclusion is now
`HEAVY_FACTOR_HUB_RULED_CHART.md`.  Every leaf mask has augmentation
\(S>1\), hence contains a factor of augmentation magnitude at least
two.  The common centre complement has only \(O(\log U)\) such factor
occurrences.  One normalized heavy irreducible factor therefore
divides \(t^{5/9-o(1)}\) fixed-tangent leaf masks.  Its Newton
direction puts this almost-full family in the explicit reciprocal
chart

\[
 z_j=\frac{h}{2\rho w_j},\qquad
 \rho^2+\tau_0+\frac{h^2}{4\rho^2w_j^2}+\frac h{w_j}X.
\]

This removes augmentation-unit richness as an obstruction to finding
one power-large common direction.  The entropy theorem remains the
finer synchronization of the *complete* heavy skeleton.

`UNIT_SWITCH_WIDTH_ATLAS.md` shows that the complete-skeleton
residuals are divisors of one common quotient with
\(\Omega(\log t)\) augmentation-unit factor occurrences.  Numerical
Newton width turns their height parameters into distinct weighted
subset sums and the \(w_j\)'s into their reciprocals.

Finally, `SIMULTANEOUS_POSITIVE_COMPLEMENT_NO_GO.md` proves that even
positivity of both complements in a transverse pair does not make the
signed quotient positive.  For every \(S\ge4\), it constructs a
genuine two-row Euclidean exact block with \(U=3S<S^2\), positive
tangent sets, a shared literal tangent, and a negative switching
coefficient.  Thus the next positive theorem must use simultaneous
constraints from the full power-large leaf family; no two-row
positivity argument can close the branch.

`POWER_LARGE_SIMULTANEOUS_SWITCH_CORE.md` now records the simultaneous
structure on the almost-full heavy-factor hub.  On
\(K=t^{5/9-o(1)}\) rows one has
\[
 F_j=GR_j,\quad P_{A_0}=GB,\quad B=R_jQ_j,\quad P_{A_j}=F_0Q_j,
 \qquad Q_j(1)=C=U/S<S.
\]
The residuals occupy at least \(\lceil K/2\rceil\) divisor classes of
one \(B\), forcing \(\Omega(B)\ge(5/9-o(1))\log_2t\) and an almost-full
weighted width atlas.  Its distance formula is valid on a fixed-sign
half; a literal three-row common-tangent exact block shows it fails
across opposite signs even when both residual widths vanish.

If the quotient direction is transverse to the centre direction,
positivity of \(F_0Q_j\) forces \(Q_j\) itself to be a \(C\)-term mask.
The rowwise clean/contaminated partition has a class of size at least
\(\lceil K/2\rceil\); contamination means only that a quotient direction
returns to the centre space and does not imply that the quotient is
signed.  A separate mask/signed partition also has a class of that size,
and every signed row is contaminated.

`CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md` closes the entire
same-line cyclotomic model, including signed quotients.  For two selected
scales \(m,n\), with \(g=(m,n)\), positivity of the common-centre
multiples has a nonnegative cyclic shadow of mass \(C\).  A sharp
CRT--Fourier lemma then forces

\[
 m/g\le C,\qquad n/g\le C.
\]

Consequently every family has size at most
\(1+2\sum_{r=2}^C\varphi(r)\le C^2=t^{1/9+o(1)}\), polynomially below
the required \(t^{5/9-o(1)}\).  The finite-quotient theorem in
`FINITE_QUOTIENT_SHADOW_ESCAPE.md` extends this bound to every centre
mask which tiles a finite abelian quotient.  The exact identity

\[
 (1+x+x^4)(1-x^4+x^5+x^7)
 =1+x+x^6+x^7+x^9+x^{11}
\]

shows the sharp boundary: the smallest aperiodic three-term centre can
hide a signed quotient of augmentation two, but supplies only one row.

`MULTIDIRECTIONAL_TENSOR_SWITCH_BARRIER.md` gives \(2^k\) signed
switches at the exact endpoint augmentations while satisfying the
displayed simultaneous identities and all three mask positivities.  It
is deliberately only a positive-multiple normal-form barrier, not an
exact-block model: it takes \(F_0=G\), so centre--leaf
transversality/coprimality fails, and its mixed tensor source masks are
not scalar copies of one \(X\).  Within this model every homothety class
has at most \(k+1\), sharply.  Thus the surviving algebraic gate must use
both omitted interfaces simultaneously: a transverse scalar-copy
simultaneous-switch theorem for aperiodic centres.

`PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md` rules out the simplest
transverse repair of that tensor barrier. If all \(2^k\) \(\Phi_6\)
switch states remain masks, every switch-direction fibre has at least
\(2^k\) terms, with equality only for the standard binary tensor box.
For a transverse \(S\)-term centre, coefficientwise nonnegativity of the
regularizer after quotienting out the switch directions then forces
\(2^k\le C\). This quotient nonnegativity is explicitly an extra
hypothesis: the unresolved repair must use strong signed quotient
cancellation, and still must meet the common-\(X\) interface.

For binary-box centres,
TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md removes the extra projection
sign hypothesis. A separating finite quotient can be chosen to tile the
centre while annihilating the transverse leaf span. It preserves every
independent \(\Phi_6\) factor in a nonnegative shadow of exact mass \(C\),
so two tensor patterns have at most \(\log_2C\) switches in either
direction. At the endpoint the family is at most

\[
 S^{H_2(1/7)}
 =t^{0.4601899388\ldots}
 \ll t^{5/9-o(1)}.
\]

In particular the genuine scalar-copy endpoints \(X\) and \(3X\) force
\(C\ge S\), contradicting \(C<S\). This now closes the signed transverse
repair of the explicit binary-box tensor model. It remains specific to
binary \(X\) and independent \(\Phi_6\) residuals.

`FULL_EUCLIDEAN_INTERVAL_MULTIROW_NO_GO.md` records a **new,
author-verified, not yet blind-audited, and not-finally-admitted** scope
candidate left by the first theta no-go.  For every nonsquare \(S\) and
\(2\le C<S\), interval tilings give one centre and one leaf for every
divisor \(m\mid C\) with \(m^2<C\).  Every row has all \(U=SC\) positive
tangents, every one of its \(SU\) source--target distances maps
bijectively to one common spectrum, all rows share a literal tangent,
and the whole construction is realized by genuine points in
\(\mathbb R^3\).  The centre is transverse to every leaf.  Squarefree
\(C\) gives \(2^{\omega(C)-1}\) leaves, so the full Euclidean interface
supports arbitrarily many rows.  However the construction always has
fewer than \(\sqrt C=t^{1/36+o(1)}\) leaves, far below the required
\(t^{5/9-o(1)}\).  It therefore proves that the power-large scale, not
merely completion of all tangent cells, is an essential input.  It does
not improve the inherited public exponent \(N^{3/5-o(1)}\).

The five admitted focused suites contribute 22 tests; together with the
repaired seven-test simultaneous core, the admitted signed-switch lane has
64/64 tests passing.  The post-audit interval candidate separately adds
four author-verification tests and is not included in that admitted count.
The signed-switch theorem manuscripts and their dependency map have passed
blind cross-audit; see `SIGNED_SWITCH_BLIND_AUDIT_II.md`.

See `SIGNED_SWITCH_RESULT_DEPENDENCY_MAP.md` for the non-overlapping
hypotheses and residual gates of the three signed-switch theorems,
`CLAIM_LEDGER.md` for claim boundaries, and `RESEARCH_LOG.md` for the
live proof audit.
