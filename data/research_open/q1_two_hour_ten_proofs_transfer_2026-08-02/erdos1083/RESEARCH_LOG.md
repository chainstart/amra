# Research log

Date: 2026-08-02

## 20:09--20:30: source extraction

- Read the non-sofic, Connes rigidity, permanent circuit/formula, quantum parallel
  repetition, and GapCVP walkthroughs.
- Located the corresponding Lean mechanisms at snapshot `94bc0fe`.
- Wrote `METHOD_TRANSFER_PLAYBOOK.md`, mapping explicit objects, bounded
  local-to-global potentials, mass-preserving repetition, cancellation-stable
  complexity, and counterexample-first testing to the four #1083 gates.

## 20:30--20:45: signed energy and reciprocal frame

- Replaced coefficientwise quotient positivity by the integer potential
  \(\delta(q)=\frac12\sum q(q-1)\).
- Proved exact autocorrelation debt, edit stability, and the elementary-prime
  Fourier nonvanishing lemma.
- Derived the rowwise and aggregate common-mask reciprocal-frame identities.
- Found and verified a tiny equality case; then pinned it below the stronger
  previously admitted full-transverse Euclidean no-go.

## 20:45 onward: transversality and stability red team

- Computed that the full-transverse quotient
  \(Q_S=x+y-xy+xy^S+x^Sy\) has the minimum possible debt \(\delta=1\).
  This kills any rowwise positive-gap route, even with Euclidean realization.
- Expanded positive-versus-negative convolution overlap to prove the
  popular-difference theorem.  The minimum-debt endpoint forces
  \(t^{13/18+o(1)}\) representations of one nonzero difference of \(X\).
- Removed exactness from the norm calculation and obtained the stable collision
  ledger.  This identifies factorial output defect as the exact quantity an outer
  cleaning argument must control.
- Found the five-term reciprocal mask \(1+x+x^3+x^5+x^6\).  A Rabin test modulo
  three proves irreducibility; the substitution \(y=x+x^{-1}\) proves both
  non-torsion unit-circle zeros and off-circle roots.  Nearest roots of unity give
  \(0<\sigma_n\le15\pi/n\), closing the proposed minimum-singular-value shortcut.
- A bounded SAT search then found an exact signed quotient of augmentation two for
  that same centre.  Exact expansion gives a ten-term mask and \(\delta=2\), so the
  spectral no-go is attached to a genuine signed escape rather than an irrelevant
  polynomial.
- Kept the public theorem and the outer extraction explicitly open.
