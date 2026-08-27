# Independent audit of RR.1--RR.3

## Verdict

**PASS at scoped standalone-decisive-lemma level.**

RR.1 and RR.2 are valid all-parameter support-minimal counterfamilies for
the frozen local mechanisms. RR.3 is a valid supporting full-occurrence
graph theorem. None of these results bounds the full transversal number,
rounds the promoted fractional cover, or constructs the required coherent
infinite density-one set.

## Blind protocol

The audit first read only the closure contract and decisive statement.
The independent reconstruction was then written and hashed:

\[
\texttt{42fdb0992bdc06127731842d44d98a2f77eae462f61e87be491201e3a4aed9f7}.
\]

Only after this hash was fixed were the author evidence and verifier opened.
The author's arguments agree with the blind reconstruction.

## RR.1 checks

For fixed \(L\geq3\) and \(s\geq L\), repeated Bertrand intervals give
increasing primes

\[
N^{1/L}<p_1<\cdots<p_{2s}<2^{2s+1}N^{1/L}.
\]

The path vertex-products have equal shore products. With
\(c_i=\lceil\log_2q_i\rceil\), the ceiling difference satisfies
\(-s<C<s+1\), so the two-adic imbalance is \(\Delta=K-C>0\).
Evenly distributing \(\Delta\) on the \(s+1\)-vertex shore costs at most
\(K/(s+1)+2\) at each vertex.

Both necessary strict inequalities hold:

\[
1-\frac2L-\frac1{s+1}>0
\]

gives nonnegative final exponents, and

\[
\frac1{s+1}<\frac1L
\]

places every term strictly above \(N^{1-1/L}\) for sufficiently large
\(K\). The powers of two add no active prime. Every \(p_i\) occurs
squarefreely and active degree is at most two.

For an arbitrary signed subrelation, the \(p_i\)-valuation equations are
\(z_{i-1}+z_i=0\). They force zero or the full alternating path, proving
support-minimality in the locked Finset variant. Active-prime supports also
prove distinctness. Increasing labels make descending-prime elimination
propagate through all \(2s\) edges. This last conclusion is correctly scoped
to the frozen sequential local-peel mechanism; it does not exclude a global
owner.

## RR.2 checks

For disjoint nonempty prime sets \(A,B\), \(r=|A|\ne|B|=s\), and a new
largest prime \(p\), the shores

\[
A\cup\{p\prod B\},\qquad B\cup\{p\prod A\}
\]

are disjoint Finsets, have equal product, and have unequal cardinality.
Prime vertices cannot collide with the two composite vertices, and the two
composites cannot collide because \(A,B\) are nonempty and disjoint.

Each prime in \(A\) or \(B\) ties its singleton coefficient to one composite
coefficient; the \(p\)-equation ties the composites. Hence every nonzero
subrelation is the full double star. The top fibre has exactly two terms,
while stripping \(p\) leaves the coprime ratio
\((\prod B)/(\prod A)\) with independently unbounded support sizes. This
proves exactly the claimed bounded-top-fibre obstruction.

## RR.3 checks

Matching each full prime occurrence across the shores gives a bipartite
multigraph with degree \(\Omega(n)\). This works with multiplicity and for
every choice of occurrence matching.

Every connected component separately balances every prime valuation. If
there were more than one component, the nonzero total shore-cardinality
difference would force a proper component with nonzero difference, hence a
proper bad subrelation. Minimality therefore makes every matching connected.

For support size \(v=r+s\), \(r>s\), and \(\Omega(n)\geq d\), the number of
matched occurrence edges satisfies

\[
e\geq dr\geq d(v+1)/2.
\]

Thus

\[
\beta=e-v+1\geq(d/2-1)v+d/2+1.
\]

The extra \(d/2\) is justified by strict shore imbalance. Standard
Turán--Kubilius for \(\Omega\) gives

\[
\#\{n\leq N:\Omega(n)<\tfrac12\log\log N\}
=O(N/\log\log N)=o(N),
\]

so \(d\to\infty\) after a legitimate zero-density deletion. This is only a
complexity statement; no cycle-packing-to-repair implication is asserted.

## Verifier and dependencies

The author verifier was rerun:

\[
\texttt{python3 evidence/verify_residue_aware_kills.py}
\]

and returned \(\texttt{PASS}\). Its SHA-256 is

\[
\texttt{6000976780a71927fdf38a0ceb2d085c19ad4b12344c886cb284bc0166a30828}.
\]

It exactly checks representative RR.1/RR.2 identities, tail inequalities,
active degrees, token behavior, and small support-minimality. It does not
purport to prove universal quantifiers or RR.3; those are supplied by the
symbolic proofs above.

RR.1 uses only Bertrand's postulate, unique factorisation, and elementary
ceiling estimates. RR.2 uses unique factorisation. RR.3 uses occurrence
matching plus the standard Turán--Kubilius estimate for \(\Omega\).

## Scope and recommendation

Recommend promotion only under
\(\texttt{standalone\_decisive\_lemma}\), comprising RR.1--RR.2 and the
supporting RR.3 lemma. The phrases about forest safety, active cycle rank,
bounded local depth, and token descent must be read as refutations of the
precisely frozen M786R-01/02/03/05/06/07/09/10/11 claims.

Forbidden promotion levels are
\(\texttt{global\_interface\_closed}\),
\(\texttt{main\_exponent\_improved}\),
\(\texttt{main\_term\_improved}\), and
\(\texttt{original\_problem\_closed}\).
The survivors M786R-04, M786R-08, and M786R-12 remain open.

No public search for the exact Erdős problem or its solution was performed,
so external priority remains uncertain.
