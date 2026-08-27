# Independent reconstruction: faithful linear embedding

## Verdict

**PASS (independent reconstruction and statement gate).**

The natural-language theorem in `evidence/FAITHFUL_LINEAR_EMBEDDING.md` has a
complete reconstruction: subject to its stated domains \(K\in\mathbb Z\),
\(K\ge 1\), \(B\in\mathbb Z\), and \(B\ge 3\), all requested mathematical
dependencies check. The finite replay is also exactly reproducible. The
corrected frozen statements in `decisive_lemma.json` and
`closure_contract.json` now preserve the theorem's objects, quantifiers,
parameter domains, three budget hypotheses, and conclusions. The earlier
statement mismatch is resolved, and no mathematical dependency gap remains.

## Frozen-statement check

Both corrected frozen statements specify a finite simple linear hypergraph
\(G=(X,\mathcal E)\), with \(X\) the union of its nonempty edges and maximum
degree \(D\), and define
\(r=\lceil\log_2(D+1)\rceil+1\). Both quantify integers \(K\ge1\) and
\(B\ge3\), and both include all three hypotheses

\[
\min_{e\in\mathcal E}|e|>K,\qquad
\pi(B)-1\ge r|X|,\qquad
2r\log_2B+5\le K.
\]

The strict minimum-edge condition, together with \(K\ge1\), excludes empty
edges. The conclusions cover one unequal-cardinality equal-product relation
per edge, a primitive circuit for the full prime-valuation matrix, exact
pairwise support intersections, an isomorphic edge-intersection graph, and
exactly preserved matching and transversal numbers. These are precisely the
claims established by the reconstruction below. In particular, the corrected
integer domains justify the integral powers of two used by the construction.
The frozen statement and reconstructed proof now match with no remaining
quantifier, parameter-range, hypothesis, or conclusion gap.

## Independent mathematical reconstruction

### 1. Prime budget and partition count

Put

\[
r=\lceil\log_2(D+1)\rceil+1.
\]

An \(r\)-element set has

\[
\frac{2^r-2}{2}=2^{r-1}-1
\]

unordered nontrivial bipartitions. Since
\(2^{r-1}=2^{\lceil\log_2(D+1)\rceil}\ge D+1\), this count is at least \(D\).
Consequently the incident edges at each \(x\) can receive distinct unordered
bipartitions of its block \(R_x\).

For integer \(B\ge3\), exactly \(\pi(B)-1\) primes at most \(B\) are odd. The
hypothesis \(\pi(B)-1\ge r|X|\) therefore supplies \(r|X|\) distinct odd primes,
which split into disjoint \(r\)-element blocks \(R_x\). This proves the stated
prime budget without reuse of a prime between host vertices.

### 2. Raw path identity

For an ordered edge \(e=\{x_1,\ldots,x_m\}\), write its successive path-edge
labels as

\[
\alpha_1,\beta_1,\alpha_2,\beta_2,\ldots,\alpha_m,\beta_m.
\]

The even parity class consists of
\(a_i=\alpha_i\beta_i\), while the other class consists of

\[
b_0=\alpha_1,\quad b_j=\beta_j\alpha_{j+1}\ (1\le j<m),
\quad b_m=\beta_m.
\]

Every path-edge label occurs exactly once in each product, so

\[
\prod_{i=1}^{m}a_i=\prod_{j=0}^{m}b_j.
\]

Every factor is an odd integer greater than one because each side of every
assigned bipartition is nonempty.

### 3. Padding exponents and exact two-adic equality

Let \(c_i=\lceil\log_2a_i\rceil\) and
\(d_j=\lceil\log_2b_j\rceil\). No \(a_i\) or \(b_j\) is a power of two, hence

\[
2^{c_i-1}<a_i<2^{c_i},\qquad
2^{d_j-1}<b_j<2^{d_j}.
\]

The shared exponent is nonnegative. Indeed,
\(a_i\le B^r\) gives \(c_i\le r\log_2B+1\), and thus

\[
K-c_i-2\ge K-r\log_2B-3\ge r\log_2B+2>0.
\]

Therefore \(u_i=2^{K-c_i-2}a_i\) is integral and satisfies
\(2^K/8<u_i<2^K/4\).

Writing each ceiling as its exact logarithm plus an error in \((0,1)\), the
raw product identity gives

\[
C_e:=\sum_{j=0}^m d_j-\sum_{i=1}^m c_i\in(-m,m+1).
\]

With
\(\Delta_e=K-C_e+2m\), the inequalities \(m>K\ge1\) imply

