# Same-model cross-audit: location-blind subdivision bridge

## Scope and verdict

This is a fresh same-model cross-audit by a non-author agent.  It is not
human peer review, does not inherit the author audit, and does not use old
cross-audits as a substitute for the reconstruction below.  I read the final
source, evidence, and frozen logs without modifying or rebuilding the author
files.

**Verdict: PASS for the finite Lean theorem, and CONDITIONAL PASS for the
natural growing-subdivision instantiation.  No mandatory correction was
found.**

The condition is already stated in the author evidence: Lean proves the
finite algebra uniformly in an arbitrary finite family, while the production
of fixed block-uniform comparison losses \(C,D\), and the eventual sequence
instantiation, remain natural mathematics inside the pinned,
location-blind Konyagin architecture.  The result is not a theorem about
arbitrary subdivisions, signed cancellation, prime-location-adaptive covers,
or Erdos 451.

## 1. Frozen source and build evidence

The current SHA-256 of formal/ParametricRanges.lean is

    d5a039d2fb7a30f4302bb0c04b42ce73cebbd46ad29db5e6b57bdf8bdf48dfe2

and agrees with formal/logs/final-sha256.txt,
evidence/lean_parametric_ranges.json,
evidence/lean_parametric_ranges.md, and formal/README.md.  The adjacent
recorded hashes for ParametricInterface.lean, verify_inside_guard.sh,
lakefile.toml, and lake-manifest.json also match the current files.

The frozen replay log records guard unit
openmath-task-20260826-204654-272766.scope, exit status zero, peak whole
replay RSS \(6{,}575{,}412\) KiB, and zero swap.  The fresh range-build log
records unit openmath-task-20260826-203707-264733.scope, \(107.22\) seconds,
peak RSS \(7{,}052{,}716\) KiB, zero swap, and exit status zero.  The final
control and AMRA-validation logs record units
openmath-task-20260826-205024-275772.scope and
openmath-task-20260826-205059-276009.scope, with final control and validation
passing.  The package-test log records five passing tests under
openmath-task-20260826-204950-275140.scope.

The printed axioms for every new bridge theorem are exactly
\(\mathrm{propext}\), \(\mathrm{Classical.choice}\), and
\(\mathrm{Quot.sound}\).  The evidence JSON reports no sorryAx, and the
current source contains no sorry.  I did not start a new Lean process in this
read-only audit.

## 2. Candidate cardinality tail

Let \(C\) be a finite set of natural offsets, with
\({\rm mass}\leq |C|\).  For a natural cut \(a\), at most \(a\) natural
numbers are below \(a\), because

\[
 \{x\in C:x<a\}\subseteq\{0,\ldots,a-1\}.
\]

Splitting \(C\) at \(a\) therefore gives

\[
 |\{x\in C:a\leq x\}|
 =|C|-|\{x\in C:x<a\}|
 \geq {\rm mass}-a.                                \tag{1}
\]

This is exactly candidate_cardinality_tail, including the direction of the
natural subtraction.  With \(a=\lfloor{\rm mass}/2\rfloor\),

\[
 {\rm mass}-\lfloor{\rm mass}/2\rfloor
 \geq\lfloor{\rm mass}/2\rfloor,
\]

which proves candidate_half_mass_tail at both parity endpoints.

For the natural source, PI\((\theta)\) supplies distinct offsets below
\(k^\theta\) with

\[
 m_k=\left\lfloor A_\theta{k^\theta\over\log k}\right\rfloor.
\]

Applying (1) to those offsets puts at least
\(\lfloor m_k/2\rfloor\) candidates in the deterministic tail beginning at
\(\lfloor m_k/2\rfloor\).  The evidence's occurrences of \(m_k/2\) are
asymptotic shorthand; the Lean theorem carries the floors correctly.  No
short-interval distribution of candidates has been inferred.

## 3. Partition telescope

For any finite cut sequence,

\[
 \sum_{j=0}^{s-1}(x_{j+1}-x_j)=x_s-x_0.            \tag{2}
\]

The induction in interval_partition_length_sum is exactly the addition of
the last difference to the preceding telescope.  Strict increase is not
hidden in that lemma: it is used at the source to make block lengths
positive, and positivity is an explicit premise of
LocationBlindTermwiseSubdivisionAt.

The finite certificate remembers only positive weights \(h_j\) and the
identity \(\sum h_j=H\), rather than the cut points themselves.  Every
genuine finite full-tail partition maps into this interface.  The abstract
predicate is therefore at least as broad as the geometric source at this
step, which is safe for a no-go theorem.

