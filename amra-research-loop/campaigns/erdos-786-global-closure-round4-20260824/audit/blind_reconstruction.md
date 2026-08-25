# Blind reconstruction of GC.1 and MC.1

## Isolation protocol

This document was written after reading only `closure_contract.json` and
`decisive_lemma.json`.  No file under `evidence/`, no verifier, and no author
proof was opened.  The purpose is to separate the projective-plane
combinatorics from the genuinely nontrivial arithmetic lift and to freeze all
quantifier and boundary obligations before comparison with the author proof.

## 1. Exact variant and target scope

`H_N` has vertex set `{2,...,N}`.  A bad support consists of two disjoint
finite sets of distinct integers with equal products and unequal
cardinalities.  After cancellation its signed vector has coefficients in
`{-1,0,1}`.  GC.1 is not a lower bound for `tau(H_N)`: it asserts a sparse
subfamily `F_K subset H_(2^K)` with matching number one and transversal number
larger than `log_2 N`.  If valid, its only admissible promotion class is a
standalone decisive obstruction to specified cluster-repair interfaces.

## 2. Projective-plane cluster skeleton

Fix a sufficiently large integer `K`.  Bertrand's postulate supplies a prime

\[
 K<q<2K.                                             \tag{B2.1}
\]

The projective plane `PG(2,q)` has

\[
 v=q^2+q+1
\]

points and the same number of lines; every line contains `q+1` points, every
point lies on `q+1` lines, and any two distinct lines meet in exactly one
point.

The arithmetic lift required by the decisive statement can be isolated as
the following interface.

> **Arithmetic lift AL(q,K).**  There are distinct point integers `x_P` and,
> for every projective line `L`, a finite private set `U_L`, such that
> `C_L={x_P:P in L} union U_L` is the support of a support-minimal
> distinct-Finset equal-product relation of normalized defect `-1`; every
> integer of every `C_L` lies strictly in `(2^K/32,2^K]`; the private sets are
> mutually disjoint and contain no point integer; and no private integer on
> one line equals any integer on another line.

Assuming AL, the claimed cluster properties are immediate and exact.

- `C_L intersect C_M={x_P}` for the unique projective point `P=L intersect M`.
- The circuit-intersection graph is complete, hence connected.
- Every two circuits meet, so `nu(F_K)=1`.
- A fixed projective line `L_0` supplies `q+1` point integers meeting every
  circuit, so `tau(F_K)<=q+1`.
- Conversely, a point integer belongs to exactly `q+1` circuits and a private
  integer to only one.  Any set of at most `q` integers therefore meets at
  most `q(q+1)=q^2+q<v` circuits by the union bound.  Some circuit is missed,
  so `tau(F_K)>=q+1`.

Thus

\[
 \nu(F_K)=1,
 \qquad \tau(F_K)=q+1>K=\log_2(2^K).                \tag{B2.2}
\]

The lower-bound argument permits a mixture of point and private integers; it
does not assume a transversal lies inside the projective point set.

## 3. Independent arithmetic-lift obligations

The proposition statement by itself does not specify the lift AL.  A valid
proof must meet all of the following simultaneous conditions.

### 3.1 Prime/exponent budget when `q>K`

A naive lift assigning a distinct private prime to every line incidence and
multiplying all `q+1` incidence primes into the shared point integer cannot
work: even the product of `q+1` factors at least two exceeds
`2^(q+1)>2^K=N`.  Thus the author construction must avoid per-incidence prime
products at shared vertices.  A global supply of `O(q^2)` or `O(q^3)` primes
is not by itself enough; the product or exponent sum entering each individual
integer must remain at most `K` bits.

The top-band fractional weight also gives a useful consistency check.  Every
`n>N/32` has

\[
 w_N(n)=\frac{\log(N/n)}{\log N}<\frac5K.
\]

Since the promoted fractional cover assigns total weight at least one to a
bad support, any such support needs more than `K/5` vertices.  The fact that a
projective line has `q+1>K` points is compatible with this necessary lower
bound, but it leaves no license to omit most line points.

### 3.2 Exact padding and the strict band

If an unpadded odd core `Q` is replaced by
`a=2^(K-ceil(log_2 Q)-d)Q`, then the undecremented value is in `(N/2,N]`.
To conclude the strict band `(N/32,N]` from this estimate alone one needs
`d<=4`; `d=5` yields only `(N/64,N]`.  Any different padding formula must be
audited with its own strict inequalities.  All exponents must be nonnegative,
including the worst private or exceptional vertices, and the equality of the
two total 2-adic exponents must be exact, not modulo anything.

