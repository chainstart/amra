# OPG-1757 transfer-round claim ledger

Date: 2026-08-02

## T1. Exact effective-height spectrum

**Status: PROVED / EXECUTABLY VERIFIED.**

For the four frozen common-base sums (odd/even sufficient kernels and
odd/even page remainders), the effective height of a kernel monomial
`c*s^m*beta^j` is `m-j`.  The complete top-height pieces are exactly (6)--(8)
of `COMPLETE_LOG_LAYER_THEOREM.md`; every omitted monomial loses at least one
height unit.

Evidence: exact symbolic extraction in `verify_complete_log_layer.py`, pinned
to old source SHA-256
`a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125`.

## T2. Complete-channel fixed-index certificate

**Status: PROVED.**

For `p=6,7`, the complete top-height generating identities are

\[
 2y^2(y-(1+x)^2)^{p-2}
\]

for the sufficient kernel and

\[
 2(p-2)x^2(1+x)y^2(y-(1+x)^2)^{p-3}
\]

for the lower-base part of the page remainder.  After `y=e^(2x)`, every
coefficient from degree `2p-4` onward is strictly positive because

\[
 e^{2x}-(1+x)^2=x^2+\sum_{n\ge3}2^n x^n/n!.
\]

Consequently each fixed transport column has an eventually positive
sufficient kernel and page remainder.  This is not a claim that each base is
positive separately; several bases have negative top-height pieces.

## T3. Growing-index sufficient-kernel chamber

**Status: PROVED.**

For any sequence `s_n->infinity`, `k_n->infinity`, and
`k_n=O(log s_n)`, the `p`-base term

\[
 2s_n\binom{L_{s_n}}{k_n}p^{k_n}
\]

is positive and asymptotically dominates the entire sufficient sum.  A lower
base `a<p` costs `(a/p)^k` and gains at most a fixed power of `k`; a
lower-height term also costs `s^(-1)` times a fixed power of `k`.

This is an asymptotic chamber theorem, not a full finite-parameter theorem.

## T4. Growing-index page chamber and transition

**Status: PROVED.**

Let `q=p-1`.  In the page remainder, the only two terms that can compete are

\[
 A_q=2(p-2)s^2\binom{M_s}{k-3}q^{k-3}>0,
 \qquad
 A_p=c_p\binom{M_s}{k-2}p^{k-2}>0,
\]

where `(c_6,c_7)=(36,50)`.  Precisely,

\[
 [\beta^k]Q_{p,s}=A_q(1+o(1))+A_p(1+o(1))
\]

uniformly along every sequence with `k->infinity` and `k=O(log s)`.

The exhaustiveness is as follows.

- Every height `-1` base `a<q` is
  `O(poly(k)(a/q)^k) A_q=o(A_q)`.
- Every omitted `q`-base monomial is `o(A_q)`; its top companion at shift two
  is already smaller by `O(1/k)`.
- The `p` base has exactly one height `-2` top monomial; all its other
  monomials are `o(A_p)`.
- All remaining monomials have both a lower base or a lower height and are
  absorbed by the preceding bounds.

Thus no third scale can enter the transition.  The ratio is

\[
 A_5/A_6\sim(4/125)sk(5/6)^k,
 \qquad
 A_6/A_7\sim(49/2160)sk(6/7)^k.
\]

The low chamber (`A_q` dominant), high chamber (`A_p` dominant), and tied
transition are all positive.  This is stronger than identifying a candidate
asymptotic main term: the error is `o(A_q)+o(A_p)`, so it remains smaller than
the positive sum even when the two terms are comparable.

## T5. Uniform eventual logarithmic-gap theorem

**Status: PROVED.**

There exists a **single** absolute integer `S_gap` such that

\[
 \forall s\ge S_{\rm gap}\;\forall d\in\mathbb Z,
 \quad 31\le d<241\log s
 \Longrightarrow
 [z^d]R_s^{\rm o}>0\ \wedge\ [z^d]R_s^{\rm e}>0.
\]

