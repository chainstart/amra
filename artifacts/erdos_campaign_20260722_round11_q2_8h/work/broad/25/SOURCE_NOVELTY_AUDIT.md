# Erdős #25: source and preliminary novelty audit

Date checked: 2026-07-22.

## Sources checked

- The official problem page, <https://www.erdosproblems.com/25>, still lists
  the general activated one-residue-class problem as open.
- Jakub Chojecki's public note, *On Erdős Problem 25*,
  <https://www.ulam.ai/research/erdos25.pdf> (dated 19 March 2026), proves the
  summable reciprocal-modulus case and a pairwise-coprime case and develops a
  first-kill reduction.  A direct text check found no occurrence of the terms
  `chain`, `width`, or `clique`; the note does explicitly discuss the
  instability of naive inclusion--exclusion.
- Francisco Araújo, *Sarnak's Program for Erdős Sieves. Part I: Topological
  Dynamics and Light Tails*, <https://arxiv.org/abs/2602.24031> (submitted 27
  February 2026), treats light-tail hypotheses in a broader dynamical
  framework.
- Earlier local audits also checked the Davenport--Erdős theorem on multiples
  and Erdős's primitive-sequence summability theorem; those results underlie
  several already known special cases but do not state the graph-complexity
  criteria used here.

## What was and was not established

The directed check above found no exact statement matching the formulas below,
but adversarial internal comparison also found that some formally new-looking
statements add no new coverage:

1. a fresh finite Dilworth partition at every cutoff with low divisibility
   width (**downgraded**: after global redundancy removal this forces only
   polylogarithmically many effective moduli and hence a summable reciprocal
   tail, so the conclusion follows from the known light-tail case);
2. `o(x)` compatible-clique count (or the degeneracy bound) after redundant
   classes are removed;
3. logarithmically averaged compatible-clique entropy;
4. the pointwise and logarithmically averaged hybrid light-tail /
   low-clique-core criterion;
5. the harmonic-weighted compatible-clique boundary criterion.
6. the Möbius-compressed activated-intersection criterion, including its
   stronger two-state form that combines the common complete progression
   before charging the deleted first representative, in both natural- and
   logarithmic-density forms.

This is only a preliminary novelty screen, not proof of priority or an
exhaustive literature review.  In particular, terminology may differ across
covering-systems, sieve, Boolean-complexity, and periodic-set literature.
No publication claim should be made before a systematic MathSciNet/zbMATH
search and review by a specialist.

The new Möbius formulation is algebraically standard in spirit (finite
inclusion--exclusion grouped through an intersection poset).  The audit has
not established that its particular activated `(L,r,epsilon)` boundary
criterion is absent from the covering-systems literature.  Its value here is
the exact exponential separation from raw clique accounting on the realised
squarefree finite blocks, not a priority claim.  No infinite-system example
separating the covered classes of the two criteria has been proved.

## Publication boundary

The non-downgraded criteria form a coherent structural package and are stronger
than a single isolated lemma.  Uniformly bounded compatibility degeneracy is
also already subsumed by light tails: finitely color the compatibility graph;
within each color the complete classes are disjoint, so their reciprocal
moduli sum to at most one.  Any genuine novelty in the degeneracy criterion
therefore requires growing degeneracy or an actual clique bound much sharper
than that crude estimate.  The package still does not close Erdős #25 or
change a known universal exponent and remains below the SCI-Q2 threshold.
