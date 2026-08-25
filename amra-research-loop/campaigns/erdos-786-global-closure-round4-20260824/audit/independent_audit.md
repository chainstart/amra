# Independent audit of GC.1 and supporting MC.1/CR.1

## Verdict

**PASS.**  GC.1 is an all-sufficiently-large-parameter arithmetic realization
of the projective-plane line hypergraph with

\[
 \nu(\mathcal F_K)=1,
 \qquad \tau(\mathcal F_K)=q+1>K=\log_2N.
\]

The construction respects the distinct-Finset variant, all line circuits are
support-minimal and have consistently normalized defect `-1`, every pair of
supports meets in exactly one integer, and every term lies strictly in
`(N/32,N]`.  MC.1 also passes with its stated all-sufficiently-large-multiplier
quantifier and density bound.

The promotion recommendation is **standalone_decisive_lemma only**.  GC.1
refutes the packing-local cluster theorem and the precisely scoped mechanisms
listed below.  It gives no positive-density lower bound for `tau(H_N)`, no
finite `o(N)` transversal, and no coherent natural-density construction.
Therefore `global_interface_closed`, `main_term_improved`,
`main_exponent_improved`, and `original_problem_closed` are all rejected.

## Blind protocol

Before reading any author evidence or verifier, I reconstructed the
projective-plane packing/transversal calculation, isolated the arithmetic
lift, proved MC.1 independently, and froze
`audit/blind_reconstruction.md`.  Its SHA-256 remains

```text
3983d10db6203074c58fbbe592801657c41f34ac01f19869512a24bbc298f195
```

This hash covers exactly the frozen GC.1 statement and the then-current MC.1
supporting statement.  CR.1 was added to `decisive_lemma.json` only after the
blind file had been written and hashed.  I therefore audit CR.1 below by the
ordinary statement/dependency/scope protocol; it is neither represented as a
blind reconstruction nor used as the basis of this promotion recommendation.

The blind reconstruction explicitly identified the apparent `q>K` prime
budget obstruction, the strict-band decrement threshold, Finset collision
checks, support minimality, and randomized coverage quantifiers.  The author
proof supplies a valid construction for every one of these interfaces.

## 1. Prime budget and the projective-plane arithmetic lift

Put `m=q+1`, where Bertrand gives a prime `K<q<2K`, and use `PG(2,q)`.
For each projective point `x`, the author takes

\[
 r=\lceil\log_2(m+1)\rceil+1
\]

point-private odd primes.  The number of unordered nontrivial bipartitions of
an `r`-set is

\[
 \frac{2^r-2}{2}=2^{r-1}-1\ge m,
\]

so the `m` incident lines receive distinct partitions
`Q_x=Q_(x,L)^- dot-union Q_(x,L)^+` with both halves nonempty.

This is exactly how the proof evades the no-go recorded in the blind audit.
It does not multiply one new prime per incidence into the shared point.
Instead only `r=O(log q)` primes enter the common point product, and incident
lines reuse that block through distinct halves.

There are

\[
 (q^2+q+1)r=O(K^2\log K)
\]

required odd primes.  The standard bound `pi(X)>>X/log X` supplies all of them
below `K^6`.  Therefore a complete point block, or the union of subsets from
two point blocks, has binary logarithm

\[
 O(r\log K)=O((\log K)^2)=o(K).
\]

This simultaneously proves the global prime supply and the per-integer
exponent budget; the two issues are not conflated.

## 2. Exact line circuits, equality, defect, and minimality

On a line `L={x_1,...,x_m}`, the consecutive path-edge labels are

\[
 A_{x_1,L},B_{x_1,L},\ldots,A_{x_m,L},B_{x_m,L}.
\]

The `m` odd path vertices have raw values
`A_(x_i,L)B_(x_i,L)=a_(x_i)`, independent of the incident line.  The `m+1`
even values are the two endpoint halves and the adjacent products
`B_(x_i,L)A_(x_(i+1),L)`.  Every edge label occurs once on each shore, so the
raw products agree exactly.