Quantifier proof: apply the argument first to each of the four certificate
sums.  If one lacked a threshold, for each `n` one could choose `s_n>=n` and
an offending integer `d_n`.  With `k_n=d_n+8` or `d_n+10`, either an infinite
bounded subsequence exists, in which case a further subsequence has constant
`k` and contradicts T2, or an unbounded subsequence exists, from which a
further subsequence satisfies `k_n->infinity` and contradicts T3--T4.  These
are exhaustive for an integer sequence.  Since
`k_n<=241 log s_n+10`, all uses of `k=O(log s)` are uniform.  Taking the
maximum of four thresholds gives one threshold for all certificate sums.  If
one instead begins with nonpositive actual transports, the old lower-bound
implication forces at least one certificate failure; finite pigeonhole fixes
that certificate on a subsequence.  Finally enlarge the threshold until the
whole logarithmic layer lies in both natural bulk ranges.

The theorem is eventual.  `EFFECTIVE_GAP_BOUND.md` proves that its threshold
may be chosen below the explicit 117-digit integer displayed there.  The
post-freeze high-range audit T5h separately makes the complementary old
range effective.

## T5e. Effective gap threshold

**Status: PROVED / EXECUTABLY VERIFIED.**

The `S_gap` of T5 may be chosen no larger than

```text
557318272747802613573322901489669353946699423886389776921726369126099873157883699268070504958536925059099817311331374
```

The proof splits at `k=1000`, uses exact fixed-index leading/error ratios
below the split, and exact monotone rational majorants above it.  See
`EFFECTIVE_GAP_BOUND.md` and `effective_gap_bound.py`.

## T5h. Effective high logarithmic range

**Status: PROVED / INDEPENDENT AUDIT PROMOTED.**

For all four certificate sums, the old `d>=241 log s` proof has the explicit
common threshold

```text
S_high = 182963662611742278515145357606424176862843.
```

Exact lower-base coefficient norms give four thresholds `102`, `S_high`,
`75`, and `1494048895141509478550315587139453832856`.  Their maximum has 42
digits and is strictly smaller than the 117-digit number in T5e.  The
low/high retained binomial indices are legal throughout the bulk ranges,
and the old all-parameter top bands introduce no further threshold.

Independent evidence: `HIGH_RANGE_CROSS_AUDIT_BY_ERDOS776.md`, SHA-256
`c5c99cf29ffb500f76fbc8b02300d53bb604e7130666c759429685839fd63a32`,
and `cross_audit_high_range_by_erdos776.py`, SHA-256
`bf982323a57370440cab9fad55643267b5f06709325425dbaebe2fa2f27fb0a8`.
The verifier pins both the old recurrence SHA-256 and the digest of all four
expanded component families.

## T6. Eventual complete third-active transports

**Status: PROVED WITH AN EXPLICIT EFFECTIVE EVENTUAL THRESHOLD.**

Choose `S_transport` equal to the 117-digit upper bound in T5e.  It dominates
the effective high-range threshold in T5h, all gap-certificate requirements,
and every support/geometry guard.  For each integer coefficient degree
`0<=d<=2s-4`, exactly one of the following
applies:

1. `0<=d<=30`: old universal low-column theorem;
2. `31<=d<241 log s`: T5;
3. `241 log s<=d<=2s-4`: old logarithmic-boundary theorem, whose proof already
   includes the bulk/top-band splice.

The strict and non-strict inequalities leave no integer boundary gap.  Hence
both candidate transports are coefficientwise strictly positive for every
`s>=S_transport`.

This does **not** prove the transports for all finite `s`.  Moreover,
the 117-digit bound is intentionally crude and is only an upper bound for
eventual positivity, not the first valid parameter.

## C1. Finite stress scan

**Status: CORROBORATION ONLY; NOT USED IN T1--T6.**

Exact integer coefficient scans are reported by
`stress_complete_log_layer.py`.  Their range and count are recorded in
`STRESS_TEST_REPORT.md`.  No conclusion outside the scanned parameter set is
drawn from them.

## Firewall

The following remain **OPEN**:

- coefficientwise positivity of both transports for every stable finite `s`;
- a universal third-active row theorem;
- later active rows and arbitrary-host transfer;
- the original OPG-1757 proposition.
