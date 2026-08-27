# Author audit: M10 prime-gap zero band

Date: 2026-08-27

Classification: **same-model author audit, not independent reconstruction.**

## Dependency check

- The support equivalence `2|N-qp|<=p-k` is already proved in the frozen
  round-3 spectral ledger.
- The only new external theorem is Baker--Harman--Pintz, Theorem 1: a prime
  occurs in `[x-x^(21/40),x]` for all sufficiently large `x`.
- No result about Erdős 451 was searched for or imported.

## Endpoint reconstruction

For `12k<=N<=k^(59/40)/4`, an odd
`t in [4N/(3k),3N/(2k)]` exists because the interval has length at least
two.  With `x=2N/t` and `w=k/t`, direct rational arithmetic gives

```text
4k/3 <= x <= 3k/2,
w/x <= 1/24,
23k/18 <= x-w < x+w <= 25k/16,
w >= (8/3) k^(21/40) > x^(21/40).
```

The BHP prime in `[x-x^(21/40),x]` is therefore strictly inside the
quotient gap.  Strictness is important: a prime at a support endpoint would
not annihilate the local factor.  Here it cannot occur because
`w>x^(21/40)`.

For the width-one reduction the annihilating prime is above `23k/18`, so it
is not the removed prime `p_0=k+1`.  This verifies the only new scope issue
introduced by the dilation.

## Adversarial limits

1. The result is asymptotic because the BHP threshold is not made explicit.
2. The finite script is not evidence for the universal prime theorem.
3. The zero bands are polynomial, whereas the target prefix is
   `exp(O(k/log k))`.
4. The result controls support (hence the full triangular weight) inside the
   band, but supplies no weighted density estimate beyond it.
5. No claim of closure, exponent improvement, novelty, or independent audit
   is permitted.

The theorem is a genuine advance over the previous `|ell|<k` ledger and is
especially useful for the `p_0` dilation, but it does not change the AMRA
phase or promotion decision.
