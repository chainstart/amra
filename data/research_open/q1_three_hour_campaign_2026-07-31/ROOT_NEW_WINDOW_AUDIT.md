# Root audit for the renewed three-hour window

Date: 2026-07-31

Renewed clock: 17:05:46--20:05:46 HKT.

This file records checks performed independently of the problem-owner
agents.  It is a live audit and not a claim that any named open problem has
been solved.

## Baseline

At the start of the renewed window the whole campaign suite returned

```text
32 passed in 33.15s
```

The later problem-specific suites are recorded below as they land.

## OPG-1757: fixed deficit three

The proposed fourth attack concerns exactly
\[
n=2s-8,\qquad s\ge4.
\]
The overlap/excess relations were independently checked:
\[
r=2\ell+e+f+a,\qquad
c+d+e+f=6-\ell.
\]
Since \(c,d\ge1\), these relations really do restrict every endpoint to
\(e\le4\).  The five partitions of excess four are all present, so the
endpoint list does not silently omit a nonbinary species.

Both executable routes were run at the root:

- the symbolic endpoint/assembly certificate checks 45 endpoints and 345
  denominator-aware values;
- the direct-position endpoint enumerator plus the inherited primitive
  page-transfer checks the same 345 values and 84 nonzero pooled rows.

Their respective SHA-256 digests are

```text
b3a61e4490fe6c298a7ecb5d775942dcfc5586a6c9217efeae71e303ad0d552c
ee808d89398c3f05cd373e84b1d086a6039667d1221e4897554584fbfeccfdda
```

The seven normalized factors have strictly positive coefficients after
the substitution \(s=u+5\).  Subject to the already audited
denominator-aware Abel lemma, this proves
\[
B_{2s-8}(s,\beta)>_{\mathrm{coeff}}0\quad(s\ge5),
\qquad B_0(4,\beta)=0.
\]
It does not prove another value of the fixed deficit, all pooled layers,
or arbitrary-host OPG-1757.

## OPG-1757: fixed deficit four

The same finite-reduction theorem was next instantiated at
\[
n=2s-9.
\]
The main certificate checks 63 endpoints, 588 denominator-aware endpoint
values, five overlap orders, and all nine beta offsets.  More importantly,
an independent proof route does not use those endpoint formulas: the
pre-existing primitive page-transfer supplies \(r+11\) exact values for
offset \(r\), exactly the number required by the previously proved
\(\deg R_{4,r}\le r+10\) bound.  All 135 independent values agree with
the proposed formulas.  The two executable digests are

```text
d7077e98219656bd21bdf5c4b322690a0cc91e40727ae44d376fca7be4eb159c
4522fb4b1e0a4180f38314fb4244ba5f35ff645d476d369d388a510475225815
```

Every normalized factor has zero constant term and strictly positive
higher coefficients after \(s=u+5\).  Hence
\[
B_{2s-9}(s,\beta)>_{\mathrm{coeff}}0\quad(s\ge6),
\qquad B_1(5,\beta)=0.
\]
This is the fifth deepest complete-split pooled layer, not an induction in
the deficit.

## OPG-1757: fixed deficit five

The next instantiation is
\[
n=2s-10.
\]
The full route uses 84 endpoints and exactly 924 denominator-aware Abel
values; the count-consistency firewall rejects the tempting mixed count
of 81 endpoints with 924 values.  All eleven beta offsets contain the
proved boundary factor \((s-4)(s-5)\).  The main endpoint/assembly
certificate and the independent primitive rational certificate have
digests

```text
b57014668227d7981c207f93a051d6c497ea59417414721874792a13ecfd955e
cb48205d645974aeebee2b371ea11db3b01ce7b19225dd6bb2c77dd9bfd4d754
```

