# Mechanism falsification: residue-aware round

The exact replay command is

```text
python3 evidence/verify_residue_aware_kills.py
```

with source SHA-256

```text
6000976780a71927fdf38a0ceb2d085c19ad4b12344c886cb284bc0166a30828
```

The verifier returns `PASS`.  It checks exact equal products, strict rough
high-tail membership, active degrees, token transfer, and exhaustive small
minimality instances.  RR.1 and RR.2 are universal because of their symbolic
constructions, not because of the finite loop.

## Alteration/dependency family

### M786R-01 killed: local degree and `L` do not bound event support

Fix `L>=3` and maximum active degree two.  RR.1 permits arbitrary `s`, hence
support `2s+1` and diameter `2s`, while preserving high-tail membership,
roughness, squarefree active primes, and support minimality.  No function of
`L` and maximum active degree alone bounds a residual bad-event support.

### M786R-02 killed: bad components need not contain an active cycle

The active-incidence graph of RR.1 is the path `P_(2s+1)`, with cycle rank
zero.  It is nevertheless one support-minimal unequal relation.  A feedback-
vertex deletion that only pays for cycles can leave the whole bad tree.

### M786R-03 killed: no bounded-radius bad subrelation in a bad tree

Unique edge-prime equations on the connected path force all signed
coefficients to alternate with one common nonzero magnitude.  Thus every
proper support has no bad subrelation.  As `s` is arbitrary, a uniformly
bounded-radius local witness cannot exist.

### M786R-04 survives: full-component arithmetic alteration

RR.1 says this mechanism must treat a complete long tree as one event or
cluster; RR.2 says its boundary residue can have unbounded fan.  Neither
family proves that the union of such clusters has linear hitting cost.
The exact surviving target remains a symbolic repair bound

\[
 |D_N|\le g(N)\sum_n w_N(n)+o(N),\qquad g(N)=o(\log N),       \tag{7}
\]

using actual shared valuation rows.  No theorem establishing (7) is present.

## Largest-prime ownership family

### M786R-05 killed: top fibre size does not bound residue complexity

RR.2 has top-prime fibre cardinality exactly two for every `r,s`, but after
stripping the top prime its cofactors are `Y=prod B` and `X=prod A`.  Their
independent prime supports have sizes `s` and `r`, which are arbitrary.

### M786R-06 killed: fixed `L` and active degree do not bound peel depth

In RR.1 order the edge primes increasingly from left to right.  The largest
prime joins the right endpoint to its neighbor.  After it is stripped, the
neighbor cofactor still contains the next edge prime; the next valuation
balance therefore transfers the residue one edge left.  Repeating follows
all `2s` path edges.  Since `s` is arbitrary at fixed `L` and maximum degree
two, no claimed bound depending only on those two parameters exists.

### M786R-07 killed: coprime top cofactors do not split the global state

The RR.2 cofactors `X` and `Y` are coprime, but each prime of `X` also occurs
in a lower singleton on the opposite shore, and likewise for `Y`.  Together
with the top edge they form one connected double-star circuit.  Coprimality
of the two exposed cofactors is not a component decomposition.

### M786R-08 survives: global residue owner flow

The local bounded-fan and bounded-depth versions are dead, but a global owner
could in principle hit an entire path or double star at one vertex and share
that owner across many circuits.  The noncircular target is an explicit owner
map from ordered valuation/cofactor states satisfying the same
`g(N)=o(log N)` distinct-owner bound as (7).  No such map or load proof is
known here.

## Recursive potential and coherence family

### M786R-09 killed: cycle rank is zero on a bad starting state

RR.1 is a bad support-minimal tree.  A potential required to be positive on
every bad state cannot be active cycle rank, and a strict-decrease argument
cannot start from zero.

### M786R-10 killed: top stripping need not decrease token count

At the last RR.1 edge, the two incident integer tokens are replaced by their
two nontrivial cofactors.  The neighbor cofactor retains the preceding edge
prime.  Thus the token count is two before and two after the step, and the
same phenomenon repeats along the path.  Prime height decreases, but token
count does not.

### M786R-11 killed in its no-reserve future-safety form

The lower set `A union B` of distinct primes in RR.2 is admissible by unique
factorization.  A later prime `p` and two later integers `pY,pX` create the
new minimal relation

\[
A\cup\{pY\}\quad\text{versus}\quad B\cup\{pX\}.
\]

Therefore finite-prefix safety is not hereditary merely because all old
decisions were safe.  This kills only the stated premise that future primes
cannot create cross-prefix relations.  A monotone rule that reserves enough
future deletions, or a summable revision rule, is different.

### M786R-12 survives: global multiscale potential with reserve

A viable potential must see global path support/fan, not only one peel.  It
must telescope cofactor height or log-defect across arbitrary RR.1 depth and
pay RR.2 future completions from a summable reserve.  The exact finite target
is (7); the infinite target additionally requires summable pointwise
revisions and a zero-upper-density deletion set.  These claims remain open.

## Selection

Nine of twelve mechanisms are killed.  The survivors represent the three
required genuinely different families:

* `M786R-04`: probabilistic/dependent full-component alteration;
* `M786R-08`: deterministic global residue-aware owner flow;
* `M786R-12`: recursive multiscale potential with coherent reserve.

No survivor is asserted proved, and no density-one conclusion follows from
RR.1 or RR.2.
