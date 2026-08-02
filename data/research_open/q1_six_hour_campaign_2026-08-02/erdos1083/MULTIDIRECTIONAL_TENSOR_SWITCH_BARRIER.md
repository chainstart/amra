# Erdős #1083: a power-large positive-multiple normal-form barrier

Date: 2026-08-02

Status: **PROVED — INDEPENDENT CROSS-AUDIT PASSED**

## 0. Outcome

There is no upper bound on the simultaneous-switch family using only the
displayed Laurent-UFD identities, all three mask positivities, and the
endpoint augmentations.  Two further inputs inherited from the exact block
are absent here and must not be suppressed:

1. centre--leaf transversality, equivalently the coprimality interface
   \(\gcd(F_0,F_J)=1\); and
2. the requirement that all source masks \(F_J\) be scalar copies of one
   fixed set \(X\).

For every \(k\ge1\) and every positive integer \(C\), there are integral
Laurent polynomials

\[
 G,\ F_0,\ B,\quad
 R_J,\ Q_J\qquad(J\subseteq[k])
\tag{0.1}
\]

such that

\[
 \boxed{
 B=R_JQ_J,\qquad
 GB,\quad GR_J,\quad F_0Q_J
 \text{ are all \(0/1\) masks}}
\tag{0.2}
\]

and

\[
 \boxed{
 G(1)=F_0(1)=2^k=:S,\quad
 R_J(1)=1,\quad Q_J(1)=C,\quad
 (GB)(1)=(F_0Q_J)(1)=SC=:U.}
\tag{0.3}
\]

There are \(2^k\) pairwise nonassociate divisors \(R_J\mid B\). Every
nonempty \(J\) gives a genuinely signed quotient \(Q_J\), and its Newton
directions meet the centre direction space.

If \(k\) is a multiple of \(14\) and

\[
 C=2^{k/14},
\tag{0.4}
\]

then

\[
 C=S^{1/14},\qquad U=S^{15/14}.
\tag{0.5}
\]

These are exactly the frozen relative scales

\[
 S=t^{7/9+o(1)},\qquad
 C=t^{1/18+o(1)},\qquad
 U=t^{5/6+o(1)}.
\tag{0.6}
\]

The construction has \(K=2^k=S=t^{7/9+o(1)}\) switches, more than the
required \(t^{5/9-o(1)}\).

This is not an exact-block countermodel.  In the construction
\(F_0=G\), so \(F_0\) divides every source mask \(GR_J\); in particular
the centre and leaves are not transverse.  Independently, although the
source masks \(GR_J\) have the right common cardinality, the mixed tensor
boxes are not all scalar copies of one fixed set \(X\). For every positive
\(\mathbb Q\)-linearly independent real embedding, a homothetic subfamily
has at most \(k+1=O(\log S)\) members. This bound is sharp for a special
one-dimensional exponent encoding; a generic embedding improves it to
two. Thus the construction proves only the following normal-form warning:

\[
 \boxed{\text{the identities, positivities, and augmentations alone do not
 bound the multidirectional switch family.}}
\tag{0.7}
\]

## 1. The tensor construction

Use independent Laurent variables \(x_1,\ldots,x_k,z\). Put

\[
 A_i=1+x_i,\qquad
 T_i=1-x_i+x_i^2.
\tag{1.1}
\]

The elementary switch identity is

\[
 \boxed{A_iT_i=1+x_i^3,\qquad T_i(1)=1.}
\tag{1.2}
\]

Let \(D=P_C(z)=1+z+\cdots+z^{C-1}\), and define

\[
 F=\prod_{i=1}^kA_i,\qquad
 G=F_0=F,\qquad
 B=D\prod_{i=1}^kT_i.
\tag{1.3}
\]

For each \(J\subseteq[k]\), set

\[
 R_J=\prod_{i\notin J}T_i,\qquad
 Q_J=D\prod_{i\in J}T_i.
\tag{1.4}
\]

Then \(B=R_JQ_J\). Moreover,

\[
\begin{aligned}
 GB
 &=D\prod_{i=1}^k(1+x_i^3),\\
 GR_J
 &=\prod_{i\in J}(1+x_i)
   \prod_{i\notin J}(1+x_i^3),\\
 F_0Q_J
 &=D\prod_{i\notin J}(1+x_i)
   \prod_{i\in J}(1+x_i^3).
\end{aligned}
\tag{1.5}
\]

