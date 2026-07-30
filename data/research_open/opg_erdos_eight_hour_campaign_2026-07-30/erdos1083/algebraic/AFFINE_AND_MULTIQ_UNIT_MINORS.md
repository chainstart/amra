# Exact inverse-symmetrized minors and their failure modes

## Claim ledger

| ID | Result | Status | Relation to Erdős #1083 |
|---|---|---|---|
| A | Exact full minor for arbitrary distinct integral affine shifts | Human proof; exact finite regression | Independent coefficient-container obstruction |
| B | Superfactorial lower bound for integral nodes | Human proof | Strengthens A, but gives no exponent gain |
| C | Union of \(r\) Pell-unit power axes has additive rank exactly \(r+1\) after both inverse symmetrizations | Human proof; exact finite regression | Counterexample to rank-only generalizations |
| D | The axis union has a coefficient box giving \(>1/4\) overlap for every shift, but only \(N^{o(1)}\) parameters | Human proof | Negative result: collapse plus popularity is still insufficient |
| E | Every unit-word family with pairwise distinct coordinate supports has an explicit full row-rank minor | Human proof; exact finite regression | General polynomial-size word-set obstruction |
| F | Low additive rank forces concentration on few coordinate supports | Immediate human corollary of E | Model-specific inverse theorem |
| G | A large ambient-basis determinant does not force a large arbitrary GAP | Explicit counterexample | Prevents an invalid upgrade of A/E |

No item in this file improves the inherited \(3/5\) exponent, constructs a
counterexample to Erdős #1083, or is presently claimed to be new in the
literature.  The contribution is a proved structural boundary for the
algebraic search.

## 1. Arbitrary-node affine-unit determinant

Let \(d\geq4\), let \(a_1,\ldots,a_d\) be distinct integers, and put

\[
 P(x)=\prod_{j=1}^d(x+a_j),\qquad
 q_i(x)=\frac{P(x)}{x+a_i}.
\]

Fix integers \(M\ne0\) and \(h\), and define

\[
 U_i=x+a_i-Mq_i+h,\qquad C_i=x+a_i+Mq_i.
\]

Coefficient rows below are in the ordered basis
\(1,x,\ldots,x^{d-1}\).

### Theorem A

For the \(d\) rows

\[
 U_1,C_1,U_2,C_2,U_3,\ldots,U_{d-2},
\]

\[
\boxed{\left|\det\operatorname{Coeff}
(U_1,C_1,U_2,C_2,U_3,\ldots,U_{d-2})\right|
=4|M|^{d-2}|a_2-a_1|
\left|\prod_{1\le i<j\le d-2}(a_j-a_i)\right|.}
\tag{1}
\]

In particular, the determinant is independent of the common offset \(h\).

### Proof

Work in the exterior power of the \(d\)-dimensional space of polynomials
of degree below \(d\).  Write \(\ell_i=x+a_i\).  For \(i=1,2\),

\[
\begin{aligned}
(-Mq_i+\ell_i+h)\wedge(Mq_i+\ell_i)
  &=-Mq_i\wedge(2\ell_i+h)+h\wedge\ell_i.
\end{aligned}
\tag{2}
\]

In the full wedge of the selected \(d\) rows, a nonzero term must contain
exactly \(d-2\) vectors from
\(\operatorname{span}(q_1,\ldots,q_{d-2})\) and exactly two affine
vectors.  Any use of the last term \(h\wedge\ell_i\) in (2), or of an
affine term from one of \(U_3,\ldots,U_{d-2}\), leaves at least three
affine vectors and therefore vanishes.  Up to sign, the full wedge is
thus

\[
 M^{d-2}q_1\wedge\cdots\wedge q_{d-2}
 \wedge(2\ell_1+h)\wedge(2\ell_2+h).
\tag{3}
\]

The last two factors satisfy

\[
(2x+2a_1+h)\wedge(2x+2a_2+h)
=4(a_2-a_1)x\wedge1.
\tag{4}
\]

It remains to evaluate
\(q_1\wedge\cdots\wedge q_{d-2}\wedge x\wedge1\).
Set

\[
 R(x)=(x+a_{d-1})(x+a_d),\qquad
 p_i(x)=\prod_{\substack{1\le j\le d-2\\j\ne i}}(x+a_j),
\]

so \(q_i=Rp_i\).  Multiplication by the monic quadratic \(R\), followed
by adjoining \(x,1\), gives a block-triangular coefficient change with
unit determinant.  Hence

