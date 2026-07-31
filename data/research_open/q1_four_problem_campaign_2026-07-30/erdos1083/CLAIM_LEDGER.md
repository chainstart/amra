# Erdős #1083 four-problem campaign: claim ledger

Date: 2026-07-30

## 1. Main problem

| Claim | Status | Evidence boundary |
|---|---|---|
| \(f_3(N)\gg N^{3/5+\delta}\) for some fixed \(\delta>0\) | **OPEN** | No upper bound excludes the synchronized nonaligned pair. |
| Erdős #1083 is solved | **FALSE AS A DESCRIPTION OF THIS WORK** | The desired \(N^{2/3-o(1)}\) bound is not proved. |
| The critical \(2/9\) hub is excluded | **NOT PROVED** | It is converted to an explicit synchronized-chart alternative. |

## 2. New all-parameter statements

| Claim | Status | Evidence |
|---|---|---|
| \(\sum_\lambda E^+(T_\lambda,\lambda X)\le S\sum_\lambda|T_\lambda|+R(R-1)S(S-1)\) for distinct nonzero \(\lambda\) and \(T_\lambda\subseteq T_\ast\) | **PROVED** | `MULTIDILATE_ENERGY_AND_NONALIGNED_SYNCHRONIZATION_THEOREM.md`, Theorem 1 |
| Aggregate spectra obey \(\sum_\lambda|\mathcal V_\lambda|\ge\mathcal N^2/(\mathcal N+\mathcal B)\) | **PROVED** | Theorem 2, two Cauchy--Schwarz applications |
| Under \(HU\ge R^2S\), \(HSU\ge4D\), two spectra share at least \(S^2U^2/(8D)\) labels | **PROVED** | Theorem 3 |
| The energy theorem has been certified as globally novel in the literature | **NOT AUDITED** | It is elementary and new to this repository; no priority claim is made. |

## 3. Euclidean and endpoint statements

| Claim | Status | Evidence |
|---|---|---|
| A fixed-\((A,\rho)\) bundle consists of pairwise nonaligned congruent circles when centre heights differ | **PROVED** | Their perpendicular axes are parallel and distinct. |
| The exact row spectrum is \(\rho^2+z^2+T_z+2\rho zX\) | **PROVED / exact verifier PASS** | Direct three-dimensional expansion |
| A surviving \(\kappa=2/9\) endpoint hub forces \(S\ge t^{7/9-o(1)},U\ge t^{5/6-o(1)},H\ge t^{19/9-o(1)}\) in one bundle | **PROVED CONDITIONALLY** | Uses the audited critical hub scalar inequalities |
| The bundle satisfies \(HU\ge t^{1/6-o(1)}R^2S\) | **PROVED CONDITIONALLY** | Exact exponent elimination |
| Two nonaligned rows share \(t^{2/9-o(1)}\) distinct anchor-to-axis distance labels | **PROVED CONDITIONALLY** | Theorem 3 plus the endpoint exponents |
| At least \(t^{35/18-o(1)}\) labels each occur in \(t^{13/18-o(1)}\) nonaligned row spectra | **PROVED CONDITIONALLY** | Quadratic height-fibre cap \(q_d\le2SR\) plus aggregate support |
| For every fixed \(\varepsilon>0\), \(t^{17/6-o(1)}\) nonaligned row pairs each share \(t^{2/9-\varepsilon-o(1)}\) labels | **PROVED CONDITIONALLY** | Total intersection mass, row-spectrum cap, and exact endpoint exponents |
| Matching \(t^{2/9-o(1)}\) or synchronized nonaligned bundle dichotomy | **PROVED CONDITIONALLY** | Exact \(\kappa=2/9\) matching-or-hub theorem plus the new bundle theorem |
| The shared spectrum already gives more than \(t^{3+o(1)}\) total distances | **NOT PROVED** | A cross-row overlap upper bound or exceptional-family classification is missing. |
| Mathialagan--Sheffer's nonaligned-circle theorem closes the synchronized network | **NO** | It gives \(t^{28/27-o(1)}\) per source-circle pair and no aggregate reuse bound for axis spectra. |
| A bundle de-reuse lemma alone would solve all of #1083 | **NO** | It would discharge the hub; the rich-matching branch still needs a Euclidean expansion theorem. |

“Conditionally” refers to the explicit critical pair-codegree and
cell-cap setup.  The finite-real Theorems 1--3 do not depend on that
setup.

## 4. Verification

New package:

```text
python3 verify_multidilate_nonaligned_bundle.py
status: PASS
56 finite rational systems audited
6 pytest tests passed
```

Focused dependency suite:

```text
24 passed
```

Finite tests are falsification and exact arithmetic certificates.
The all-parameter results rest on the written proofs.

## 5. Publication boundary

The result is stronger than the earlier “one repeated circle” or
“many concentric circles” alternatives: it forces a polynomial bundle
of pairwise nonaligned rich circles and a quantified two-row spectral
synchronization.

It is a credible new section and endpoint milestone for a larger
inverse-structure paper.  It is not by itself certified as a Chinese
Academy Q1 paper because:

1. the global distinct-distance exponent is unchanged;
2. the endpoint dichotomy retains a live exceptional alternative;
3. priority for the elementary multidilate inequality has not been
   exhaustively audited; and
4. the critical pair-codegree reduction remains an explicit upstream
   hypothesis in the self-contained conditional formulation.