Independence of the variables makes every displayed product a direct
\(0/1\) mask. Evaluating at one proves (0.3).

Each \(T_i=\Phi_6(x_i)\) is irreducible, and distinct variables make the
\(T_i\)'s pairwise nonassociate. Hence the \(R_J\)'s are pairwise
nonassociate divisors of \(B\). If \(J\ne\varnothing\), the product
\(\prod_{i\in J}T_i\) has negative coefficients: choose the
\(-x_i\) term in exactly one selected coordinate and constant terms in
all others. Multiplication by the independent positive mask \(D\) does
not remove that negative coefficient. Thus \(Q_J\) is genuinely signed.

Its support differences contain a nonzero multiple of the \(x_i\)
direction for every \(i\in J\), while

\[
 W_0=\operatorname{span}_{\mathbb Q}\{x_1,\ldots,x_k\}.
\tag{1.6}
\]

Therefore every nonempty \(J\) is direction-contaminated. The empty set
is the single clean mask quotient \(Q_\varnothing=D\), exactly respecting
the clean/contaminated firewall.

## 2. Exact endpoint calibration

Take \(k=14\ell\). Then

\[
 S=2^{14\ell},\qquad C=2^\ell,\qquad U=2^{15\ell}.
\tag{2.1}
\]

Set \(t=S^{9/7}=2^{18\ell}\). Direct calculation gives

\[
 S=t^{7/9},\qquad C=t^{1/18},\qquad U=t^{5/6}.
\tag{2.2}
\]

The full tensor family has

\[
 K=2^k=S=t^{7/9}.
\tag{2.3}
\]

Any \(t^{5/9-o(1)}\) subfamily may therefore be retained. All displayed
augmentation, divisor, positivity, and direction-contamination conditions
survive this restriction.  Centre--leaf transversality and the common-
\(X\) scalar-copy condition do not.

## 3. Why no exponent encoding recovers a power-large scalar-copy family

Embed the variables by positive \(\mathbb Q\)-linearly independent real
steps \(\alpha_1,\ldots,\alpha_k\). The source mask \(GR_J\) becomes, up
to translation, the binary tensor box

\[
 X_J=
 \left\{
 \sum_{i=1}^k\varepsilon_i
 3^{\,1_{i\notin J}}\alpha_i:
 \varepsilon_i\in\{0,1\}
 \right\}.
\tag{3.1}
\]

\(\mathbb Q\)-linear independence makes every signed subset sum of the
generators distinct. In the difference multiset, a one-coordinate
difference occurs with multiplicity \(2^{k-1}\), whereas a difference
using \(r\ge2\) coordinates occurs with multiplicity \(2^{k-r}\). Thus
the one-coordinate directions are intrinsic to the point set. The \(k\)
edge magnitudes of this affine cube are

\[
 \left\{
 3^{\,1_{i\notin J}}\alpha_i:i\in[k]
 \right\},
\tag{3.2}
\]

up to permutation.

Put

\[
 q_i=\log_3\alpha_i,\qquad
 \epsilon_i(J)=1_{i\notin J}.
\tag{3.3}
\]

\(\mathbb Q\)-linear independence implies that the \(\alpha_i\), hence
the \(q_i\), are pairwise distinct. It also forbids
\(3^{\epsilon_i}\alpha_i=3^{\epsilon_j}\alpha_j\) for \(i\ne j\), so
none of the edge-log multisets below has a hidden collision.

Homothety of \(X_J\) and \(X_L\) is equivalent to equality of edge-log
multisets

\[
 \{q_i+\epsilon_i(J):i\in[k]\}
 =
 \{q_i+\epsilon_i(L)+c:i\in[k]\},
\qquad c=\log_3|\lambda|.
\tag{3.4}
\]

For a bit pattern \(\epsilon\), define the exponential sums

\[
 A(t)=\sum_{i=1}^ke^{tq_i},\qquad
 B_\epsilon(t)=\sum_{\epsilon_i=1}e^{tq_i}.
\tag{3.5}
\]

Equation (3.4) is exactly

\[
 A(t)+(e^t-1)B_{\epsilon(J)}(t)
 =
 e^{ct}\bigl(A(t)+(e^t-1)B_{\epsilon(L)}(t)\bigr).
\tag{3.6}
\]

Summing the elements of the two multisets in (3.4) gives

\[
 c=\frac{|\epsilon(J)|-|\epsilon(L)|}{k}.
\tag{3.7}
\]

