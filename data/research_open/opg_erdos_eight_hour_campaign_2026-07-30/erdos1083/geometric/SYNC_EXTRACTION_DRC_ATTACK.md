# Erdős #1083: DRC and entropy audit of the synchronization bridge

Date: 2026-07-30

## 0. Status

- **HUMAN PROOF:** source incidences alone force one rich angular column,
  but do not force even two active angles on one common fibre.  This is
  optimal under the inherited marginals.
- **HUMAN PROOF:** a weighted dependent-random-choice argument extracts
  fixed-size sets of rotation labels that are simultaneously dense on
  \(N^{2/5-o(1)}\) fibres.
- **HUMAN PROOF:** neither certificate supplies the anchored same-radius
  incidence energy required by `SPARSE_ANGLE_INCIDENCE_EXPANSION.md`.
- **FINITE REGRESSION:** the verifier checks the exact split extremizer and
  the weighted distinct-angle DRC inequality.
- **OPEN GAP:** there is no unconditional improvement over the \(3/5\)
  distance exponent.

The obstruction here is combinatorial and differs from the conic-incidence
route.

## 1. Weighted fibres–angles data

Remove the harmless common-axis contribution.  For an off-axis circular
fibre \(C\), put
\[
a_C=|A_C|.
\]
For an active angle \(\alpha\), define
\[
s_{C,\alpha}
 =|A_C\cap\{\alpha,\alpha+\pi\}|\in\{0,1,2\},
\qquad
w_{C,\alpha}
 =|A_C\cap(A_C+2\alpha)|.
\]
Then
\[
q_\alpha^\circ=\sum_Cs_{C,\alpha},\qquad
r_\alpha^\circ=\sum_Cw_{C,\alpha},
\tag{1}
\]
with
\[
0\le w_{C,\alpha}\le a_C,\qquad
\sum_Ca_C=N.
\tag{2}
\]

At the inherited critical node,
\[
\begin{aligned}
D&=N^{3/5+o(1)},\\
M&=N^{1/5-o(1)},\\
q_\alpha^\circ&\ge Q-o(Q)=N^{3/5+o(1)},\\
r_\alpha^\circ&\ge R-o(R)=N^{1-o(1)}.
\end{aligned}
\tag{3}
\]
Only the exponent content of (3), not additive near-equality \(R=N-o(N)\),
is inherited.

## 2. The exact source-incidence extraction limit

Let \(G_s\) be the unweighted bipartite graph whose left vertices are the
active angles and whose right vertices are the circular fibres, with
\(\alpha C\) an edge when \(s_{C,\alpha}>0\).

### Theorem 1: optimal marginal source rectangle — HUMAN PROOF

Every active angle has at least
\[
\left\lceil q_\alpha^\circ/2\right\rceil
\]
neighbouring fibres.  Thus the marginals force
\[
K_{1,\lceil(Q-o(Q))/2\rceil}.
\tag{4}
\]
They do not force \(K_{2,1}\): there are admissible angular-fibre systems at
the critical exponents in which every source fibre is incident to exactly
one active angle.

Proof.  The lower bound follows from \(s_{C,\alpha}\le2\).  The construction
in Section 3 has \(s_{C,\alpha}\in\{0,1\}\), left degree \(Q\), right degree
one, and hence zero codegree for every pair of angles. \(\square\)

Consequently the largest guaranteed source rectangle has exactly one angle.
No DRC argument using only these source marginals can produce a common
two-angle fibre.

## 3. A split source–rotation extremizer

The original extremizer in `CIRCLE_INTERFACE_NO_GO.md` puts the same angular
progression on every fibre.  It is therefore a best-case synchronization
example, despite being an obstruction to marginal capacity estimates.  The
following split version is the relevant extraction stress test.

For an integer \(t\ge3\), set
\[
N=t^5,\quad D_0=t^3,\quad M=t,\quad Q=t^3,\quad
S=t^2.
\]
Choose \(\theta/\pi\) irrational and active angles
\(\alpha_j=j\theta\), \(1\le j\le t\).

### Rotation reservoir

Take
\[
F_0=t^2(t-1)
\]
fibres of size \(S\).  On the \(C\)-th reservoir fibre use a generically
translated progression
\[
A_C=\{\phi_C+K\theta,\ldots,\phi_C+(K+S-1)\theta\},
\tag{5}
\]
where \(K>2t\).  Choose the phases \(\phi_C\) so that no active source angle
or antipode occurs and, if desired, no angular point is shared by two
reservoir fibres.  Translation does not change the correlation:
\[
w_{C,\alpha_j}=S-2j.
\tag{6}
\]

