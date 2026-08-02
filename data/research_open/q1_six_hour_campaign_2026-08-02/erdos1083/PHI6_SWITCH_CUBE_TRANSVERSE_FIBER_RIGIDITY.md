# Erdős #1083: transverse fibre rigidity for the \(\Phi _6\) switch cube

Date: 2026-08-02

Status: **PROVED — INDEPENDENT CROSS-AUDIT PASSED**

## 0. Outcome

The positive-multiple tensor barrier uses the elementary signed switch

\[
 T_i=1-z_i+z_i^2,
 \qquad (1+z_i)T_i=1+z_i^3.
\tag{0.1}
\]

This note gives the first rigidity statement for an attempted *transverse*
repair of that model.  Let \(z_1,\ldots,z_k\) be independent directions,
put \(T_J=\prod_{i\in J}T_i\), and suppose that

\[
 \boxed{A T_J\text{ is a finite \(0/1\) mask for every }J\subseteq[k].}
\tag{0.2}
\]

Then every nonempty fibre of \(A\) parallel to the switch lattice has at
least \(2^k\) terms.  Equality is rigid:

\[
 \boxed{A_{\rm fibre}=m\prod_{i=1}^k(1+z_i)}
\tag{0.3}
\]

for a monomial \(m\).  Thus the ordinary binary tensor box is the unique
minimum-mass all-subset positive state.

Now suppose

\[
 A=F_0H,\qquad F_0(1)=S,\qquad H(1)=C>0,
\tag{0.4}
\]

where \(F_0\) is an \(S\)-term mask and its direction space is transverse
to the rational span \(W\) of the switch directions.  Let \(\pi_W\) be
projection modulo \(W\).  If the collapsed regularizer \(\pi_W(H)\) is
coefficientwise nonnegative, then

\[
 \boxed{2^k\le C.}
\tag{0.5}
\]

At the frozen endpoint \(C=t^{1/18+o(1)}\), a full \(\Phi _6\) switch
cube with more than \(C\) states therefore cannot be repaired merely by
placing the centre transverse to the tensor directions.  It must use
genuine signed cancellation even *after quotienting out all switch
directions*.

This is a local rigidity theorem for the full \(\Phi _6\) cube.  It does
not handle an arbitrary divisor family, does not impose the common-\(X\)
scalar-copy condition on the source masks, and does not settle the
exact-block branch or Erdős #1083.

## 1. The one-dimensional automaton

Write a nonzero one-dimensional mask as

\[
 f(z)=\sum_{n\in\mathbb Z}a_nz^n,
 \qquad a_n\in\{0,1\},
\tag{1.1}
\]

with \(a_n=0\) outside a finite interval.  If

\[
 f(z)(1-z+z^2)=\sum_nb_nz^n,
\tag{1.2}
\]

then

\[
 b_n=a_n-a_{n-1}+a_{n-2}.
\tag{1.3}
\]

Of the eight binary triples
\((a_{n-2},a_{n-1},a_n)\), precisely two give a coefficient outside
\(\{0,1\}\):

\[
 010\longmapsto-1,
 \qquad 101\longmapsto2.
\tag{1.4}
\]

Hence

\[
 \boxed{fT\text{ is a mask}\iff
 \text{the zero-padded word of }f\text{ avoids }010\text{ and }101.}
\tag{1.5}
\]

Equivalently, every run of ones has length at least two, and any zero run
between two one-runs has length at least two.  In particular every
nonzero such \(f\) has at least two terms.  If it has exactly two, they
must be consecutive, so

\[
 f=z^r(1+z).
\tag{1.6}
\]

This elementary automaton is useful because it uses both positive states;
no positivity of the signed factor \(T\) is asserted.

## 2. All-subset fibre theorem

Let \(\Gamma\) be a torsion-free abelian exponent group and let
\(u_1,\ldots,u_k\in\Gamma\) be \(\mathbb Z\)-linearly independent.  Write
\(z_i=[u_i]\), \(\Lambda=\bigoplus_i\mathbb Zu_i\), and
\(T_i=1-z_i+z_i^2\).

### Theorem 2.1

If \(A\in\mathbb Z[\Gamma]\) satisfies (0.2), then the restriction of
\(A\) to every nonempty coset of \(\Lambda\) has at least \(2^k\)
terms.  A fibre has exactly \(2^k\) terms if and only if it has the form
(0.3).

#### Proof

Multiplication by every \(T_J\) preserves each \(\Lambda\)-coset, so it
suffices to work in
\(\mathbb Z[z_1^{\pm1},\ldots,z_k^{\pm1}]\).  We induct on \(k\).
The case \(k=1\) is (1.5)--(1.6).

For the induction step write

\[
 A=\sum_{n\in\mathbb Z}A_n z_k^n.
\tag{2.1}
\]

For every \(J\subseteq[k-1]\), coefficient comparison in the
\(z_k\)-direction shows that \(A_nT_J\) is a mask.  Therefore every
nonzero slice \(A_n\) has at least \(2^{k-1}\) terms by induction.

