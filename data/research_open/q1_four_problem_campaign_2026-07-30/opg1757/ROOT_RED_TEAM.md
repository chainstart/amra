# OPG-1757 root red-team audit

Date: 2026-07-30

## 0. Verdict

| Item | Verdict | Qualification |
|---|---|---|
| \([\beta^r]K_k(s,\beta)>0\) for \(r=5,6,7,8\) and all \(k,s\ge4\) | **PASS** | The unbounded parameter statement is forced by proved bidegree bounds and complete exact interpolation rectangles. It is not inferred from holdouts. |
| Positivity of the shifted \(Q_r(k-4,s-4)\) | **PASS** | All 148 displayed certificate coefficients are strictly positive; the boundary \(k=s=4\) is included. |
| Connected-component/Cayley implementation | **PASS AS AN INDEPENDENT SAMPLE AUDIT** | It is a genuinely different recurrence, but five saved points (plus four extra red-team points) do not constitute a second all-parameter proof. |
| Dominant-zero localization and spectral error estimate | **PASS, CONDITIONAL ON THE INHERITED ANALYTIC THEOREM** | The new rational bracket and error conversion are correct. Rouché uniqueness, the modulus gap, genus-zero factorization and the Jensen constant are inherited, not reproved by the new verifier. |
| OPG-1757 / the complete \(\alpha^2\) layer | **FAIL / OPEN** | Neither follows from a finite kernel window or from the leading long-band asymptotic. |
| Standalone Q1-level main theorem | **FAIL** | The results are rigorous and useful manuscript components, but do not yet supply the infinite-rank or full-Rayleigh closure needed for a secure Q1 main theorem. |

The mathematical claims actually made in the two theorem notes pass this
audit. The publication-grade claim must remain narrower: this round produced
two valid unbounded auxiliary theorems, not a solution of OPG-1757.

## 1. Why the finite grid really proves the four identities

Let \(d=r+4\), and let \(d_d(k,s)\) be the coefficient of \(\beta^d\)
in the raw determinant. A pair of forests with \(d\) total edges uses at
most \(d\) page labels and at most \(d\) core labels. Sorting by the used
label sets therefore makes \(d_d\) a polynomial of degree at most \(d\)
in each population variable (equivalently, it has binomial-basis degree
at most \(d\)).

The exact deconvolution is
\[
n_d=d_d-\sum_{p=1}^{d-4}
\binom{2s-2k-2}{p}k^p n_{d-p}.
\]
The multiplier in the \(p\)-th summand has \(k\)-degree at most \(2p\)
and \(s\)-degree at most \(p\). Combining this with the already proved
degree bounds for \(n_4,\ldots,n_8\), and then inducting for
\(d=9,\ldots,12\), gives
\[
\deg_k n_d\le 2d-6,\qquad \deg_s n_d\le d.
\]
This is the essential proof obligation. It is not supplied by a numerical
scan.

The resulting interpolation dimensions are exactly:

| \(r\) | \(d\) | Degree bounds \((\deg_k,\deg_s)\) | Nodes | Exact grid size |
|---:|---:|---:|---:|---:|
| 5 | 9 | \((12,9)\) | \(13\times10\) | 130 |
| 6 | 10 | \((14,10)\) | \(15\times11\) | 165 |
| 7 | 11 | \((16,11)\) | \(17\times12\) | 204 |
| 8 | 12 | \((18,12)\) | \(19\times13\) | 247 |

Thus the 746 values are not “746 pieces of evidence”: for polynomials
within the proved bidegree spaces, the four rectangles uniquely determine
the four identities. The eight off-grid evaluations are logically
redundant bug checks. They cannot repair a missing degree proof, but no such
gap was found here.

The interpolation is performed on the reduced numerator \(n_d\), before
division by \(2k(k-1)\). Hence the nodes \(k=0,1\) do not introduce a
division-by-zero issue. The primitive forest transfer remains exact at
those polynomial-extension nodes.

## 2. Full-domain shifted positivity

After
\[
m=k-4,\qquad v=s-4,
\]
the certificate has the form
\[
[\beta^r]K_k(s,\beta)
=\frac{(m+1)(m+2)}{c_r}Q_r(m,v).
\]
The red-team coefficient audit gave:

| \(r\) | \(c_r\) | Nonzero terms of \(Q_r\) | Smallest coefficient | Largest coefficient |
|---:|---:|---:|---:|---:|
| 5 | 15 | 21 | 4 | 675904 |
| 6 | 90 | 32 | 8 | 17830144 |
| 7 | 315 | 40 | 8 | 206024448 |
| 8 | 2520 | 55 | 16 | 4042908672 |

Every coefficient is strictly positive. Since \(m,v\ge0\) on the claimed
domain and \((m+1)(m+2)>0\), strict positivity follows even at the corner
\((k,s)=(4,4)\). This also validates the nontrivial region \(s<k\);
positivity is in \((k-4,s-4)\), not in the earlier auxiliary coordinate
\((k-4,s-k)\).

## 3. Independence of the Cayley recurrence

The second implementation decomposes a weighted bipartite forest by the
component containing the least unused core vertex. For a component on core
set \(I\) and page set \(J\), its factor
\[
|J|^{|I|-1}
\left(\sum_{i\in I}w_i\right)^{|J|-1}
\prod_{i\in I}w_i
\]
is the correct weighted bipartite Cayley formula. The recursion chooses
the labelled page subset, recursively assigns the unused pages, and leaves
unselected pages isolated; no missing isolated-page factor was found.

