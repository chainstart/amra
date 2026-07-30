# Erdős #1083 algebraic line

## Outcome

This directory contains a proved algebraic boundary, not an improvement
of the three-dimensional distinct-distance exponent.

The main theorem generalizes the consecutive-unit determinant to arbitrary
distinct integral affine shifts:

\[
|\Delta|=
4|M|^{d-2}|a_2-a_1|
|\operatorname{Vandermonde}(a_1,\ldots,a_{d-2})|.
\]

Consequently, irregular integral nodes cannot beat the consecutive-node
coefficient-volume obstruction.  A counterexample in the proof note also
shows why an ambient determinant cannot be promoted to a lower bound for
every generalized arithmetic progression: one may take the shift vectors
themselves as box generators.

The counterexample-first audit also gives a sharp contrast inside
multiquadratic fields:

- a union of \(r\) independent Pell-unit power axes can contain \(rL\)
  parameters while all inverse-symmetrized images have additive rank only
  \(r+1\);
- those shifts admit an elementary coefficient box with overlap density
  \(>1/4\), but the parameter count is still only logarithmic in the box
  size;
- every unit-word family with pairwise distinct coordinate supports,
  even with arbitrary positive powers and only polynomially many words,
  has an explicit nonzero full row-rank minor; every Boolean subfamily is
  a special case.
- consequently, low additive rank of \(t+Mt^{-1}\) forces the words to
  concentrate on few coordinate supports, a precise model-specific
  inverse theorem.

For an infinitely proper box, this also gives the quantitative tradeoff
\[
|P+P|/|P|\ge(3/2)^{\text{number of represented supports}}.
\]
Hence polynomially many distinct supports are incompatible with
subpolynomial doubling in this model.

See [AFFINE_AND_MULTIQ_UNIT_MINORS.md](AFFINE_AND_MULTIQ_UNIT_MINORS.md)
for the human proofs, scope restrictions, and claim ledger.

## Files

- `AFFINE_AND_MULTIQ_UNIT_MINORS.md`: theorem statements, proofs, and
  interpretation;
- `LITERATURE_SCOPE_AUDIT.md`: targeted primary-source comparison and
  publication boundary;
- `verify_affine_minor_and_torus_axes.py`: exact symbolic certificate;
- `test_verify_affine_minor_and_torus_axes.py`: regression test.

## Verification

```bash
python3 verify_affine_minor_and_torus_axes.py
python3 -m unittest -v test_verify_affine_minor_and_torus_axes.py
```

Expected certificate SHA-256:

```text
fc40bc9d2097d3b76d45aea54b60f37fb2b0b04965e8913975d5f7a608e9d4a1
```

## Publication status

The exact identities may be useful components of a future inverse theorem,
but no novelty search has yet established them as independently
publishable.  More importantly, they do not improve the \(3/5\) exponent.
The viable next question is whether the inherited proof tree forces enough
support nonconcentration for a basis-normalized minor theorem; unit rank by
itself provably does not.
