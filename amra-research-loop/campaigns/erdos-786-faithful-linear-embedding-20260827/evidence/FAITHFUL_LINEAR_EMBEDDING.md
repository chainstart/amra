# Faithful arithmetic realization of finite linear hypergraphs

## Theorem

Let \(G=(X,\mathcal E)\) be a finite simple linear hypergraph with
\(X=\bigcup_{e\in\mathcal E}e\), maximum degree \(D\), and no empty edge.
Let
\[
 r=\lceil\log _2(D+1)\rceil+1.
\]
Suppose that integers \(K\ge1\) and \(B\ge3\) satisfy
\[
 \min_{e\in\mathcal E}|e|>K,\qquad
 \pi(B)-1\ge r|X|,\qquad
 2r\log _2B+5\le K. \tag{1}
\]
Then there is a family \(\mathcal R_K(G)\) of unequal-cardinality
equal-product relations with the following properties.

1. There is one relation \(S_e\) for every \(e\in\mathcal E\).  If
   \(|e|=m\), its shores have sizes \(m\) and \(m+1\), so its oriented
   cardinality defect is \(-1\).
2. Every integer in every support belongs to \((2^K/32,2^K]\).
3. Each relation vector is a primitive circuit of its prime-valuation
   matrix.  In particular, it is support-minimal.
4. For distinct \(e,f\in\mathcal E\),
   \[
      |S_e\cap S_f|=|e\cap f|,
   \]
   and the common integer, when it exists, is the label of the common host
   vertex.
5. The edge-intersection graph, matching number, and transversal number are
   preserved:
   \[
      \nu(\mathcal R_K(G))=\nu(G),\qquad
      \tau(\mathcal R_K(G))=\tau(G).
   \]

The construction is explicit once the prime blocks, one ordering of every
edge, and one orientation of every assigned bipartition are fixed.

## 1. Degree-coded prime blocks

There are
\[
 2^{r-1}-1\ge D
\]
unordered nontrivial bipartitions of an \(r\)-element set.  By (1), choose
\(r|X|\) distinct odd primes not exceeding \(B\), and split them into
disjoint blocks \(R_x\) of size \(r\), one block for each \(x\in X\).

Assign a distinct unordered nontrivial bipartition of \(R_x\) to each edge
\(e\ni x\).  Orient it arbitrarily and write
\[
 R_x=R^-_{x,e}\mathbin{\dot\cup}R^+_{x,e},\qquad
 \alpha_{x,e}=\prod_{p\in R^-_{x,e}}p,\qquad
 \beta_{x,e}=\prod_{p\in R^+_{x,e}}p.
\]
The shared raw value
\[
 a_x=\alpha_{x,e}\beta_{x,e}=\prod_{p\in R_x}p
\]
does not depend on the incident edge.

Fix an edge \(e=\{x_1,\ldots,x_m\}\), in any order.  Give a path on
\(2m+1\) vertices the successive edge labels
\[
 \alpha_{x_1,e},\beta_{x_1,e},\ldots,
 \alpha_{x_m,e},\beta_{x_m,e}.
\]
One parity class has the \(m\) shared raw values \(a_{x_i}\).  The other
has the \(m+1\) private raw values
\[
 b_0=\alpha_{x_1,e},\quad
 b_j=\beta_{x_j,e}\alpha_{x_{j+1},e}\ (1\le j<m),\quad
 b_m=\beta_{x_m,e}.
\]
Every path-edge label occurs once in each parity class, and therefore
\[
 \prod_{i=1}^m a_{x_i}=\prod_{j=0}^m b_j. \tag{2}
\]

## 2. Explicit two-adic balancing

Put \(M=2^K\),
\[
 c_x=\lceil\log _2a_x\rceil,
 \qquad u_x=2^{K-c_x-2}a_x.
\]
Every \(a_x\) is odd and greater than one, so it is not a power of two and
\[
 M/8<u_x<M/4. \tag{3}
\]

For the private raw values put \(d_j=\lceil\log _2b_j\rceil\).  Before a
correction, \(2^{K-d_j}b_j\in(M/2,M)\).  Define
\[
 C_e=\sum_{j=0}^m d_j-\sum_{i=1}^m c_{x_i},
 \qquad
 \Delta_e=K-C_e+2m. \tag{4}
\]
After cancelling the exact logarithms by (2), \(C_e\) is the sum of
\(m+1\) ceiling errors in \((0,1)\) minus the sum of \(m\) such errors.
Consequently
\[
 -m<C_e<m+1.
\]
Since \(m>K\),
\[
 0<\Delta_e<K+3m<4(m+1). \tag{5}
\]

