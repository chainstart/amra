# Dense ruled-column stability without a complete radial grid

Date: 2026-07-30

## 1. Result

The translated-column theorem in
`AFFINE_HEIGHT_RULED_COLUMN_STABILITY.md` assumes that every pair in
\(\mathcal J\times\mathcal A\) supplies a consecutive vertical column.
Neither completeness nor consecutiveness is needed.  A dense bipartite
incidence graph of columns, each carrying many bounded integer heights,
already forces the same critical distance expansion.

Let
\[
\mathcal J\subset\mathbb Z,\qquad
\mathcal A\subset\mathbb Z_{>0},\qquad |\mathcal J|\ge2,
\]
and let
\[
\mathcal E\subseteq\mathcal J\times\mathcal A
\]
be the set of occupied slope--radial columns.  For every
\((j,a)\in\mathcal E\), let
\[
\mathcal Z_{j,a}\subset[-Z,Z]\cap\mathbb Z,\qquad
|\mathcal Z_{j,a}|\ge H,                            \tag{1}
\]
and suppose that \(P\) contains
\[
 (a,ja,z),\qquad z\in\mathcal Z_{j,a}.              \tag{2}
\]
Put
\[
d_a=|\{j:(j,a)\in\mathcal E\}|,\qquad
\Psi(\mathcal E)=\sum_{a\in\mathcal A}d_a(d_a-1).  \tag{3}
\]
Thus \(\Psi\) is the number of ordered pairs of distinct occupied
columns sharing one radial parameter.  Also put
\[
L=\max\mathcal J-\min\mathcal J,\qquad
R=\max\mathcal A,                                   \tag{4}
\]
\[
T_\times=\max_{1\le n\le RL}\tau(n),               \tag{5}
\]
\[
T_2=\max_{1\le n\le (RL)^2+(2Z)^2}4\tau(n).        \tag{6}
\]

### Theorem 1 (dense lattice ruled-column expansion)

If \(\Psi(\mathcal E)>0\), then
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{H\,\Psi(\mathcal E)}
{|\mathcal J|T_\times T_2}.
}                                                    \tag{7}
\]
In particular, Cauchy--Schwarz gives the parameter-only bound
\[
\boxed{
|\Delta^2(P)|
\ge
\frac{H}
{|\mathcal J|T_\times T_2}
\left(
\frac{|\mathcal E|^2}{|\mathcal A|}
-|\mathcal E|
\right).
}                                                    \tag{8}
\]
The right side of (8) is used only when its parenthesis is positive.

### Corollary 2 (critical dense-column escape)

Fix \(C>0\).  Suppose, as \(t\to\infty\),
\[
\begin{aligned}
&\mathcal J\subset[-Ct,Ct]\cap\mathbb Z,\qquad
  \mathcal A\subset[1,Ct]\cap\mathbb Z,\\
&|\mathcal E|=t^{2-o(1)},\qquad
  H=t^{2-o(1)},\qquad H\le Ct^2,\\
&\mathcal Z_{j,a}\subset[-Ct^2,Ct^2]\cap\mathbb Z
  \quad((j,a)\in\mathcal E).
\end{aligned}                                       \tag{9}
\]
Then
\[
\boxed{|\Delta^2(P)|\ge t^{4-o(1)}.}                \tag{10}
\]

Thus the terminal ruled branch is stable under all three operations:

1. arbitrary deletion of heights inside individual columns;
2. arbitrary bounded integral translations of individual columns; and
3. deletion of \(t^{2-o(1)}\)-density worth of slope--radial pairs.

What remains to be extracted from the four-plane energy is a dense
polynomial-height integer coefficient chart with tall fibres, not a
complete common radial Cartesian product or a height progression.

## 2. Proof of Theorem 1

For \(k\in\mathcal J\), define its radial-star multiplicity
\[
S_k
=
\sum_{\substack{j\in\mathcal J\\j\ne k}}
|\{a:(k,a),(j,a)\in\mathcal E\}|.                  \tag{11}
\]
Every ordered pair counted by \(\Psi\) occurs once in the sum of these
stars, so
\[
\sum_{k\in\mathcal J}S_k=\Psi(\mathcal E).          \tag{12}
\]
Choose \(k_0\) with
\[
S_{k_0}\ge\frac{\Psi(\mathcal E)}{|\mathcal J|}.    \tag{13}
\]

