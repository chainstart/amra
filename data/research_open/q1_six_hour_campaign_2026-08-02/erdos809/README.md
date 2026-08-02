# Erdős #809 — 2026-08-02 six-hour attack

Start: 2026-08-02 10:34:51 HKT

Baseline: `669bbad1908e7ab7d8382a8b508e67757006e90c`

## Frozen public statement

For fixed `k >= 3`, let `F_k(n)` be the minimum number of colours needed
on an `n`-vertex graph with `floor(n^2/4)+1` edges so that every
`C_{2k+1}` is rainbow.  The open case is `k=3`: prove or refute

\[
F_3(n)\sim n^2/8.
\]

The cases `k >= 4` are inherited as known.  Nothing in this directory
changes the public status unless the full `C_7` interface is closed.

## Frozen local gate

The maximum-degree branch is reduced to a global reserve obstruction.
The same-neighbourhood star has a quadratic exit.  The remaining `B`-side
configuration is one centred opposite-neighbourhood zero-star satisfying
the exact reserve/residual inequality from the 2026-08-01 campaign.  The
outer-`A` residual is separate.

This round first attacks the fact that all leaves of an opposite star live
in one common complementary host.  Their *union* has a smaller common
exceptional set than any individual leaf.  This gives a new exact
intersection-versus-synchronization theorem; see
`OPPOSITE_STAR_COMMON_HOST_DICHOTOMY.md`.

The synchronized endpoint is then connected back to the *actual* global
reserve: each leaf outside the union host is isolated inside the active
leaf set, while every nonisolated leaf consumes one synchronization
deficit.  See `OPPOSITE_STAR_SYNCHRONIZATION_RESERVE.md`.

The first integer synchronization threshold is rigid: below
`A_L=ell` the leaves are independent, while equality with any leaf edge
forces a complete leaf system.  See
`OPPOSITE_STAR_LEAF_DEFICIT_RIGIDITY.md`.

A quantitatively dense leaf system can itself supply enough pairwise
`C_7`-compatible edges to close the colour target; see
`OPPOSITE_STAR_DENSE_LEAF_COLOR_EXIT.md`.

At the nonempty critical endpoint `A_L=ell`, clique adjacency forces
the leaf colour supports to be disjoint and yields a stronger
missing-`A` rectangle; see
`OPPOSITE_STAR_CRITICAL_CLIQUE_ENDPOINT.md`.

For arbitrary leaf graphs, every centre colour supports an independent
leaf subset; reserve failure then bounds that independence number and
strengthens both coordinate and `M_B` transference bounds.  See
`OPPOSITE_STAR_COLOUR_SUPPORT_COMPRESSION.md`.

The full union host, rather than only the common intersection, is
anticomplete to the centre neighbourhood.  This removes every
synchronization-defect loss from the resulting \(A\)-side rectangle
and yields a closed quadratic colour-mass cap; see
`OPPOSITE_STAR_UNION_RECTANGLE_ENERGY.md`.

An exact three-budget conservation identity then shows that defect not
paid by the actual \(B\)-reserve must enlarge that same union rectangle,
giving a sharper quadratic-root cap; see
`OPPOSITE_STAR_THREE_BUDGET_CONSERVATION.md`.

The same synchronization deficit also exposes a missing rectangle
inside the maximum-degree set `A`, giving a simultaneous two-budget
certificate; see `OPPOSITE_STAR_COMMON_COORDINATE_ENERGY.md`.

Minimum degree and the exact edge ledger transfer that canonical
missing rectangle back into a lower bound for the required `M_B`
budget; see `OPPOSITE_STAR_RECTANGLE_BUDGET_TRANSFERENCE.md`.

The formerly separate outer-`A` residue is now localized exactly to
the low-`B`-degree good edges; see
`OUTER_A_LOW_DEGREE_RESIDUE_THEOREM.md`.

If the internal-\(A\) part of that low residue is sufficiently large,
minimum degree makes it a direct pairwise-\(C_7\)-compatible colour
family; see `OUTER_A_INTERNAL_LOW_DENSE_EXIT.md`.

Colourwise cancellation eliminates the former free cross-low term:
the only positive remainder is a mixed colour anchored to a unique
high internal edge.  See
`../erdos1083/ERDOS809_OUTER_LOW_MIXED_HIGH_IDENTITY.md` and its
independent audit `OUTER_A_MIXED_HIGH_INDEPENDENT_AUDIT.md`.