\[
\left|\det\operatorname{Coeff}(q_1,\ldots,q_{d-2},x,1)\right|
=\left|\det\operatorname{Coeff}(p_1,\ldots,p_{d-2})\right|.
\tag{5}
\]

The \(p_i\) are the scaled Lagrange basis at
\(-a_1,\ldots,-a_{d-2}\); their coefficient determinant is the
Vandermonde product in (1), up to sign.  Equations (3)--(5) prove (1).
\(\square\)

### Corollary B: the consecutive nodes are extremal

For any \(n\) distinct integers \(b_1,\ldots,b_n\),

\[
\left|\prod_{i<j}(b_j-b_i)\right|
\geq\prod_{m=1}^{n-1}m!.
\tag{6}
\]

Indeed, reorder the nodes as \(c_1<\cdots<c_n\).  Then
\(c_j-c_i\geq j-i\), and multiplication gives (6).  Taking
\(n=d-2\) in (1) yields

\[
|\det|\geq
4|M|^{d-2}\prod_{m=1}^{d-3}m!,
\tag{7}
\]

with equality for consecutive nodes with \(|a_2-a_1|=1\).
Thus allowing irregular integral nodes cannot reduce the previously
observed superfactorial determinant.

If \(\theta\) has degree \(d\) and
\(\prod_i(\theta+a_i)=1\), then
\((\theta+a_i)^{-1}=q_i(\theta)\), so (1) is also a number-field
statement.  Without the degree-\(d\) hypothesis, (1) remains a polynomial
identity but need not be an additive-rank statement in
\(\mathbb Q(\theta)\).

### Precise container consequence

For an axis-aligned coefficient box
\[
B=\prod_{j=0}^{d-1}\{0,\ldots,L_j-1\}\subset\mathbb Z^d
\]
whose difference set contains the selected coefficient rows, Hadamard
expansion gives
\[
\prod_jL_j>\frac{|\det|}{d!}.
\tag{8}
\]
The same assertion holds for a general proper rank-\(d\) box only when
the determinant is computed in that box's generator coordinates.
An ambient power-basis determinant alone does **not** give a
basis-independent lower bound for every generalized arithmetic
progression.  This distinction is essential in applying (1).

In fact the unrestricted upgrade is false in the strongest elementary
way.  Given any independent lattice vectors \(h_1,\ldots,h_d\), however
large their determinant in the ambient basis, the proper box
\[
P=\left\{\sum_{i=1}^d m_ih_i:m_i\in\{0,1\}\right\}
\tag{9}
\]
has only \(2^d\) elements and satisfies
\[
|P\cap(P+h_i)|=2^{d-1}
\]
after orienting the translation consistently.  In the generator
coordinates of \(P\), the shift matrix is the identity and its determinant
is \(1\), not the ambient determinant.  Thus A is an exact
**coefficient-box obstruction**, not by itself a theorem about every
low-doubling container.

## 2. A rank-only conjecture fails

Let \(D_1,\ldots,D_r\) have independent squareclasses, and work in the
totally real multiquadratic field
\[
K=\mathbb Q(\sqrt{D_1},\ldots,\sqrt{D_r}).
\]
For each \(i\), choose a positive norm-one Pell unit
\[
\varepsilon_i=A_i+B_i\sqrt{D_i}>1,\qquad
A_i^2-D_iB_i^2=1,\quad A_iB_i\ne0.
\]

The units are multiplicatively independent.  If
\(\prod_i\varepsilon_i^{n_i}=1\), apply the Galois automorphism which
changes only the sign of \(\sqrt{D_i}\), and divide the transformed
identity by the original one.  This gives
\(\varepsilon_i^{-2n_i}=1\), hence \(n_i=0\).

For \(L\ge1\), consider the union of power axes
\[
T_{\rm ax}=\{\varepsilon_i^k:1\le i\le r,\ 1\le k\le L\}.
\tag{10}
\]
Write
\(\varepsilon_i^k=A_{ik}+B_{ik}\sqrt{D_i}\).  For any nonzero integer
\(M\),
\[
\begin{aligned}
\varepsilon_i^k+M\varepsilon_i^{-k}
 &=(1+M)A_{ik}+(1-M)B_{ik}\sqrt{D_i},\\
\varepsilon_i^k-M\varepsilon_i^{-k}
 &=(1-M)A_{ik}+(1+M)B_{ik}\sqrt{D_i}.
\end{aligned}
\tag{11}
\]

