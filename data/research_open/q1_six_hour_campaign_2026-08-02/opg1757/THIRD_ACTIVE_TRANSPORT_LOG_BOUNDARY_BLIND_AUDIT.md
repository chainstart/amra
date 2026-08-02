# Blind audit of the OPG third-active transport package

Date: 2026-08-02

Auditor: campaign root (author swap)

Verdict: **PASS AFTER REPAIR**

Public status: **OPG-1757 remains open**

## 1. Scope and repair

I reconstructed the claims in

- `THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md`,
- `THIRD_ACTIVE_TRANSPORT_TOP_BANDS.md`,
- `THIRD_ACTIVE_TRANSPORT_INTERIOR_SYMBOL.md`,
- `THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md`, and
- `THIRD_ACTIVE_TRANSPORT_FIXED_LAYER_OBSTRUCTION.md`.

The logarithmic theorem itself is correct.  One quantifier in its prose
needed repair: because its threshold `S` is existential, the statement
that the only remaining coefficients lie in

\[
31\le d<241\log s
\]

is an eventual statement for `s>=S`, not a classification of every finite
parameter below `S`.  The source now says this explicitly.  I also repaired
display-only corruption (two stray exponent commas, three missing display
closures, one misplaced `aligned` tag, and old list separators).  None of
those display repairs changed an expression used by a verifier.

## 2. Independent reconstruction of the four dominant sums

Write `u_a=1+a*beta`.  Clearing the positive powers and denominators gives
four sums of the form

\[
 T_{s,k}=\sum_{a=2}^p[\beta^k]u_a^L C_{a,s}(\beta).
\]

Reading the page definitions forward, rather than reading the reported
table backward, gives the following data.

| object | `p` | `L` | transport index `k` | kernel degree | lower-base `s` degree | retained shifts |
|---|---:|---:|---:|---:|---:|---:|
| odd sufficient | 6 | `2s-15` | `d+8` | 19 | 11 | 0 or 19 |
| even sufficient | 7 | `2s-17` | `d+10` | 23 | 13 | 0 or 23 |
| odd page difference | 6 | `2s-14` | `d+8` | 18 | 8 | 2 or 18 |
| even page difference | 7 | `2s-16` | `d+10` | 22 | 10 | 2 or 22 |

The shifts by 8 and 10 come from the cleared factors `beta^8` and
`beta^10`; the page exponents follow directly from subtracting
`u_p^2 F_(p,s)` from `F_(p,s+1)`.  Direct collection from the frozen page
kernels reproduces the four dominant shifted-positive certificates with
126, 176, 80, and 120 positive monomials.  The retained low coefficients
are

\[
2(s-2),\quad2(s-2),\quad36,\quad50,
\]

and independent factor/evaluation checks confirm strict positivity of all
four reported high coefficients on `s>=8,9,8,9`, respectively.

## 3. Retained-shift legality

If the low retained binomial index lies in `[0,L]`, it is legal by
definition.  Otherwise use the high shift.  On the claimed bulk ranges its
residual index is, respectively,

\[
d-11\le L-8,\qquad d-13\le L-10,
\]

\[
d-10\le L-8,\qquad d-12\le L-10.
\]

The lower inequalities are automatic once the existential threshold is
enlarged, because `d>=241 log s`.  Thus one retained term is legal on every
target coefficient; no binomial with a negative or overlarge lower index is
used.  The independent verifier checks this coefficient by coefficient
through `s=4000` (millions of rows), while the displayed inequalities are
the all-parameter proof.

## 4. The constant 241 and uniformity

For a lower base `a<p` and fixed kernel shifts `i,j`, direct cancellation
of the two binomial terms gives

\[
 \frac{|c_{a,j}(s)|a^{k-j}\binom L{k-j}}
 {c_{p,i}(s)p^{k-i}\binom L{k-i}}
 \le C s^{M+q}\left(\frac{p-1}{p}\right)^k.
\]

The binomial ratio costs at most `(L+1)^q`; all remaining shift powers are
constant.  The worst polynomial degrees are `19+11=30` for `p=6` and
`23+13=36` for `p=7`.  Independently,

\[
 \log(6/5)>9/50,\qquad \log(7/6)>11/72,
\]

so

\[
241(9/50)=43.38>30,
\qquad
241(11/72)=36.819\ldots>36.
\]

Consequently the lower-base total is
`O(s^(30-241 log(6/5)))` or
`O(s^(36-241 log(7/6)))`, uniformly in the whole target row, and tends to
zero.  There are finitely many lower monomials and four objects, so one
absolute enlarged threshold `S` works simultaneously.  Discarding the
other nonnegative dominant-base terms then leaves a strict positive term;
the proof does not infer strictness from a nonnegative limit.

