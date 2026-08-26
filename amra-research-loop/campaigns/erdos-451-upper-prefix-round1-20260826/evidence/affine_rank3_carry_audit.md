# Canonical affine rank-three carry audit

This note stays in `survivor_deepening`, keeps `closes=[]`, and studies only
the full-support term after the canonical absorber

\[
 A=\lfloor k/\log^2 k\rfloor,\qquad Q={k+A\choose A}.
\]

It gives an exact rank-three Fourier and carry formula, then falsifies one
specific rank-two-to-rank-three tensor handoff.  It does not claim a block
bound or a solution of Erdos 451.

## 1. The sufficient affine support scale

For `p=k+b>k+A`, retain the notation

\[
 g_p^Q(t)=g_p(Qt-(k+1)),\qquad G_p^Q(t)=b\,g_p^Q(t).
\]

If `S` is a set of remaining primes, let `L(S)` be the number of dyadic
offset blocks met by `S`.  The following pointwise estimate would be
sufficient when inserted in the exact nonempty-support expansion:

\[
 \left|\sum_{t\in J}\prod_{p\in S}G_p^Q(t)\right|
 \le k^{D L(S)}(\log k)^{C|S|}k^{|S|}              \tag{1}
\]

for every fixed integer interval `J` and every nonempty `S`.  Indeed, after
restoring the local factors `b^{-1}` and the box density `D_T`, the nonempty
support error is at most

\[
 k^{DL}D_T\prod_{p=k+b\in T}
 \left(1+\frac{k(\log k)^C}{b}\right)
 \le k^{DL}(1+(\log k)^C)^{|T|},                    \tag{1a}
\]

where `L=O(log log k)` is the total number of blocks.  The logarithm of
(1a) is `o(k)`, as is `log D_T^{-1}`.  Thus a sufficiently long fixed prefix
has positive main term after this error.  This is not a translate average.
Estimate (1) remains open.

## 2. Exact rank-three global-frequency formula

Fix three remaining primes

\[
 p_i=k+b_i,\qquad P=p_1p_2p_3,qquad
 F(x)=\prod_{i=1}^3(x-b_i),
\]

and put

\[
 R_A(x)=(-1)^A{x-1\choose A},\qquad
 H_i=R_A(b_i)F'(b_i).
\]

Because the rank is three, the general inverse-binomial Vandermonde identity
has no additional sign:

\[
 H_i\equiv Q(P/p_i)\pmod {p_i}.                     \tag{2}
\]

Let `mu` be uniform on the affine CRT product set

\[
 t\bmod p_i\in\{0,-Q^{-1},\ldots,-(b_i-1)Q^{-1}\}.
\]

For a global frequency `a mod P`, define

\[
 h_i(a)\equiv aH_i^{-1}\pmod {p_i},\qquad
 K_i(h)=\frac1{b_i}\sum_{j=0}^{b_i-1}e_{p_i}(-hj).
\]

Then CRT factorization gives the exact formula

\[
 \widehat\mu(a)=\prod_{i=1}^3K_i(h_i(a)).            \tag{3}
\]

The full-support term in the fixed interval count is therefore

\[
 \delta\sum_{\substack{a\bmod P\\(a,P)=1}}
 \widehat\mu(a)\sum_{t\in J}e_P(-at),
 \qquad \delta=\prod_{i=1}^3\frac{b_i}{p_i}.         \tag{4}
\]

Equations (3)--(4) retain the signs of the interval kernel and the prefix
kernel.  In particular,

\[
 K_i(-h)=\overline{K_i(h)}
\]

pairs `a` with `P-a` into twice a real part, but supplies no automatic
smallness.  Taking absolute values in (4) would return the already rejected
absolute-support bridge.

## 3. Rank-three algebraic cancellation and exact modular carries

The Vandermonde weights obey the Lagrange identities

