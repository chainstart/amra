# Round-3 finite audit of the full inhomogeneous Fejer majorant

Date: 2026-08-27

Classification: **finite falsification/diagnostic only**.  This note concerns
the positive `L=2` majorant with the reconstruction-safe half-width
`b_i=d_i/2`.  It does not falsify the exact Fourier formulation or Erdos
451.

## Exact scanner

`work/m10_round1/full_inhomogeneous_fejer_scan.cpp` enumerates every integer
global lift `0<|H|<h`.  The period, width product, ceiling defining `h`,
alias test, and all local-membership decisions use integer/GMP arithmetic;
only the final nonnegative triangular mass is accumulated in `long double`.

Source SHA-256:

```text
2a99fe5b4dad8c2a7d84df6ef2a552d417181e68b5f57ba89779a56aaa84d4bd
```

Guarded compile:

```text
unit: openmath-task-20260827-014715-370434.scope
exit: 0
maximum RSS: 145112 KiB
swaps: 0
```

The first complete batch used `B=0`, `C=5/2` and unit
`openmath-task-20260827-014736-370608.scope` (exit 0, maximum RSS 4160 KiB,
swaps 0).  A second complete batch used `C=3` and unit
`openmath-task-20260827-014743-370667.scope` (exit 0, maximum RSS 4160 KiB,
swaps 0).

## Results

```text
k   m   C      h           S                  S<2
10  4   5/2         9547   2.48528965658273   no
16  5   5/2       159271   2.38867106005240   no
22  6   5/2       873328   2.20854978167072   no
27  7   5/2      9568111   1.24320940120454   yes
30  7   5/2     15981322   2.19774486292709   no
34  8   5/2     57494727   1.28588931134362   yes

10  4   3          19796   2.37268208687387   no
16  5   3         396317   2.31826393102676   no
22  6   3        2607741   2.11397358328674   no
27  7   3       34284269   1.03970442819543   yes
30  7   3       57263966   2.10761550049717   no
34  8   3      247216801   1.18904092595190   yes
```

The failures at `k=10,16,22,30` all contain the prime `p=k+1`, hence one
coordinate of width `d=1`.  At the reconstruction-safe half-width `b=1/2`,
the only compact local frequency is zero and its triangular coefficient is
`1/b=2`.  Increasing the time constant did not remove the effect.  In a
third guarded run (`openmath-task-20260827-015230-371354.scope`), the
completed `k=30` rows were

```text
C=4: S=2.08438566541357
C=5: S=2.08347561644291
C=6: S=2.08342593868245.
```

The requested `C=8` tail of that batch was terminated after the stable
trend was established; the three displayed rows had already completed.
The scope remained below 3 MiB and at zero swap while observed.

## Geometric boundary check

One tempting repair is to replace `b_i=d_i/2` by `(d_i+1)/2`, because the
open coordinate interval then contains exactly the integer residues
`0,...,d_i-1`.  That coordinatewise observation alone is insufficient for
the continuous box-spline proof: the common time supplied by support
membership is real and still has to be reconstructed as an integer.

Indeed the enlarged located intervals have the form

```text
I_i=(p_i a_i-d_i, p_i a_i+1).
```

For any two coordinates `i,j`, CRT supplies an integer `N` with
`N=0 (mod p_i)` and `N=-d_j (mod p_j)`.  Taking
`p_i a_i=N` and `p_j a_j=N+d_j` gives

```text
I_i intersect I_j=(N,N+1),
```

which contains real points where both compact densities are positive but
contains no integer common time.  By contrast `b_i=d_i/2` gives common
half-integer endpoints, the parity feature used by the existing integral
reconstruction lemma.

Therefore the larger-width repair requires a new discrete-time bridge or a
separate integrality argument.  It cannot be inserted into the existing
continuous reconstruction merely from positivity at open support.

## Consequence

The finite data are positive for some systems without `d=1` and negative
for every tested system with `d=1`.  The present all-prime positive
majorant is therefore not yet a uniform closure route.  A viable successor
must either treat the exact `d=1` congruence outside the continuous spline,
or replace the continuous common-time reconstruction by a genuinely
discrete nonnegative kernel while retaining a density-scale joint bound.