The independent route uses 176 primitive values over \(6\le s\le26\)
and does not import the endpoint assembly.  Each normalized factor has
strictly positive coefficients after \(s=u+6\).  Hence
\[
B_{2s-10}(s,\beta)>_{\mathrm{coeff}}0\quad(s\ge6),
\qquad B_0(5,\beta)=0.
\]
Together with the top two layers, this closes the six deepest nonzero
complete-split pooled layers \(q=0,\ldots,5\).  It is still not an
arbitrary-deficit or arbitrary-host theorem.

## OPG-1757: all-deficit top-two endpoint theorem

The 84 endpoint formulas reveal a uniform leading/subleading law.  A
rooted-hypertree EGF and Lagrange inversion now prove it for arbitrary
endpoint excess:
\[
Q_{h,e,c}(s)
=A_{e,c}s^{2c+2e-2}
+A_{e,c}b_{h,e,c}s^{2c+2e-3}
+O(s^{2c+2e-4}),
\]
where
\[
A_{e,c}=\frac1{2^{c+e-1}(c-1)!e!},
\]
\[
b_{h,e,c}
=\frac{(15-4e)(c-1)-e(4e+5)}3-h(c+2e-1).
\]
The leading Rayleigh terms cancel termwise, and the next terms cancel
under endpoint transposition.  Since the denominator-aware reduction
already proves that \(R_{q,r}=s^rC_{q,r}\) is a polynomial, this improves
the all-fixed-deficit degree bound to
\[
\deg R_{q,r}\le2q+r.
\]
The executable regression checks the law on all 84 certified endpoints,
checks the rooted/unrooted EGF on 119 primitive endpoints, and checks 496
instances of the transposition involution.  Its digest is

```text
1c2c26adc83e310b6290817416ee8678560222c91c132d43d522d0c31725ac54
```

Endpoint polynomiality and arbitrary-\(q\) positivity remain open.

## Erdős #809: nonempty-shore congestion