## 4. Weighted extraction

Write

\[
 E_j=e^{\log T_{1,j}}+e^{\log T_{2,j}}>0,\qquad
 \varepsilon=e^{-M-q}.
\]

From positive \(h_j\), \(\sum h_j=H\), and

\[
 \sum_jh_jE_j\leq H\varepsilon
               =\varepsilon\sum_jh_j,             \tag{3}
\]

some \(j\) satisfies \(E_j\leq\varepsilon\).  Otherwise every summand
\(h_j(E_j-\varepsilon)\) would be positive.  Since both exponentials are
positive,

\[
 \log T_{1,j}\leq-M-q,\qquad
 \log T_{2,j}\leq-M-q.                             \tag{4}
\]

This reconstructs exists_weighted_cost_le and
locationBlindSubdivision_exists_good_block.  Neither argument contains
\(|s|\), a minimum block length, or a comparable-size assumption.

If an actual Konyagin block count has an integer-point weight larger than
the geometric \(h_j\), or includes additional nonnegative third and additive
terms, discarding those excess nonnegative quantities only weakens the
abstract premise (3).  It cannot invalidate the no-go extraction.

## 5. Block invariant and endpoint constants

For \(r\geq2\), let

\[
\begin{aligned}
 L_1&={\log D+r\log\lambda+2\log W\over2r-1},\\
 L_2&={\log\delta+2\log W-\log D-r\log\lambda\over r-1}.
\end{aligned}
\]

The denominators are positive and direct cancellation gives

\[
 (2r-1)L_1+(r-1)L_2=\log\delta+4\log W.             \tag{5}
\]

Thus \(W\geq1\) implies \(4\log W\geq0\); increasing \(W\) cannot make the
invariant smaller.  This verifies the direction of
locationBlind_first_two_invariant_ge_delta_of_W_ge_one.

Combining (4) with the safe-tail inequality gives

\[
 (3r-2)(M+q)\leq(1-\theta)K+M+C.                   \tag{6}
\]

At \(c\geq(1-\theta)/3\), so \(1-\theta\leq3c\), and with

\[
 cK-DM\leq rM,
\]

equation (6) yields

\[
 (3r-2)q\leq(3D+3)M+C.                             \tag{7}
\]

The constants and directions in locationBlind_endpoint_excess_budget are
therefore correct.

For the finite-family theorem, (4), \(M>0\), and \(q\geq0\) imply
\(L_1<0\), so the conditional order premise is legally invoked.  It gives

\[
 3cK-(3D+2)M\leq(3r-2)M.                           \tag{8}
\]

Multiplication by \(q\geq0\) preserves the direction.  The theorem's strict
separation premise and (8) give

\[
 ((3D+3)M+C)M<(3r-2)qM.
\]

Division by the strictly positive \(M\) gives the strict reverse of (7).
This is exactly the contradiction in
locationBlindTermwiseSubdivision_endpoint_no_go.  No division by a
possibly negative coefficient occurs.

## 6. Natural source mapping

### Uniform safe-tail loss

On the cardinality tail, for all sufficiently large \(k\),

\[
 p-k\geq\lfloor m_k/2\rfloor
      \geq c_\theta{k^\theta\over\log k},\qquad
 p\leq k+k^\theta .
\]

For a contiguous factor group of length \(h\leq k\), the one-sided
nearest-integer implication requires

\[
 \delta_j\geq{p-h\over p}\geq{p-k\over p}
      \geq c'_\theta{k^{\theta-1}\over\log k}.      \tag{9}
\]

Taking logarithms, with \(K=\log k\) and \(M=\log\log k\), gives

\[
 \log\delta_j\geq-(1-\theta)K-M-C_\theta.          \tag{10}
\]

The constant is independent of the block because every block covers part
of the same deterministic tail.  Since \(W_j\geq1\), (10) implies the
certificate's safe inequality after adding \(4\log W_j\).  The source
inequality directions are correct.

### Uniform order loss and the upper bound on \(r_j\)

The source derivative comparison is

\[
 \log D_j=\log n_j+\log(r_j!)
          -(r_j+1)\log x_j+O(1),                  \tag{11}
\]

with \(x_j=k+O(k^\theta)\) and \(n_j=n+O(k)\).  The pinned theorem imposes

\[
 r_j\leq\tfrac12k^{1-\theta}.                     \tag{12}
\]

Because

\[
 \log(x_j/k)=O(k^{\theta-1}),
\]