\[
 \sum_i\frac1{F'(b_i)}=0,\qquad
 \sum_i\frac{b_i}{F'(b_i)}=0,\qquad
 \sum_i\frac{b_i^2}{F'(b_i)}=1.                    \tag{5}
\]

The canonical binomial factor has the partial-fraction decomposition

\[
 \frac1{(k+x)R_A(x)}
 =\frac1{Q(x+k)}+
 \sum_{a=1}^A
 \frac{(-1)^a a{A\choose a}}{(k+a)(x-a)}.           \tag{6}
\]

Taking the second divided difference of (6) at `b_1,b_2,b_3` proves

\[
 \sum_{i=1}^3\frac1{p_iH_i}
 =\frac1{QP}+
 \mathcal R_S,
 \quad
 \mathcal R_S:=\sum_{a=1}^A
 \frac{(-1)^a a{A\choose a}}
 {(k+a)\prod_{i=1}^3(b_i-a)}.                       \tag{7}
\]

This rational cancellation occurs before modular inversion.  The precise
effect of modular inversion can also be separated.  For a full-support
global frequency `ell`, choose `u_i(ell)` in `{1,...,p_i-1}` with

\[
 u_i(\ell)\equiv \ell H_i^{-1}\pmod {p_i},\qquad
 m_i(\ell)=\frac{H_i u_i(\ell)-\ell}{p_i}.           \tag{8}
\]

Put `U(ell)=sum_i u_i(ell)P/p_i`.  By (2), there is an integer
`nu(ell)` such that

\[
 QU(\ell)=\ell+\nu(\ell)P.                           \tag{9}
\]

Dividing (8) by `p_iH_i`, summing, and using (7) and (9) cancels the common
term `ell/(QP)` and gives the exact **rank-three carry identity**

\[
 \boxed{\quad
 \sum_{i=1}^3\frac{m_i(\ell)}{H_i}
       +\ell\mathcal R_S
 =\frac{\nu(\ell)}Q.\quad}                          \tag{10}
\]

Thus the inverse-binomial/Vandermonde structure really does cancel the
smooth rational part.  What remains is not zero: it is the global CRT carry
`nu(ell)`.  Since `0<u_i(ell)<p_i`, the trivial range for `nu` has length on
the order of `3Q`; (10) alone gives no small discrepancy factor.

The same derivation extends exactly to rank `r`.  One takes

\[
 H_i=(-1)^{r-1}R_A(b_i)F_S'(b_i)
\]

and the `(r-1)`-st divided difference of (6).  The signs cancel, leaving the
same form (7) with `product_i(b_i-a)`, and hence the same carry identity
(10).  This is a genuine unbounded-support algebraic identity, but it
compresses the vector of local carries to one integer `nu`; the individual
kernel factors in (3) still depend on the entire vector `u_i(ell)`.

## 4. A strict failure of constant-one tensor handoff

Define the exact full-period interval norm

\[
 M_Q(S)=\max_J\left|\sum_{t\in J}\prod_{p\in S}G_p^Q(t)\right|.
                                                                    \tag{11}
\]

The maximum can be computed as the range of the integer prefix sums over one
period, since every nonempty product has mean zero.  A tempting handoff from
rank two is

\[
 M_Q(\{p,q,r\})\le k\max_{\{u,v\}\subset\{p,q,r\}}M_Q(\{u,v\}),    \tag{T}
\]

which would say that multiplying by the bounded third factor costs only its
supremum norm.  This is false.  The guarded exact instance

\[
 k=22,\quad A=2,\quad Q=276,\quad(p,q,r)=(37,41,43)
\]

has

\[
 M_Q(\{37,41,43\})=8,761,532,
\]

whereas the three pair norms are `9812`, `6750`, and `7406`.  Hence

\[
 \frac{M_Q(\{37,41,43\})}
 {22\max M_Q(\text{pair})}=40.5882036838\ldots.      \tag{12}
\]

The local combined inverses are `(1,7,1)`, the modular carries in (8) at
`ell=1` are `(59,-209,53)`, and `nu(1)/Q=61/276`.  The algebraic cancellations
(5)--(10) are all exact in this example; they do not prevent the interval
kernels from aligning.

This kills (T), and any stated universal constant below the exact ratio in
(12), but no more.  The same triple has

\[
 M_Q(\{37,41,43\})=1.70006938\ldots\,k^5,            \tag{13}
\]

so it is fully consistent with (1) using a fixed `D>=2`.  Finite enumeration
cannot decide that asymptotic theorem.

## 5. Boundary for the next step

The rank-three calculation identifies a sharper gap than a generic request
for Fourier cancellation.  One needs a signed estimate for (4) that controls
the **joint carry word**

\[
 \ell\longmapsto(u_1(\ell),\ldots,u_r(\ell),\nu(\ell))             \tag{14}
\]

with only `k^D(log k)^{Cr}` loss per dyadic block.  The scalar identity (10)
does not determine the vector entering the product of interval kernels, and
the exact counterexample shows that multiplying rank-two interval norms is
not a valid substitute.

Identity (10) supplies no inequality by itself.  Without new distribution or
variation control on the joint word (14), it is an algebraic reparameterization
of the CRT carries and is not promoted to a survivor-closing lemma.

This leaves two honest possibilities within the same mechanism: prove a
multi-frequency signed bound for the joint carry word using (10), or find an
asymptotic family forcing more than every fixed polynomial block loss.  No
such theorem or family is established here, so phase and `closes` remain
unchanged.
