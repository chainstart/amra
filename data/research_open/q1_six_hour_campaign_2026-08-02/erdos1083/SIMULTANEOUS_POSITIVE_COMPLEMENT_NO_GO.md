# Erdős #1083: simultaneous positive complements still permit a signed switch

Date: 2026-08-02

## 0. Result

A tempting next step after the mask-factor theorem is:

> if two transverse source masks divide the same positive spectrum,
> and both complementary factors are positive set masks, then their
> common algebraic quotient must itself be positive.

This is false even with the endpoint inequality \(U<S^2\), a common
literal tangent, positive tangent squares, and genuine
\(\mathbb R^3\) reverse-circle points.

For every integer \(S\ge4\), there are:

- one \(S\)-point source set \(X\);
- two transverse nonzero scalars \(\lambda_0,\lambda_1\);
- positive \(U\)-element tangent sets \(T_0,T_1\), where
  \(U=3S<S^2\);
- one common tangent \(\tau_*\in T_0\cap T_1\); and
- one common \(SU=3S^2\)-element spectrum \(\widetilde V\)

such that

\[
 \widetilde V=(1+z_i^2+T_i)\oplus\lambda_iX,
\qquad \lambda_i=2z_i
\quad(i=0,1),
\tag{0.1}
\]

but the UFD switching quotient between the two factorizations has a
negative coefficient.

Thus:

\[
\boxed{\text{positivity of every complement in one transverse pair
does not make the quotient a mask.}}
\tag{0.2}
\]

The remaining positive route must use simultaneous constraints from
a power-large leaf family, not a two-row positivity lemma.

## 1. The all-parameter mask identity

In two Laurent variables put

\[
 P_S(x)=1+x+\cdots+x^{S-1}
\tag{1.1}
\]

and

\[
 \boxed{
 Q_S(x,y)=x+y-xy+xy^S+x^Sy.}
\tag{1.2}
\]

The quotient \(Q_S\) has one negative coefficient and

\[
 Q_S(1,1)=3<S.
\tag{1.3}
\]

Nevertheless all three polynomials

\[
\begin{aligned}
 P_{A_0}&=P_S(y)Q_S,\\
 P_{A_1}&=P_S(x)Q_S,\\
 P_{V_0}&=P_S(x)P_S(y)Q_S
\end{aligned}
\tag{1.4}
\]

are \(0/1\) mask polynomials, with respectively

\[
 |\operatorname{supp}A_0|
 =|\operatorname{supp}A_1|=3S,
\qquad
 |V_0|=3S^2.
\tag{1.5}
\]

To see this without relying on symbolic expansion, define

\[
 R_S(y)=(1-y+y^S)P_S(y)
       =1+y^{S+1}+\cdots+y^{2S-1}.
\tag{1.6}
\]

Then

\[
 A_0=xR_S(y)+yP_S(y)+x^SyP_S(y).
\tag{1.7}
\]

The three displayed supports are disjoint and each has \(S\)
monomials.  The formula for \(A_1\) is symmetric.

Multiplying (1.7) by \(P_S(x)\) gives three disjoint regions:

\[
\begin{array}{ll}
0\le i\le S-1,&1\le j\le S,\\
S\le i\le2S-1,&1\le j\le S,\\
1\le i\le S,&j=0\ \text{or}\ S+1\le j\le2S-1.
\end{array}
\tag{1.8}
\]

They contain \(S^2,S^2,S^2\) monomials.  Hence \(P_{V_0}\) is a
\(3S^2\)-term \(0/1\) mask.

Equation (1.4) is therefore the coefficientwise pair of exact direct
tilings

\[
 V_0=A_0\oplus\operatorname{supp}P_S(x)
    =A_1\oplus\operatorname{supp}P_S(y).
\tag{1.9}
\]

The shared signed quotient is precisely \(Q_S\), of augmentation

\[
 C=U/S=3<S.
\tag{1.10}
\]

This directly falsifies the proposed positivity upgrade; neither
small quotient augmentation nor positivity of both complements and
the total spectrum suffices.

## 2. Embed the masks in the additive real line

Let

\[
 K_S=S+\frac{S-1}{\sqrt2},\qquad
 d=\frac{K_S}{2S^2},
\tag{2.1}
\]

and choose the \(\mathbb Q\)-independent exponent steps

\[
 \alpha=d,\qquad \beta=\frac d{\sqrt2}.
\tag{2.2}
\]

Map a monomial \(x^my^n\) to the additive real exponent

\[
 m\alpha+n\beta.
\tag{2.3}
\]

The irrational ratio \(\alpha/\beta=\sqrt2\) makes this map injective
on exponent pairs.  Consequently the three positive polynomials in
(1.4) become honest finite subsets