Every coherent zero-star's total leaf--colour incidence mass is paid
linearly by \(D_B\), yielding \(2\ell\le H\le D_B\) and the universal
selected-star cap \(E_0\le4f(D_B-\ell)\).  See
`../erdos1083/ERDOS809_ZERO_STAR_DEFECT_MASS_LEDGER.md` and
`ZERO_STAR_DEFECT_MASS_INDEPENDENT_AUDIT.md`.

In the opposite branch, retaining the truncation term in the exact
reserve energy gives
\(R_L+\Xi\le2(g+1)\ell+2(D_B-H)-2\).  Moreover the common residual
contains the centre and every leaf outside the union host, so
\(r\ge t+1\) and the isolated-leaf term is charged explicitly.
See
`OPPOSITE_STAR_DEFECT_SLACK_ENERGY.md` and its independent audit
`OPPOSITE_STAR_DEFECT_SLACK_INDEPENDENT_AUDIT.md`.

The maximum witness supplies a second basepoint in the common residual,
improving this to \(r\ge t+2\) and \(\rho_c\ge3\).  Combining three
disjoint missing-pair families with the exact average-degree ceiling
first excludes \(g\le2\).  Charging the remaining common-residual
vertices against the maximum-degree cap then eliminates both apparent
\(g=3\) parity endpoints.  Thus B-opposite requires
\(g=\Delta-\delta\ge4\).  Optimizing the same charge over the centre
degree and synchronization size gives the much stronger parity-sharp
scalar barriers
\(n\le2g^2-2g-6\) (even) and
\(n\le2g^2-2g-3\) (odd), hence \(g=\Omega(\sqrt n)\).  Both constants
are attained by explicit graphs satisfying the local
degree/opposite-shore hypotheses and, for \(g\ge5\), \(L_4(2)\).  They
admit rainbow recolourings with a zero-shore pair of multiplicity \(g\),
but the forced missing-star reserve already pays all \(D_B=g\), so they
do not realize hard reserve failure.  See
`MAXIMUM_WITNESS_OPPOSITE_DEGREE_SPREAD.md`.

The square-root note has now passed an independent blind audit recorded
in `MAXIMUM_WITNESS_SQRT_SPREAD_BLIND_AUDIT.md`.  The audit reconstructed
the four charges, parity factorization, sharp graphs, recolouring defect
and reserve, and all typed \(L_4(2)\) templates.  One local expository
repair spells out the two possible \(C_7\) endpoint pairings; no theorem
statement or constant changed.

All inherited and new coordinates are composed in
`MAXIMUM_WITNESS_CANONICAL_HARDNESS_NORMAL_FORM.md`, which gives one
explicit two-branch obstruction system for a hard maximum witness.

## Status

- Erdős #809: **OPEN / NOT CLAIMED**.
- Maximum-degree Case 1: **OPEN / NOT CLAIMED**.
- New common-host dichotomy: **PROVED**, pending independent cross-audit.
- New synchronization--reserve bridge: **PROVED**, pending independent
  cross-audit.
- New common-coordinate missing-energy theorem: **PROVED**, pending
  independent cross-audit.
- New synchronization-free union-host energy theorem: **PROVED and
  independently cross-audited**.
- New exact three-budget conservation theorem: **PROVED and independently
  cross-audited**.
- New rectangle-to-`B` budget transference: **PROVED**, pending
  independent cross-audit.
- New exact low-degree localization of `R_A`: **PROVED**, pending
  independent cross-audit.
- New internal-low dense colour exit: **PROVED**, pending independent
  cross-audit.
- New mixed-high outer-residue identity: **PROVED and independently
  audited**.
- New zero-star defect-mass ledger: **PROVED and independently
  audited**.
- New opposite-star defect-slack energy and common-residual basepoint
  bound: **PROVED and independently audited**.
- New parity-sharp maximum-witness degree-spread barrier
  \(g=\Omega(\sqrt n)\), including complete elimination of the apparent
  \(g=3\) endpoint: **PROVED and independently blind-audited after one
  local expository repair**.
- Canonical maximum-witness hardness normal form: **PROVED by composition
  and independently reaudited after repair, then sharpened by the two
  separately audited ledgers above**; this certifies only an exhaustive
  necessary A / B-same / B-opposite normal form.
- Full opposite-star closure and outer-`A` absorption: **OPEN**.