Orienting odd vertices positively and even vertices negatively gives

\[
 \delta_L=m-(m+1)=-1.
\]

This also fixes the sign of every shared point consistently across all
incident lines.

For support minimality, choose any prime in each nonempty edge label.  Point
blocks are disjoint and the two halves at one point are disjoint, so that
prime appears in exactly the two path endpoints of its edge and nowhere else
on the line.  For any signed kernel vector, its valuation equation forces the
two endpoint coefficients to be negatives.  Path connectedness then forces
the zero vector or the full alternating vector (up to global sign).  Thus no
proper subset admits any equal-product signing, not merely no subrelation in
the displayed orientation.  Adding powers of two does not affect this odd
prime certificate.

## 3. Padding and the strict `(N/32,N]` boundary

For a shared point, with `c_x=ceil(log_2 a_x)`, the fixed value

\[
 u_x=2^{K-c_x-2}a_x
\]

satisfies

\[
 N/8<u_x\le N/4.
\]

The exponent is nonnegative for all sufficiently large `K` because
`c_x=o(K)`.

For the `m+1` even raw values `b_j`, let
`d_j=ceil(log_2 b_j)` and

\[
 C_L=\sum_{j=0}^{m}d_j-\sum_{i=1}^{m}c_{x_i}.
\]

Raw product equality implies that `C_L` is the difference of `m+1` even
ceiling errors and `m` odd ceiling errors, hence

\[
 -m<C_L<m+1.                                         \tag{A3.1}
\]

Before decrementing the even exponents, their excess over the already fixed
odd exponents is exactly

\[
 \Delta_L=K-C_L+2m.                                 \tag{A3.2}
\]

It is positive.  Since `m=q+1>K`, (A3.1) gives the strict integer bound

\[
 0<\Delta_L<K+3m<4(m+1).
\]

Distributing `Delta_L` over `m+1` even vertices therefore uses decrement at
most four, not five.  Every initial exponent is `K-o(K)`, so all decrements
are legal.  An undecremented even value lies strictly in `(N/2,N]`; after at
most four decrements it lies strictly in `(N/32,N]`.  Equation (A3.2) makes
the total 2-adic exponents equal, proving exact integer-product equality.

Thus the potentially incompatible conditions `q>K`, `N=2^K`, available
primes, nonnegative padding, and the strict factor-32 band are compatible.

## 4. Finset distinctness and exact pairwise intersections

Actual odd-prime supports distinguish every category.

- A shared point uses its complete block `Q_x`.
- A private endpoint uses a proper nonempty half of one block.
- An internal private vertex uses nonempty proper halves from two distinct
  consecutive point blocks.

Inside one line, the participating block sets distinguish different path
positions.  Across two lines, equality of private odd supports would require
the same participating point blocks.  Distinct projective lines share only
one block.  At that shared block, distinct unordered bipartitions imply that
no half from one incident line equals either half from another: equality of a
half or its complement would make the unordered partitions identical.

Consequently private supports on different lines never coincide with one
another or with a complete point block.  Powers of two cannot turn different
odd supports into equal integers.  Two line circuits therefore meet exactly
in the common padded point belonging to their unique projective intersection.
All shores are genuine Finsets and are disjoint.

## 5. Exact `nu` and `tau`

Pairwise one-point intersection makes the event-intersection graph complete
and gives `nu(F_K)=1`.

The `q+1` point integers on any fixed projective line meet every circuit, so
`tau<=q+1`.  For the reverse inequality, suppose a repair set of size at most
`q` contains `s` shared points.  Those hit at most `s(q+1)` circuits, while
the remaining at most `q-s` private integers hit at most one each.  Hence it
hits at most

\[
 s(q+1)+(q-s)=q(s+1)\le q^2+q<q^2+q+1
\]

of the line circuits.  Some line remains, so `tau=q+1`.  This count covers
mixed point/private repair sets and proves the exact value, not merely the
point-blocking number.

