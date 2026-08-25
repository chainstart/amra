# Erdős #859: exact-density route audit

## Exact finite reduction

For fixed \(t\), let

\[
 \mathcal W_t=\{\operatorname{lcm}(S):S\subseteq\{1,\ldots,t\},
 \text{ the elements of }S\text{ are distinct, and }\sum_{s\in S}s=t\}.
\]

Then \(t\) is a sum of distinct divisors of \(n\) if and only if at least one
member of \(\mathcal W_t\) divides \(n\).  Removing every member divisible by
another leaves a minimal divisibility antichain that generates the same union
of multiples.  Collapsed inclusion-exclusion over the lcm closure of this
antichain gives \(d_t\) as an exact rational number.

`work/compute_859_density.py` implements this reduction with integer lcms and
`Fraction` arithmetic.  For \(t\le12\), a second method enumerates the complete
period \(\operatorname{lcm}(1,\ldots,t)\) and agrees exactly.

## Result and kill gate

The guarded run computes every \(d_t\) exactly for \(1\le t\le66\).  Selected
values are

| \(t\) | exact/decimal density | minimal generators | collapsed terms |
|---:|---:|---:|---:|
| 22 | 0.3237895231703281 | 17 | 504 |
| 24 | 0.3726957567043716 | 22 | 1,117 |
| 45 | 0.2785444445804724 | 77 | 59,859 |
| 55 | 0.2934991714222489 | 108 | 249,881 |
| 61 | 0.29748497947023395 | 147 | 1,296,279 |
| 66 | 0.2754410345095004 | 167 | 1,265,325 |

The numerator and denominator of every value are retained in the JSON; the
decimals above are only readable summaries.  At \(t=67\), collapsed
inclusion-exclusion crossed the frozen cap of 2,000,000 live terms, so the run
stopped as planned.  Peak complexity, rather than memory failure, is the
recorded boundary.

The finite values fluctuate, but they supply neither two infinite separated
subsequences nor a uniform estimate.  In particular, the diagnostic quantity
\(-\log d_t/\log\log t\) is not treated as a fitted exponent.

## Decision

Freeze the generic lcm-closure enumeration route.  Resume only if there is a
symbolic description of the minimal generators for a genuine infinite
subsequence (prime, prime-power, or smooth \(t\)), or a Möbius/automaton
compression whose state count is proved subexponential.  Merely raising the
2,000,000-term cap is not a resume event.
