# Cross-audit: exact interval scan for the periodized Fejer bridge

Date: 2026-08-27

Audit type: same-model mathematical and implementation cross-audit of
`work/m10_round1/periodized_bridge_exact_interval_scan.cpp`.  This is not an
independent human review and the author source was not modified.

Verdict: **PASS in the declared finite-scan scope.**  The integer membership,
triangular normalization, support histogram and finite scope reconstruct
exactly.  Independent guarded runs reproduce every reported `C=1` failure,
the `C=2` values through rank ten, and a rational-`C` case.  An intermediate
Boost-based arbitrary-precision patch was not buildable in this environment;
the current source uses the installed GMP C++ interface and has now passed a
fresh guarded compile and high-rank replay.

## 1. Actual block and integer scale

For the supplied `k,Delta`, the source forms the **complete** actual prime
block

```text
p prime, p<2k, Delta<=p-k<2Delta.
```

Thus it is not a selected subblock.  With `d_i=p_i-k` it computes

```text
P=product_i p_i,  D=product_i d_i,
2b=2 floor((Delta-1)/2)+1,
h=ceil(k^2 C^q P/D).
```

For rational input `C=C_num/C_den`, the patched formula is exactly

```text
h=ceil(k^2 C_num^q P/(C_den^q D)).
```

The test `2h<P` is precisely the no-alias hypothesis used by the `L=2`
Fejer bridge.  The old signed-`__int128` implementation could overflow
before its range test.  The current `mpz_class` algebra removes that
mathematical defect and the guarded build links the declared installed
libraries `-lgmpxx -lgmp`.

## 2. Membership and normalization

For each integer `1<=H<h`, centered reduction modulo every odd `p_i` gives
the unique `a_i` with `-p_i/2<a_i<p_i/2` and `a_i==H (mod p_i)`.  The code
admits exactly

```text
|a_i|<b  for every i,
```

because `2*abs(a_i)>=2b` is rejected.  It multiplies

```text
beta_i(a_i)=b^(-1)(1-|a_i|/b)
             =(2/(2b))(1-2|a_i|/(2b)),
```

then the global triangular factor `1-H/h`.  Centered residue uniqueness and
evenness identify the negative lifts with the positive lifts, while the
origin contributes `b^(-q)`.  Hence the printed value is exactly, up to the
final long-double evaluation,

```text
S=(P/h)[b^(-q)+2 sum_(1<=H<h, all |a_i(H)|<b)
                    (1-H/h) product_i beta_i(a_i(H))].
```

This is equation (R3.16), including the factor `P/h`; no hidden `P`, `h`, or
factor-two normalization is missing.  Boundary weights would be zero, and
the source consistently uses the strict support convention.

The positive support histogram increments only after all coordinates pass
membership and records `#{i:a_i!=0}`.  `admitted_total_H=1+2N_positive`
therefore counts the origin and both signs.  It is a diagnostic count, not a
weight and not a proof of `S<2`.

All membership decisions, the histogram and `h` are integer operations.
Only the final weighted sum and conversion of `P` use `long double`.
Consequently a value extremely close to two would need an error interval or
exact rational replay.  The displayed failures/passes below are separated
from two by much more than floating rounding at their scales.

## 3. Independent finite reproduction

Guarded old-source runs (before the arbitrary-precision dependency patch)
reproduced the complete-block `C=1` failures:

```text
(k,Delta,q)       h          S(C=1)       support histogram for H>0
(57,32,7)       1019476      2.928087268   {5:8,6:36,7:176}
(100,64,8)      5318182      3.989495594   {6:9,7:132,8:1021}
(118,64,9)     24091441      7.742589110   {7:1,8:65,9:484}
(117,64,10)    60692261     15.477197745   {8:7,9:51,10:342}
```

Thus `C=1` is genuinely false for this **strong positive majorant** already
in finite actual blocks.  It does not refute the smaller exact-carry Fourier
sum and says nothing directly about Erdős 451.

The same exact-membership implementation gave

```text
(57,32,7):   S(C=2)=1.010813016,
(100,64,8):  S(C=2)=1.002870796,
(118,64,9):  S(C=2)=1.022549451,
(117,64,10): S(C=2)=1.006700721.
```

The rank-ten run used the prior fixed-width source, but its exact intermediate
integer numerator is below `2^127`; its membership path is unchanged in the
GMP source.  The final GMP source independently replayed the rank-nine line
with identical `h`, histogram, and `S`.  It also replayed the rational case

```text
(k,Delta,q,C)=(100,64,8,13/10):
h=43382037, S=1.189832738013204.
```

This confirms that both numerator and denominator powers are incorporated in
the exact ceiling.  It is a distinct parameter choice from the author's
other rational diagnostics and remains finite evidence only.

Additional fixed preselection scans of complete blocks first used
`30<=k<=300`, dyadic `Delta`, `3<=q<=10`, with `h<=5e6`, total `h` budget
`3e7`, and then `h<=1e8`, total budget `1e8`.  They scanned 22 and 17 cases
respectively, reaching rank six, and found no `C=2` failure.  A final GMP
scan used `30<=k<=1000`, `h<=1e9`, and total `h` budget `1e10`; it scanned
79 cases and, in particular, **all 12 eligible rank-seven complete blocks**
in that declared box.  It found no failure.  The largest `S` by rank in the
final scan was

```text
q=3: 1.013508381, q=4: 1.018958666,
q=5: 1.025601345, q=6: 1.028138643, q=7: 1.010813016.
```

The candidate ordering `(-q,h,k,Delta)` and all budgets were fixed
before inspecting `S`, but this is still finite falsification evidence only.
Together with the four high-rank cases it does not prove a uniform `C=2`
theorem, monotonicity in `C`, or any asymptotic estimate.

## 4. Reproducibility and remaining numeric scope

The current source hash is
`f521a4c9fafbb1dc703c9dd4b8cae98787741ccf4cda42811a9e3dfacbd9ed2b`.
It compiled under guard with

```text
g++ -O3 -std=c++20 periodized_bridge_exact_interval_scan.cpp
    -lgmpxx -lgmp
```

and the fresh rank-nine replay used unit
`openmath-task-20260827-013231-367839.scope`, peak RSS `4160 KiB`, zero swap.
The rational replay used unit
`openmath-task-20260827-013227-367818.scope` with the same peak and zero swap.

`P,D,C^q,h` and membership are arbitrary-precision/integer.  The output
still converts `P` to `long double` and accumulates `S` in `long double`;
therefore a future case close to two or beyond its finite exponent range
would require a controlled-error or exact-rational summation.  That does not
affect the reproduced cases, whose margins are macroscopic relative to
floating roundoff.

Final classification: the finite scan formula, support ledger, current build,
and reproduced numbers pass.  No asymptotic `S<2` result is claimed.
