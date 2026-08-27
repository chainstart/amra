# Blind independent reconstruction: stretched-exponential equal-defect clusters

## Blind protocol and exact scope

This reconstruction was frozen before opening any author evidence in this
campaign.  At this stage I read only `campaign_state.json`,
`closure_contract.json`, and the read-only predecessor campaign
`erdos-786-global-closure-round4-20260824`.  In particular I did not inspect
this campaign's `evidence/`, `decisive_lemma.json`, `information_loss_map.json`,
`representations.json`, `mechanisms.json`, `kill_tests.json`, `survivors.json`,
`audit.json`, or `decision.json`.

Write (H_N) for the hypergraph in the closure contract.  The theorem to be
reconstructed is the following scoped assertion: for every sufficiently
large integer (N), there is a connected family \(\mathcal F_N\) of
support-minimal distinct-Finset equal-product relations of unequal
cardinalities such that

1. every integer in every support lies in the fixed band \((N/64,N]\);
2. every two distinct supports intersect in exactly one integer;
3. all relations have the same normalized defect;
4. \(\nu(\mathcal F_N)=1\); and
5. \(\tau(\mathcal F_N)\ge
   2^{\sqrt{\log_2 N}/200}\).

This would be a standalone decisive lemma only.  It is a lower bound for the
transversal number of a sparse subfamily of (H_N), not an upper bound
\(\tau(H_N)=o(N)\), and it supplies no coherent infinite density-one
construction.

## 1. Parameters, projective plane, and prime supply

Fix a sufficiently large integer (N), and put

\[
 K=\lfloor\log_2 N\rfloor,\qquad M=2^K,
 \qquad s={\sqrt K\over100},\qquad R=\lceil2^s\rceil.
\]

Bertrand's postulate supplies a prime (q) with

\[
 R<q<2R.                                                     \tag{1.1}
\]

For large (K), (q>K).  Let (P,L) be the points and lines of the
projective plane of order (q).  Put

\[
 v=q^2+q+1,\qquad m=q+1.
\]

There are (v) points and (v) lines, every line contains (m) points,
every point lies on (m) lines, and two distinct lines meet in exactly one
point.

For each point (x), choose a point-private block (Q_x) of

\[
 r=\lceil\log_2(m+1)\rceil+1
   =\lceil\log_2(q+2)\rceil+1                            \tag{1.2}
\]

distinct odd primes.  All (Q_x) are pairwise disjoint.  The required number
of primes is (vr=O(q^2\log q)).  The standard elementary prime-counting
lower bound \(\pi(X)\ge cX/\log X\), for an absolute (c>0) and all large
(X), gives

\[
 \pi(q^3)-1>vr                                                \tag{1.3}
\]

for all sufficiently large (q).  Thus every selected prime may be taken at
most (q^3).  This proves actual prime supply rather than merely counting
formal labels.

The number of unordered nontrivial bipartitions of an (r)-element block is

\[
 {2^r-2\over2}=2^{r-1}-1\ge m.                              \tag{1.4}
\]

Assign a different such bipartition

\[
 Q_x=Q^-_{x,\ell}\mathbin{\dot\cup}Q^+_{x,\ell}
\]

to every line \(\ell\) through (x), and define

\[
 A_{x,\ell}=\prod_{p\in Q^-_{x,\ell}}p,
 \qquad B_{x,\ell}=\prod_{p\in Q^+_{x,\ell}}p,
 \qquad a_x=A_{x,\ell}B_{x,\ell}=\prod_{p\in Q_x}p.        \tag{1.5}
\]

Both halves are nonempty.  The integer (a_x) is independent of the line
through (x).

The bit budget is uniform.  If (t=\log_2q), a raw integer below uses at most
two point blocks and hence has binary logarithm at most (6rt).  From (1.1),
for large (K),

\[
 t<s+2,\qquad r\le t+3<s+5,
\]

and therefore

\[
 6rt<6(s+5)(s+2)
     ={6\over10^4}K+O(\sqrt K)=o(K).                       \tag{1.6}
\]

In particular every raw logarithmic ceiling used below is at most (K-5)
once (K) is sufficiently large.  This checks both the global supply of
distinct primes and the per-integer exponent budget.

## 2. A support-minimal equal-defect path on each line

Fix a projective line \(\ell=\{x_1,\ldots,x_m\}\), in any order.  Form a
path with consecutive edge labels

\[
 A_{x_1,\ell},B_{x_1,\ell},A_{x_2,\ell},B_{x_2,\ell},
 \ldots,A_{x_m,\ell},B_{x_m,\ell}.                         \tag{2.1}
\]

The (m) vertices in one parity class have raw labels (a_{x_i}).  The
(m+1) vertices in the other parity class have raw labels

