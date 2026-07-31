# Erdős #809 — phase-one freeze

Freeze time: 2026-08-01 01:53 HKT

## Classification

- Erdős #809: **OPEN / NOT CLAIMED**.
- Maximum-degree Case 1: **OPEN / NOT CLAIMED**.
- Global \(B\)-reserve obstruction: **reduced to an exact canonical
  matching/star trichotomy**.
- Outer-\(A\) residue \(R_A\): **still separate and open**.

## Proved during this phase

1. The adaptive defect-token problem has an exact matroid-intersection
   criterion, but the stronger numerical closure uses only the global
   reserve union.
2. Every global obstruction forces exact repeated-zero mass,
   low-boundary localization, and the vertex-cover defect inequality.
3. A linear matching of zero-shore pairs synchronizes through a common
   missing anchor into aligned anticomplete endpoint blocks.  Iteration
   gives
   \[
   |\mathcal Q|
   \ge
   \frac{d_0}{2\overline M-d_0}f^2.
   \]
4. The synchronized blocks have common complementary hosts and an
   anchored missing-energy lower bound.
5. A matching with colour mass \(H_F\) satisfies the new weighted
   two-energy inequality
   \[
   d_0^2H_F^2
   \le
   \overline M^2M_A|\mathcal Q|.
   \]
6. Any remaining repeated mass concentrates on a same- or
   opposite-neighbourhood coherent star.
7. A same-type star with \(\ell\) leaves forces
   \[
   |\mathcal Q|\ge\binom{\ell}{2}-\kappa\ell
   \]
   and has an explicit closed weighted cap.
8. An opposite-type star satisfies the exact leafwise
   reserve--residual inequality (5) in
   OPPOSITE_STAR_RESERVE_ENERGY.md, including the coarse form
   \[
   2|\mathcal Q|
   \ge
   2W_L+R_L-2(m-\delta-1)\ell.
   \]

The composition is Theorem 1.1 of
GLOBAL_WEIGHTED_OBSTRUCTION_TRICHOTOMY.md.  It leaves one centred
opposite-star residue, rather than an arbitrary aggregate of
zero-shore rectangles.

## Audit status

The core synchronization, common-host, and rectangle-transference
proofs passed an independent blind audit:

- every labelled graph on at most six vertices;
- 178,151 zero-pair matchings;
- the exact anchor, orientation, batch-disjointness, and potential
  arguments.

That audit found and triggered repairs to two harmless scope corners
and one finite-verifier orientation model.  The later weighted and
star extensions have:

- direct all-parameter proofs;
- 21 local regression tests passing together;
- 20,000 random weighted incidence/graph checks;
- exhaustive checks on 33,866 small graphs for each star type;
- 94,276 same-star leaf subsets and 6,600 active opposite-star subsets;
- over 12 million exact parameter checks.

They still require an independent phase-two blind audit before any
publication claim.

## Exact next gate

Under genuine global reserve failure, prove that the opposite-star
residue
\[
 2W+R
 \le
 2(D_B-1)+2(m-\delta-1)\ell
\]
either pays the edge-energy slack \(S_m\) or supplies an aligned
\((1/2+s-o(1))n\)-vertex compatible core through the common
complementary host and \(L_4(2)\) connectors.  Then absorb the separate
outer-\(A\) residue.
