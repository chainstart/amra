# Independent red-team audit of ruled-transfer stability

Date: 2026-07-30

Audited files:

- `RULED_STABILITY_EXTRACTION_ATTACK.md`
- `AFFINE_HEIGHT_RULED_COLUMN_STABILITY.md`

## 1. Verdict

\[
\boxed{
\begin{array}{c}
\text{TENSOR NO-GO: PASS AFTER SYMMETRY QUALIFICATION}\\
\text{AFFINE-HEIGHT EUCLIDEAN SUBCASE: PASS}
\end{array}
}
\]

The no-go correctly proves that dyadic pigeonholing, DRC on the
plane-pair/distance support, a second endpoint-level DRC, and label-only
BSG do not force a polynomial two-sided ruled core from the
representation tensor alone.

The initial finite model omitted the compulsory symmetry
\[
R_{\alpha,\beta}(d)=R_{\beta,\alpha}(d).
\]
The revised argument repairs this by sampling supports on unordered
plane pairs and copying each row to the reverse orientation; endpoint
partitions are transposed in the reverse direction.  This changes only
absolute factors.  Claims about four common rows are now correctly
restricted to four independent unordered plane-pair types.

The new Euclidean theorem is a rigorous nontrivial terminal branch:
common signed-radial support and long vertical interval columns force
near-maximal distance expansion even under arbitrary bounded integral
height translations.

## 2. Audit of the dyadic ledger

At a level with cell weight \(t^\omega\), total mass \(t^8\) forces
\[
|E|=t^{8-\omega}.
\]
With \(t^2\) plane-pair vertices and \(t^3\) labels, the two average
degrees are
\[
t^{6-\omega},\qquad t^{5-\omega}.
\]
The incidence cap gives \(\omega\le4+o(1)\), while the maximum of
\(t^5\) tensor cells gives \(\omega\ge3-o(1)\) for a mass-carrying
level.

If the label degrees are regular, one label has representation mass
\[
t^{5-\omega}t^\omega=t^5,
\]
and hence the aggregate energy is
\[
t^3(t^5)^2=t^{13}.
\]
The diagonal energy is
\[
t^{8-\omega}t^{2\omega}=t^{8+\omega}\le t^{12}.
\]
All exponents in the no-go are correct.

The no-go does not claim that every dyadic level of an arbitrary
Euclidean configuration is regular or individually carries
\(t^{13-o(1)}\) energy.  It only exhibits a single regular level that
already satisfies all tensor hypotheses.  That is sufficient to refute
an extraction based solely on those hypotheses.

## 3. Audit of the probabilistic obstruction

On unordered plane-pair types, choose support probability \(p=t^{-1}\).
The expected degrees are
\[
t^3p=t^2,\qquad t^2p=t.
\]
For four fixed independent unordered types, their common label count is
\[
\operatorname{Bin}(t^3,t^{-4})
\]
with mean \(t^{-1}\).  For fixed \(K>8\), the probability of at least
\(K\) common labels is \(t^{-K+o(1)}\).  The union bound over at most
\(t^8\) four-tuples succeeds.

Copying a support to the reverse orientation creates a mandatory
identical row.  It does not create coherence among independent
unordered types.  With weight \(t^4\), the symmetrized model has
\[
\begin{aligned}
\text{row mass}&=t^6,\\
\text{total mass}&=\Theta(t^8),\\
\mathfrak E_{\rm diag}&=\Theta(t^{12}),\\
\mathfrak E_{\rm all}&=\Omega(t^{13}).
\end{aligned}
\]
Thus the tensor barrier survives the symmetry correction.

The balanced endpoint partition has density \(t^{-2}\) in a
\(Q\times Q\) cell, \(Q=t^3\).  Two fixed source endpoints have expected
common target count \(t^{-1}\).  Transposing the partition for the
reverse orientation again preserves the obstruction.

## 4. Audit boundary of BSG and rotation data

Equality of completed distance labels is not an additive-energy
identity on endpoint coordinates.  Arbitrary permutation of the labels
preserves the tensor and all its energies.  Therefore label-only BSG
cannot recover a radial/height decomposition.

The split rotation reservoir has exact total mass \(t^5\), source
marginal \(q_\alpha=t^3\), rotation marginal
\(r_\alpha=t^{5-o(1)}\), and normalized rotation codegree
\(t^{7-o(1)}\).  It is an abstract compatibility construction only.
The report explicitly does not claim a simultaneous Euclidean
few-distance realization.  This claim boundary is correct.

## 5. Independent audit of the Euclidean subcase

For each recovered slope \(j\), radial parameter \(a\), and height index
\(h\), the theorem assumes the actual point
\[
(a,ja,\sigma_{j,a}+h).
\]
Fixing \(k_0=\min\mathcal J\) and comparing equal radial parameters gives
\[
|p-q|^2
=\bigl(a(j-k_0)\bigr)^2
+\bigl(\sigma_{j,a}-\sigma_{k_0,a}+h\bigr)^2.
\]

There are two and only two losses:

1. the product \(a(j-k_0)\) has at most \(\tau(n)\) representations;
2. a completed integer label \(x^2+y^2=n\) has at most
   \(r_2(n)\le4\tau(n)\) representations.

Selecting one \((j,a)\) for every product \(x\) makes the pairs
\((x,y)\) distinct before the second loss.  Negative translated heights
cause no problem because \(r_2(n)\) counts signed integer
representations.  The bounds on \(a\), slope diameter, shifts, and
column length keep \(n=O(t^4)\), so both divisor losses are \(t^{o(1)}\).

Therefore
\[
|\Delta^2(P)|
\ge
\frac{|\mathcal A|(|\mathcal J|-1)H}
{T_\times T_2},
\]
and the critical hypotheses yield \(t^{4-o(1)}\).  The theorem and its
common-height and affine-height corollaries pass.

## 6. Remaining gap

The positive theorem begins after a common integer slope chart, common
signed-radial support, and long vertical intervals have been extracted.
It does not derive them from
\(\mathfrak C_{\rm plane}\ge t^{13-o(1)}\).

The surviving research problem is consequently narrower:

\[
\boxed{
\text{use the Euclidean four-plane quadratic to force coefficient/radial
alignment, or prove that failure of alignment expands distances.}
}
\]

The tensor no-go shows why this step cannot be replaced by generic
dyadic/DRC/BSG machinery; the affine-height theorem shows that absolute
height alignment is no longer part of the obstruction.

## 7. Reproduction

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/erdos1083/geometric
pytest -q \
  test_verify_ruled_stability_extraction.py \
  test_verify_affine_height_ruled_columns.py
python3 verify_ruled_stability_extraction.py
python3 verify_affine_height_ruled_columns.py
```
