# Gårding moving-certificate route for OPG-1757

## Status

This is a survivor-deepening note for `M004`, not a proof of OPG-1757 and not
a novelty claim.  The key representation and recursive criterion are due to
Fang--Ma (arXiv:2604.27755v2, 2026).  The point of this note is to replace the
failed fixed coefficient/channel searches by the exact moving certificate
that the current literature exposes.

Primary sources:

- Fang--Ma, *Gårding polynomials*, arXiv:2604.27755v2, especially Proposition
  13.9, Lemma 14.5, Problem 14.17, and Appendix B:
  https://arxiv.org/abs/2604.27755
- Erickson, *Sums of squares and negative correlation for spanning forests of
  series parallel graphs*, arXiv:1008.3660:
  https://arxiv.org/abs/1008.3660
- Wagner, *Negatively correlated random variables and Mason's conjecture*,
  arXiv:math/0602648:
  https://arxiv.org/abs/math/0602648

## Exact bridge

For a matroid `M`, let

```
C_M(w) = sum_{X subset E, E\X independent} w^X.
```

For a graphic matroid, `C_M` is the inversion of the unrooted forest
polynomial.  Thus `C_M` is Rayleigh if and only if the weighted unrooted
forest polynomial is Rayleigh.  A multi-affine Gårding polynomial with
nonnegative coefficients is Rayleigh, so it suffices to prove that graphic
matroids are C-Gårding.  Fang--Ma explicitly leave this as Problem 14.17.

For an edge `e`, define

```
xi_e(M) = C_{M\e} - C_{M/e}.
```

The coefficients of `xi_e` are nonnegative.  Proposition 13.9 states the
recursive equivalence

```
M is C-Gårding
  iff there exists e such that
      M\e is C-Gårding
      and xi_e(M) triangleleft C_{M\e}.
```

Here `f triangleleft g` is a positivity-component domination condition; it is
not coefficientwise nonnegativity and not merely positivity on the positive
orthant.  This is exactly the missing information discarded by mechanisms
`M001`, `M007`, and `M012`.

## Why this changes the search architecture

The failed routes fixed one edge order or demanded every coefficient/channel
be nonnegative.  The correct recursive statement only asks that **some edge**
work at each minor and permits the edge to change after deletion.  Its
certificate lives on the distinguished positivity component of
`C_{M\e}`, so negative monomial coefficients in a Rayleigh difference do not
refute it.

The old K4 coefficient obstruction is therefore diagnostic rather than fatal.
Appendix B of Fang--Ma verifies a positivity-component certificate for the
**spanning-set** polynomial of `M(K4)` (not directly the `C/xi_e` certificate)
using the identity

```
(xy+z-2)(yz+x-2)(xz+y-2)
  - (xyz-1)(x+y+z-3)^2
  = (x-1)^2 (y-1)^2 (z-1)^2.
```

It is only an analogy to the same qualitative phenomenon as our exact
disjoint-K4 formula:
the negative cross coefficient belongs inside a complete square plus positive
channels, not in an individually positive coefficient row.

Erickson's series-parallel SOS theorem and Fang--Ma's closure under
series-parallel connections and 2-sums subsume the cactus/one-sum probes in
this campaign.  Those probes remain useful checks, but are not frontier
lemmas.

## Exact next lemma

The strongest closure-equivalent next lemma is:

> **Moving-edge domination lemma (graphic case).**  Every nonempty loopless
> graphic matroid `M=M(G)` has an edge `e` such that
> `xi_e(M) triangleleft C_{M\e}`.

Strong induction on `|E(M)|`, followed by Proposition 13.9, then proves that
all graphic matroids are C-Gårding and hence proves weighted OPG-1757.  A
3-connected-only search is justified only after explicitly decomposing a
minimal counterexample using direct sums, series/parallel connections, and
2-sums; this reduction cannot be silently assumed because `M\e` need not
remain 3-connected.  The lemma is stronger than Rayleigh and is currently
open; failure of this stronger lemma would not disprove OPG-1757.

## First adversarial host and kill tests

K4 is already covered by the at-most-six-element theorem.  After the explicit
decomposition reduction, `W4` (8 edges) is a smaller new 3-connected simple
host; K5 (10 edges) remains the first especially symmetric host and is useful
for orbit reduction.

For each edge orbit in a host `G`:

1. Construct `C_{M\e}`, `C_{M/e}`, and `xi_e` exactly.
2. Reject tests that check only the positive orthant: domination is defined on
   the full distinguished positivity component.
3. Search negative rays from the positive component boundary.  A point with
   `C_{M\e}>0` in the distinguished component but `xi_e<=0` kills that edge.
4. Kill the moving-edge lemma for `G` only if every edge orbit is killed.
5. If an edge survives, seek an exact boundary reduction/SOS certificate;
   numerical sampling is routing evidence only.

The resource-safe first computation is orbit-reduced exact/symbolic work on
K5 specializations.  Lean is reserved for checking any resulting polynomial
identity or inequality after the analytic component membership has been
proved on paper; Lean should not be used as a positivity-component search
engine.

## Promotion decision

No promotion.  This note identifies a literature-backed representation and a
closure-equivalent decisive lemma, but proves neither the moving-edge
domination lemma nor OPG-1757.  Public status remains unchanged.
