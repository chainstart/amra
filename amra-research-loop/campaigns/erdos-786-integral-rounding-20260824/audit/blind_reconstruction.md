# Blind reconstruction: integral-rounding successor

## Protocol and statement

This reconstruction was frozen before reading `kill_tests.json`, any file
under this campaign's `evidence/`, its verifier, or the pre-existing
`audit.json`.  The inputs were the closure contract, information-loss map,
representation/mechanism/survivor registries, and the statement/dependency
fields of `decisive_lemma.json`.

The theorem to reconstruct is: for every sequence \(\eta_K>0\) satisfying

\[
 K\eta_K\longrightarrow\infty,                       \tag{1}
\]

all sufficiently large \(K\), with \(N=2^K\), admit a support-minimal
equal-product relation between distinct finite sets of unequal sizes, every
integer of which lies strictly in

\[
 (N^{1-\eta_K},N].                                    \tag{2}
\]

The construction below independently proves that statement.

## 1. Normalizing the moving width and choosing the graph

Replace \(\eta_K\) by

\[
 \bar\eta_K=\min(\eta_K,1/2).
\]

Then \(K\bar\eta_K\to\infty\), and a construction in the narrower
\(\bar\eta_K\)-tail also lies in the original tail.  Thus assume from now on
that \(0<\eta_K\le1/2\), and put

\[
 s=s_K=\left\lceil\frac4{\eta_K}\right\rceil.         \tag{3}
\]

Equation (1) gives \(s=o(K)\).  This implication alone does **not** give
\(s\log s=o(K)\), so a dense edge-prime graph cannot be used without an
extra hypothesis.  Use instead the path \(P_{2s+1}\), whose bipartition
\(A\sqcup B\) has

\[
 |A|=s+1,qquad |B|=s.                                 \tag{4}
\]

Label its \(2s\) edges by distinct odd primes.  For a vertex \(v\), let
\(b_v\) be the product of the one or two edge primes incident to \(v\).
Every edge prime occurs once in \(\prod_{v\in A}b_v\) and once in
\(\prod_{v\in B}b_v\), so

\[
 \prod_{v\in A}b_v=\prod_{v\in B}b_v.                 \tag{5}
\]

The bases \(b_v\) are pairwise distinct by unique factorization: their sets
of incident edge labels are distinct nonempty subsets.

Bertrand's postulate gives the crude all-parameter bound that the \(j\)-th
prime is below \(2^{j+1}\).  Hence every chosen edge prime is at most
\(2^{2s+2}\), and

\[
 \lambda_v:=\log_2 b_v\le4s+4=o(K).                   \tag{6}
\]

This is the prime-size estimate needed for nonnegative padding.  Merely
observing that there are finitely many primes would not be uniform in \(K\).

## 2. Integer padding intervals and exact product balance

For each vertex define integer endpoints

\[
 \ell_v=\left\lfloor K(1-\eta_K)-\lambda_v\right\rfloor+1,
 \qquad
 u_v=\left\lfloor K-\lambda_v\right\rfloor.           \tag{7}
\]

By (6), \(\ell_v\ge0\) and \(u_v-\ell_v\ge
K\eta_K-O(1)>0\) for all sufficiently large \(K\).  Every integer
\(a_v\in[\ell_v,u_v]\) therefore satisfies the strict and weak inequalities

\[
 2^{K(1-\eta_K)}<2^{a_v}b_v\le2^K.                    \tag{8}
\]

Let \(\Lambda=\sum_{v\in A}\lambda_v=sum_{v\in B}\lambda_v\), where
the equality is (5).  Denote the sums of the lower and upper endpoints on a
shore by \(L_A,U_A,L_B,U_B\).  The floor inequalities give

\[
\begin{aligned}
 L_A&\le(s+1)(1-\eta_K)K-\Lambda+(s+1),\\
 U_B&\ge sK-\Lambda-s,
\end{aligned}
\]

and hence

\[
 U_B-L_A\ge((s+1)\eta_K-1)K-(2s+1)>0                 \tag{9}
\]

for large \(K\), because \((s+1)\eta_K\ge4\) and
\(s=o(K)\).  Similarly,

\[
 U_A-L_B\ge K+s\eta_KK-(2s+1)>0.                     \tag{10}
\]

Thus the two integer intervals of attainable total padding exponents,
\([L_A,U_A]\) and \([L_B,U_B]\), overlap.  Every integer between the sum
of the individual lower endpoints and the sum of their upper endpoints is
attainable by distributing unit increments greedily among the vertices.
Choose one common total \(T\) in the intersection and exponents
\(a_v\in[\ell_v,u_v]\) on both shores with

\[
 \sum_{v\in A}a_v=T=\sum_{v\in B}a_v.                 \tag{11}
\]

Put \(n_v=2^{a_v}b_v\).  Equations (5) and (11) give the exact product
identity

\[
 \prod_{v\in A}n_v=\prod_{v\in B}n_v,                \tag{12}
\]

while (4) makes the shore cardinalities unequal.  Equation (8) supplies the
strict tail inclusion.  Since every \(b_v\) is odd and the odd parts are
pairwise distinct, the padded integers \(n_v\) remain pairwise distinct,
regardless of coinciding padding exponents.

## 3. Signed support minimality