For a missing pair \(bb'\subseteq B\), fix a shore path
\[
b-p-q-b'.
\]
The coordinate-role argument in the fourth attack was checked directly.
One repeated colour must be left-rooted at \(p\) or right-rooted at \(q\).
There is at most one of each type, and coexistence gives the simple cycle
\[
b-p-q-b'-a-v-c-b,
\]
containing the two edges of the left-rooted colour.  All seven vertices
are distinct by \(b,b'\notin N[v]\) and the induced-matching condition.
Thus a nonempty shore has exact congestion at most one.

The full four-stage #809 suite returned

```text
16 passed in 25.97s
```

The remaining inference is not a local congestion bound: it is the
aggregate treatment of zero-shore pairs and the outer-\(A\) residual.
Any zero shore is also an \(S=\varnothing\) instance of the older
no-three-step structural dichotomy, which is the next global route to
test.

The subsequent structural pass strengthens the local zero-shore estimate.
If \(h=\lambda(b,b')\), coordinate injectivity and inducedness give
disjoint sets \(X,Y\subseteq A\), each of size \(h\).  Zero shore makes
the whole rectangle \(X\times Y\) absent, so
\[
M_A\ge h^2.
\]
The R003 common-neighbour branch further gives
\(h\le n-2\delta\).  Exact-four robustness forces the connector-triple
hypergraph to have transversal number at least three.  These statements
were checked, but at fixed positive \(s\) the R003 exceptional blocks can
still have linear size.  No aligned-core conclusion follows without a new
aggregate theorem.

## Erdős #776: rank-44 audit

The sampled canonical expansions at
\[
V=288,289,300,379,500,1000,2000,10000
\]
share the same high-rank template through rank three.  That observation is
only discovery evidence and is not used as a uniform theorem.  Instead,
the third attack defines an explicit algebraic block \(J_{44}(V)\) without
assuming that the displayed template is canonical, and Pascal telescoping
then gives the unconditional identity
\[
H_{44}-D_{44}
=\binom{V-55}{2}-R_2(V),
\qquad R_2(V):=D_{44}(V)-J_{44}(V).
\]

A tempting carry-free approach was also falsified.  Fully unrolling every
additive \(V\)-tax by Kruskal--Katona subadditivity produces an upper bound
far above \(H_{44}\); at \(V=288\) its excess over the actual \(D_{44}\)
is about \(1.51\times10^{52}\), whereas \(H_{44}-D_{44}=25058\).
Consequently a proof must retain the late canonical template or an
equally sharp potential; termwise global subadditivity cannot close the
gate.

The third attack gives two quantifier-safe reformulations:
\[
D_{44}<H_{44}
\iff
E_{31}<\binom{N-1}{31}+\binom{N-2}{30},
\qquad N=V-25,
\]
Thus the genuinely stronger sufficient target
\(D_{44}-J_{44}\le7V\) would close the gate.  The adjacent \(6V\)
proposal is rigorously false at \(V=288\), where the algebraic tail is
1970.  Neither the rank-31 comparison nor the \(7V\) bound has been
proved.

## Final renewed-window additions

### OPG fixed deficit six

The seventh attack proves
\[
B_{2s-11}(s,\beta)=0\quad(s=6),
\qquad
B_{2s-11}(s,\beta)>_{\rm coeff}0\quad(s\ge7).
\]
The main route checks 108 endpoints and 1,368 denominator-aware endpoint
values.  The independent primitive page-transfer route uses the sharpened
\(\deg R_{6,r}\le12+r\) bound and three boundary roots, so it needs exactly
\(\sum_{r=0}^{12}(10+r)=208\) values.  The independent and main digests are

    da7b0e5430ab29140cbf3847777a5790ce65fea1f3a161daecd35af706c45d25
    73245de5eb600ffa7727ce130c362f76c71decc64236112aae496a4974d8c887

All thirteen shifted coefficient polynomials have thirteen strictly
positive coefficients.  This closes \(q=6\) only; it is not an induction in
\(q\).

### Erdős #776 quotient--remainder entry certificate

The fourth attack replaces the coarse ceiling loss by an exact decomposition
\(V=288m+t\).  Exact rational verification over 230 transitions and all 288
residue classes per transition proves that first moving-block entry residual
rank at most 233 forces \(D_{18}<P_{18}\).  Equivalently,
\[
D_{248}<H_{248}\Longrightarrow D_{18}<P_{18}
\qquad(V\ge288).
\]
The endpoint margin is 4,928.  The same certificate first fails at residual
rank 234 by 31,997; this is a failure of the invariant, not a counterexample
to the underlying target.  The premise \(D_{248}<H_{248}\) and #776 remain
open.

The root quick verifier, including an exact scan through \(V=1000\), returned
PASS.  The longer agent scan through \(V=20000\) found no \(R_2\le7V\)
counterexample, but is finite evidence only.

### Erdős #809 residual-moment route

The seventh and eighth attacks prove the exact opposite-pair core identity,
the weighted endpoint identity
\[
\mathcal R_{\rm opp}
=\sum_v\omega(v)\left(\frac n2-d(v)\right),
\]
and a low-degree-support condition sufficient for an aligned core.

A three-clique-chain family satisfying the full maximum-witness contract,
\(L_4(2)\), and the rainbow-\(C_7\) condition refutes the attempted inference
from absorption-certificate failure to a little-\(o\) residual moment.
However, it has \(D_A=D_B=M_B\), so the exact budget closes and it is not a
counterexample to #809.  The 40-vertex verifier checks 780 endpoint pairs,
equivalent to 578,760 deletion cases.  Erdős #809 remains open.

## Final regression

- all 70 distinct campaign unit-test cases were covered across the root runs;
- top-two endpoint audit: PASS;
- \(q=5\) plus #809 seventh-stage tests: 9 passed in 356.34 seconds;
- \(q=6\) plus #809 eighth-stage tests: 11 passed in 254.02 seconds;
- remaining smoke suite: 53 passed in 104.60 seconds;
- #776 quick verifier: PASS;
- whitespace, control-character, and scope-firewall audits: PASS.
