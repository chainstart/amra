# A constant optimization in the van Doorn--Tang lower bound

## Claim

Assume the short-prime-interval input used in van Doorn--Tang: fix
`theta` in `(2/5,3/5)` such that `(k,k+k^theta)` contains
`>>_theta k^theta/log k` primes for all sufficiently large `k`.  The proof of
Theorem 1.1 in arXiv:2606.19863 works, without a new number-theoretic input, for
every fixed

```text
c < min((1-theta)/6, 1/12).
```

In particular, uniformly for the stated theta range one may take `c=1/16`.
Thus the same argument gives

```text
n_k > exp((log k)^2/(16 log log k))
```

for all sufficiently large `k`, improving the displayed `1/20` constant in the
June 2026 preprint.  This is a candidate strengthened corollary of that proof,
not a resolution of Erdős #451.

## Reconstruction

Only Section 6 of the cited proof changes.  Put `L=log k`, `l=log log k`,
assume

```text
k^(2+theta)/2 < n <= exp(c L^2/l),
```

and let `r` be the least positive integer satisfying
`n r! <= k^(r+theta)`.  Exactly as in the paper, with

```text
r0 = ceil(2c L/l),
```

one has `r<=r0`, while the lower endpoint for `n` forces `r>=3`.  For every
fixed `epsilon>0` and all sufficiently large `k`,

```text
r <= (2c+epsilon)L/l.
```

Use the paper's same value

```text
lambda^r = k^(r+1-(1-theta)(2r-1)/(3r-2))/(n r!).
```

The first two bracketed terms in its equation (1) are both

```text
k^((theta-1)/(3r-2)).
```

Since `3r-2 <= (6c+epsilon)L/l`, these are

```text
<= (log k)^(-(1-theta)/(6c+epsilon)) = o(1/log k)
```

whenever `6c<1-theta` (choose epsilon after fixing `c,theta`).

The paper bounds the third bracketed term by `k^(-1/(6r))`.  The refined
asymptotic bound on `r` gives

```text
k^(-1/(6r)) <= (log k)^(-1/(12c+epsilon)) = o(1/log k)
```

when `12c<1`.

Finally, the paper's estimate for the additive term `r lambda` is unchanged.
Its exponent is maximized at `r=3`, where it equals

```text
(9-2theta)/21 < theta
```

because `theta>2/5>9/23`.  Hence `r lambda=o(k^theta/log k)` independently of
`c`.  The small, medium, and medium-large ranges in Sections 2, 3, and 5 are
also unchanged.  Substitution in equation (1) therefore yields
`K=o(k^theta/log k)` throughout the enlarged large-`n` range.

For `c=1/16` the three relevant uniform rational margins are

```text
(1-3/5)-6/16 = 1/40,
1-12/16       = 1/4,
2/5-(9-2(2/5))/21 = 1/105.
```

They are replayed exactly by `work/verify_constant_optimization.py`.

## Evidence and limits

- Primary source: W. van Doorn and Q. Tang, *Consecutive integers free of
  certain prime factors*, arXiv:2606.19863v1 (18 June 2026).
- The reconstruction reuses their Theorem 4.1, Konyagin's theorem, and the
  Baker--Harman--Pintz short-prime-interval input.  It does not independently
  reprove those external theorems.
- A web novelty search on 26 August 2026 found the `1/20` preprint but no public
  `1/16`, `1/15`, or `19/240` refinement.  Priority therefore remains
  uncertain until the authors or another number theorist check the argument.
- The exact rational script is an algebra audit, not an independent natural
  proof reconstruction.