It shares neither the page-partition state space nor its recurrence with
the primary verifier. It therefore is a useful independent implementation
audit. Its logical scope must nevertheless be stated accurately:

- the saved program checks five parameter pairs;
- the red team additionally checked
  \((k,s)=(7,4),(8,4),(7,6),(8,5)\);
- all four new ranks agreed exactly at all nine pairs;
- this remains a pointwise audit, not an independent interpolation proof.

The all-parameter theorem stands on the primary degree-plus-interpolation
argument. The Cayley calculation makes implementation error much less
likely but is not needed to establish uniqueness.

## 4. Dominant zero and spectral asymptotics

Write
\[
H(z)=\sum_{j\ge0}(-1)^j\lambda_jz^j,\qquad \lambda_j>0.
\]
The inherited recurrence gives the decreasing-tail estimate required for
the alternating bounds. Exact arithmetic verifies
\[
\sum_{j=0}^{5}L_j(1961/1000)^j>0,\qquad
\sum_{j=0}^{4}L_j(1962/1000)^j<0.
\]
The parities are correct: the degree-five sum is a lower bound and the
degree-four sum is an upper bound. Together with inherited uniqueness of
the zero in \(|z|<21/10\), this proves
\[
\frac{1961}{1000}<\rho<\frac{1962}{1000}.
\]

The inherited analytic chain was rerun and passes:

1. strict Rouché margin
   \(868586809/54058752000>0\), so exactly one zero lies in the disk and
   there is no boundary zero;
2. \(H(2)<0\) and \(H(0)=1\), locating that zero on the positive real
   axis;
3. every other zero therefore has modulus strictly greater than \(21/10\);
4. the order-\(\le1/2\) bound gives the genus-zero product;
5. Jensen annuli give
   \[
   \sum_{\rho_\nu\ne\rho}|\rho_\nu|^{-n}
   <63(21/10)^{-n}\qquad(n\ge2).
   \]

Since
\[
G_{n-1}=3\sum_\nu\rho_\nu^{-n},
\]
division by \(3\rho^{-n}\) gives, without a missing factor of three,
\[
\left|\frac{G_{n-1}}{3\rho^{-n}}-1\right|
<63\left(\frac{\rho}{21/10}\right)^n
<63\left(\frac{327}{350}\right)^n.
\]
The thresholds \(61,72,95,129\) for relative errors
\(1,1/2,1/10,1/100\) were recomputed exactly and are correct.

The qualification is provenance, not a mathematical failure:
`verify_dominant_zero_spectral_asymptotic.py` itself checks the new
rational bracket and constants, but imports the coefficient sequence and
assumes the earlier Rouché/Jensen theorem. A paper must include or cite
that complete analytic proof; the new script alone is not a standalone
proof of zero uniqueness.

## 5. Increment over Tang--Zhang and Fang--Ma

Tang--Zhang, arXiv:2603.10738, prove pairwise negative correlation for
fixed-component forests (and related spanning-subgraph families) on
complete graphs when the order is sufficiently large. The present kernel
window is different: it concerns a two-orbit complete-split reduction,
is uniform in both \(k\) and \(s\), and gives exact low-\(\beta\) layers.
No direct overlap with their stated theorem was found. Equally important,
the current result is not stronger than Tang--Zhang in their setting and
does not extend their full negative-correlation conclusion to
complete-split graphs.

Fang--Ma, arXiv:2604.27755, introduce the Gårding framework and derive
Rayleigh/negative-dependence consequences for several matroid classes.
The prior local audit reports that their proved closure classes do not
cover general complete-split graphic matroids. The new eight-layer
univariate certificate is therefore not subsumed by the presently
identified Fang--Ma cases. Conversely, positivity of eight specialized
coefficients does not prove that the complete-split forest polynomial is
C-Gårding or I-Rayleigh.

Accordingly, the defensible novelty statement is:

> an exact, all-\((k,s)\), eight-layer positive kernel window and an
> explicit dominant-zero law for an auxiliary all-rank leading sequence.

It is not defensible to claim a Fang--Ma-type structural closure, a
Tang--Zhang extension of pairwise negative correlation, the complete
\(\alpha^2\) layer, or OPG-1757. A MathSciNet/zbMATH/Scopus-level priority
search remains necessary before submission.

## 6. Publication assessment

The four kernel identities are real unbounded theorems because the
parameters \(k,s\) are unrestricted; “finite rank” should not be confused
with “finite parameter scan.” The spectral statement is also a genuine
all-rank asymptotic theorem. Both are suitable as substantial sections of
the larger OPG manuscript.

They are not yet a secure Q1 main result:

- the kernel theorem stops at \(\beta^8\);
- the pooled alternating inversion is untouched;
- the spectral theorem controls only the leading coefficient of each
  long band;
- neither result proves the full complete-split Rayleigh difference;
- the original all-graph OPG conjecture remains open.

A plausible Q1 upgrade still requires at least one genuinely infinite
structural closure: positivity of all kernel ranks, elimination of the
pooled inversion and closure of the complete \(\alpha^2\) layer, or a
Gårding/Rayleigh-preserving operation covering the whole complete-split
family.

## 7. Reproduction log

Executed successfully:

```text
pytest -q data/research_open/q1_four_problem_campaign_2026-07-30/opg1757
....                                                                     [100%]
4 passed in 10.94s
```

Also rerun successfully:

- the inherited exact Rouché/Jensen certificate;
- the new exact dominant-zero certificate;
- four additional exact Cayley cross-check points, including \(s<k\).

No repository commit or push was performed by this audit.
