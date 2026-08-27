# New-problem portfolio round 2 — 2026-08-25

This is a bounded 180-agent-minute round.  It uses AMRA admission, kill, and
evidence gates.  All solver and enumeration work is launched through
`/home/biostar/work/projects/openmath/bin/openmath-memory-guard`.

The round does not invoke the OpenMath `open-math-research` skill: that skill
requires a minimum eight-hour persistent campaign, while this portfolio is
deliberately capped to protect the user's weekly token and memory budgets.

No finite computation in this package is evidence for a universal theorem
unless an accompanying proof explicitly supplies the missing quantifiers.

## Outcome

- #538 produced a complete scoped theorem for the squarefree rank-two layer:
  admissibility is triangle-freeness and a weighted complete bipartite graph
  is optimal.
- #317 produced a singleton-prime modular obstruction and a complete finite
  certificate for every `5 <= n <= 1,000,000`.  The remaining infinite-tail
  residue statement is explicit and unproved.
- #859 produced exact rational densities through `t=66`; the generic closure
  crossed the frozen two-million-term cap at `t=67` and was stopped.

No exact public problem was closed.  All three admitted targets are frozen
behind theory-level resume gates; #389 remained reserve because its iteration
has no monotone termination measure.