\[
0<\Delta_e<K+3m<4(m+1).
\]

Euclidean division
\(\Delta_e=h_e(m+1)+s_e\), \(0\le s_e<m+1\), and the prescribed balanced
choice \(t_j\in\{h_e,h_e+1\}\) give

\[
\sum_jt_j=\Delta_e,
\qquad 0\le t_j\le
\left\lceil\frac{\Delta_e}{m+1}\right\rceil\le4.
\]

A private raw label uses primes from at most two blocks, so

\[
d_j\le 2r\log_2B+1,
\qquad
K-d_j-t_j\ge K-(2r\log_2B+1)-4\ge0.
\]

Thus every \(v_j=2^{K-d_j-t_j}b_j\) is integral. Before the decrement,
\(2^{K-d_j}b_j\in(2^K/2,2^K)\); since \(0\le t_j\le4\), this yields

\[
2^K/32<v_j<2^K.
\]

Finally, substituting the definition of \(C_e\) and
\(\sum_jt_j=\Delta_e\) gives the exact identity

\[
\begin{aligned}
\sum_{j=0}^m(K-d_j-t_j)
&=(m+1)K-\sum_jd_j-\Delta_e\\
&=mK-\sum_ic_i-2m\\
&=\sum_{i=1}^m(K-c_i-2).
\end{aligned}
\]

Together with the raw odd-part identity, this proves
\(\prod_i u_i=\prod_jv_j\). The shores have \(m\) and \(m+1\) entries, hence
oriented cardinality defect \(-1\).

### 4. Primitive circuit for the full valuation matrix

Order the \(2m+1\) columns along the auxiliary path as

\[
v_0,u_1,v_1,u_2,\ldots,u_m,v_m.
\]

For each of its \(2m\) edges, choose an odd prime from that nonempty edge
label. Because all vertex blocks are disjoint, the chosen prime has valuation
one on exactly the two endpoint columns and valuation zero on every other
column of the relation. Hence every rational kernel vector \(\gamma\) of the
*full* valuation matrix obeys
\(\gamma_i+\gamma_{i+1}=0\) along every path edge. Connectivity forces it to
be a scalar multiple of the full alternating vector.

The proved integer product equality says that the alternating vector lies in
the kernel for every valuation row: all unselected odd-prime rows as well as
the row for \(2\). Thus the full kernel is exactly one-dimensional. Its
primitive integral generator has all coefficients \(+1\) or \(-1\), so every
coefficient is nonzero and no proper subset of columns is dependent. This is
a primitive circuit and gives support minimality. The argument is not merely
a rank check on the selected witness-prime submatrix; it controls the full
valuation matrix.

### 5. Collisions and exact intersections

Unique factorization lets one read from an integer's odd part both the host
blocks represented and the particular prime subsets used. A shared label
\(u_x\) uses the whole block \(R_x\). An endpoint private label uses one
nonempty proper subset of one block, and an internal private label uses
nonempty proper subsets of two distinct blocks. Multiplication by a power of
two cannot erase these distinctions.

Within a relation, the ordered path has no repeated host vertex. Its internal
private footprints are its distinct adjacent vertex pairs; its two endpoint
footprints are distinct; and a shared label is distinguished from an endpoint
private label by using the full block rather than a proper subset. Hence all
support labels are distinct and the two shores are disjoint.

Across distinct host edges, a two-block private footprint cannot recur:
recurrence would put the same two host vertices in both edges, contradicting
linearity. A one-block private footprint can occur only at a common host
vertex. Distinct incident edges were assigned distinct unordered
bipartitions; equality of either oriented selected half would also make the
complementary halves equal and therefore make the unordered partitions equal.
So such private labels cannot coincide. No private label equals a shared
label because a private one uses only a proper part of any one-block
footprint, whereas a shared one uses the full block.

It follows that private labels are globally relation-unique and the only
labels common to \(S_e\) and \(S_f\) are \(u_x\) for \(x\in e\cap f\). Thus

\[
|S_e\cap S_f|=|e\cap f|,
\]

with size zero or one by linearity. The sentence in the evidence saying that
the “footprint identifies every path position” is slightly imprecise if
“footprint” means only the set of contributing blocks: \(u_{x_1}\) and the
endpoint private value at \(x_1\) have the same one-block footprint. The
subsequent full-block/proper-subset distinction repairs this wording, and the
collision proof itself is valid.

### 6. Preservation of matching and transversal numbers