\[
 b_0=A_{x_1,\ell},\quad
 b_i=B_{x_i,\ell}A_{x_{i+1},\ell}\ (1\le i<m),\quad
 b_m=B_{x_m,\ell}.                                         \tag{2.2}
\]

Every path-edge label occurs once in the product of each parity class, so

\[
 \prod_{i=1}^m a_{x_i}=\prod_{j=0}^m b_j.                 \tag{2.3}
\]

Orient the (m) point vertices positively and the (m+1) private vertices
negatively.  The normalized cardinality defect is exactly

\[
 \delta_\ell=m-(m+1)=-1,                                  \tag{2.4}
\]

the same for every line and with the same positive sign at every shared
point.

This relation is support-minimal.  Each nonempty edge label in (2.1) contains
a prime appearing in exactly the two endpoints of that path edge and nowhere
else on the line.  If a signed valuation-kernel vector is supported on any
subset of the path vertices, the valuation at this prime forces the two
endpoint coefficients to be opposites.  Connectivity propagates this along
the path, so the vector is zero or is the full alternating path vector up to
sign.  Hence no proper support carries any equal-product subrelation.  The
argument works for all integer coefficients and therefore in particular for
the required coefficients in \(\{-1,0,1\}\).

## 3. Exact power-of-two padding and the strict band

Let

\[
 c_x=\lceil\log_2 a_x\rceil,
 \qquad u_x=2^{K-c_x-2}a_x.                                \tag{3.1}
\]

By (1.6) the exponent is nonnegative for large (K).  Since (a_x) is an
odd integer greater than one, it is not a power of two, and consequently

\[
 M/8<u_x<M/4.                                              \tag{3.2}
\]

Use this same padded point integer on all lines through (x).

For the private raw values in (2.2), put

\[
 d_j=\lceil\log_2 b_j\rceil,
 \qquad C_\ell=\sum_{j=0}^m d_j-\sum_{i=1}^m c_{x_i}.      \tag{3.3}
\]

Equation (2.3) cancels the exact logarithms.  There are (m+1) ceiling
errors on the private side and (m) on the point side, all strictly between
zero and one because all raw values are odd and greater than one.  Thus

\[
 -m<C_\ell<m+1.                                            \tag{3.4}
\]

Initially pad every private vertex to (2^{K-d_j}b_j\), which lies strictly
in \((M/2,M)\).  Relative to the already fixed point exponents in (3.1), the
excess total power of two on the private side is

\[
 \Delta_\ell
  =\sum_{j=0}^m(K-d_j)-\sum_{i=1}^m(K-c_{x_i}-2)
  =K-C_\ell+2m.                                           \tag{3.5}
\]

This is a positive integer.  Because (m=q+1>K), (3.4) gives

\[
 0<\Delta_\ell<K+3m<4(m+1).                              \tag{3.6}
\]

Distribute exactly \(\Delta_\ell\) decrements as evenly as possible among
the (m+1) private powers of two.  No vertex receives more than four
decrements.  By (1.6), each final exponent remains nonnegative, and every
private value lies strictly in

\[
 (M/(2\cdot2^4),M)=(M/32,M).                              \tag{3.7}
\]

Equation (3.5) makes the final total 2-adic exponents equal.  Together with
(2.3), this proves exact integer-product equality; it is not merely a
congruence or approximate balance.  Equations (3.2) and (3.7) put every
vertex in \((M/32,M]\).

Adding powers of two does not change the odd-prime propagation certificate,
so support minimality survives padding.

## 4. Finset distinctness and exact intersections

Unique factorization of the odd parts separates all actual integers.

* A point integer (u_x) uses the complete block (Q_x).
* A private endpoint uses a nonempty proper half of one block.
* A private internal vertex uses nonempty proper halves of two distinct
  consecutive point blocks.

Within one line, the participating point block or ordered adjacent pair of
blocks distinguishes the path positions.  A complete block cannot equal a
proper half or a union of halves from two different blocks.

Across two distinct lines, there is only one common point block.  Private
vertices using two blocks therefore cannot have the same odd support across
the two lines.  Private endpoints could involve the common block on both
lines, but their halves are distinct: equality of either half with either
half from the other line would make the two unordered bipartitions identical,
contrary to their assignment.  A private endpoint and a private internal
vertex involve different numbers of point blocks.  Thus private integers on
different lines neither coincide with each other nor with a point integer.

Powers of two cannot make integers with different odd supports equal.
Consequently every line relation has two disjoint Finset shores, all its
support elements are distinct, and two distinct line supports intersect in
exactly the padded point integer corresponding to their unique projective
intersection.

