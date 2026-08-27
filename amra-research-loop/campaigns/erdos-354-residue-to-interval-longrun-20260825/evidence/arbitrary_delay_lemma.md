# Arbitrarily delayed unit relations for Erdős #354

For every integer N ≥ 1, there are positive α, β with α/β irrational such
that the subset sums of

    {⌊2^s α⌋, ⌊2^s β⌋ : 0 ≤ s ≤ N}

contain no two consecutive integers.

Take α = 20. Choose an irrational β whose binary floor-carry recurrence begins

    b₀ = 7,  b₁ = 15,  b_(s+1) = 2 b_s  for 1 ≤ s < N.

Equivalently, β may be chosen in the nonempty binary cylinder beginning with
`7.100…0`, with the first N carries prescribed as above and an aperiodic tail
placed later. Such a β is irrational, hence α/β is irrational.

Every ⌊2^s α⌋ is divisible by 5. Among the displayed β-terms, b₀ = 7 ≡ 2
(mod 5), while b_s = 15·2^(s−1) is divisible by 5 for 1 ≤ s ≤ N. A finite
subset may use b₀ at most once, so every displayed subset sum is congruent to
either 0 or 2 modulo 5. No two such residues differ by 1 modulo 5. Therefore
no two subset sums are consecutive.

This is a no-go result for any parameter-independent finite-prefix bound, any
bounded-gap supply of signed unit relations, and any argument claiming that
one short interval must appear after a universal number of binary scales. It
does **not** refute completeness: the delayed aperiodic tail eventually breaks
the mod-5 obstruction, and the proof gives no control after that break.

The guarded exact checkpoint `interval_delay_search.json` independently found
the depth-22 instance with x₀ = 20, y₀ = 7, all tested x-carries zero, and the
tested y-carries equal to 1, 0, …, 0.
