# Erdős #1083: a near-full heavy-factor hub and ruled chart

Date: 2026-08-02

## 0. The strengthening

In the transverse-heavy exact-block branch, one centre row \(0\) and
one literal tangent \(\tau_0\) have a transverse leaf family \(L\)
with

\[
 |L|=t^{5/9+o(1)}.
\tag{0.1}
\]

Write

\[
 V=A_i\oplus\lambda_iX,\qquad
 F_i=P_{\lambda_iX},\qquad
 |X|=S,\quad |A_i|=U<S^2.
\tag{0.2}
\]

Here (1.3) below implies \(S\mid U\), so \(U\ge S\ge2\) and
\(\lfloor\log_2U\rfloor\ge1\).  Then there is one nonconstant
irreducible Laurent factor \(G\) with

\[
 |G(1)|\ge2
\tag{0.3}
\]

which divides at least

\[
 \boxed{
 \left\lceil
 \frac{|L|}{\lfloor\log_2U\rfloor}
 \right\rceil}
\tag{0.4}
\]

leaf masks.  At the frozen endpoint this is

\[
 \boxed{t^{5/9-o(1)}}
\tag{0.5}
\]

leaves.

Thus the high-rank quotient clique has an almost-full subfamily with
one genuine common polynomial factor and one common nonzero Newton
direction.  The former augmentation-unit obstruction affects
synchronization of the *entire* factorization, but it does not prevent
one common heavy factor.

For a nonzero Newton direction \(h\) of \(G\), every leaf in this
subfamily has

\[
 \lambda_j=\frac h{w_j},\qquad
 z_j=\frac h{2\rho w_j},
 \qquad 0\ne w_j\in
 W:=\operatorname{span}_{\mathbb Q}(X-X).
\tag{0.6}
\]

Its common-tangent distance cell is therefore

\[
 \boxed{
 \rho^2+\tau_0+
 \frac{h^2}{4\rho^2w_j^2}
 +\frac h{w_j}X.}
\tag{0.7}
\]

This is a \(t^{5/9-o(1)}\)-row denominator-free reciprocal ruled
chart inside the literal exact block.

## 1. Proof of the heavy-factor hub

Work in the common finitely generated torsion-free group ring

\[
 R=\mathbb Z[\Gamma],
\tag{1.1}
\]

a Laurent-polynomial UFD.  Centre--leaf transversality gives

\[
 \gcd(F_0,F_j)=1.
\tag{1.2}
\]

Since \(F_j\mid P_V=P_{A_0}F_0\), Euclid's lemma gives

\[
 F_j\mid P_{A_0}
\qquad(j\in L).
\tag{1.3}
\]

Factor \(P_{A_0}\) into irreducibles, listing occurrences with
multiplicity.  Since \(P_{A_0}(1)=U\ne0\), every factor has nonzero
integer augmentation.  The number \(r_{\rm heavy}\) of occurrences
satisfying augmentation magnitude at least two obeys

\[
 2^{r_{\rm heavy}}\le U,
\qquad
 r_{\rm heavy}\le\lfloor\log_2U\rfloor.
\tag{1.4}
\]

On the other hand,

\[
 F_j(1)=S\ge2.
\tag{1.5}
\]

If every irreducible factor of \(F_j\) had augmentation magnitude one,
their product would also have magnitude one, contradicting (1.5).
Thus every leaf mask contains at least one heavy irreducible factor of
\(P_{A_0}\).

Normalize irreducibles up to Laurent associates, and choose one such
factor type for each leaf.  There are at most
\(r_{\rm heavy}\le\lfloor\log_2U\rfloor\) possible types.  Pigeonholing
proves (0.4).

The common complement \(P_{A_0}\) is a \(0/1\) set mask and hence has
content one.  No constant integer prime divides it.  The selected
heavy irreducible \(G\) is therefore nonconstant, so its Newton
polytope has a nonzero direction.

## 2. Ruled-chart conversion

For every selected leaf,

\[
 G\mid F_j=P_{\lambda_jX}.
\tag{2.1}
\]

Newton-polytopal additivity puts

\[
 \operatorname{dir}(\operatorname{Newt}G)
 \subseteq
 \lambda_jW\otimes_{\mathbb Q}\mathbb R.
\tag{2.2}
\]

Choose one nonzero rational exponent direction \(h\) of \(G\).
Because the direction spaces are rational, \(h\in\lambda_jW\), so
\(h=\lambda_jw_j\) for some \(0\ne w_j\in W\).  This proves (0.6).
Substitution in

\[
 \rho^2+\tau_0+z_j^2+2\rho z_jX
\tag{2.3}
\]

gives (0.7).

Distinct row scalars give distinct \(w_j\).  No bounded denominator,
height, or finite subset of \(W\) is claimed.

## 3. Relation to the full heavy skeleton

The heavy-skeleton entropy theorem remains useful but has a different
role:

- this theorem synchronizes **one** heavy irreducible factor on
  \(t^{5/9-o(1)}\) rows;
- `HEAVY_SKELETON_RULED_CHART.md` synchronizes the **complete**
  heavy-factor multiset on
  \(t^{0.2610894430\ldots+o(1)}\) rows;
- `UNIT_SWITCH_WIDTH_ATLAS.md` linearizes all remaining
  augmentation-unit variation on the latter family.

There is no contradiction between the exponents.  The almost-full
hub is the strongest current common-direction result; the smaller
family carries more complete factor data.

## 4. Claim firewall

The theorem is conditional on the literal exact common-spectrum block
and on the transverse-heavy tangent-overlap branch.  It does not:

- extract exact partitions from the original near-extremal geometry;
- make the signed quotient \(P_{A_0}/F_j\) a positive mask;
- bound the reciprocal parameters \(w_j\);
- prove that the ruled chart alone has more than \(t^3\) distances;
- or refute Erdős #1083.

The common direction comes from \(G\), not from the false inference
that pairwise-nontransverse spaces have a total common intersection.

## 5. Reproduction

```bash
python3 verify_heavy_factor_hub_ruled_chart.py
python3 -m unittest -v test_heavy_factor_hub_ruled_chart.py
```

Finite checks certify the factor-hub pigeonhole, endpoint exponent,
and reciprocal substitution.  The all-parameter UFD statement is the
proof above.