Support minimality must exclude every proper signed relation on the same
vertices, not merely a subrelation preserving the displayed shore labels.
Suppose coefficients \(\epsilon_v\in\{-1,0,1\}\) give a multiplicative
relation on a subset of the \(n_v\).  For an edge \(e=uv\), its private odd
prime appears only in \(b_u,b_v\), so its valuation equation is

\[
 \epsilon_u+\epsilon_v=0.                             \tag{13}
\]

Along the connected path, if one coefficient is zero then all are zero; if
one is nonzero then all are nonzero and the signs alternate.  The latter is
exactly the full bipartition orientation, up to global sign.  The 2-adic
valuation is balanced by (11).  Hence (12) has no nonempty proper-support
subrelation and is support-minimal in the full cancelled-coefficient sense.

This completes the natural all-parameter proof of IR.1.

## 4. Exact consequences for M01--M03

### M786I-01: moving hard threshold

Suppose a claimed threshold deletes \(n\le N^{1-\delta_N}\), where
\(\delta_N\log N\to\infty\).  On powers \(N=2^K\), set
\(\eta_K=\delta_{2^K}\) and, if necessary, apply the preceding
\(\min(\eta_K,1/2)\) normalization.  Then \(K\eta_K\to\infty\), and IR.1
places a bad minimal support wholly above the deleted threshold for every
sufficiently large power.  The universal transversal claim is therefore
false.

### M786I-02: finite nested threshold union

A union of nested lower-tail thresholds is exactly its largest member,
whether the finite number of listed thresholds is fixed or varies with
\(N\).  If that union has size \(o(N)\), its endpoint \(X_N=o(N)\) can be
written as \(N^{1-\delta_N}\) with

\[
 \delta_N\log N=\log(N/X_N)\longrightarrow\infty.
\]

IR.1 then leaves a minimal circuit above the entire union.  Thus the kill is
all-parameter for precisely nested global lower tails; it says nothing about
non-nested arithmetic deletions.

### M786I-03: unaltered independent proportional rounding

Let \(q_N(n)\le g_Nw_N(n)\), where \(g_N=o(\log N)\), and deletions are
independent.  On \(N=2^K\), write \(h_K=g_{2^K}\) and choose

\[
 \eta_K=\frac1{\sqrt{K\max(1,h_K)}}.                  \tag{14}
\]

Then \(K\eta_K\to\infty\) and \(h_K\eta_K\to0\).  On the IR.1 circuit,
every vertex satisfies

\[
 w_N(n)=\frac{\log(N/n)}{\log N}<\eta_K,
\]

so \(q_N(n)<1\) for all circuit vertices for sufficiently large \(K\).
Independence makes the probability of deleting none of its finitely many
vertices

\[
 \prod_{n\in E}(1-q_N(n))>0.                          \tag{15}
\]

Therefore the sampled set is not a transversal with probability one.  This
refutes only unaltered independent rounding and supplies no lower bound on
the success probability after arithmetic alteration.  The broader wording
“all probabilities below one” is already killed by (15) for any fixed bad
support; IR.1 is what makes the refutation compatible with the affordable
proportional bound in the moving thin tail.

## 5. Blind checks of the other advertised kills

* **Rank one.**  In the powers-of-two exponent row, for
  \(0\le j<r\), the disjoint triples
  \[
  2^{3j+1}2^{3j+2}=2^{6j+3}
  \]
  lie among \(2^1,\ldots,2^{6r}\).  They force transversal number at least
  \(r\) although the exponent matrix has rank one.  This refutes a universal
  constant-times-rank bound.
* **One active degree.**  A relation among squarefree active-prime incidence
  vectors all of degree \(d>0\) has \(d|S|=d|T|\), so a single degree is
  admissible.  It cannot carry density \(1-o(1)\) when the active reciprocal
  mass diverges: on finite prime cylinders the active indicators are
  independent Bernoulli variables (with conditional probabilities
  \(1/(p+1)\) after imposing squarefreeness), and the maximum Poisson-binomial
  atom is \(o(1)\) as its variance diverges.  The exact conditioning and
  variance hypotheses must appear in the author proof.
* **Adjacent active degrees.**  Label the edges of connected
  \(K_{s+1,s}\) by private active primes and use incident-prime products at
  its vertices.  The two shore degrees are \(s\) and \(s+1\), while the
  unequal shore products agree.  Connectivity gives signed support
  minimality as in (13).  Hence a union of those adjacent degree strata is
  not certified by total incidence.
* **Fixed cylinder.**  Given a fixed finite controlled prime set, choose the
  path edge primes and padding prime outside it.  Every constructed integer
  then lies in the controlled zero-signature cell, so admitting the whole
  cell cannot be admissible.

## 6. Provisional promotion scope

IR.1 is not an integrality-gap lower bound: one vertex deletion hits each
individual constructed circuit.  It does not prove \(\tau(H_N)=o(N)\) or
its negation and has no infinite coherence consequence.  If the author
evidence matches the path, prime bound, integer interval overlap, strict
tail, and signed minimality checks above, the correct classification is a
**standalone scoped obstruction** to the frozen threshold/unaltered-rounding
mechanisms.  It is not `main_term_improved`, `global_interface_closed`, or
`original_problem_closed`.  The three residue-aware survivor routes may
continue in a successor allocation after that scoped promotion.