There are at least two nonzero slices.  Indeed, choose any monomial in
the support of one slice and inspect its coefficient word along the
\(z_k\)-line.  It is nonempty, and (1.5) says that it contains at least
two ones.  Consequently

\[
 A(1)=\sum_n A_n(1)\ge2\cdot2^{k-1}=2^k.
\tag{2.2}
\]

If equality holds, exactly two slices are nonzero and both attain the
inductive equality.  Every occupied \((k-1)\)-dimensional location must
occur in both slices, again by the one-dimensional lower bound.  Their
supports therefore coincide, and their two \(z_k\)-positions are
consecutive by (1.6).  Thus

\[
 A=z_k^r(1+z_k)A',
\tag{2.3}
\]

where \(A'\) is an equality case in rank \(k-1\).  Induction gives
(0.3).  Conversely, (0.1) shows directly that (0.3) makes every
\(AT_J\) a mask. QED.

The proof also shows that the conclusion is fibrewise: different
\(\Lambda\)-cosets cannot help one another cancel a bad coefficient.

## 3. Transverse projection consequence

Let

\[
 W=\operatorname{span}_{\mathbb Q}\{u_1,\ldots,u_k\}
 \subseteq\Gamma\otimes_{\mathbb Z}\mathbb Q,
\tag{3.1}
\]

and project the exponent group modulo \(W\).  The image group is
torsion-free: if a nonzero multiple of an exponent lies in \(W\), then
the exponent itself lies in the rational subspace \(W\).

### Corollary 3.1

Assume (0.2)--(0.4),

\[
 W(F_0)\cap W=\{0\},
\tag{3.2}
\]

and \(\pi_W(H)\ge0\) coefficientwise.  Then (0.5) holds.

#### Proof

Condition (3.2) makes the \(S\) support points of \(F_0\) distinct after
projection modulo \(W\).  Since \(\pi_W(H)\) is nonzero and nonnegative,
there is no cancellation in

\[
 \pi_W(A)=\pi_W(F_0)\pi_W(H).
\tag{3.3}
\]

For finite nonempty subsets \(E,D\) of a torsion-free abelian group,
\(|E+D|\ge|E|+|D|-1\).  One proof is to choose a translation-invariant
total order and list the strictly increasing chain

\[
 e_1+d_1<\cdots<e_{|E|}+d_1
 <e_{|E|}+d_2<\cdots<e_{|E|}+d_{|D|}.
\tag{3.4}
\]

Thus \(\pi_W(A)\) has at least \(S\) nonzero coefficients.  Each is the
number of terms of \(A\) in one \(W\)-coset.  A nonempty \(W\)-coset
contains a nonempty \(\Lambda\)-fibre, so Theorem 2.1 makes its mass at
least \(2^k\).  Finally

\[
 SC=A(1)\ge S2^k,
\tag{3.5}
\]

and cancellation of \(S\) proves \(C\ge2^k\). QED.

The bound is sharp: take \(F_0\) in directions transverse to the
\(u_i\)'s and \(H=\prod_i(1+z_i)\).  Then \(C=2^k\), and all masks in
(0.2) are direct products.

## 4. Exact boundary for the campaign

In a proposed tensor repair write

\[
 Q_J=H\prod_{i\in J}(1-z_i+z_i^2),
 \qquad A_J=F_0Q_J.
\tag{4.1}
\]

If all \(2^k\) complements \(A_J\) are masks, the centre is transverse
to the switch span, and \(\pi_W(H)\ge0\), then Corollary 3.1 leaves at
most

\[
 2^k\le C=t^{1/18+o(1)}
\tag{4.2}
\]

rows.  This is far below \(t^{5/9-o(1)}\).

The remaining tensor escape is exact and narrow: \(\pi_W(H)\) must be
signed, and the positive mask \(\pi_W(F_0H)\) must compress the \(S\)
distinct projected centre terms into at most

\[
 \frac{SC}{2^k}
\tag{4.3}
\]

occupied quotient fibres.  For the endpoint calibration \(2^k=S\), this
is at most \(C\) fibres.  The aperiodic identity in
`FINITE_QUOTIENT_SHADOW_ESCAPE.md` shows that signed compression exists
for one factor, but no power-large transverse all-subset construction is
known.

This result does **not** prove that an arbitrary exact-block residual
contains an independent \(\Phi_6\) cube, nor that the mixed source masks
in the tensor barrier are scalar copies.  It closes only the
nonnegative-projection route to repairing that explicit barrier.

## 5. Reproduction

~~~bash
python3 verify_phi6_switch_cube_transverse_fiber_rigidity.py
python3 -m unittest -v test_phi6_switch_cube_transverse_fiber_rigidity.py
~~~

The verifier exhausts all one-dimensional binary words through length
12, all masks in a \(3\times3\) rank-two grid, the equality models through
rank six, and the sharp transverse-projection construction.  The
all-parameter claims are proved above.