### Theorem C

The \(2rL\) elements in (11) span exactly
\[
\operatorname{span}_{\mathbb Q}
\{1,\sqrt{D_1},\ldots,\sqrt{D_r}\},
\]
and therefore have additive rank \(r+1\).  Consequently every minor of
size \(r+2\) vanishes, even though \(T_{\rm ax}\) contains \(rL\)
distinct parameters from a rank-\(r\) multiplicative group.

To see equality rather than only the upper bound, use \(k=1\).  The two
coefficient rows in the coordinates \(1,\sqrt{D_i}\) have determinant
\(4MA_iB_i\ne0\).  They span both \(1\) and \(\sqrt{D_i}\), and varying
\(i\) gives the asserted \(r+1\) dimensions.

This is a counterexample to any proposed theorem which tries to obtain a
minor whose order grows with the total number \(rL\) of parameters using
only multiplicative independence or unit rank.  It does not contradict a
theorem asking for only \(O(r)\) directions under additional support or
nonconcentration hypotheses.

### Popular overlap does not rescue the axes

The collapse in Theorem C is compatible with uniformly popular
translations.  In the coefficient lattice with basis
\(1,\sqrt{D_1},\ldots,\sqrt{D_r}\), let \(H_j\) be the maximum absolute
value of coordinate \(j\) among all shifts in (11), and take
\[
B=\prod_{j=0}^r\{0,\ldots,2H_j\}.
\tag{12}
\]
Every shift in (11) uses only the constant coordinate and one radical
coordinate.  Therefore
\[
\frac{|B\cap(B+h)|}{|B|}
=\prod_{j:h_j\ne0}\left(1-\frac{|h_j|}{2H_j+1}\right)
>\frac14.
\tag{13}
\]

This gives the desired *local* combination of collapsed high minors and
popular overlap.  It still fails the global parameter count.  Since
\(|B_{iL}|\) grows exponentially in \(L\), the radical-coordinate side
lengths in (12) give
\[
\log|B|=\Omega(rL),\qquad |T_{\rm ax}|=rL=O(\log|B|)=|B|^{o(1)}.
\tag{14}
\]
Thus this growing-field family remains far below the required power-law
number of parameters.

## 3. Support-diverse unit words have full row rank

The axis collapse might suggest replacing (10) by products from different
axes.  Let \(\mathcal W\) be an arbitrary family of distinct subsets of
\([r]\), and form the Boolean unit words
\[
T_{\mathcal W}=
\left\{t_S=\prod_{i\in S}\varepsilon_i:S\in\mathcal W\right\}.
\tag{15}
\]

Use the radical basis
\[
e_T=\prod_{i\in T}\sqrt{D_i},\qquad T\subseteq[r].
\]
The coefficient of \(e_T\) in \(t_S\) vanishes unless \(T\subseteq S\);
when \(T\subseteq S\), it equals
\[
\prod_{i\in T}B_i\prod_{i\in S\setminus T}A_i.
\tag{16}
\]
Inversion multiplies this coefficient by \((-1)^{|T|}\).

### Theorem E

Order \(\mathcal W\) by nondecreasing cardinality and select from the
coefficient matrix of
\((t_S+Mt_S^{-1})_{S\in\mathcal W}\) the columns
\((e_T)_{T\in\mathcal W}\) in the same order.  For \(M\ne\pm1\), the
resulting \(|\mathcal W|\)-minor is
\[
\boxed{
\det_{\mathcal W}=
\prod_{S\in\mathcal W}
\left[
\bigl(1+M(-1)^{|S|}\bigr)
\prod_{i\in S}B_i
\right]\ne0.}
\tag{17}
\]

Indeed, (15) makes the selected matrix lower triangular: a nonzero entry
in row \(S\), column \(T\) requires \(T\subseteq S\), hence
\(|T|\le|S|\), and equality of the cardinalities forces \(T=S\).
The diagonal entries are precisely the factors in (17).

This proves full row rank for **every** Boolean word family, including
families of only polynomial size in \(r\); it is not merely a calculation
for the full cube.  Quantitatively, for integral Pell units and
\(|M|>1\),
\[
|\det_{\mathcal W}|\ge (|M|-1)^{|\mathcal W|}.
\tag{18}
\]