Since `q>K=log_2 N`, GC.1 refutes every packing-local cluster bound
`tau(F)<=h(N)nu(F)` with `h=o(log N)`.  It is strictly stronger than the old
common-witness star or private-satellite tests, but remains a sparse-cluster
obstruction.

## 6. Equal defects, subtraction, and randomized owners

Every shared point has coefficient `+1` and every line has defect `-1`.
Subtracting two line vectors cancels their unique common point and produces
defect zero.  It does not produce a petal-only bad relation.  Thus defect
stratification or equal-defect subtraction alone cannot collapse the host.

The randomized corollary is valid with the exact coverage quantifier.  If a
realized randomized owner set contains an owner from every circuit, then
every outcome is a transversal and has at least `q+1` distinct vertices.
Therefore its expectation is also at least `q+1>K`, contradicting an
`O(log log N)` bound at packing number one.  If an interpretation of
`M786G-07` bounded only a pre-alteration set that may leave circuits uncovered
and allowed uncharged later repairs, it would not imply the claimed coverage
or close the rounding problem; GC.1 makes no claim against such a nonclosing
variant.

## 7. Supporting result MC.1

The blind proof of MC.1 matches the author proof.  For disjoint finite seeds
`P,Q` with unequal sizes and products `X!=Y`, sufficiently large `t` removes
all fixed-set collisions and gives the bad relation

\[
 P\cup\{tY\}\quad\text{versus}\quad Q\cup\{tX\}.
\]

If an admissible set contains the seed, its deletion set meets every pair
`{tX,tY}`.  A deleted integer is an `X`-endpoint for at most one multiplier
and a `Y`-endpoint for at most one, so it covers at most two pairs.  With
`M=max(X,Y)`, this gives

\[
 |D\cap[1,MT]|\ge T/2-O_{P,Q}(1)
\]

and hence natural deletion density at least `1/(2M)` when the limit exists.
In fact, taking `floor(U/M)` gives the same lower bound for the lower density;
the author's weaker upper-density statement without a limit is safe.

The author states `P,Q` nonempty, whereas the summary in
`decisive_lemma.json` says finite.  This is not a mathematical gap: if exactly
one seed is empty, the same collision and endpoint-count proof applies with
the empty product equal to one; both cannot be empty because their sizes are
unequal.  If a seed contains the forbidden integer 1, the antecedent that an
admissible set contains it is vacuous.

MC.1 kills guard-only permanent-prefix coherence.  It does not kill charged
old-seed revision, and its lower bound is not uniform over all seeds.

## 8. Post-blind supporting result CR.1

CR.1 was added after the blind reconstruction was frozen, so this is an
ordinary dependency and scope check.  The conditional theorem is correct.
Let

\[
 X_k=\{2,\ldots,2^k\},\quad
 C_k=(T_{k+1}\mathbin\triangle T_k)\cap X_k,
\]

and assume `|T_k|/2^k -> 0` together with
`|C_k cap X_j| <= rho_k 2^j` for all `j<=k`, where
`sum rho_k<infinity`.  For

\[
 S=\bigcup_k T_k\cap(X_k\setminus X_{k-1}),\qquad
 R=\bigcup_k C_k,
\]

every `T_m` is contained in `S union R`: an integer is either selected at its
first dyadic entry, or its first absent-to-present transition is one of the
recorded changes.  Hence `D=B union S union R` meets every finite bad support,
using the residual transversal when that support misses `B`.

The two density estimates have the stated quantifiers.  At dyadic endpoints,

\[
 {|S\cap X_m|\over2^m}\leq\sum_{k\leq m}a_k2^{k-m}=o(1),
\]

while applying the prefix bound with `j=k` for `k<m` and with `j=m` for
`k>=m` gives

\[
 {|R\cap X_m|\over2^m}
 \leq\sum_{k<m}\rho_k2^{k-m}+\sum_{k\geq m}\rho_k=o(1).
\]

The first terms in these displays are geometric convolutions and the second
recourse term is an `ell^1` tail.  The usual factor-two comparison between an
arbitrary cutoff and the next dyadic endpoint promotes this to full natural
density zero for `S union R`.  Thus `D triangle B` has density zero, `d(D)=beta`,
and its complement is admissible of density `1-beta`.

