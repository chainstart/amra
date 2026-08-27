# Independent arithmetic alteration: two all-parameter obstructions

This note uses only the promoted fractional cover

\[
w_N(n)=\frac{\log(N/n)}{\log N}
\]

and the promoted theorem IR.1. It does not use unfinished evidence from
another campaign. The conclusions below refute two precise implementations
of M786R-04; they do not refute an adaptive alteration which contracts several
circuit clusters simultaneously. Throughout, logarithms in exponents are
base two and \(N=2^K\).

## 1. Prime-labelled path lemma

Let \(P=v_0v_1\cdots v_{2s}\). Give its \(2s\) edges pairwise coprime
labels \(b_1,\ldots,b_{2s}>1\), and put

\[
q_i=\prod_{e\ni v_i}b_e.
\]

If every \(b_e\) has a prime divisor which divides no other edge label, then

\[
\prod_{i\ {\rm even}}q_i=\prod_{i\ {\rm odd}}q_i.             \tag{1.1}
\]

After multiplying the \(q_i\)'s by powers of two which preserve (1.1), the
resulting \(s+1\)-versus-\(s\) relation is support-minimal. Indeed, the
private prime on \(v_{i-1}v_i\) forces the two endpoint indicators in any
subrelation to agree. Connectedness makes all indicators equal, so the only
subrelations are the empty and full ones.

For odd prime labels put

\[
c_i=\lceil\log q_i\rceil,\qquad
\epsilon_i=c_i-\log q_i\in[0,1).
\]

Give every odd-indexed vertex exponent \(K-c_i\). On the even side start
with the same exponent and subtract integers \(d_i\geq0\) whose total is

\[
\sum_{i\ {\rm even}}d_i
=\Delta:=K-\left(\sum_{i\ {\rm even}}c_i-
                         \sum_{i\ {\rm odd}}c_i\right).       \tag{1.2}
\]

The equality of the unpadded products gives

\[
-s<C:=\sum_{i\ {\rm even}}c_i-\sum_{i\ {\rm odd}}c_i<s+1.    \tag{1.3}
\]

Thus (1.2) is possible when \(K>s+1\). Even distribution gives

\[
\max d_i\leq\left\lceil\frac{K+s}{s+1}\right\rceil.           \tag{1.4}
\]

The padded values

\[
a_i=2^{K-c_i-d_i}q_i\quad(i\ {\rm even}),\qquad
a_i=2^{K-c_i}q_i\quad(i\ {\rm odd})                           \tag{1.5}
\]

give an exact support-minimal bad relation whenever the exponents are
nonnegative. Its exact fractional weight is

\[
\begin{aligned}
W(P)&=\sum_i w_N(a_i)\\
&=\frac{\sum_i\epsilon_i+\Delta}{K}
=1+\frac{2}{K}\sum_{i\ {\rm odd}}\epsilon_i.                 \tag{1.6}
\end{aligned}
\]

For \(s=\lfloor K/4\rfloor\), (1.4) yields

\[
\max d_i\leq5,\qquad a_i>N/64,\qquad
1\leq W(P)<3/2,\qquad\max_i w_N(a_i)<6/K,                    \tag{1.7}
\]

provided all edge labels are at most \(N^{1/8}\) and \(K\) is sufficiently
large. Distinct odd-prime supports make all \(a_i\)'s distinct.

## 2. Obstruction A: exponential raw dependency degree

### Proposition A

For every sufficiently large \(K\), \(H_{2^K}\) contains

\[
M_K\geq\frac{2^{K/10}}{K}                                    \tag{2.1}
\]

support-minimal bad circuits \(C_1,\ldots,C_{M_K}\), all contained in
\((N/64,N]\), such that

\[
C_j\cap C_{j'}=\{x_K\}\quad(j\ne j'),                        \tag{2.2}
\]

and each circuit satisfies (1.7).

Take \(s=\lfloor K/4\rfloor\) and the safe odd internal path index \(r=3\)
(more generally any odd \(3\le r\le2s-3\)).
On every path give the two edges incident with \(v_r\) the labels \(3\)
and \(5\). Give all remaining edges path-specific distinct prime labels in

\[
[N^{1/16},N^{1/8}].                                          \tag{2.3}
\]

The elementary estimate \(\pi(X)\gg X/\log X\) supplies enough primes for
(2.1). Apply (1.2)--(1.5), decrementing only the even shore. Since \(r\)
is odd, the common value

\[
x_K=2^{K-\lceil\log15\rceil}15                               \tag{2.4}
\]

is not decremented. Every other path vertex contains a path-specific odd
prime, proving (2.2). Equations (1.1)--(1.7) prove exact equality,
minimality, and all bounds.

Suppose vertices are independently deleted with probabilities

\[
p_v\leq g(K)w_N(v),\qquad g(K)=o(K).                          \tag{2.5}
\]

Let \(A_j\) be the event that \(C_j\) is uncovered. Then

\[
\Pr(A_j)=\prod_{v\in C_j}(1-p_v)
\geq\exp\bigl(-(3/2+o(1))g(K)\bigr).                         \tag{2.6}
\]

Indeed, \(\max p_v\leq6g(K)/K=o(1)\),
\(\sum_{v\in C_j}p_v\leq(3/2)g(K)\), and
\(\log(1-z)\geq-z/(1-z)\). The events in (2.2) form a clique in the
variable-overlap dependency graph, hence

\[
D_K\geq M_K-1,\qquad
\log D_K\geq(\log2)K/10-O(\log K).                            \tag{2.7}
\]

