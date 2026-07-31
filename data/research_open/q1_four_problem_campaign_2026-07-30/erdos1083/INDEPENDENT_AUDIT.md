# Independent reconstruction audit: multidilate energy and the \(2/9\) bundle

Date: 2026-07-30

## 1. Audit verdict

| Item | Verdict |
|---|---|
| Exact distinct-dilate energy inequality | **PASS** |
| Aggregate-support consequence | **PASS** |
| Two-row set-intersection consequence | **PASS** |
| Many-label/many-row spectral graph | **PASS** |
| Abundance of synchronized row pairs | **PASS** |
| Reverse-circle geometric translation | **PASS** |
| Endpoint exponent deductions | **PASS** |
| Unconditional improvement of \(f_3(N)\) | **NOT CLAIMED / NOT PROVED** |
| Standalone Q1 novelty | **NOT CERTIFIED** |

The proof was reconstructed from the definitions rather than inferred
from the verifier.  The finite verifier separately exhausts small
rational systems and checks the exact endpoint fractions.

## 2. Reconstruction of the energy inequality

For one dilation \(\lambda\), an energy solution is
\[
\tau+\lambda x=\tau'+\lambda x'.
\tag{2.1}
\]
There are exactly \(S|T_\lambda|\) solutions with \(x=x'\), because
then \(\tau=\tau'\).

If \(x\ne x'\), equation (2.1) forces
\[
\lambda=\frac{\tau'-\tau}{x-x'}.
\tag{2.2}
\]
It also forces \(\tau\ne\tau'\).  Since the dilation parameters are
distinct, one ordered quadruple
\[
(\tau,\tau',x,x')
\in T_\ast^2\times X^2
\]
with unequal entries in both coordinates is charged at most once
over the entire dilation family.  The number of such quadruples is
exactly
\[
R(R-1)S(S-1).
\tag{2.3}
\]
This reconstructs
\[
\sum_\lambda E^+(T_\lambda,\lambda X)
\le
S\sum_\lambda|T_\lambda|+R(R-1)S(S-1).
\]

No order, positivity, integrality, or genericity assumption is used.
The only indispensable hypotheses are that all rows lie in one
\(T_\ast\) and that the dilates are distinct.

## 3. Reconstruction of the support and overlap steps

Let \(r_\lambda(v)\) be the row representation function.  Then
\[
\sum_vr_\lambda(v)=S|T_\lambda|,
\qquad
\sum_vr_\lambda(v)^2=E_\lambda.
\]
Twice applying Cauchy--Schwarz gives
\[
\left(S\sum_\lambda|T_\lambda|\right)^2
\le
\left(\sum_\lambda|\mathcal V_\lambda|\right)
\left(\sum_\lambda E_\lambda\right).
\tag{3.1}
\]
Substitution of the energy bound proves the aggregate-support
formula.

Under \(HU\ge R^2S\), its denominator is at most twice its diagonal
term, so
\[
\mathcal S:=\sum_\lambda|\mathcal V_\lambda|
\ge HSU/2.
\tag{3.2}
\]
Under \(HSU\ge4D\), this gives \(\mathcal S\ge2D\).

Let \(q_v\) count rows whose **sets**, not multisets, contain \(v\).
Then
\[
\sum_{\lambda\ne\lambda'}
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|
=
\sum_vq_v(q_v-1)
\ge
\frac{\mathcal S^2}{D}-\mathcal S
\ge
\frac{\mathcal S^2}{2D}.
\tag{3.3}
\]
Division by \(H(H-1)\) and (3.2) give
\[
\max_{\lambda\ne\lambda'}
|\mathcal V_\lambda\cap\mathcal V_{\lambda'}|
\ge
\frac{S^2U^2}{8D}.
\]
The constant \(1/8\) is therefore valid; no missing factor of \(H\)
or \(D\) was found.

For the spectral graph, a fixed \(d,x,\tau\) leaves
\[
z^2+2\rho xz+(\rho^2+\tau-d)=0,
\]
so it contributes to at most two height rows.  Hence \(q_d\le2SR\).
The labels below degree \(HSU/(4D)\) carry less than \(HSU/4\)
memberships, whereas total membership is at least \(HSU/2\).
Dividing the remaining mass by \(2SR\) gives at least \(HU/(8R)\)
rich labels.  This independently recovers both endpoint exponents
\[
h+m-1\ge35/18,\qquad
h+a+m-3\ge13/18.
\]

For pair abundance, the total ordered intersection is at least
\[
t^{2(h+a+m)-3-o(1)}.
\]
Pairs below \(t^{2a+2m-3-\varepsilon}\) carry a
\(t^{-\varepsilon+o(1)}\) fraction of that mass.  A remaining pair
contains at most \(t^{a+m+o(1)}\) labels.  Division leaves
\[
t^{2h+a+m-3-o(1)}
\ge t^{17/6-o(1)}
\]
ordered pairs; unordered pairs differ by the factor two only.  The
overlap threshold is at least
\(t^{2/9-\varepsilon-o(1)}\).  All inequality directions check.

## 4. Reconstruction of the Euclidean interface

An anchor source point is
\[
p=(A+\rho\cos\phi,0,w_0+\rho\sin\phi),
\]
and a target point producing the row circle at height \(w_i\) is
\[
q=(A,y,w_i).
\]
Writing \(z_i=w_0-w_i\), exact expansion gives
\[
|p-q|^2
=
\rho^2+y^2+z_i^2+2\rho z_i\sin\phi.
\tag{4.1}
\]

The two possible cosine signs over one sine value lose at most a
factor two in the source set.  The two possible signs of \(y\) over
one \(y^2\) lose at most a factor two in the target row.  These are
absolute constants and do not affect any endpoint exponent.

Equal merged circles on one fixed \((A,\rho^2)\) line have equal
centre height.  Hence different circles in that line have distinct
heights, so all \(z_i\), and therefore all \(2\rho z_i\), are
distinct.  Their perpendicular axes are parallel distinct lines.
Thus the extracted circles are genuinely nonaligned; the conclusion
is not a relabeling of the earlier concentric-circle obstruction.

## 5. Independent endpoint arithmetic

At \(\kappa=2/9\), the inherited scalar inequalities used are
\[
\begin{aligned}
a+b+m&\ge19/3,\\
b+m&\le50/9,\\
11a+2b&\le18,\\
m&\ge5/6,\qquad m\le1,\\
c&\le46/9-3m,\qquad b=c+h,
\end{aligned}
\]
up to \(o(1)\).

They imply:

1. \(a\ge7/9\) by subtracting the total-triple capacity from the
   weighted mass;
2. \(a\le16/27+2m/9\) by inserting
   \(b\ge19/3-a-m\) into \(11a+2b\le18\);
3. \(h\ge11/9-a+2m\) by subtracting the rich-line upper bound for
   \(c\) from the mass lower bound for \(b\);
4. \(h\ge19/9\) after using the upper bound for \(a\) and
   \(m\ge5/6\);
5. the reuse margin
   \[
   h+m-(2+a)\ge1/6;
   \]
6. the aggregate-support exponent
   \[
   h+a+m\ge67/18>3;
   \]
7. the synchronized-overlap exponent
   \[
   2a+2m-3\ge2/9.
   \]
8. the many-label and row-degree exponents
   \[
   h+m-1\ge35/18,\qquad
   h+a+m-3\ge13/18.
   \]
9. the synchronized-pair count exponent
   \[
   2h+a+m-3\ge17/6.
   \]

All inequalities are monotone in the required direction over
\(5/6\le m\le1\).  The exact-fraction verifier independently returns
the boundary values
\[
(a,h,\text{reuse},\text{support},\text{overlap})
=
\left(\frac79,\frac{19}{9},\frac16,
\frac{67}{18},\frac29\right).
\]

## 6. Regression evidence

The new verifier:

- exhausts 56 small rational row systems;
- checks the energy injection and both Cauchy--Schwarz identities;
- verifies the geometric distance formula on six exact rational
  circle--axis pairs and the parabolic row-degree cap;
- certifies every endpoint fraction.

The focused dependency suite returned:

```text
24 passed
```

This includes the inherited matching-or-hub, weighted reverse-circle,
fixed-\(A\) linearization, cross-height, and new multidilate tests.

## 7. Red-team boundary

The new theorem does not upper-bound
\[
|\mathcal V_z\cap\mathcal V_{z'}|.
\]
It lower-bounds that intersection in every surviving endpoint hub.
Therefore it narrows the obstruction but does not contradict it.

The current proof would become an endpoint exclusion if one proved,
uniformly outside a classified exceptional family,
\[
|\mathcal V_z\cap\mathcal V_{z'}|
\le t^{2/9-\epsilon}
\]
for the extracted rows.  No such estimate is present, and this audit
rejects any claim of a \(3/5+\delta\) consequence without it.

No exhaustive literature-priority audit was performed for the
elementary all-parameter inequality.  It is new to the AMRA proof
tree; global novelty and journal placement remain unverified.

The adverse-direction \(o(1)\) calculation, fixed-\(\varepsilon\)
order, and nearest-neighbour comparison with Mathialagan--Sheffer
Theorem 1.4 are separately reconstructed in
`QUANTIFIER_AND_GEOMETRIC_GAP_AUDIT.md`.  That audit confirms that the
known two-circle theorem applies but yields only
\(t^{28/27-o(1)}\) source--source distances per minimally rich pair.
It does not provide the aggregate axis-spectrum de-reuse estimate
needed here.
