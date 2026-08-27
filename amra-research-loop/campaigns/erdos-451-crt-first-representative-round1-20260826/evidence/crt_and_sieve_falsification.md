# CRT and sieve admission evidence

The guarded exact scan and its separate predicate replay are stored in
`crt_admission_scan.json` and `../audit/crt_admission_replay.json`.

## What the computation establishes

- For each scanned `k`, the allowed residues modulo `p in (k,2k)` are exactly
  `{0,k+1,...,p-1}` and the full-period density is exactly
  `D_k=product(1-k/p)`.
- Exact first representatives were recovered through `k=50`; for `k=55,...,75`
  the interval through 50,000,000 was certified empty.  These are finite
  predicate checks, not new asymptotics.
- For most nonzero `h<=4k`, the exact joint density `J_k(h)` is zero.  Two
  survivors separated by `h` require, for every `p`, that the circular distance
  of `h` modulo `p` be at most `p-k-1`.  The survivors therefore have strong
  arithmetic repulsion and are not a Poisson process at short distances.
- At `H=exp((log 4)k/log k)`, any squarefree product of primes in `(k,2k)` that
  remains at most `H` contains only `floor(log H/log k)` primes.  The measured
  fraction falls from `0.286` at `k=100` to `0.139` at `k=30000`, consistent
  with the rigorous asymptotic ratio `O(1/log k)`.

## Mechanisms killed

The density alone does not locate the first representative (M451-01).
Translation-averaged first and second moments do not imply a statement about
the fixed initial translate (M451-02, M451-03).  Ordinary uncompressed
inclusion-exclusion below level `H` sees a vanishing fraction of the dense
constraints (M451-04).  Subset products of interval primes cannot simultaneously
provide `Theta(k/log k)` effective decision bits and magnitude
`exp(O(k/log k))` (M451-05).  A fractional cover or large-sieve inequality that
forgets the fixed prefix has the same quantifier loss (M451-06, M451-11).
The one-variable local-lemma dependency graph is complete (M451-10), and finite
agreement has no all-`k` reduction (M451-12).

These conclusions rule out the stated mechanisms only.  In particular, the
support ledger does not rule out a compressed high-order sieve identity, and
the correlation calculation does not rule out a pointwise Fourier theorem.
