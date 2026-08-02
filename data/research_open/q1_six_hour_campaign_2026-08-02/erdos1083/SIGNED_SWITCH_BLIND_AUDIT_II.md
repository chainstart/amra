# Blind cross-audit II: signed switches and the exact-block firewall

Date: 2026-08-02, 15:35--16:12 HKT

Status: **FROZEN — FOUR THEOREMS PASS AFTER THREE MINIMAL REPAIRS**

## 0. Scope, baseline, and verdict

This audit independently reconstructed the definitions and proofs in

1. `CYCLOTOMIC_SIMULTANEOUS_POSITIVE_MULTIPLE_BOUND.md`;
2. `FINITE_QUOTIENT_SHADOW_ESCAPE.md`;
3. `PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md`;
4. `TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md`;

and checked their use in `SIGNED_SWITCH_RESULT_DEPENDENCY_MAP.md` and the
two-interface firewall of `MULTIDIRECTIONAL_TENSOR_SWITCH_BARRIER.md`.
The author verifiers were not used as proofs.  The repository baseline was

```text
git HEAD 669bbad1908e7ab7d8382a8b508e67757006e90c
```

The input manuscript hashes were

| file | input SHA-256 |
|---|---|
| cyclotomic bound | `37424af1c86a8394c9e27bcb2b2f59d5307b153d438bf6c634a083ce9bb9ce17` |
| finite quotient / escape | `4d3a9c2c77b7b9cf7ee87c526870213cc5c21f91bcb559b6e4f5bb7087855b4d` |
| transverse fibre rigidity | `ab1894a4ec01b65432b92b1a470595b2d33732910e65b849af9c49ad966f6549` |
| binary-box switch bound | `39397b561c7cebcfdcd7c118c0518c5cf17e96277448decff47ba3b4796a11d3` |
| dependency map | `31a291514758f68045d70360efbd243c4dab8119217b3e86c7abca4df2781a95` |
| tensor barrier | `6a93d718d704bae18fa97558985eaa0b58178d91427dc6fa991e9ee1759bea04` |

The verdicts are:

| item | verdict | reason |
|---|---|---|
| cyclotomic \(C^2\) theorem | **PASS** | The cyclic shadow has exact mass \(C\), preserves the reduced factor, and the CRT mass lemma gives both reduced ratios at most \(C\) |
| \(C=0\) firewall | **PASS** | The live hypothesis is \(1\le C<S\); at \(C=0\), the positive mask is zero and \(Q=0\), so arbitrary \(\mathcal D\) would indeed be vacuous |
| finite-quotient shadow theorem | **PASS** | Coefficientwise tiling gives a nonnegative external shadow of exact mass \(C\), and coefficient comparison preserves every external divisor |
| cyclotomic consequence in the finite-shadow note | **REPAIR \(\to\) PASS** | The imported prime hypothesis on \(S\) was only implicit; it is now stated in the outcome and Section 2 |
| aperiodic escape | **PASS** | The signed identity is exact; \(1+x+x^4\) has no torsion zero and therefore tiles no finite quotient |
| all-subset \(\Phi _6\) fibre theorem | **PASS** | The one-dimensional forbidden-word automaton and slice induction prove mass \(2^k\) and rigid equality |
| transverse global consequence | **PASS** | It correctly uses the *additional* assumption \(\pi_W(H)\ge0\); exact-block positivity alone does not supply it |
| signed binary-box theorem | **REPAIR \(\to\) PASS** | The proof and exponent \(0.460189938897\ldots\) are correct; only the last displayed digit of the gap was repaired |
| dependency map | **REPAIR \(\to\) PASS** | “last row” incorrectly pointed at the signed binary-box row; it now points to the transverse-fibre row containing the extra sign hypothesis |
| tensor firewall | **PASS** | The tensor barrier fails both exact-block interfaces: transversality because \(F_0=G\), and common-\(X\) because its power-large mixed boxes are not homothetic |

No theorem-strengthening repair was needed, and no claimed implication to
the full Erdős problem survived without its stated hypotheses.

## 1. Reconstructed common algebra

All four arguments take place in an integral Laurent group ring of a
finitely generated torsion-free exponent group.  The common positive datum
is

\[
F_0R=B,\qquad B\text{ a nonzero }0/1\text{ mask},\qquad
F_0(1)=S,\qquad R(1)=C.
\tag{1.1}
\]

Augmentation gives

\[
B(1)=SC.
\tag{1.2}
\]

