# Paper readiness: eight-variable K5-e marked-host theorem

## Candidate paper claim

The intended paper theorem is the complete eight-variable local marked-host
statement frozen in `closure_contract.json`: positivity of `xi_03` on the
distinguished component of the deletion polynomial for `K5-{34,03}`.

This is a standalone local theorem relevant to the uniform-forest negative
correlation program. It is not a proof of OPG-1757 for arbitrary graphs.

## What is currently exact

- the complete five-variable stabilizer-fixed theorem from round six;
- the `b`-Rayleigh boundary reduction and exact chamber ledger;
- 63 of 81 negative-page activity chambers;
- exact Gram, Schur, copositive, and Bernstein certificates for all closed
  chambers, with reconstruction scripts and frozen hashes;
- the PNL fourth-Newton `q`-maximal chart on `q>=1/16`, including the new
  fourth annulus with 19,207,461 strictly positive nonzero controls.

## What still blocks a theorem

The decisive lemma remains conditional. Eighteen negative-page chambers are
not globally closed. In the PNL representative, the new search shows that
the uniform three-box dyadic pattern breaks on `[1/32,1/16]`; a finite list
of repeated annulus certificates is therefore not a closure argument.

The next decisive sublemma should be stated around the `q=0` accumulation
face: after the existing fourth-Newton blow-up, prove nonnegativity on a full
neighborhood of the zero face by an exact factorization, Schur complement,
or a further weighted blow-up whose compact remainders admit finitely many
Bernstein boxes. This must cover the entire `q<1/16` tail at once.

The companion `v`-maximal fourth chart, other transverse maximum directions,
the RLP higher weighted orders, generic contact strata, and the remaining
compact interiors also require finite closure.

## Required audit before submission

After the 18 chambers close, move exactly one phase to `independent_audit`.
An auditor must reconstruct the forest polynomial from the graph, replay the
chamber partition without using author-generated intermediate polynomials,
check union/completeness of all chamber domains, and verify the exact
certificate hashes. Only then can the paper claim the eight-variable local
theorem.

The title and abstract must explicitly say "K5-e marked-host" or equivalent;
they must not say the general uniform-forest conjecture is solved.