\[
 A_0,A_1,V_0\subset\mathbb R
\tag{2.4}
\]

with the exact direct decompositions (1.9).

Set

\[
 \varepsilon=\frac1{4S},\qquad
 X=\{0,\varepsilon,\ldots,(S-1)\varepsilon\},
\tag{2.5}
\]

and

\[
 \lambda_0=\frac\alpha\varepsilon,\qquad
 \lambda_1=\frac\beta\varepsilon,\qquad
 z_i=\frac{\lambda_i}{2}.
\tag{2.6}
\]

Then

\[
 P_{\lambda_0X}=P_S(x),\qquad
 P_{\lambda_1X}=P_S(y).
\tag{2.7}
\]

Their rational direction spaces are

\[
 \alpha\mathbb Q,\qquad\beta\mathbb Q,
\tag{2.8}
\]

which are transverse.

## 3. A literal common positive tangent

The support description (1.7) contains

\[
 a_0=S\alpha+S\beta\in A_0,
\qquad
 a_1=\beta\in A_1.
\tag{3.1}
\]

The parameter choice (2.1)--(2.6) was made so that

\[
\begin{aligned}
 a_0-a_1
 &=S\alpha+(S-1)\beta
   =dK_S=\frac{K_S^2}{2S^2},\\
 z_0^2-z_1^2
 &=\frac{\alpha^2-\beta^2}{4\varepsilon^2}
   =\frac{K_S^2}{2S^2}.
\end{aligned}
\tag{3.2}
\]

Choose a common translation \(R\) so large that both sets

\[
 T_i=R+A_i-1-z_i^2
\tag{3.3}
\]

are positive.  They have \(|T_i|=3S\), and (3.2) gives the literal
common tangent square

\[
 \tau_*
 =R+a_0-1-z_0^2
 =R+a_1-1-z_1^2
 \in T_0\cap T_1.
\tag{3.4}
\]

Define the translated common spectrum

\[
 \widetilde V=R+V_0.
\tag{3.5}
\]

For each row,

\[
\begin{aligned}
 1+z_i^2+T_i+2z_iX
 &=R+A_i+\lambda_iX\\
 &=R+V_0=\widetilde V,
\end{aligned}
\tag{3.6}
\]

and the sum is direct.  This proves (0.1).  The tangent universe is
even bounded by

\[
 |T_0\cup T_1|\le6S-1.
\tag{3.7}
\]

## 4. Genuine Euclidean realization

Every \(x\in X\) lies in \([0,1)\).  Fix \(A>1\) and take the source
points on a unit circle

\[
 p_x=(A+\sqrt{1-x^2},0,x).
\tag{4.1}
\]

For \(i\in\{0,1\}\) and \(\tau\in T_i\), take the actual target

\[
 q_{i,\tau}=(A,\sqrt\tau,-z_i).
\tag{4.2}
\]

Direct calculation gives

\[
 \|p_x-q_{i,\tau}\|^2
 =1+z_i^2+\tau+2z_ix.
\tag{4.3}
\]

Thus the abstract masks are realized by genuine points and actual
squared distances in \(\mathbb R^3\).  All tangent squares are
positive, the two height rows are distinct and transverse, and they
share the actual collinear target coordinate \(\tau_*\).

## 5. Exact scope of the no-go

This model satisfies more than the signed-quotient firewall in
`HEAVY_SKELETON_RULED_CHART.md`:

- both complements are positive \(0/1\) masks;
- their products with the corresponding source masks are direct;
- the total spectrum is a positive \(0/1\) mask;
- \(C=3<S\) and \(U=3S<S^2\);
- the two source spaces are transverse;
- the tangent sets are positive and share a literal element;
- and all cells have a genuine Euclidean realization.

It does not contradict the triangle firewall because there are only
two transverse rows.  It is not a #1083 counterexample: it has two
rows rather than the endpoint \(q=t^{13/18+o(1)}\) block and does not
control every pairwise distance of the complete Euclidean point set.

The sharp remaining question is therefore:

> Can one fixed centre row support a power-large family of such
> simultaneous positive switches whose leaf spaces are pairwise
> nontransverse and whose tangent sets live in the endpoint common
> universe?

No two-row positivity argument can answer this.

## 6. Reproduction

```bash
python3 verify_simultaneous_positive_complement_nogo.py
python3 -m unittest -v test_simultaneous_positive_complement_nogo.py
```

The verifier checks the \(0/1\) identities for a parameter range, the
strict \(U<S^2\) ledger, exact irrational embedding, common tangent,
full row spectra, and Cartesian distance formula.
