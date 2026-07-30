# Targeted literature and novelty audit

Audit date: 2026-07-30.

## Search target

The search asked whether the following specific objects were already
standard named results:

1. determinants of coefficient vectors
   \(t+Mt^{-1}\) for multiquadratic Pell-unit words;
2. a support-indexed triangular minor for a polynomial-size unit-word
   family;
3. inverse-symmetrized unit minors used as additive-container
   obstructions in higher-dimensional distinct-distance problems.

Queries combined “multiquadratic units”, “radical basis”, “Pell units”,
“determinant”, “inverse symmetrized”, “multiplicative group”, “S-unit”,
and “distinct distances in \(\mathbb R^3\)”.  The search was deliberately
targeted rather than a claim of exhaustive bibliographic coverage.

## Closest primary sources found

1. J.-H. Evertse, H. P. Schlickewei and W. M. Schmidt,
   [*Linear equations in variables which lie in a multiplicative
   group*](https://annals.math.princeton.edu/2002/155-3/p04),
   Annals of Mathematics 155 (2002), 807--836.

   This gives uniform bounds for nondegenerate solutions of a linear
   equation in a finite-rank multiplicative group.  It is conceptually
   relevant to additive relations among units, but it does not state the
   coefficient-basis determinant identities proved here, nor does its
   abstract provide a basis-normalized container-volume theorem.

2. D. S. Dummit and H. Kisilevsky,
   [*Unit Signatures in Real Biquadratic and Multiquadratic Number
   Fields*](https://arxiv.org/abs/1904.04411).

   This is a direct source for the surrounding arithmetic of units in
   real multiquadratic fields, especially norm-one units and independent
   unit signatures.  Its stated results concern signature rank and
   fundamental-unit structure, not additive ranks of
   \(t+Mt^{-1}\) coefficient vectors.

The targeted search did not locate the exact formulas in
`AFFINE_AND_MULTIQ_UNIT_MINORS.md`.  That negative search result is not
evidence of novelty: the proofs are short triangular/Kronecker
determinant arguments and could occur under different terminology.

## Publication decision

The current package should not be submitted or described as a
stand-alone high-impact result.

- The identities are rigorous and unbounded.
- The support-diversity theorem directly handles polynomial-size
  unit-word sets, proves a support-concentration inverse statement, and
  supplies a useful falsification/design rule.
- The theorem is presently tied to a special multiquadratic coordinate
  model.
- Its determinant is in the radical coefficient basis; a general
  low-doubling container may use a different generator basis.
- The basis-independent part is only the forced progression rank; the
  exponential doubling consequence requires an infinitely proper box.
- No theorem here is yet forced by the inherited Erdős #1083 proof tree,
  and no exponent improves on \(3/5\).

A potentially publishable continuation would need both:

1. a basis-normalized inverse theorem saying that popular hyperbola
   translations force support diversity or an equivalent nonconcentration
   condition in the actual progression coordinates; and
2. explicit exponent bookkeeping showing a strict gain after every
   branch of the three-dimensional distance argument is restored.

Until then, the correct label is **independent structural obstruction and
search-space reduction**, not positive progress on the original
conjecture.