The exact-intersection result makes two arithmetic supports disjoint exactly
when their host edges are disjoint. It therefore gives an isomorphism of the
edge-intersection graphs and proves
\(\nu(\mathcal R_K(G))=\nu(G)\).

If \(T\subseteq X\) is a host transversal, then
\(\{u_x:x\in T\}\) meets every arithmetic support, proving
\(\tau(\mathcal R_K(G))\le\tau(G)\). Conversely, take any arithmetic
transversal. Retain its shared labels. Every selected private label belongs to
exactly one support \(S_e\), so replace it by any \(u_x\in S_e\). Duplicates
may reduce, but cannot increase, cardinality, and every support remains hit.
The corresponding host vertices form a host transversal, proving the reverse
inequality and hence equality of transversal numbers.

## Finite replay and hashes

The replay was run from the campaign directory with

```text
python3 evidence/verify_faithful_embedding.py
```

Results:

- script SHA-256:
  `a6e5c14bd9763614726fae7cf3cee5031dfaa23096b605bbd10eb6a2e2aeb901`;
- that hash equals the `script_sha256` stored in the recorded replay;
- regenerated output SHA-256:
  `2938a56dc88609a31981f65e4cf1fc5def70015c306435fa1f5fb58af6558928`;
- recorded replay SHA-256:
  `2938a56dc88609a31981f65e4cf1fc5def70015c306435fa1f5fb58af6558928`;
- byte comparison of regenerated and recorded JSON: identical;
- replay status: `PASS` for \(K=128\), \(B=10000\), three edges of size
  \(129\), \(384\) vertices, maximum degree \(2\), and block size \(3\);
- recorded and reproduced invariants:
  \(\tau_{\rm host}=\tau_{\rm arithmetic}=2\) and
  \(\nu_{\rm host}=\nu_{\rm arithmetic}=1\).

This is exact finite corroboration only. It does not supply the universal
step; that step is supplied by the reconstructed argument above.

## Dependency, closure, and novelty findings

The proof retains exactly the disclosed mathematical restrictions: a finite
simple linear host, strict minimum edge size \(>K\), enough odd primes for
disjoint degree-coded blocks, and the bit budget
\(2r\log_2B+5\le K\). It proves neither a corresponding construction for
nonlinear hosts nor a removal of the edge-size or budget hypotheses. It also
does not bound the full equal-product hypergraph or settle the stated infinite
density-one problem.

Accordingly, the corrected frozen statements and the argument support a
conditional `global_interface_closed` result and a
`standalone_decisive_lemma`. It does not establish
`original_problem_closed`, `main_term_improved`, or `main_exponent_improved`.

The only bounded comparison information available in the authorized proof
and closure records is the assertion that toric-circuit, set-intersection, and
multiplicative-Sidon comparisons were checked. No primary bibliographic
records or direct priority evidence occur in the authorized materials.
Therefore the novelty classification remains **`priority_uncertain`**; the
statement correction supplies no new priority evidence, and no priority claim
is certified here.

The projective-plane paragraph is an application rather than a dependency of
the frozen theorem. Its reference to a “predecessor estimate” is not derived
inside the authorized evidence set, so this audit does not independently
certify that external estimate. Conditional on the displayed predecessor
inequality and the standard projective-plane facts invoked there, the stated
specialization is consistent with the proved theorem.

## Scope boundary and next permitted action

Reviewed:

- `campaign_state.json`;
- `closure_contract.json`;
- `decisive_lemma.json`;
- `evidence/FAITHFUL_LINEAR_EMBEDDING.md`;
- `evidence/verify_faithful_embedding.py`;
- `evidence/faithful_embedding_replay.json`;
- the AMRA skill instructions and their phase-gate, schema, and evidence-policy
  references.

Not reviewed: mechanism records, kill tests, survivors, decision records,
prior reviews, evaluation prose, any other campaign evidence, or external
literature. Mechanism-retention and kill decisions are therefore outside this
audit. No author evidence or campaign state was edited.

The correction recheck read only the corrected `closure_contract.json`,
corrected `decisive_lemma.json`, and this existing independent report; it did
not reopen author evidence or any other campaign artifact.

Current phase: `independent_audit`. Artifact updated:
`audit/independent_reconstruction.md`. Independent reconstruction/statement
gate result: `PASS`. The next permitted action is the campaign's promotion
decision, subject to its normal validation of artifacts outside this narrow
recheck. No mechanism status was assessed or changed. No original-problem,
main-term, or main-exponent status changed in this audit.
