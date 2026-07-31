# Erdős #1083 two-hour breakthrough attack

Date: 2026-07-31

This round deliberately avoided another small exponent optimization.
It stress-tested the synchronized nonaligned-row endpoint and found
the exact block-diagonal equality model hidden by its moment bounds.

The main note proves the parabolic lift, classifies the exact abstract
block equality case, identifies two sharp (1/18)-scale information
thresholds, and gives a genuine three-row Euclidean counterexample to
automatic spectral separation.  A base-three hypercube construction
extends that counterexample to arbitrarily many nonaligned rows while
recording its exact tangent-universe cost.  The main positive result is
a torsion-free group-ring theorem: an exact identical-spectrum block
at the endpoint can contain at most two pairwise transverse rational
dilation spaces.  This converts the block branch into a stability and
commensurability problem.  A further parabolic-resolution theorem
compresses all cross-row block collisions to one fixed tangent
difference carrying exponent \(19/18\) worth of exact quadratic
relations.

Files:

- `BREAKTHROUGH_ATTACK.md` — proofs, counterexample, and new
  block-vs-diffuse target;
- `INDEPENDENT_AUDIT.md` — reconstruction of every exact theorem and
  the stability boundary;
- `GEOMETRIC_INTERFACE_RED_TEAM.md` — full positivity, distinctness,
  nonalignment, target-plane, label, and endpoint-interface audit;
- `CLAIM_LEDGER.md` — strict proved/open/refuted boundary;
- `verify_spectral_block_breakthrough.py` — exact certificates;
- `test_verify_spectral_block_breakthrough.py` — nine regression tests.

Reproduce with:

```bash
python3 verify_spectral_block_breakthrough.py
pytest -q
```