For every pair \((j,a)\) counted by \(S_{k_0}\), retain its sign and put
\[
x=a(j-k_0)\ne0.                                     \tag{15}
\]
For fixed signed \(x\), a positive divisor \(a\mid |x|\) determines
\(j=k_0+x/a\) uniquely.  Every \(x\)-fibre therefore has size at most
\(\tau(|x|)\le T_\times\).  The set
\(\mathcal X\) of resulting products has
\[
|\mathcal X|
\ge
\frac{\Psi(\mathcal E)}
{|\mathcal J|T_\times}.                             \tag{16}
\]

For each \(x\in\mathcal X\), retain one representing pair
\((j_x,a_x)\).  Both \((j_x,a_x)\) and \((k_0,a_x)\) belong to
\(\mathcal E\).  Choose one anchor
\[
z_x^0\in\mathcal Z_{k_0,a_x}
\]
and any \(H\)-element subset
\(\mathcal H_x\subseteq\mathcal Z_{j_x,a_x}\).  The points
\[
\begin{aligned}
p_{x,z}
&=(a_x,j_xa_x,z),\\
q_x
&=(a_x,k_0a_x,z_x^0),
\qquad z\in\mathcal H_x,
\end{aligned}                                       \tag{17}
\]
belong to \(P\).  Their squared distances are
\[
|p_{x,z}-q_x|^2=x^2+(z-z_x^0)^2.                  \tag{18}
\]
For fixed \(x\), the \(H\) integers \(z-z_x^0\) are distinct.
Thus (18) supplies \(|\mathcal X|H\) distinct integer input pairs
\((x,y)\).

Every label is positive and at most
\[
(RL)^2+(2Z)^2.
\]
For fixed \(n\), the number of signed integer pairs satisfying
\[
x^2+y^2=n
\]
is
\[
r_2(n)=4\sum_{d\mid n}\chi_4(d)\le4\tau(n)\le T_2. \tag{19}
\]
Dividing the input count by this fibre bound and using (16) proves
(7).

Finally,
\[
\sum_a d_a^2
\ge\frac{(\sum_a d_a)^2}{|\mathcal A|}
=\frac{|\mathcal E|^2}{|\mathcal A|}.
\]
Since \(\Psi=\sum_a d_a^2-|\mathcal E|\), equation (8) follows.
\(\square\)

## 3. Proof of Corollary 2

The range hypotheses give
\[
RL=O(t^2),\qquad
(RL)^2+(2Z)^2=O(t^4).
\]
The uniform divisor estimate over every fixed polynomial range yields
\[
T_\times T_2=t^{o(1)}.                              \tag{20}
\]
Moreover,
\[
\frac{|\mathcal E|^2}{|\mathcal A|}-|\mathcal E|
=t^{3-o(1)},                                        \tag{21}
\]
because \(|\mathcal A|=O(t)\) and the average radial degree
\(|\mathcal E|/|\mathcal A|=t^{1-o(1)}\) tends to infinity.  Since
\(|\mathcal J|=O(t)\) and \(H=t^{2-o(1)}\), substitution into (8)
gives (10). \(\square\)

## 4. Exact interface gain

The complete-grid hypothesis used previously was
\[
|\mathcal J\times\mathcal A|=t^{2-o(1)}
\quad\text{with every pair occupied}.
\]
Theorem 1 replaces it by the second-moment condition
\[
\Psi(\mathcal E)=t^{3-o(1)},                        \tag{22}
\]
which follows automatically from
\(|\mathcal E|=t^{2-o(1)}\) in \(O(t)\) radial classes.
Equivalently, one only needs a slope--radial incidence graph of
near-maximal edge count.  A single high-codegree base plane is then
forced by averaging.

This does not extract \(\mathcal E\) or the tall lattice fibres from
\(\mathfrak C_{\rm plane}\).  It removes two unnecessary demands from
the missing stability lemma:

- exact completeness of the radial grid; and
- consecutive or aligned vertical height sets.

The still-open bridge is:
\[
\mathfrak C_{\rm plane}\ge t^{13-o(1)}
\quad\Longrightarrow\quad
\text{a dense polynomial-height integer coefficient chart,
or distance expansion}.
\]

## 5. Verification

`verify_dense_ruled_columns.py` constructs incomplete column graphs
with both interval and gapped height fibres, audits (12), selects the
maximizing radial star, checks the signed-product fibre in (15),
and checks the genuine Euclidean distance fibres in (18).  The finite
program is a regression; the arbitrary-parameter proof is Sections
2--3.