### Disjoint source fibres

For each \(j\), take \(Q=t^3\) new singleton fibres containing only
\(\alpha_j\).  Use disjoint fibres for different \(j\)'s.  These give
\[
q_{\alpha_j}=Q
\]
and no rotation success.

The total mass is
\[
F_0S+MQ=t^4(t-1)+t^4=t^5=N.
\]
Moreover
\[
r_{\alpha_j}=F_0(S-2j),
\]
so
\[
\min_jr_{\alpha_j}
=t^3(t-1)(t-2)
=N\left(1-\frac3t+\frac2{t^2}\right).
\tag{7}
\]
All reservoir fibres have only \(S-1<D_0\) nonzero chord labels; singleton
fibres have none.

The source graph is the disjoint union of \(M\) stars of degree \(Q\):
\[
\max_C\deg_{G_s}(C)=1,\qquad
\max_{\alpha\ne\beta}|N_s(\alpha)\cap N_s(\beta)|=0.
\tag{8}
\]
Nevertheless
\[
\sum_\alpha q_\alpha r_\alpha=t^{9}(1-o(1)),
\]
and all inherited single-axis capacity exponents are respected.

The reservoir and source fibres can also be assigned unrelated radii, with
all source radii distinct.  Thus the marginals do not force a nontrivial
same-radius source incidence class.

This is an abstract angular-fibre extremizer, not an \(N\)-point Euclidean
few-distance configuration.  Its role is to prove logical insufficiency of
the listed marginals.

## 4. What weighted DRC does recover

The rotation data are much denser than the source graph.  Normalize
\[
\mu(C)=a_C/N,\qquad
f_\alpha(C)=w_{C,\alpha}/a_C\in[0,1],
\]
omitting empty fibres.  Put
\[
\rho=R/N.
\]
Then
\[
\mathbb E_\mu f_\alpha\ge\rho.
\tag{9}
\]

Fix \(0\le\tau<\rho\), and join \(\alpha\) to \(C\) when
\[
f_\alpha(C)\ge\tau.
\]
Writing
\[
p=\frac{\rho-\tau}{1-\tau},
\tag{10}
\]
(9) gives
\[
\mu(N(\alpha))\ge p
\tag{11}
\]
for every active angle.

For an integer \(h\le M\), let \(\mathcal B_h(x)\) be the linear
interpolation of \(\binom d h\) between the integers
\(\lfloor x\rfloor,\lceil x\rceil\).

### Theorem 2: weighted distinct-angle DRC — HUMAN PROOF

Some \(h\) distinct active angles are simultaneously \(\tau\)-dense on a
set of fibres of \(\mu\)-mass at least
\[
\boxed{
\frac{\mathcal B_h(Mp)}{\binom Mh}.
}
\tag{12}
\]
If \(a_C\le A_{\max}\), the number of common fibres is at least
\[
\frac{N}{A_{\max}}
\frac{\mathcal B_h(Mp)}{\binom Mh}.
\tag{13}
\]

Proof.  Let \(d_C\) be the number of threshold incidences at \(C\).
Averaging common neighbourhood mass over all \(h\)-subsets of angles gives
\[
\frac1{\binom Mh}\sum_C\mu(C)\binom{d_C}{h}.
\]
Equation (11) implies
\[
\sum_C\mu(C)d_C\ge Mp.
\]
The sequence \(d\mapsto\binom dh\) is discretely convex, since its second
difference is \(\binom d{h-2}\).  Jensen with its lower convex envelope
proves (12).  Since every fibre has mass at most \(A_{\max}/N\), (13)
follows. \(\square\)

At (3), choose \(\tau=\rho/2\).  Then \(p=N^{-o(1)}\).  With
\(A_{\max}\ll D\), every fixed \(h\) gives
\[
N^{2/5-o(1)}
\]
common rotation-dense fibres.

More generally, the DRC guarantee remains nonempty only while roughly
\[
h\lesssim
\frac{\log(N/D)}{\log(1/p)}
\tag{14}
\]
and \(h\le Mp\).  Because \(p=N^{-o(1)}\) is the only inherited control,
(14) does not force \(h=N^\varepsilon\) for any fixed \(\varepsilon>0\).

Most importantly, a rotation label \(\alpha\) records many pairs separated
by \(2\alpha\); it does not say that the angular point \(\alpha\) itself is
present.  The split extremizer makes this distinction literal.  Theorem 2
therefore does not produce the source columns required by the sparse
height–angle theorem.

## 5. Dyadic regularization and entropy