(12) is exactly what makes

\[
 r_j\log(x_j/k)=O(1)                              \tag{13}
\]

uniformly over the blocks.  Without (12), the comparison loss in (11)
could grow with \(r_j\), and a fixed \(D\) would not follow.

If \(L_{1,j}<0\), then \(2r_j-1>0\),
\(\log\lambda_j\geq0\), and \(\log W_j\geq0\) imply
\(\log D_j<0\).  At

\[
 n=\left\lfloor\exp(cK^2/M)\right\rfloor,
\]

one has \(\log n_j=cK^2/M+o(1)\).  Dropping the nonnegative
\(\log(r_j!)\) from (11), and using (13), gives

\[
 (r_j+1)K\geq cK^2/M-O(1),
\]

and hence

\[
 r_jM\geq cK-DM                                   \tag{14}
\]

for one fixed block-independent \(D\).  The \(+1\) costs one \(M\), and the
fixed derivative and shifted-base comparisons are absorbed into the same
constant.

This derivation requires the constants in (11)-(13) to be uniform over the
whole \(k\)-dependent family.  That uniformity is part of the explicitly
named pinned, location-blind architecture.  It is stated as a natural
source hypothesis and is not silently claimed as a Lean theorem.

### Little-o to \(q_k\to\infty\)

Let

\[
 e_k={\sum_jh_jE_j\over H_k}.
\]

The numerator is strictly positive for every nonempty finite certificate,
so \(\log e_k\) is defined.  The total bound
\(\sum h_jE_j=o(H_k/K)\) says \(e_kK\to0\).  Defining

\[
 q_k=-M-\log e_k=-\log(e_kK)
\]

therefore gives \(q_k\to+\infty\), and
\(e_k=e^{-M-q_k}\) exactly.  In particular \(q_k\geq0\) eventually, as
required by the finite theorem.

For fixed \(C,D,c>0\), \(K/M^2\to\infty\) and \(q_k\to\infty\) imply the
finite separation eventually.  Explicitly,

\[
 (3D+2)M\leq cK,\qquad
 ((3D+3)M+C)M<2cK,\qquad q_k\geq1
\]

eventually, whence

\[
 ((3D+3)M+C)M
 <2cK\leq(3cK-(3D+2)M)q_k.                        \tag{15}
\]

This validates the equality endpoint without extracting fixed exponents
\(\alpha,\beta>1\).

## 7. Growing finite quantifier and scope

At each outer scale, the Lean theorem accepts an arbitrary type with an
arbitrary nonempty finite set \(s_k\).  Its proof is uniform in
\(|s_k|\).  A sequence whose finite cardinalities grow at any rate is
therefore handled by applying the same finite theorem separately for each
sufficiently large \(k\); no limiting index set, compactness, or stable
block label is used.

The parameters \(\theta,c,C,D\) must remain fixed across that sequence.
The quantities \(K,M,q,H,s\), block locations, weights, orders, scales, and
\(W\)'s may vary as allowed by the predicate.  The one-block examples in
the evidence correctly show why allowing \(C_k\) or \(D_k\) to grow
destroys the abstract endpoint theorem.

The bridge covers every finite-at-each-scale,
full-deterministic-tail, location-blind subdivision whose nonnegative
Konyagin bounds are summed independently and whose source comparisons have
uniform losses.  It does not cover:

- an infinite partition at a fixed \(k\);
- a sparse cover selected after inspecting actual prime locations;
- cancellation between blocks or signed combined estimates;
- a stronger local-prime or exponential-sum theorem;
- source geometries for which (9), (11), or (12) fails.

The decisive lemma, decision, and evidence JSON preserve these boundaries.
They do not turn the informal claim that any conceivable growing
subdivision has an LP image into a Lean theorem, and they retain the
unconditional BHP constant \(19/120\) rather than treating the scoped no-go
as a solution of Erdos 451.

## Final classification

- Candidate-cardinality tail: **PASS**.
- Arbitrary finite partition telescope: **PASS**.
- Positive weighted extraction: **PASS**.
- Endpoint no-go directions and constants: **PASS**.
- Natural source mapping to fixed \(C,D\): **CONDITIONAL PASS within the
  explicitly stated pinned location-blind architecture**.
- Arbitrarily growing finite block count: **PASS**, with fixed losses and
  finite-at-each-scale quantifiers exactly as stated.
- Lean hash, replay, axiom, and control evidence: **PASS**.

Mandatory corrections: **none**.

No author source, evidence file, Lean file, or B-line artifact was changed.
