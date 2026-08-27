# Literature boundary and source ambiguity

Checked: 2026-08-27.

This is an author-side scoped search, not an independent novelty audit.

## Primary problem source

Paul Erdős, *A survey of problems in combinatorial number theory*, Annals of
Discrete Mathematics 6 (1980), 89--115, p. 114:

* https://www.renyi.hu/~p_erdos/1980-03.pdf

The displayed formulation says that each product runs over a subset of the
sequence, so it is naturally the distinct-elements variant.  The same
paragraph reports that Ruzsa answered both density-one questions negatively,
claimed upper density below `1/e` for the infinite problem, and a fixed
positive finite deficit.  No proof or publication is identified there.

## Current status record and ambiguity

The maintained Erdős Problems entry #786, last edited 2026-04-11, separates
two variants:

* https://www.erdosproblems.com/786
* https://www.erdosproblems.com/forum/thread/786

It records the additive-function obstruction for products with repetition,
but treats the distinct-elements version as open.  The entry explicitly
notes the conflict with the wording and Ruzsa attribution in the 1980 source
and suggests that the old attribution may have conflated the variants.  The
2026 discussion contains a contiguity heuristic for short products, not a
published all-parameter theorem implying the finite linear deficit in the
distinct-elements model.

This ambiguity prevents a claim that Theorem G.2 is the unconditional best
result ever known.  It does not invalidate G.1--G.3, whose variant is frozen
and explicit.

## Additive-function result

P. Erdős, I. Ruzsa, and A. Sárközi, *On the number of solutions of
`f(n)=a` for additive functions*, Acta Arithmetica 24 (1973), 1--9,
DOI `10.4064/aa-24-1-1-9`:

* https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/24/1/98716/on-the-number-of-solutions-of-f-n-a-for-additive-functions
* https://matwbn.icm.edu.pl/ksiazki/aa/aa24/aa2411.pdf

The paper bounds level sets of additive functions.  It applies directly after
the standard linear-algebra reduction when factor repetition is permitted.
That reduction uses multiplicities and is not a proof for distinct Finsets.
The grid theorem neither invokes nor improves the additive-function theorem.

## Multiplicative Sidon literature

The following primary papers were checked for nearby terminology and graph
encodings:

* H. Liu and P. P. Pach, *The number of multiplicative Sidon sets of
  integers*, arXiv:1808.06182.
* D. Wood, *Colourings of the Cartesian Product of Graphs and Multiplicative
  Sidon Sets*, arXiv:math/0511262.

Multiplicative `k`-Sidon sets forbid equal products with equal shore length
`k`, or equations `ax=by` with bounded coefficients.  Theorem G.2 instead
uses unequal shores and studies the deletion transversal of a complete
family of long `K_(d-1,d)` relations.  No matching statement or the
`log N-2 sqrt(log N log log N)` transversal scale was located in these
sources.

## Scoped search outcome

Targeted searches for prime-labelled complete-bipartite equal-product
families, multiplicative hypergraph transversals, and the exact asymptotic
scale did not locate a primary source containing G.1--G.3.  Search absence is
not proof of novelty.  The novelty state remains `priority_uncertain` until a
fresh independent reviewer searches MathSciNet/ZbMATH and reconstructs the
proof without the author package.

## Publication implication

If independently verified and found novel, G.2 is a substantial partial
result: it changes the proved lower-bound scale in the present campaign from
stretched exponential to `N^(1-o(1))` and is robust under arbitrary repair.
It does not resolve either density-one question.  The unresolved 1980 Ruzsa
attribution is the principal priority and positioning risk for a top-tier
submission.