### 3.3 Finset distinctness and intersections

The construction must distinguish:

1. two projective point integers;
2. two private integers on one circuit;
3. private integers on different circuits;
4. a private integer and a projective point integer;
5. the two shores of one relation.

Equality cannot be excluded merely by naming formal labels: after padding,
unique factorisation of the actual odd supports or another injective invariant
must rule it out.  The same check must show that two line supports have no
accidental second intersection beyond their projective point.

### 3.4 Equal products, defect, and support minimality

For every line, the two shores must have exactly equal integer products and
cardinality difference exactly `-1` in one consistent normalization.  Because
`q` is an odd prime, `q+1` is even; simply signing the projective points alone
cannot have odd defect `-1`.  Some private structure is therefore necessary.

Support minimality requires more than equality of the displayed full
products.  The clean sufficient certificate would be a connected
prime-occurrence graph with a private prime (or independently separating
valuation) on each propagation edge.  If the proof instead combines several
locally equal gadgets, it must exclude a proper gadget as an equal-product
subrelation.  Adding a standalone defect gadget would fail this test.

### 3.5 Cluster theorem actually refuted

Once AL and (B2.2) hold, any deterministic theorem of the exact form

\[
 \tau(\mathcal F)\le h(N)\nu(\mathcal F),
 \qquad h(N)=o(\log N),                              \tag{B3.1}
\]

for every realized equal-defect arithmetic cluster is contradicted, since
`nu=1` and `tau=q+1>K`.  The same example does not refute a charge involving
fractional cluster mass, occurrence probability, or external circuits.

A randomized statement requires a separate quantifier check.  If a random
owner set `R` must cover **every** circuit with probability one, then every
outcome in its support is a transversal and
`E|R|>=tau=q+1`.  If it covers each fixed circuit only with high marginal
probability, or all circuits only with probability below one, the deterministic
transversal lower bound does not automatically apply.  Any claimed randomized
corollary must state which event is almost sure and cannot exchange
`for every circuit` with `with high probability`.

## 4. Independent reconstruction of MC.1

Let `P,Q` be disjoint finite sets with `|P|!=|Q|`, products

\[
 X=\prod_{a\in P}a,
 \qquad Y=\prod_{b\in Q}b,
 \qquad X\ne Y.
\]

Suppose an admissible infinite set `S` contains `P union Q`.  For every
sufficiently large integer `t`, the two new integers `tX,tY` are distinct,
lie outside the fixed set `P union Q`, and the shores

\[
 P\cup\{tY\},
 \qquad Q\cup\{tX\}                                 \tag{B4.1}
\]

are disjoint.  Their products are both `tXY`, and their cardinality
difference remains `|P|-|Q|!=0`.  Therefore admissibility forces at least one
of `tX,tY` to be absent from `S` for every `t>=t_0`.

Let `D` be the complement of `S` and put `M=max(X,Y)`.  For
`t_0<=t<=T/M`, both elements of the forced pair lie in `[T]`.  A fixed integer
can occur as `tX` for at most one `t` and as `sY` for at most one `s`, so one
deleted integer covers at most two such pairs.  Hence

\[
 |D\cap[T]|\ge\frac12\left(\left\lfloor\frac TM\right\rfloor-t_0+1\right).
                                                               \tag{B4.2}
\]

It follows that

\[
 \liminf_{T\to\infty}\frac{|D\cap[T]|}{T}
 \ge\frac1{2\max(X,Y)}.                              \tag{B4.3}
\]

Thus the statement is actually stronger than a claim conditional on the
existence of a natural deletion density.  Boundary cases to check in the
author proof are empty `P` or `Q` (empty products equal one), possible
appearance of 1, cancellation if `tX` or `tY` belongs to the fixed seed, and
the necessity of `X!=Y`.  All are harmless once `S` really contains the
disjoint seed and `t` is chosen beyond the finite collision set.

MC.1 only kills a guard-only coherence rule that permanently admits such a
seed without charged revision.  It does not rule out revising old seed
elements, assigning the positive density cost to a predeclared reserve, or
otherwise paying for the completion family.

## 5. Blind status

The projective-plane values `nu=1`, `tau=q+1`, the implication
`q+1>K`, and MC.1 are independently reconstructed.  GC.1 remains conditional
at the blind stage on the exact arithmetic lift AL(q,K).  The post-blind audit
must either verify every item in Section 3 from the author proof or fail the
candidate; finite incidence or padding experiments alone cannot establish the
universal lift.