Thus \(C\) is a positive integer whenever (1.1) is nonzero.  The explicit
lower bound in the cyclotomic theorem is nevertheless essential because
its formal data allow \(Q=0\): then every \(R_m\), every \(B_m\), and the
common product vanish, and an arbitrary divisor family would pass all
conditions except nonzeroness.  The current hypothesis

\[
\boxed{1\le C<S}
\tag{1.3}
\]

is therefore the correct firewall.

The exact-block connection is narrower.  A literal block supplies

\[
P_V=F_0P_{A_0}=F_jP_{A_j},\qquad
F_0(1)=F_j(1)=S,\qquad P_{A_j}(1)=U.
\tag{1.4}
\]

On a transverse centre--leaf pair, Euclid cancellation can give
\(P_{A_j}=F_0Q_j\) and hence \(C=Q_j(1)=U/S\).  None of (1.4), however,
forces the residuals to be cyclotomic, the centre to tile a finite
quotient, a full independent \(\Phi _6\) cube to occur, or the source set
to be a binary box.  Those are separate hypotheses below.

## 2. Cyclotomic simultaneous-positive multiples

### 2.1 Sharp mass lemma

For prime \(S\), \((a,S)=1\), and

\[
H_{S,a}(z)=P_S(z^a)/P_S(z),
\]

reduce a nonzero nonnegative multiple modulo \(z^{Sa}-1\).  Divisibility
forces its Fourier support into the union of the two CRT frequency axes in

\[
\mathbb Z/(Sa)\simeq\mathbb Z/a\times\mathbb Z/S.
\]

The resulting array satisfies

\[
f(i,j)+f(i',j')=f(i,j')+f(i',j).
\tag{2.1}
\]

If every entry is positive its mass is at least \(aS\).  If one entry is
zero, (2.1) writes the array as a distinguished column plus a distinguished
row; a nonzero column repeats \(S\) times and a nonzero row repeats \(a\)
times.  Hence

\[
A(1)\ge\min\{S,a\}.
\tag{2.2}
\]

Reduction cannot annihilate the polynomial because its coefficients are
nonnegative.  The multivariable fibre extension is legal because
\(H_{S,a}(y^g)\) preserves every other monomial and every residue of the
\(y\)-exponent modulo \(g\).

### 2.2 Cyclic shadow and divisibility

If \(P_S(x)R\) is a mask, reduction modulo \(x^S-1\) gives counts
\(c_0,\ldots,c_{S-1}\).  At a primitive \(S\)-th root,

\[
\sum c_r\omega^r=0.
\]

Primality makes \(P_S\) the degree-\(S-1\) minimal polynomial, so all
counts coincide.  Therefore

\[
\overline B=P_S(x)K,\qquad K\ge0,\qquad K(1)=C.
\tag{2.3}
\]

If an \(x\)-independent \(H\) divides \(B\), reducing a factorization
coefficientwise shows that every \(x)-coefficient of \(\overline B\),
and hence \(K\), remains divisible by \(H\).  This is stronger and safer
than asserting that the signed \(R\) is positive.

For two scales, the factors \(F_m/F_g\) and \(F_n/F_g\) are coprime: their
cyclotomic index sets would otherwise contain a divisor of both \(m,n\)
which does not divide \(g=(m,n)\).  Euclid's lemma, (2.3), and (2.2) give

\[
C\ge\min\{S,m/g\},\qquad C\ge\min\{S,n/g\}.
\]

Using \(C<S\) yields both reduced ratios at most \(C\).  Fixing one scale
injects the family into the coprime lattice points of \([C]^2\), whose
exact count is

\[
1+2\sum_{r=2}^C\varphi(r)\le C^2.
\]

All mass, factor-preservation, and counting interfaces pass.

## 3. Finite shadows and the aperiodic boundary

Suppose \(\pi(F_0)P_Y=P_G\) coefficientwise.  From a mask \(B=F_0R\),

\[
P_Y\pi(B)=P_G\pi(R).
\tag{3.1}
\]

The left side is coefficientwise nonnegative.  Multiplication by \(P_G\)
makes every coefficient in the finite coordinate equal, so (3.1) is
uniquely \(P_GK\) with \(K\ge0\).  Since
\(|G|=S|Y|\), augmentation gives \(K(1)=C\), with no loss factor.  If an
external \(H\) divides \(B\), comparing any finite-coordinate coefficient
in the factored version of (3.1) gives \(H\mid K\).  This proves the
shadow theorem for composite or noncyclic \(G\) as stated.

