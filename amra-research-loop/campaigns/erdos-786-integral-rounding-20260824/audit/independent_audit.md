# Independent audit: IR.1 moving thin-tail obstruction

## Verdict

IR.1 passes independent reconstruction, statement matching, and dependency
checking. The proper promotion is `standalone_decisive_lemma` only. It does
not prove `tau(H_N)=o(N)`, finite or infinite density one, or the original
distinct-Finset Erdős 786 statement.

## Blind protocol

The reconstruction was written before reading the author proof or verifier.
The frozen artifact is `audit/blind_reconstruction.md`, SHA-256
`899a3bd6c01d85e178e696b5f343b49d1a6157c77622bf875ee48f81e9a0f097`.
Unblinding found the same sparse path construction and an equivalent padding
argument.

## IR.1 quantifiers and construction

Put `theta_K=min(eta_K,1)` and `s=ceil(4/theta_K)`. From
`K eta_K -> infinity` one gets `K theta_K -> infinity` and
`s/K <= 4/(K theta_K)+1/K -> 0`. Thus the support is allowed to move with
`K`, but remains `o(K)`; there is no hidden fixed-eta assumption.

Label the `2s` edges of `P_(2s+1)` by distinct odd primes and let `q_v` be
the product of incident edge primes. The shores have sizes `s+1` and `s`,
and their `q_v` products agree because each edge prime occurs once on each
shore. Repeated Bertrand bounds the last chosen prime by `2^O(s)`; path
degree at most two therefore gives `max log_2 q_v=O(s)=o(K)`. This sparse
path is crucial: no unjustified `s log s=o(K)` estimate is used.

With `c_v=ceil(log_2 q_v)` and `e_v^(0)=K-c_v`, every initial padded value
lies in `(N/2,N]`. If `L,R` have sizes `s+1,s`, respectively, then

```
Delta = sum_L e_v^(0) - sum_R e_v^(0)
K-(s+1) < Delta < K+s.
```

For all large `K`, `Delta>0`. Distribute exactly `Delta` decrements over
the larger shore, with every decrement at most `K/(s+1)+2`. Since
`max c_v=o(K)`, all final exponents are nonnegative. The total 2-adic
exponents now agree across the shores, so the padded products agree exactly.

Every final integer is at most `N` and is strictly greater than
`N^(1-1/(s+1)-3/K)`. Here `1/(s+1)<=theta_K/4<=eta_K/4`, while
`3/K<eta_K/2` eventually. Hence the exponent loss is strictly less than
`eta_K`, proving membership in the open tail `(N^(1-eta_K),N]`.

Distinct odd parts give distinct padded integers. For support minimality,
after cancelling overlap a subrelation has coefficients in `{-1,0,1}`.
The valuation at the private prime on an edge `uv` gives
`epsilon_u+epsilon_v=0`. Connectivity of the path forces either the zero
coefficient vector or the full alternating bipartition vector. Thus there is
no proper equal-product subrelation, and the distinct-Finset variant lock is
respected.

## M01--M03

- M786I-01 passes at its full stated scope. Along `N=2^K`, an `o(N)` lower
  threshold has `2^(-K delta_(2^K))->0`, equivalently
  `K delta_(2^K)->infinity`. IR.1 puts a whole bad support in the retained
  strict tail for every sufficiently large power of two.
- M786I-02 passes at the nested-threshold scope. A finite union of nested
  lower thresholds is a single largest threshold, hence reduces exactly to
  M01. Non-nested arithmetic coarea is not killed.
- M786I-03 passes only for unaltered probability-one independent rounding.
  If `q_N(n)<=g_N w_N(n)` and `g_N=o(log N)`, take
  `eta_K=1/(2 max(1,g_(2^K)))`. Then `K eta_K->infinity`, and IR.1 supplies
  an edge on which every `q_N(n)<1/2`. Its independent miss probability
  `prod_(n in E)(1-q_N(n))` is positive. This does not refute alteration,
  resampling, or subsequent repair.

These are all-parameter route kills. They do not lower-bound the full
transversal number because one deletion hits each displayed circuit.

## Dependencies, verification, and scope

IR.1 uses unique factorization and Bertrand's postulate with their ordinary
quantifiers. The predecessor fractional-cover theorem is not used to build
the circuit; it only identifies `g_N=o(log N)` as an affordable proportional
rounding scale. The open survivors M786I-05, M786I-06, and M786I-12 are not
imported as premises.

`python3 evidence/verify_integral_rounding_kills.py` returned `PASS`; its
SHA-256 is
`4eddf2345972162e722ad95f2bcde01982f2fc109bb679d835315faa48e0b0ad`.
The finite checks corroborate exact identities and examples; the universal
quantifiers are justified by the symbolic proof above.

No public search for an exact solution was performed. Priority is therefore
`priority_uncertain` and the result remains a private campaign note.

Recommendation: promote IR.1 under `standalone_decisive_lemma` only. Do not
claim `global_interface_closed`, `main_term_improved`, or
`original_problem_closed`; the three surviving research routes may continue
separately.
