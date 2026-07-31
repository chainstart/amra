# Independent audit of the OPG-1757 four-problem-campaign results

Date: 2026-07-30

## Verdict

\[
\boxed{\text{PASS}}
\]

## Kernel-window theorem

The primary verifier performs 746 exact primitive-transfer evaluations:

| new rank | raw degree | proved \((\deg_k,\deg_s)\) bound | grid size |
|---:|---:|---:|---:|
| 5 | 9 | \((12,9)\) | 130 |
| 6 | 10 | \((14,10)\) | 165 |
| 7 | 11 | \((16,11)\) | 204 |
| 8 | 12 | \((18,12)\) | 247 |

Every reconstructed identity agrees at two points outside its
interpolation rectangle.  After the full-domain shift
\((m,v)=(k-4,s-4)\), the four positive polynomials contain respectively
21, 32, 40 and 55 nonzero monomials, all strictly positive.

The independent verifier replaces the page-state transfer by a
connected-component recurrence using the weighted bipartite Cayley
formula.  It obtains the same ranks at
\[
(k,s)=(4,4),(4,7),(5,5),(5,7),(6,8).
\]
The pair \((4,7)\) checks a genuinely off-diagonal parameter, and the
two implementations share neither state space nor recurrence.

## Dominant-zero theorem

Exact fractions verify the alternating lower and upper bounds at
\(1961/1000\) and \(1962/1000\).  The relative rate satisfies
\[
\frac{1962/1000}{21/10}=\frac{327}{350},
\]
and direct rational exponentiation gives the four printed error
thresholds \(61,72,95,129\).  The only analytic inputs reused from the
earlier independently audited theorem are the Rouché uniqueness,
genus-zero factorization and Jensen annulus bound.

## Claim boundary

The audit certifies:

- a general \(\beta^0,\ldots,\beta^8\) positive window for \(K_k\);
- exact all-parameter identities at the four new ranks;
- a dominant-zero asymptotic for the leading long-band coefficients.

It does not certify:

- positivity of every coefficient of \(K_k\);
- positivity of every pooled \(F_k\) or \(B_k\);
- full-domain positivity of every \(\gamma_{d,q}\);
- real-rootedness of all ordinary symbols;
- the complete-split Rayleigh theorem or OPG-1757.

The local literature boundary is unchanged: Liu--Chow/Myrvold supply
the forest-counting input; Tang--Zhang treat fixed-component complete
graphs asymptotically; Fang--Ma do not cover general complete-split
graphic matroids.  A systematic external priority audit is still
required before publication.