The endpoint-only counterexample is also exact:
`C_k={2,...,2^floor(k/2)}` has
`|C_k|<=2^{-ceil(k/2)}2^k` and the displayed rates sum to `2`, yet every fixed
integer at least two is toggled infinitely often and `union C_k` has density
one.  It only refutes the endpoint-only inference; it is not claimed to be a
sequence of arithmetic transversals.

CR.1 remains purely conditional.  The explicit periodic baseline
`B_Q={1} union Q N` has density `1/Q`, but no residual transversals satisfying
the prefix-Carleson premise are constructed.  Therefore CR.1 neither proves
`tau(H_N)=o(N)` nor the infinite density statement.  M786G-13 is a genuine
successor target, not a proved consequence.  This post-blind check supports
the dependency ledger only; promotion below continues to rest solely on
GC.1.

## 9. Dependencies, reproduction, and priority

The universal proof uses only standard all-parameter inputs: Bertrand's
postulate, the finite-field construction of `PG(2,q)` for prime `q`, the
elementary prime-counting lower bound, unique factorisation, and the
projective-plane incidence axioms.  No unproved arithmetic or probabilistic
dependency remains.

Replayed successfully:

```text
python3 evidence/verify_round4_cluster_alteration.py
python3 evidence/verify_round4_multiplier_completion.py
python3 evidence/verify_round4_full_residue_owner_flow.py
python3 evidence/verify_round4_global_potential_kills.py
python3 evidence/verify_round4_coherent_recourse.py
```

The first verifier returned exact projective-plane values
`(q,nu,tau)=(2,1,3),(3,1,4),(5,1,6)`.  The multiplier verifier checked exact
products and endpoint multiplicity at three seeds.  The other two package
guards also passed at their stated finite scopes.  These computations do not
establish the asymptotic theorem; the symbolic proof above does.

Relevant hashes at audit time:

```text
cba3ad261010d1a4cafbf22eb064bf6cd0edc609ebc46e9747e50108a4c32c65  evidence/ROUND4_CLUSTER_ALTERATION.md
4ff19f5c30ad0ef4907420b46e66b246146c3a67c8ce4db513186b9db2d206e5  evidence/verify_round4_cluster_alteration.py
dc384b8e7c42f77438eaf683337bcb285633ffec94cbc62247331ff34ce87a42  evidence/ROUND4_MULTIPLIER_COMPLETION_OBSTRUCTION.md
6b8668abaed4d943fe2984a1f7f743fa6e7479786b47cb323bca19ae06e891e2  evidence/verify_round4_multiplier_completion.py
59409960398586a22d84c7020c7dc3ddb61264d753a29f564bcaa343f435d1c8  evidence/ROUND4_COHERENT_RECOURSE.md
78675a65e0d64831f44eb0cc1aed64e98fd76fe7aa66ce32100cdae53c28074c  evidence/verify_round4_coherent_recourse.py
```

No public search for an exact Erdős 786 solution or benchmark was performed.
The construction is independently proved, but publication priority is
therefore `priority_uncertain`.

## 10. Promotion scope

Recommend promotion under exactly:

```text
standalone_decisive_lemma
```

The promoted statement should be GC.1.  MC.1 is a supporting exact completion
obstruction, and CR.1 is a post-blind conditional bridge; neither is part of
the promotion basis.  The following remain open and must be stated in any
promotion record:

- probability- or fractional-mass-weighted external cluster charging;
- a noncircular divisor-current energy on the full cluster quotient;
- the M786G-13 prefix-Carleson recourse premise for the periodic baseline;
- `tau(H_N)=o(N)`;
- the coherent infinite admissible set with actual natural density;
- the original distinct-Finset Erdős 786 problem.

This audit does not independently certify the priority or every auxiliary
owner/potential no-go in the decisive lemma's evidence list.  The standalone
recommendation rests only on GC.1, reconstructed here.  MC.1 and CR.1 have
passed their explicitly limited supporting-scope checks.
