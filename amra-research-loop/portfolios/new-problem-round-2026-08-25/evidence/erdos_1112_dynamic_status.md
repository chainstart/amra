# Erdős #1112 — dynamic status gate and independent transfer

## Independent scoped transfer

Assume one fixed sequence \(B\) meets \(3A\) for every positive integer
sequence \(A\) whose consecutive gaps are 2 or 3, as in the strong BHJ
counterexample. Let \(k=3m\). For an arbitrary admissible \(A\), with first
term \(a_1\), define

\[
A'=A+(m-1)a_1.
\]

Translation preserves the gaps. Hence \(B\cap3A'\ne\varnothing\). But

\[
3A'=3A+3(m-1)a_1=3A+(k-3)a_1\subseteq kA,
\]

where repeated summands are allowed. Thus the same \(B\) meets \(kA\) for
every admissible \(A\). Taking the BHJ varying-ratio construction against each
proposed constant ratio proves that \(r_{3m}(2,3)\) does not exist.

The quantifiers are sound: \(A'\) may depend on \(A\), while \(B\) remains the
single adversarial sequence fixed before \(A\) is chosen.

## Dynamic exclusion from this discovery round

During the status check, a public repository updated in August 2026 was found:
`https://github.com/beetree/math_erdos_1112`. Its statement file says that a
complete dichotomy is proved in `Erdos1112Proof/Final.lean`, with a paper and a
claimed sorry-free Lean proof of the exact public formulation. This repository
has not been independently built in this round, so no machine-check verdict is
asserted here.

The claim is nevertheless sufficient for AMRA's fail-closed novelty gate:
#1112 is reclassified from fresh discovery to `resolution_audit_only`. The
20-minute reserve is not expanded into a proof campaign. The scoped transfer
above is retained as an independent mathematical check and a future audit
lemma, not advertised as novel.