Fix \(L\). There are only \(k+1\) possible Hamming weights
\(|\epsilon(J)|\), hence only \(k+1\) possible values of \(c\). For each
fixed \(c\), the right side of (3.6) uniquely determines
\(B_{\epsilon(J)}\). Distinct real exponentials \(e^{tq_i}\) are linearly
independent, so they uniquely determine the selected index set. Therefore

\[
 \boxed{\text{every homothety class among the \(X_J\)'s has size at most
 \(k+1\).}}
\tag{3.8}
\]

The logarithmic bound is sharp. Let

\[
 \theta=3^{1/k},\qquad \alpha_i=\theta^i\quad(0\le i<k).
\tag{3.9}
\]

The polynomial \(u^k-3\) is Eisenstein at \(3\), so
\(1,\theta,\ldots,\theta^{k-1}\) are \(\mathbb Q\)-linearly independent.
For each \(0\le r\le k\), switch precisely the first \(r\) log-steps:

\[
 \{i/k+1:0\le i<r\}\cup
 \{i/k:r\le i<k\}
 =
 \{i/k+r/k:0\le i<k\}.
\tag{3.10}
\]

Thus these \(k+1\) boxes are related by the uniform scalars
\(\theta^r=3^{r/k}\).

If the \(\alpha_i\)'s are algebraically independent, the stronger
argument from (3.3) forces the edge permutation to be the identity and
the bit difference to be constant. Then only \(J=L\), or the uniformly
scaled pair \(\{\varnothing,[k]\}\), can occur; the generic class size is
at most two.

This proves one of the two exact-block failures quantitatively. The
exponential family consists of anisotropic coordinate switches, whereas a
genuine row family permits only one scalar multiplying every source
direction.  The other failure is already visible from (1.3): \(F_0=G\),
so \(\gcd(F_0,GR_J)\ne1\) for every row.

## 4. Consequences and boundary

The construction simultaneously shows:

1. factor count cannot bound the contaminated family: here
   \(\Omega(B)\ge k=\log_2K\), and all \(2^k\) divisor patterns occur;
2. positivity of \(GB\) and every \(F_0Q_J\) does not control signed
   quotients, even at the exact endpoint augmentations;
3. finite-quotient shadows do not help when the switching factors live
   inside the centre direction space rather than in an independent
   external coordinate;
4. imposing the scalar-copy hypothesis on this particular tensor model
   collapses its \(2^k\) rows to at most \(k+1\) homothetic rows, and to
   at most two for a generic embedding; this does not repair the separate
   transversality failure.

No claim is made that every general contaminated family has tensor form.
The remaining publishable target is a *transverse scalar-copy*
simultaneous-switch theorem: combine
\(\gcd(F_0,GR_j)=1\), homothety of every \(GR_j\), and positivity of every
\(F_0Q_j\) to rule out a power-large family.  The present construction
proves only that the displayed normal-form identities and positivities,
with both geometric interfaces removed, are insufficient. Erdős #1083
remains open.

`PHI6_SWITCH_CUBE_TRANSVERSE_FIBER_RIGIDITY.md` closes one attempted
repair. If a centre is made transverse to the \(k\) switch directions
and the regularizer remains nonnegative after quotienting by those
directions, positivity of the full switch cube forces \(2^k\le C\).
Thus an endpoint transverse repair of this construction would require
strong signed cancellation in the quotient. That additional possibility,
and the common-\(X\) interface, remain open.

For a binary-box centre, the stronger theorem in
TRANSVERSE_BINARY_BOX_PHI6_SWITCH_BOUND.md also removes that signed
escape: a tailored finite quotient preserves the leaf \(\Phi_6\) factors
and gives a pairwise one-sided Hamming bound \(\log_2C\). In particular,
the uniform scalar-copy endpoints \(X\) and \(3X\) would force
\(C\ge S\), impossible in the strict block. This closes the transverse
binary-box repair of the present construction; arbitrary \(X\) and
arbitrary residual divisors remain outside its scope.

## 5. Reproduction

~~~bash
python3 verify_multidirectional_tensor_switch_barrier.py
python3 -m unittest -v test_multidirectional_tensor_switch_barrier.py
~~~

The verifier checks every subset for finite tensor ranks, the signed and
contaminated classification, nonassociate divisor patterns, exact endpoint
calibration, and the generic homothety-class combinatorics. The
all-parameter identities are proved above.
