# Erdős #1083 six-hour attack

The principal result is
`APPROXIMATE_STABILITY_COUNTEREXAMPLE.md`: a genuine endpoint-scale
Følner construction showing that the earlier exact direct-tiling
transverse-rank theorem has no qualitative (o(SU)) stability
extension.

The construction keeps exact row injectivity, endpoint values of
(S,U,SU), positive tangent squares, a tangent-universe cap below
(t), and a real reverse-circle interface.  Its transverse rank
tends to infinity while every row spectrum differs from one common
spectrum in (o(SU)) entries.

It is not a counterexample to Erdős #1083; see the geometry firewall
and `CLAIM_LEDGER.md`.

`SHARP_FOLNER_TRADEOFF_AND_REPAIRED_TARGET.md` optimizes the
construction to a power-growing transverse family and proves the
exact tangent-transversality dichotomy contributed by a full frozen
block.

The exact-block branch is continued through
`TRANSVERSE_NONZERO_DIFFERENCE_THEOREM.md`,
`BOUNDED_TRANSVERSE_CYCLE_THEOREM.md`, and
`MANY_BOUNDED_CYCLES_DICHOTOMY.md`.  The last file upgrades one short
cycle to \(t^{8/9+o(1)}\) pairwise edge-disjoint short cycles and gives
a network-scale coherent/noncoherent dichotomy.  The coherent local
normal form and its strict four-row realization are classified in
`COHERENT_CYCLE_CLASSIFICATION_AND_MODEL.md`.

`SHARED_ENDPOINT_PATH_ENERGY.md` amplifies the same fixed-difference
graph through length-15 simple paths.  It fixes two endpoint rows,
both endpoint source labels, and the orientation sum on a
\(t^{2/9+o(1)}\)-sized path bundle, yielding a sparse-height-relation
versus common-defect-vector dichotomy.

In the zero-common-defect branch,
`COHERENT_THETA_AMPLIFICATION.md` iterates exact midpoint energy from
length 80 down to length 5.  It forces either a shared lifted-row hub
or an internally vertex-disjoint coherent theta graph with
\(t^{1/144+o(1)}\) arms on four fixed parabolic potential levels.

`PATH_ENERGY_MULTIPLICITY_RED_TEAM.md` independently recomputes every
path exponent and audits orientation-word, midpoint-fibre, path
simplicity, and cross-path overlap multiplicities.

`DEFECT_TRANSITION_TRICHOTOMY.md` resolves the nonzero common-defect
branch at the structural level: transition misalignment gives a
noncoherent cycle of length at most 160, while aligned defects yield
a coherent short theta-or-hub with \(t^{1/20+o(1)}\) arms.  A final
tangent/distance-label conversion is still open.

The phase-one dependency graph, branch outputs, multiplicity audit,
and common missing distance-budget interface are frozen in
`PHASE_ONE_FREEZE_0130.md`.