The subsequent \(C^2\) consequence imports the *prime-\(S\)* cyclotomic
mass lemma.  The live manuscript now says this explicitly; the general
finite-shadow theorem itself does not require primality.

The escape identity expands exactly as

\[
(1+x+x^4)(1-x^4+x^5+x^7)
=1+x+x^6+x^7+x^9+x^{11}.
\tag{3.2}
\]

If a root of unity \(\zeta\) killed \(1+z+z^4\), the three unit vectors
\(1,\zeta,\zeta^4\) would form a centred equilateral triangle.  Hence
\(\zeta\) would be a primitive cube root, but then \(\zeta^4=\zeta\), a
contradiction.  A finite cyclic tiling would therefore force the complement
indicator to have every nontrivial Fourier coefficient zero and hence to
be the impossible constant \(1/3\).  Every finite abelian quotient of
\(\mathbb Z\) reduces cosetwise to its cyclic image.  The aperiodic escape
and its claimed boundary pass.

## 4. The \(\Phi _6\) fibre theorem

For a one-dimensional mask \(f=\sum a_nz^n\), the coefficient of
\(f(1-z+z^2)\) is

\[
b_n=a_n-a_{n-1}+a_{n-2}.
\]

Among binary triples only \(010\) and \(101\) produce \(-1\) and \(2\).
Thus every nonempty admissible zero-padded word has at least two ones, and
the two-term equality case is a translate of \(1+z\).

For \(k\) independent switch directions, slice in the last direction.
Every nonzero slice satisfies all \(2^{k-1}\) lower-rank positivity states,
so it has mass at least \(2^{k-1}\).  The one-dimensional automaton forces
at least two slices.  Equality forces the same support in two consecutive
slices and inductively gives exactly

\[
m\prod_{i=1}^k(1+z_i).
\tag{4.1}
\]

This proof is fibrewise and requires the full all-subset cube.  For the
global corollary, transversality keeps the \(S\) centre terms distinct after
projection, but the assertion that at least \(S\) projected coefficients
survive uses \(\pi_W(H)\ge0\).  Once that additional sign hypothesis holds,
each occupied projected fibre has mass at least \(2^k\), and

\[
SC=A(1)\ge S2^k.
\]

The dependency map now points to this row, not the signed binary-box row.
No step infers \(\pi_W(H)\ge0\) from exact-block positivity.

## 5. Signed transverse binary boxes

### 5.1 Separating shadow

The rational dual functionals exist because the centre and leaf spans are
transverse.  Clearing their denominators by \(D\) maps the binary centre
onto \(H=\{0,D\}^k\subseteq(\mathbb Z/2D)^k\), tiled exactly by
\(Y=\{0,\ldots,D-1\}^k\).  Combining this finite map with projection
modulo the centre span kills the centre directions while retaining the
\(\mathbb Q\)-independent leaf directions.  The finite-shadow argument then
produces a nonnegative shadow of *exact* mass \(C\), preserving every leaf
factor, even if the original quotient projection is signed.

### 5.2 Independent \(\Phi _6\) mass

If a nonnegative \(K\) is divisible by \(d\) independent factors
\(1-x_i+x_i^2\), Newton-polytope multiplicativity inserts the
parallelotope \(\sum_i[0,2w_i]\).  Every one of its \(2^d\) vertex-cone
interiors contains a distinct full-dimensional cone of the refined normal
fan.  Hence \(\operatorname{Newt}(K)\) has at least \(2^d\) vertices.
Each is a nonzero coefficient of the nonnegative integral polynomial, so

\[
K(1)\ge2^d.
\tag{5.1}
\]

No positivity of the residual multiplier is used.

### 5.3 Hamming and entropy constants

Pairwise cancellation of two tensor patterns leaves coprime \(\Phi_6\)
products in the two one-sided differences.  The separating shadow and
(5.1) give

\[
|\epsilon\setminus\eta|\le\lfloor\log_2C\rfloor,
\qquad
|\eta\setminus\epsilon|\le\lfloor\log_2C\rfloor.
\]

At \(k=14\ell,C=2^\ell\), every pattern lies in a Hamming ball of radius
\(k/7\), and

\[
\begin{aligned}
H_2(1/7)&=0.59167277858232738048\ldots,\\
\frac79H_2(1/7)&=0.46018993889736574037\ldots,\\
\frac59-\frac79H_2(1/7)&=0.09536561665818981518\ldots.
\end{aligned}
\tag{5.2}
\]

