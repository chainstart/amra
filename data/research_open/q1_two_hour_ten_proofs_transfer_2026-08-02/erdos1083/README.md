# Erdős #1083 ten-proofs transfer lane

Date: 2026-08-02  
Status: **new technical transfer results; Erdős #1083 remains open**

## Outcome

The five requested proof architectures were extracted from the ten-proofs paper,
reasoning walkthroughs, and the local Lean snapshot `94bc0fe`; see
`METHOD_TRANSFER_PLAYBOOK.md`.

The first transfer produced a new exact potential for the signed residuals in the
power-large simultaneous-switch core:

\[
 \delta(q)=\frac12\sum_gq(g)(q(g)-1).
\]

`SIGNED_RESIDUAL_FACTORIAL_ENERGY.md` proves:

- \(\delta(q)\) is a nonnegative integer, vanishes exactly for a mask, and bounds
  the \(\ell^1\) distance to a mask;
- every signed quotient made positive by an \(S\)-term source pays exact negative
  autocorrelation debt \(-2S\delta(q)\);
- every arbitrary \(S\)-term source becomes Fourier-invertible on a sufficiently
  large elementary prime shadow—no finite-tiling or aperiodicity hypothesis is
  needed—and the total signed debt is an exact common-mask reciprocal-frame excess;
- cancellation forces a source difference of multiplicity at least
  \(S/(C+N_-(q))\), hence
  \(\delta(q)\ge\max\{1,\lceil S/\mu(X)\rceil-C\}\);
- the collision identity has an exact stable version when row outputs have small
  factorial defect.

At the frozen endpoint, a minimum-debt signed row forces a difference of \(X\) with
\(t^{13/18+o(1)}\) representations.  Conversely, the previously constructed fully
transverse Euclidean two-row switch has exactly \(\delta=1\), proving that no rowwise
transversality gap exists.  The remaining positive task is genuinely simultaneous:
use the common divisor lattice across \(t^{5/9-o(1)}\) rows to upper-bound the
reciprocal-frame excess, or turn the popular differences into new global distance
labels.

`APERIODIC_SMALL_DIVISOR_NO_GO.md` supplies the complementary adversarial result.
The fixed mask

\[
 1+x+x^3+x^5+x^6
\]

has no root-of-unity zero but has non-torsion unit-circle zeros, and its minimum
Fourier magnitude on \(n\)-th roots is at most \(15\pi/n\), with a
\(30\pi/n^2\) bound on infinitely many denominators.  Thus aperiodicity
guarantees invertibility on every finite cyclic shadow but gives no uniform
conditioning.  This rules out the minimum-singular-value shortcut and explains why
the weighted reciprocal-frame identity must be retained.

The same five-term centre has the explicit signed escape

\[
 (1+x+x^3+x^5+x^6)
 (1-x^5+x^8+x^{10}-x^{13}+x^{18})
 =1+x+x^3+x^9+x^{11}+x^{13}+x^{15}+x^{21}+x^{23}+x^{24},
\]

with quotient augmentation \(2<5\) and factorial debt two.  Hence its bad
conditioning occurs on a centre that genuinely hides signed cancellation, although
only in one row.  It also exhibits exact co-vanishing:
\(|PQ|^2/|P|^2=|Q|^2\le36\) on torsion characters even while
\(\min|P|\to0\), explaining why the full weighted frame remains meaningful.

## Four-gate status

| Gate | Progress in this lane | Still missing |
|---|---|---|
| arbitrary / aperiodic \(X\) | prime-shadow Fourier invertibility for every \(S<p\) mask; explicit aperiodic small-divisor no-go | an upper bound for the full weighted reciprocal-frame excess |
| signed residual | exact integer debt, edit stability, and popular-difference amplifier | simultaneous charging against the common divisor \(B\) |
| common-\(X\) | exact aggregate reciprocal-frame identity and multiplicity invariant \(\mu(\lambda X)=\mu(X)\) | exploit the power-large scalar-copy family, not one row |
| outer stability | exact approximate collision ledger using output factorial defect | derive small algebraic defect from near-extremal Euclidean cells |

## Reproduction

```bash
python3 verify_signed_residual_factorial_energy.py
python3 -m unittest -v test_signed_residual_factorial_energy.py
python3 verify_aperiodic_small_divisor_nogo.py
python3 -m unittest -v test_aperiodic_small_divisor_nogo.py
```

Current result: **12/12 tests pass**.  The verifiers explicitly record
`original_problem_proved: false` and the outer extraction firewall.
See `AUTHOR_FREEZE_2120.md` for quantifier checks, exact factorization, execution
summary, cache cleanup, and frozen hashes.