The same triangular argument is not restricted to exponents zero and one.
Let
\[
t_\alpha=\prod_{i=1}^r\varepsilon_i^{k_{\alpha i}},
\qquad k_{\alpha i}\in\mathbb Z_{\ge0},
\]
and suppose the supports
\[
S_\alpha=\{i:k_{\alpha i}>0\}
\]
are pairwise distinct.  Write
\[
\varepsilon_i^{k_{\alpha i}}
=A_{i,k_{\alpha i}}+B_{i,k_{\alpha i}}\sqrt{D_i}.
\]
Selecting the radical columns \(e_{S_\alpha}\), ordered by support
cardinality, again gives a lower triangular matrix.  Its determinant is
\[
\boxed{
\prod_\alpha
\left[
\bigl(1+M(-1)^{|S_\alpha|}\bigr)
\prod_{i\in S_\alpha}B_{i,k_{\alpha i}}
\right]\ne0.}
\tag{19}
\]
Therefore arbitrary positive powers are allowed: the operative condition
is diversity of coordinate supports, not squarefreeness of the word.
Repeated powers on the same support, as in the axes (10), are exactly the
concentration pattern not covered by this theorem.

### Corollary F: a support-concentration inverse theorem

Let \(\mathcal T\) be any finite family of words
\(\prod_i\varepsilon_i^{k_i}\), and let \(\sigma(\mathcal T)\) be the
number of distinct supports \(\{i:k_i>0\}\) represented in the family.
Then, for \(M\ne\pm1\),
\[
\dim_{\mathbb Q}
\operatorname{span}\{t+Mt^{-1}:t\in\mathcal T\}
\geq \sigma(\mathcal T).
\tag{20}
\]
Choose one word from every support and apply (19).  In particular, if
the additive rank is at most \(R\), all words lie on at most \(R\)
supports, and one support contains at least
\(|\mathcal T|/R\) words.

This is a genuine inverse statement inside the multiquadratic coordinate
model: minor collapse forces support concentration.  It is not yet an
inverse theorem for arbitrary number fields or arbitrary low-doubling
containers.

There is nevertheless a basis-independent rank consequence.  If the
difference set of a generalized arithmetic progression \(P\) contains
all these shifts, then
\[
\operatorname{rank}(P)\geq\sigma(\mathcal T),
\tag{21}
\]
because the shifts lie in the rational span of its generators.  If \(P\)
is an infinitely proper coordinate box with all side lengths at least
two, then
\[
\frac{|P+P|}{|P|}
=\prod_{j=1}^{\operatorname{rank}(P)}
\frac{2L_j-1}{L_j}
\geq(3/2)^{\sigma(\mathcal T)}.
\tag{22}
\]
Thus, with \(n=|P|\), a word family representing \(n^c\) distinct
supports cannot live in this box model while retaining \(n^{o(1)}\)
doubling.  The escape exposed
by Theorem C is precisely to place many words on the same small collection
of supports; equation (14) then shows that the simplest such escape still
has too few parameters.

For the complete family \(\mathcal W=2^{[r]}\), (17) specializes to
\[
\left|\det\operatorname{Coeff}
(t_S+Mt_S^{-1})_{S\subseteq[r]}\right|
=|1-M^2|^{2^{r-1}}
\prod_{i=1}^r|B_i|^{2^{r-1}}.
\tag{23}
\]
Equivalently, its unsymmetrized coefficient matrix is the Kronecker
product
\[
\bigotimes_{i=1}^r
\begin{pmatrix}1&0\\A_i&B_i\end{pmatrix}.
\]
Thus inverse symmetrization creates rather than removes a
coefficient-volume obstruction throughout the Boolean cube.

Together, Theorems C and E identify the relevant missing hypothesis in a
future inverse theorem: multiplicative rank alone is inadequate, while
occupancy across many support patterns can force full additive rank.
Any potentially useful theorem must quantify this support
nonconcentration and must express its determinant in the candidate
container's own coordinates.

## 4. Reproducibility

Run

```bash
python3 verify_affine_minor_and_torus_axes.py
python3 -m unittest -v test_verify_affine_minor_and_torus_axes.py
```

The exact certificate uses five irregular node sets, four offsets for
each, all consecutive degrees \(4\) through \(10\), and the independent
Pell units
\[
3+2\sqrt2,\quad2+\sqrt3,\quad9+4\sqrt5,\quad8+3\sqrt7.
\]
The current canonical certificate hash is

```text
fc40bc9d2097d3b76d45aea54b60f37fb2b0b04965e8913975d5f7a608e9d4a1
```