Thresholding in (10) is the lossless form of the relevant dyadic
regularization: it first normalizes by fibre mass and then keeps a dense
level.  Dyadically splitting the raw \(w_{C,\alpha}\)'s can reproduce (12)
up to logarithms, but cannot couple \(w\) to \(s\).

The split construction is already fully regular on the source side:

- every nonzero source weight equals one;
- every angle degree equals \(Q\);
- every source-fibre degree equals one.

Thus no dyadic cell has hidden overlap.

For a uniformly random source incidence \((\boldsymbol\alpha,\mathbf C)\),
the construction has
\[
H(\boldsymbol\alpha\mid\mathbf C)=0,\qquad
H(\mathbf C\mid\boldsymbol\alpha)=\log Q.
\]
The marginals force many choices of fibre after an angle is known, but they
do not force uncertainty—or reuse—of the angle after a fibre is known.
Entropy restates the obstruction rather than removing it.

## 6. Interface with sparse angle incidence expansion

Expanding the plane incidences into actual angular positions gives, across
all fibres,
\[
J\le2M,\qquad
I\ge\sum_\alpha q_\alpha^\circ
\ge M(Q-o(Q))=N^{4/5-o(1)}.
\tag{15}
\]
This is the strongest unconditional global sparse-incidence certificate
from the source marginals.

However, `SPARSE_ANGLE_INCIDENCE_EXPANSION.md` needs those incidences inside
one anchored common-radius family.  Neither (15) nor Theorem 2 supplies:

1. a repeated radius;
2. an actual anchor point compatible with the reused columns;
3. controlled squared-height difference multiplicity.

The split extremizer may give every source fibre a different radius.
Therefore a single radius class can contain only one incidence even though
the global count in (15) is \(N^{4/5}\).

## 7. Minimal additional cross-fibre statistic

For a common-radius family with an actual anchor \(p_0\), let

- \(E_{\rho,p_0}\) be its height–angle incidence graph;
- \(I_{\rho,p_0}=|E_{\rho,p_0}|\);
- \(J_{\rho,p_0}\) be its number of angular columns;
- \(\lambda_{\rho,p_0}\) be the maximum nonzero difference multiplicity of
  its squared height offsets.

Define the anchored same-radius expansion statistic
\[
\Xi=
\max_{\rho,p_0}
\frac{I_{\rho,p_0}^2}
 {2I_{\rho,p_0}+\lambda_{\rho,p_0}J_{\rho,p_0}^2}.
\tag{16}
\]
The sparse incidence theorem gives \(D\ge\Xi-1\).

Thus the minimum extra Euclidean input for this route is
\[
\boxed{\Xi\ge N^{3/5+\varepsilon}.}                 \tag{17}
\]
It is one scalar statement combining exactly the cross-fibre information
missing from the marginals: equal radius, anchored column reuse, and height
offset collision control.

The split extremizer shows that \(M,Q,R\), total mass, and per-fibre chord
caps do not lower-bound \(\Xi\) nontrivially.  Any proof of (17) must spend a
cross-fibre distance statistic—for example, a radius-conditioned endpoint
reuse estimate together with a bound on squared-height difference energy.

## 8. Exponent ledger

| quantity or extraction | forced scale | consequence |
|---|---:|---|
| \(D\) at inherited threshold | \(N^{3/5+o(1)}\) | baseline |
| active angles \(M\) | \(N^{1/5-o(1)}\) | input |
| source degree \(Q\) | \(N^{3/5+o(1)}\) | input |
| global source mass \(MQ\) | \(N^{4/5-o(1)}\) | arbitrary fibres |
| guaranteed source rectangle | \(1\times N^{3/5-o(1)}\) | optimal |
| common source fibre for two angles | none | split extremizer |
| fixed-\(h\) rotation common fibres | \(N^{2/5-o(1)}\) | shift labels only |
| guaranteed one-radius source mass | \(O(1)\) | no sparse gain |
| required anchored statistic \(\Xi\) | \(N^{3/5+\varepsilon}\) | open |

The unconditional exponent remains
\[
\boxed{3/5.}
\]

## 9. Claim boundary and reproduction

Theorem 1, the split-extremizer construction, Theorem 2, and the diagnosis
of (16) are human arguments.  The verifier checks exact integer scales and
the convex DRC inequality on finite weighted binary graphs.

No Euclidean \(N\)-point counterexample and no unconditional improvement of
\(f_3(N)\) is claimed.

```bash
python3 verify_sync_extraction_drc.py
pytest -q test_verify_sync_extraction_drc.py
```

The saved certificate is `sync_extraction_drc_certificate.json`.