Consequently any proof whose only compression statistic is maximum raw
circuit-event dependency degree (in particular, the symmetric condition
\(e\Pr(A_j)(D_K+1)\leq1\)) requires

\[
g(K)=\Omega(K)=\Omega(\log N).                               \tag{2.8}
\]

This is not an integrality-gap lower bound: deleting the common witness
\(x_K\) repairs the whole clique. It proves that a successful M05 theorem
must contract common-witness clusters before applying a dependency bound.

## 3. Obstruction B: internal representatives of one packed circuit

### Proposition B

For every sufficiently large \(K\), there is a support-minimal circuit
\(C\subset(N/64,N]\) and support-minimal circuits

\[
S_i\subset(N/128,N]\quad(2\leq i\leq2s-2),\qquad
s=\lfloor K/4\rfloor,                                        \tag{3.1}
\]

such that

\[
S_i\cap C=\{a_i\},                                           \tag{3.2}
\]

and the petals \(S_i\setminus\{a_i\}\) are pairwise disjoint. Therefore
every \(R\subseteq C\) which hits all circuits meeting \(C\) obeys

\[
|R|\geq2s-3\geq K/2-5.                                      \tag{3.3}
\]

Thus no universal rule can replace a packed circuit by \(o(\log N)\)
representatives selected inside that circuit and still hit every residual
circuit meeting it.

Construct \(C=\{a_0,\ldots,a_{2s}\}\) by (1.1)--(1.5), using distinct
primes

\[
N^{1/16}<\ell_1<\cdots<\ell_{2s}<N^{1/8}.                    \tag{3.4}
\]

For \(1\leq i\leq2s-1\),

\[
a_i=2^{t_i}\ell_i\ell_{i+1}.                                 \tag{3.5}
\]

For each \(2\leq i\leq2s-2\), make a new path on \(2s+1\)
vertices and put the intended shared vertex at index \(1\), on its smaller
shore. Label its first two edges by the coprime numbers

\[
A_i=2^{t_i}\ell_i,\qquad B_i=\ell_{i+1},\qquad A_iB_i=a_i.    \tag{3.6}
\]

Label every later edge by a fresh odd prime in the interval (3.4), with
disjoint fresh-prime sets for different \(i\). Every edge label has a
private odd prime.

For the satellite base values \(q_j\), put
\(c_j=\lceil\log q_j\rceil\). Give every nonroot vertex its initial
exponent \(K-c_j\), give the root no extra power of two, and decrement only
the even shore by total

\[
\Delta_i=K-C_i+(K-c_{\rm root}),\qquad
C_i=\sum_{j\ {\rm even}}c_j-\sum_{j\ {\rm odd}}c_j.           \tag{3.7}
\]

Equation (3.7) is exactly equality of total two-adic exponents. Here
\(-s<C_i<s+1\), while \(a_i>N/64\) gives
\(0\leq K-c_{\rm root}\leq5\). Even distribution has maximum decrement
at most \(6\). Also

\[
A_i=a_i/\ell_{i+1}<N^{15/16},                                \tag{3.8}
\]

so all required exponents are nonnegative for large \(K\), and all satellite
values lie in \((N/128,N]\).

Private-prime propagation proves that every \(S_i\) is support-minimal.
Unique factorisation shows that its only member in \(C\) is its root
\(a_i\): the outside endpoint adjacent to \(A_i\) has odd support
\(\{\ell_i\}\), whereas the only singleton odd supports in \(C\) are
\(\{\ell_1\}\) and \(\{\ell_{2s}\}\); all other satellite values contain a
fresh prime. The same support check makes distinct petals disjoint. This
proves (3.2), and (3.3) follows.

## 4. Exact arithmetic compression identity

Write a relation as \(z\in\{-1,0,1\}^{\{2,\ldots,N\}}\), let \(A\) be the
prime-valuation matrix, and put \(\delta(z)=\sum_vz_v\). If two bad
relations \(z,z'\) meet in exactly one vertex \(x\), normalize them so
\(z_x=z'_x=1\). Then

\[
\begin{gathered}
y=z-z'\in\{-1,0,1\}^{\{2,\ldots,N\}},\qquad Ay=0,\\
\operatorname{supp}(y)=
(\operatorname{supp}z\cup\operatorname{supp}z')\setminus\{x\},              \tag{4.1}\\
\delta(y)=\delta(z)-\delta(z').                                             \tag{4.2}
\end{gathered}
\]

Thus unequal normalized defects produce a new bad support on the two petals;
the sole exceptional case is exact normalized-defect equality. The star in
Proposition A lies in that exceptional class: every path has normalized
defect \(-1\), because the common root is on the smaller shore. Equations
(4.1)--(4.2), not raw overlap degree, are the
smallest residue datum that a future witness-contraction theorem must retain.

## 5. Exact surviving interface

For every vertex-disjoint circuit packing \(\mathcal P\),

\[
|\mathcal P|
\leq\sum_{C\in\mathcal P}\sum_{v\in C}w_N(v)
\leq\sum_{v=2}^Nw_N(v)
=(1+o(1))\frac N{\log N}.                                   \tag{5.1}
\]

Hence \(h(N)=o(\log N)\) repair representatives per packed circuit would
close the finite alteration cost. Proposition B refutes this when
representatives are selected independently inside each packed circuit;
Proposition A refutes replacement by a raw maximum-dependency estimate.

The remaining noncircular M05 target is strictly narrower: contract
common-witness clusters and charge representatives across several packed
circuits at once, retaining at least the normalized defect in (4.2), with
total charge \(o(\log N)|\mathcal P|\). No such theorem is proved here, so
neither \(\tau(H_N)=o(N)\) nor the infinite density statement follows.