Thus the requested shorthand \(0.4601899389\) is correct.  The manuscript's
former final gap digit `...1899` was repaired to `...1898`.

The endpoint patterns are

\[
F_{\mathbf0}=P_X,\qquad F_{\mathbf1}=P_{3X}.
\]

Their one-sided difference has size \(k\), so coexistence forces
\(C\ge2^k=S\), contradicting the strict block condition.  This is a valid
common-\(X\) statement: \(X\) and \(3X\) are scalar copies, and a transverse
centre \(\lambda_0X\) supplies the third copy.  It does not show that an
arbitrary exact block contains both endpoints.

## 6. Dependency and exact-block firewalls

The dependency map is logically non-overlapping and now passes:

- cyclotomic counting needs one-dimensional reduced ratios *and* a positive
  factor-preserving shadow;
- finite-quotient tiling supplies the shadow but no mass/count theorem by
  itself;
- fibre rigidity supplies a local \(2^k\) bound, while its global corollary
  additionally needs a nonnegative projected regularizer;
- the binary-box intersection removes that sign assumption only for a
  binary centre and independent \(\Phi_6\) leaf factors.

The tensor construction is not an exact-block countermodel.  It has
\(F_0=G\), so every source \(GR_J\) shares the centre factor and fails
centre--leaf coprimality/transversality.  Its mixed \(1/3\)-step boxes also
have homothety classes of size at most \(k+1\), not a power-large family of
scalar copies of one \(X\).  The prefix construction attains \(k+1\), so
this firewall is sharp within that model.

Three interfaces remain genuinely open:

1. **exact-block structure:** no theorem reduces arbitrary residual
   divisors to cyclotomic ratios or an independent \(\Phi_6\) cube;
2. **common \(X\):** the general binary switch family is not automatically
   a scalar-copy family; only the \(X\mapsto3X\) endpoint pair is;
3. **outer stability:** none of these exact identities extracts a literal
   common-spectrum block from the original near-extremal geometry with
   power-small losses.

Accordingly, the surviving conditional target is exactly the dependency
map's transverse scalar-copy simultaneous-switch theorem for an aperiodic
centre with genuinely signed quotient projections.  Erdős #1083 remains
open.

## 7. Independent checks and final hashes

`verify_signed_switch_blind_audit_ii.py` imports none of the author
verifiers.  It independently checks:

- 48 sharp cyclotomic polynomial identities;
- 39,308 finite CRT rectangular mass states and the Farey count through
  \(C=39\);
- 15 exact finite quotient tiles and 511 torsion orders for the aperiodic
  mask;
- all 8,190 nonempty binary words through length 12 and every rank-two mask
  in a \(3\times3\) box;
- 12 tailored separating binary quotient tiles, the \(X\mapsto3X\)
  identities through rank six, and the constants in (5.2).

It returns `PASS`.  After the three repairs and status freeze, the audited
files have hashes

| file | frozen SHA-256 |
|---|---|
| cyclotomic bound | `8106c8db649bdd24d4001ae88c722876b7515af8742741a134c4b76cf3ee15c3` |
| finite quotient / escape | `8bc2d92c01f98be1597a90062bf64c95155b36caa1579e7db85793e5e8a4429b` |
| transverse fibre rigidity | `d9f088fc416f082d61f60786c60b31d278bbb3d7c1ad75cb5745f6f08584f34d` |
| binary-box switch bound | `6830869efca2fb6a46353b0ebfed84537d0ba6ebae089bc75dd41931f56d9f72` |
| dependency map | `8b827a5474186bb299904eb4566b80644c176322c4e4270635382c52c5df52f7` |
| tensor barrier | `13fdf2510bf421239fb5952864523b18f21f12de148e823d432b75b5b4683ce7` |

The independent verifier and its pytest wrapper have hashes

~~~text
254580f5c0fc8683e5f69362a9163538ba00cdfc2e153cc1d7dafb29c0d4b84b  verify_signed_switch_blind_audit_ii.py
c3bdcabb3146a98d7fc79d82936fc3088dc9e4be75c45f7e25bdf35a04fd0ce2  test_signed_switch_blind_audit_ii.py
~~~

The wrapper reports `2 passed in 8.45s`; the five affected author test
modules report 22/22 passes.

These hashes include only the minimal scope/numeric/wording repairs and
the cross-audit status lines; no mathematical hypothesis was removed.
