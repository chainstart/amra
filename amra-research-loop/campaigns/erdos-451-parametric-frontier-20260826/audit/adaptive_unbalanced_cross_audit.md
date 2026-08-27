# Cross-audit: adaptive unbalanced frontier

## Scope and independence

This is a non-author cross-reconstruction of
`evidence/adaptive_unbalanced_partition_frontier.md`.  It stays inside the
same Konyagin/prime-interval model, but does **not** inherit the author's
audit, the earlier independent reconstruction, or any earlier Lean verdict.
The pinned theorem statement was used only to check the claimed interface.

## Verdict

**PASS, with two mandatory notation/quantifier clarifications that do not
change either conclusion.**  The attaining argument and the stated
location-blind cardinality-tail no-go both reconstruct.  The result is not a
no-go outside the explicitly delimited independent, nonnegative block-sum
architecture.

## Attaining argument

1. **Stopping order: PASS.**  At
   `R=ceil(a log k/loglog k)`,
   `log(nR!) <= cL^2/l+O_a(L)` whereas
   `log U_R=aL^2/l+O_{a,Q}(L)`; hence the stopping set is nonempty.  The
   test at order one fails from
   `n>k^(2+theta)/2>k^2L^(-Q)`, so the least order satisfies `2<=r<=R`.
   **Required clarification:** (4) currently declares `U_r` only for
   `r>=2`, although (6) and the minimality argument at `r=2` test `U_1`.
   Define the same displayed formula for `U_r` for every `r>=1` (the
   selected Konyagin order remains at least two).

2. **Overlap and scale choice: PASS.**  Direct subtraction gives
   `log(U_r/V_r)=(1-theta)L-Q(3r-2)l`; `r<=R` and `3Qa<1-theta` therefore
   give `V_r<=U_r`.  With
   `lambda^r=max(1,V_r/(nr!))`, one has exactly
   `Z=nr!lambda^r=max(nr!,V_r)` and hence `V_r<=Z<=U_r`.  This proves the
   displayed `T1=A<=L^(-Q)` and `T2=B<=L^(-Q)` without a hidden balancing
   assumption.

3. **Minimality, including `r=2`: PASS.**  When `lambda>1`, failure of the
   preceding test gives
   `n(r-1)!>U_(r-1)`.  At `r=2` this is precisely the already tested order-one
   failure, not an invocation of Konyagin at order one.  It yields
   `lambda^r<k^theta L^(Q(3r-4))/r`, and therefore the uniform bound
   `lambda<=k^(theta/r)L^(3Q)`; the `lambda=1` branch is immediate.

4. **Additive term and `T3`: PASS.**  Since `r>=2`, the normalized additive
   contribution is at most
   `R L^(3Q+1)k^(-theta/2)=o(1)`.  For `r=2`, `T3` is a fixed negative power
   of `k` times a log power.  For `r>=3`, the reconstructed exponent is
   `-((1-theta/3)/(2a)+o(1))l`; (3) indeed implies
   `a<(1-theta)/3<(1-theta/3)/2`, so its coefficient is strictly greater
   than one and `T3=o(1/L)`.

5. **Pinned interface: PASS.**  The pinned estimate allows a real
   `lambda>=1`, has an `r>=2` hypothesis, and its three normalized terms
   specialize to `A`, `B`, and `C_3` under the stated reciprocal-function
   derivative bounds; its additive term is `2r lambda`, whose harmless
   factor two is suppressed in the asymptotic normalization.  The selected
   `r=O(L/l)` satisfies the application's
   `r<=(1/2)k^(1-theta)` condition, and the retained range has `k<n`.

## Cardinality-tail no-go

1. **Discrete tail and the extra logarithm: PASS.**  Among integers strictly
   between `k` and `k+M_k/2`, there are fewer than `M_k/2`; hence at least
   `M_k/2` of the supplied primes have `p-k>=M_k/2`.  Choosing the PI lower
   bound with `M_k` of order `k^theta/L` gives on this tail
   `delta_j >= (p-k)/p \gg k^(theta-1)/L`.  This is the required additional
   `1/L`, including the even/odd discrete endpoint.  **Required
   clarification:** explicitly choose, rather than merely lower-bound,
   `M_k=floor(C k^theta/L)` (after reducing `C` if needed).  This records the
   upper comparison `M_k=O(k^theta/L)` used when identifying a tail of total
   length comparable to `k^theta`.

2. **Location-blind whole-tail partition: PASS.**  For every block,
   `A_j^(2r_j-1)B_j^(r_j-1)=delta_j W_j^4`.  If the sum of the independent
   nonnegative block bounds is `o(k^theta/L)`, weighted Markov on the whole
   deterministic tail supplies blocks of `1-o(1)` total length with
   `max(A_j,B_j)<=e^(-q_k)/L` for some `q_k -> infinity`.  This inference
   uses only block lengths; it neither assumes nor discovers the actual
   prime locations.

3. **Order lower bound and endpoint: PASS.**  On those blocks `A_j<1`
   forces `D_j<1`, hence at
   `n=floor(exp(cL^2/l))` one has
   `r_j>=cL/l-O(1)`.  The invariant and the tail lower bound give
   `(3r_j-2)(l+q_k)<=(1-theta)L+l+O(1)`.  This contradicts the order lower
   bound for `c>(1-theta)/3`.  At the exact endpoint
   `c=(1-theta)/3`, the logarithmic main terms can tie, but
   `(3r_j-2)q_k` exceeds the available `O(l)` slack because
   `r_j\gg L/l` and `q_k->infinity`; equality is therefore excluded as
   claimed.

4. **Exclusion range: PASS AS DELIMITED.**  The obstruction covers arbitrary
   nonuniform deterministic subdivisions, separate `r_j`, real
   `lambda_j>=1`, `W_j>=1`, and shifted contiguous factor groups of length at
   most `k`, when the only prime input is total PI cardinality and the proof
   sums the pinned nonnegative estimates independently.  It does **not**
   exclude cross-block cancellation or coupling, a stronger prime-location
   theorem, a cover selected after learning prime locations, a noncontiguous
   factor mechanism, or a different analytic estimate.