## 5. Passage back to the transports

For odd coefficients, both cleared indices are `k=d+8` and the sufficient
bulk inequality is valid through `d=2s-12`.  The reverse band `t=0,...,7`
covers exactly `d=2s-11,...,2s-4`.  For even coefficients the corresponding
ranges are `d<=2s-14` and `d=2s-13,...,2s-4`.  Hence both splices are
contiguous, with neither a hole nor an overlap assumption.

Positivity of the two page differences licenses the Bernoulli scale step;
positivity of the sufficient kernels then gives strict transport
positivity.  Combining this with the exact columns `0<=d<=30` proves, for
`s>=S`, that only

\[
31\le d<241\log s
\]

is not yet certified.  It does not prove that any coefficient there is
negative, make `S` effective, or settle all smaller parameters.

I also reconstructed the reverse-coefficient identity used for the top
bands.  The three shifts from `(s+pz)^2` are exactly the `D_t`, `D_(t-1)`,
and `D_(t-2)` terms, and the nominal highest base cancels in the `t=0`
row.  Thus the exceptional dominant bases 5 (odd) and 6 (even) are
necessary, not cosmetic.

## 6. Fixed-layer obstruction

For the odd `u_2` expansion the beta-linear coefficient of layer `r` is

\[
-32(3^r-3\,2^r+3)s
+408\,4^r-1392\,3^r+1728\,2^r-912.
\]

The factor `3^r-3*2^r+3` equals 6 at `r=3`, and its next value minus twice
its current value is `3^r-3>0`.  Hence it is positive for every `r>=3`.
The first two specializations are independently reproduced as

\[
[\beta]R_{s,3}=-96(2s-15),\qquad
[\beta]R_{s,4}=-1152(s-16),
\]

including `[beta]R_(17,4)=-1152`.  This rules out the stated architecture
that demands coefficientwise nonnegative kernels after a fixed merge
depth.  It does **not** give a negative coefficient of the summed
recurrence or of either transport.

## 7. Executable evidence

Audited source hashes after the repair are:

~~~text
7e92647cf6092c715dc5360e865e5905bbbb27b41632579baf4e4f88080633b3  THIRD_ACTIVE_TRANSPORT_LOW_COLUMNS.md
7d93d38d16cf0489a8882fc742e7c1cf2c1dec4a4fa3930b015832ef9b9adbec  THIRD_ACTIVE_TRANSPORT_TOP_BANDS.md
d50b049bbf050f89cdb68c74cc0c63aea7f2c73c878d6dcc9a70de08190d4d48  THIRD_ACTIVE_TRANSPORT_INTERIOR_SYMBOL.md
08fa2ffba8bf9a88ac88985170914ddaad7b9f64ce692127e0901529540eb2ee  THIRD_ACTIVE_TRANSPORT_LOG_BOUNDARY.md
7b4cd60428048dc5570c2658ae3fad815b0961373d9fbfebe6175c17b55a4284  THIRD_ACTIVE_TRANSPORT_FIXED_LAYER_OBSTRUCTION.md
2a15c393a641f12f01bdcfa9eddea6d026c3e7c8d99fbd967758d65d58f917d0  third_active_transport_bulk_attack.py
db02d66f26616a2445d899859833abdb26e53293d58e6c7c757ab4266865768b  third_active_transport_top_attack.py
a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125  third_active_transport_recurrence_attack.py
de94e71398cb12d11084f6b9ad3327a76630b1b1590e296e2f1a8e4ebe4e8771  verify_third_active_log_boundary_blind_audit.py
dd0a27879dce52e75b49625212622cbb3451e62e9893ad55de5f95ab6cfb38be  test_third_active_log_boundary_blind_audit.py
~~~

The independent file
`verify_third_active_log_boundary_blind_audit.py` imports none of the
author workbench.  It checks the rational slopes, all four retained-shift
interfaces, both exact splices, and the layer obstruction.  Its regression
test passed:

~~~text
1 passed in 7.38s
~~~

The author's complete pre-audit OPG test directory was also run from the
repository root and reported `24 passed in 508.46s`; the new independent
test was run separately as the one-pass result above.  Source hashes are
recorded after the final audit repair, not copied from the pre-repair
manifest.

## 8. Firewall

The audit passes the universal second-active theorem, the finite `q=7`
Newton theorem, the exact low/top third-active bands, the compact-interior
and logarithmic-boundary theorems, and the fixed-layer route obstruction
in their stated scopes.  The full third-active transports remain open on
an unbounded logarithmic layer; the universal third-active row and the
arbitrary-host OPG-1757 proposition remain open.  No result in this audit
is a proof or disproof of the public proposition.