## 5. Connectedness, matching number, and exact transversal number

Let \(\mathcal F_M\) be the family of all (v=q^2+q+1) padded line
supports.  Every two supports intersect in exactly one integer, so their
intersection graph is complete.  In particular the family is connected and

\[
 \nu(\mathcal F_M)=1.                                      \tag{5.1}
\]

Every shared point integer lies on exactly (q+1) supports; every private
integer lies on exactly one.  Hence any set of at most (q) integers meets at
most

\[
 q(q+1)=q^2+q<q^2+q+1                                    \tag{5.2}
\]

supports, even if it mixes shared and private vertices.  It misses at least
one line support, so \(\tau(\mathcal F_M)\ge q+1\).  Conversely the (q+1)
point integers on any fixed projective line meet every line support, because
any two projective lines intersect.  Therefore

\[
 \tau(\mathcal F_M)=q+1.                                  \tag{5.3}
\]

This is the transversal number among all ambient integers: vertices outside
the union hit no support and can simply be discarded.

## 6. Arbitrary-\(N\) reduction and the stated constant

Use the family just constructed at (M=2^K\) as \(\mathcal F_N\).  Since

\[
 M\le N<2M,
\]

all its vertices are at most (N), and

\[
 n>M/32>N/64.                                             \tag{6.1}
\]

Thus the required fixed top band is valid for every sufficiently large
integer (N), not just powers of two.

Let (L=\log_2N\), so (K\le L<K+1\).  For (K\ge1),

\[
 {\sqrt K\over100}\ge{\sqrt L\over200},                   \tag{6.2}
\]

because (4K\ge L\).  From (1.1) and (5.3),

\[
 \tau(\mathcal F_N)=q+1
 >2^{\sqrt K/100}
 \ge2^{\sqrt{\log_2N}/200}.                              \tag{6.3}
\]

All parameter restrictions used above (prime supply, (q>K), and the
nonnegative exponent budget) hold simultaneously beyond one absolute
threshold (K_0), hence beyond (N_0=2^{K_0}).  No finite computation is
used to infer these universal quantifiers.

## 7. Blind verdict and dependency boundary

The frozen all-(N) scoped theorem is independently reconstructed with a
stronger exact value

\[
 \tau(\mathcal F_N)=q+1>2^{\sqrt K/100}.
\]

The proof checks prime supply, individual bit budget, exact 2-adic padding,
strict band endpoints, Finset distinctness, support minimality, exact
pairwise intersections, matching number, mixed-vertex transversals, and the
arbitrary-(N) reduction.  Its only nontrivial external mathematical inputs
are the standard projective-plane construction over the prime field,
Bertrand's postulate, and a standard elementary lower bound for the
prime-counting function.  The predecessor supplies the already audited path
arithmetic template, but every quantitative choice needed for the
stretched-exponential regime is checked above.

At the blind stage the mathematical verdict is **PASS**, conditional only on
the closure contract being the exact author statement.  The required second
stage must now compare the author evidence for statement identity,
dependencies, and any hidden strengthening or loss.  No literature priority
search has been performed, so novelty must remain `priority_uncertain`.

---

## 8. Post-blind comparison with the author package

Only after the preceding reconstruction had been saved and hashed did I open
the new campaign's author artifacts.  The frozen blind SHA-256 was

```text
88d1f1279fbb95e6ffbc5da5c619432a0b0b8d2c92df24c44ca1b74eee0a6ef6
```

That hash is recorded here as the pre-comparison boundary; this appended
section necessarily changes the current file hash.

### 8.1 Statement match: PASS

`decisive_lemma.json` and `evidence/STRETCHED_CLUSTER_THEOREM.md` prove SC.1
for every sufficiently large integer $N$, not merely powers of two.  The
author statement matches every mathematical clause in `closure_contract.json`:

* the distinct-Finset version of $H_N$;
* a connected family of support-minimal bad relations;
* the common band \((N/64,N]\);
* exactly one integer in every pairwise support intersection;
* normalized defect (-1) on every line;
* matching number one; and
* transversal number strictly greater than
  (2^{\sqrt{\log_2N}/200}), which is stronger than the contract's weak
  lower-bound wording.

The proof also makes connectedness automatic because the support-intersection
graph is complete.  It does not claim either original Erdős 786 target.

### 8.2 Construction comparison and constant check: PASS

The author and blind constructions use the same mathematical architecture,
with two harmless quantitative differences.

1. The author chooses
   (Q=2^{\lfloor\sqrt K/100\rfloor}) and a prime (Q<q<2Q), whereas the
   blind proof uses (R=\lceil2^{\sqrt K/100}\rceil).  The author's lost
   floor is recovered by the deliberately weaker (1/200) target: for all
   sufficiently large $K$,
   \[
   \left\lfloor{\sqrt K\over100}\right\rfloor
     >{\sqrt{\log_2N}\over200}.
   \]
