# Blind reconstruction of RR.1--RR.3

This draft was written from the closure contract and decisive-lemma statement
only, before opening the author's proof evidence or verifier.

## Variant and notation

A bad relation consists of disjoint finite sets \(S,T\subset\{2,\ldots,N\}\)
with

\[
\prod_{a\in S}a=\prod_{b\in T}b,\qquad |S|\ne|T|.
\]

Support-minimal means that no nonempty proper subset of \(S\cup T\) supports
another unequal-cardinality equal-product relation. Coefficients in any
candidate subrelation are therefore in \(\{-1,0,1\}\).

## RR.1: independent construction

Fix \(L\geq3\) and \(s\geq L\). Let \(N=2^K\), \(y=N^{1/L}\), and let
\(K\) tend to infinity. Standard prime distribution supplies distinct
increasing primes

\[
y<p_1<\cdots<p_{2s}<C_s y                                   \tag{B1}
\]

for a constant \(C_s\). On the path \(v_0v_1\cdots v_{2s}\), label
\(v_{i-1}v_i\) by \(p_i\) and define

\[
q_i=\prod_{e\ni v_i}p_e.
\]

The two path shores satisfy

\[
\prod_{i\ {\rm even}}q_i=\prod_{i\ {\rm odd}}q_i
=\prod_{j=1}^{2s}p_j,                                       \tag{B2}
\]

and have sizes \(s+1\) and \(s\).

Put \(c_i=\lceil\log_2 q_i\rceil\). Initially pad each vertex to
\(2^{K-c_i}q_i\in(N/2,N]\). Since the logarithms in (B2) cancel,

\[
-s<C:=\sum_{i\ {\rm even}}c_i-\sum_{i\ {\rm odd}}c_i<s+1.    \tag{B3}
\]

The difference between the initial total two-adic exponents on the two
shores is

\[
\Delta=K-C>0.                                                \tag{B4}
\]

Subtract nonnegative integers of total \(\Delta\) from the \(s+1\) even-side
exponents, as evenly as possible. The maximum subtraction is

\[
d_{\max}\leq\left\lceil\frac{K+s}{s+1}\right\rceil
=\frac{K}{s+1}+O_s(1).                                      \tag{B5}
\]

The resulting products remain equal. Their exponents are nonnegative for
large \(K\), because internal vertices obey

\[
c_i\leq\frac{2K}{L}+O_s(1),\qquad
\frac2L+\frac1{s+1}<1                                       \tag{B6}
\]

for \(L\geq3,\ s\geq L\). Every resulting integer exceeds
\(N^{1-1/L}\), since

\[
\frac1{s+1}<\frac1L                                         \tag{B7}
\]

and the \(O_s(1)\) ceiling loss is absorbed for large \(K\).

Each active prime \(p_i>y\) occurs squarefreely at the two endpoints of its
path edge, so maximum active degree is two and the active-incidence graph is
the increasingly labelled path.

For support-minimality, write a subrelation as signs
\(z_i\in\{-1,0,1\}\). The \(p_i\)-valuation equation is

\[
z_{i-1}+z_i=0.                                               \tag{B8}
\]

Connectedness forces \(z_i=(-1)^iz_0\) for every \(i\). Hence \(z=0\), or
the full displayed relation, or its reverse. Distinct active-prime supports
also make the constructed integers distinct. This proves RR.1 for
arbitrarily large powers \(N=2^K\).

## RR.2: independent construction

Let \(A,B\) be disjoint nonempty prime sets of sizes \(r,s\), let
\(r\ne s\), and let \(p>\max(A\cup B)\). Write

\[
P_A=\prod_{a\in A}a,\qquad P_B=\prod_{b\in B}b.
\]

The two shores

\[
A\cup\{pP_B\},\qquad B\cup\{pP_A\}                           \tag{B9}
\]

are disjoint Finsets and satisfy

\[
P_A(pP_B)=P_B(pP_A).                                        \tag{B10}
\]

Their cardinalities \(r+1,s+1\) are unequal. For every \(a\in A\), its
valuation equation ties the coefficient of the prime vertex \(a\) to that
of \(pP_A\); every \(b\in B\) similarly ties \(b\) to \(pP_B\); and the
\(p\)-equation ties the two composite terms with opposite signs. Thus every
nonzero subrelation uses the full support, proving support-minimality.

The top \(p\)-fibre has one term on each shore. Removing \(p\) leaves the
coprime residue ratio \(P_B/P_A\), whose numerator and denominator supports
have arbitrary unequal sizes. This is the asserted residue-complexity
obstruction.

## RR.3: independent reconstruction

For a relation \(S,T\), expand each \(n\) into its multiset of prime
occurrences. For every prime, match all occurrences on \(S\) to all
occurrences on \(T\), arbitrarily. This gives a bipartite multigraph \(G\)
on \(S\cup T\); an edge is a matched prime occurrence and

\[
\deg_G(n)=\Omega(n).                                        \tag{B11}
\]

Every such occurrence matching is connected. Otherwise, each graph
component separately has balanced valuation for every prime, hence equal
products on its two local shores. Since the total shore cardinalities are
unequal, at least one component has unequal local shore cardinalities. It
would be a proper bad subrelation, contradicting support-minimality.

Put \(h=|S|+|T|\) and \(q=|E(G)|\). If every term has
\(\Omega(n)\geq d\), then, because both shore degree sums equal \(q\),

\[
q\geq d\max(|S|,|T|)\geq\frac{d(h+1)}2.                     \tag{B12}
\]

The cycle rank of the connected multigraph is therefore

\[
\beta(G)=q-h+1
\geq\left(\frac d2-1\right)h+\frac d2+1.                    \tag{B13}
\]

This reconstructs the exact extra \(d/2\) term: it uses the strict
cardinality inequality, not merely minimum degree.

Finally Turán--Kubilius for the additive function \(\Omega\) gives

\[
\sum_{n\leq N}\bigl(\Omega(n)-\log\log N\bigr)^2
=O(N\log\log N).                                             \tag{B14}
\]

Thus deleting the integers with
\(\Omega(n)<\tfrac12\log\log N\) costs \(O(N/\log\log N)=o(N)\).
On the remaining host one may take
\(d=\tfrac12\log\log N\to\infty\). This supports RR.3 only as a
full-occurrence complexity statement; it does not itself yield a transversal
or a rounding theorem.

## Blind scope verdict

The three claims are mutually consistent and reconstruct all-parameter
proofs. RR.1 and RR.2 are standalone countermechanisms to bounded
active-depth and bounded top-fibre-residue descriptions. RR.3 shows that
full occurrence graphs in a density-one host are necessarily connected and
have growing cycle surplus. None lower-bounds \(\tau(H_N)\), rounds the
fractional cover, or constructs a coherent infinite admissible set.

The author package must still be checked for: exact floors in (B3)--(B7),
nonnegative padding, Finset distinctness, private-prime minimality, the
double-star prime/composite collision cases, the word “every” in occurrence
matching, and use of Turán--Kubilius for \(\Omega\) rather than only
\(\omega\).