Write
\[
 \Delta_e=h_e(m+1)+s_e,
 \qquad 0\le s_e<m+1,
\]
and define the decrement vector explicitly by
\[
 t_j=\begin{cases}
 h_e+1,&0\le j<s_e,\\
 h_e,&s_e\le j\le m.
 \end{cases} \tag{6}
\]
Then
\[
 \sum_{j=0}^m t_j=\Delta_e,
 \qquad
 \max_jt_j=\left\lceil\frac{\Delta_e}{m+1}\right\rceil\le4. \tag{7}
\]
Define
\[
 v_{j,e}=2^{K-d_j-t_j}b_j.
\]
Each private raw value uses primes from at most two blocks, so
\(d_j\le2r\log _2B+1\).  Equations (1) and (7) give
\(K-d_j-t_j\ge0\).  Moreover,
\[
 M/32<v_{j,e}\le M. \tag{8}
\]

The equality of total two-adic exponents is not implicit: using (4), (6),
and \(C_e=\sum d_j-\sum c_{x_i}\), one obtains
\[
\begin{aligned}
 \sum_{j=0}^m(K-d_j-t_j)
 &= (m+1)K-\sum_{j=0}^m d_j-\Delta_e\\
 &= mK-\sum_{i=1}^m c_{x_i}-2m\\
 &= \sum_{i=1}^m(K-c_{x_i}-2).
\end{aligned} \tag{9}
\]
Together, (2) and (9) prove
\[
 \prod_{i=1}^m u_{x_i}=\prod_{j=0}^m v_{j,e}. \tag{10}
\]

## 3. Primitive valuation circuits

Let \(V_e\) be the matrix whose columns are indexed by the \(2m+1\)
integers in (10), whose rows are indexed by their prime divisors, and whose
entry in row \(p\), column \(z\) is \(v_p(z)\).

For each edge of the auxiliary path, choose one prime from its nonempty
label.  That prime occurs on exactly the two endpoint columns of that path
edge and nowhere else in the relation.  Hence every vector
\(\gamma\in\ker_{\mathbb Q}V_e\) satisfies
\[
 \gamma_z+\gamma_{z'}=0
\]
on each adjacent pair \(zz'\).  Connectivity of the path forces
\(\gamma\) to be a scalar multiple of the full alternating vector.
Equation (10) shows that this alternating vector also satisfies the row for
the prime two.  Thus the complete valuation kernel is one-dimensional.
Its primitive integral generator has every coefficient equal to \(1\) or
\(-1\) and has full support.  It is therefore a primitive circuit, and no
proper cancelled equal-product subrelation exists.

## 4. Incidence fidelity

The odd-prime block footprint of an integer is the set of \(x\in X\) whose
block \(R_x\) contributes a prime divisor.  A shared value \(u_x\) has
footprint \(\{x\}\) and uses the full block.  A private endpoint has a
one-point footprint and uses a nonempty proper half.  A private internal
vertex has a two-point footprint and uses nonempty proper halves of two
blocks.

Within one relation, the footprint identifies every path position.  Across
two relations, a two-point footprint cannot recur because linearity forbids
one vertex pair from lying in two different host edges.  At a one-point
footprint, different incident edges use different unordered bipartitions;
equality of either selected half would force equality of the two unordered
partitions.  Powers of two do not change odd parts.  Consequently all
private values are globally edge-unique, no private value equals a shared
value, and two relation supports meet exactly in the shared labels of the
host-edge intersection.  Since the host is linear, this intersection has
size zero or one.

It follows immediately that a set of relation supports is pairwise disjoint
if and only if the corresponding host edges are pairwise disjoint.  Hence
the matching numbers agree, and the edge-intersection graphs are isomorphic.

Every transversal of \(G\) maps through \(x\mapsto u_x\) to a transversal
of \(\mathcal R_K(G)\), so
\(\tau(\mathcal R_K(G))\le\tau(G)\).  Conversely, start with any transversal
of \(\mathcal R_K(G)\).  Retain each selected shared label.  Replace every
selected private value, which lies on one support \(S_e\), by an arbitrary
shared label \(u_x\) with \(x\in e\).  The replacement can only decrease
cardinality, and the resulting shared labels still meet every support.
Their host vertices form a transversal of \(G\).  Therefore
\(\tau(G)\le\tau(\mathcal R_K(G))\), proving equality and the theorem.

## 5. Projective-plane specialization

For \(G=\mathrm{PG}(2,q)\), take \(D=q+1\),
\(|X|=q^2+q+1\), \(B=q^6\), and
\(r=\lceil\log _2(q+2)\rceil+1\).  The prime number theorem gives the prime
budget for large \(q\).  The predecessor estimate
\(12(\log _2q+3)\log _2q<K/4\) implies the bit-budget inequality in (1),
and its choice \(q>K\) gives the edge-size condition.  The exact equalities
\(\nu=1\) and \(\tau=q+1\) of the projective-plane line hypergraph therefore
transfer without a separate arithmetic hitting calculation.

## Boundary

The theorem is conditional on the explicit prime and scale budget and on
linearity.  It does not realize arbitrary non-linear hypergraphs by the same
two-block footprint construction, remove the minimum-edge-size hypothesis,
bound the transversal number of the full equal-product hypergraph, or settle
the infinite density-one problem.