2. The author places the required (O(q^2\log q)) odd primes below (q^6),
   while the blind reconstruction observes that (q^3) already suffices
   asymptotically.  The weaker (q^6) cutoff is still valid.  It gives at
   most (6r\log_2q) bits for a point block and at most
   (12r\log_2q) bits for a two-block private vertex.  With
   \(\log_2q<\sqrt K/100+1\) and (r\le\log_2q+3), this is less than
   $K/4$ for every sufficiently large $K$, leaving more than enough room
   for the four padding decrements.

The ceiling discrepancy, exact power-of-two balance, and strict band are all
correct.  In the author's notation,

\[
-m<C_L<m+1,
\qquad
\Delta_L=K-C_L+2m,
\qquad
0<\Delta_L<K+3m<4(m+1).
\]

Thus an even distribution uses at most four decrements and keeps each private
integer strictly above (2^K/32).  The common point integers lie strictly
above (2^K/8).  Embedding (2^K\le N<2^{K+1}) changes the lower band by
only a factor two, giving the required strict (N/64) endpoint.

The global odd-prime-support argument rules out every collision category:
point/point, point/private, same-line private/private, and cross-line
private/private.  Distinct unordered partitions at the unique common point
exclude both direct and complementary half collisions.  Private primes on
each path edge propagate valuation coefficients along the connected path,
so zero and the full alternating vector are the only kernel possibilities.
This proves support minimality rather than merely equality of the displayed
products.

The exact hitting calculation also permits mixed shared/private transversals.
At most (q) chosen vertices hit at most (q(q+1)<q^2+q+1) lines, while the
(q+1) shared points on a fixed line hit every line.  Therefore the author's
\(\nu=1\) and \(\tau=q+1\) claims are exact.

### 8.3 Dependency check: PASS

The proof has no unproved campaign-local bridge.  Its external mathematical
inputs are exactly:

* Bertrand's postulate;
* the standard projective plane over the prime field of order (q); and
* the prime number theorem in the weak form
  \(\pi(q^6)\gg q^6/\log q\).

Each is used with its correct hypotheses.  The predecessor supplies the
read-only path-gadget template, but the new author proof restates and checks
the raw product identity, valuation propagation, padding, and intersection
arguments, so there is no hidden dependency on an unaudited predecessor
claim.  The all-$N$ assertion is derived symbolically and does not depend on
the finite replay.

I reran

```text
python3 amra-research-loop/campaigns/erdos-786-stretched-cluster-20260826/evidence/verify_stretched_cluster.py
```

and it returned `status: PASS`.  Its reported source SHA-256,
`9a664db9f7500522688754ffffdbfcdad319cd3d35bc14f64a3eea61c8681773`,
matches the verifier file.  This is correctly classified as a bounded guard
for small projective planes, partition counts, and sample integer inequalities;
it is not used to infer the universal theorem.

### 8.4 Promotion-decision check: FAIL as currently encoded

The mathematical theorem passes, but `decisive_lemma.json` currently lists
both

```text
main_exponent_improved
standalone_decisive_lemma
```

under `closes`.  This conflicts with the frozen closure contract, which says
that promotion of this scoped theorem counts **only** as
`standalone_decisive_lemma` unless an original target is also closed.  SC.1
does not prove \(\tau(H_N)=o(N)\) and does not provide a coherent infinite
density-one construction.  Quantitatively improving the predecessor's sparse
cluster lower bound therefore does not satisfy the campaign's
`main_exponent_improved` promotion condition.

The permitted recommendation is exactly:

```text
standalone_decisive_lemma
```

This is a metadata/promotion-scope failure, not a defect in SC.1's proof.
Because the independent-audit phase gate includes the promotion-decision
check, the package should not advance with the current `closes` array.

### 8.5 Novelty and final verdict

No primary-literature search was performed: the task was local-only, and the
campaign contract permits only a post-reconstruction priority check.  The
novelty status is therefore:

```text
priority_uncertain
```

Final classifications:

```text
mathematical_status: proved
independent_reconstruction: passed
statement_match: passed
dependency_check: passed
novelty_check: priority_uncertain
promotion_decision_check: failed_as_encoded
publication_state: private_campaign_note
```

**Final audit verdict: FAIL for advancement as currently encoded.**  The
SC.1 theorem itself is **PASS** and supports promotion as a
`standalone_decisive_lemma` only.  Removing the unsupported
`main_exponent_improved` classification is the sole identified blocker in the
reviewed package.
