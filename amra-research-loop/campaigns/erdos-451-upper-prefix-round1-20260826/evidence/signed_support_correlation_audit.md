# Signed support-stratified correlation audit

This third-stage note remains in `survivor_deepening` with `closes=[]`.  It
expands the fixed interval exactly by Fourier support, proves the rank-two
carry formula and bounds, and audits whether gap-sensitive pair recursion can
have subexponential total loss.

## 1. Exact support expansion

For `p=k+b`, use the common-start coordinate `s=n-(k+1)` and define

\[
 g_p(s)=\frac p b\,\mathbf 1_{[0,b)}(s\bmod p)-1.    \tag{1}
\]

For a set `T` of interval primes, put

\[
 D_T=\prod_{p=k+b\in T}\frac b p,
 \qquad
 C_S(J)=\sum_{s\in J}\prod_{p\in S}g_p(s).           \tag{2}
\]

Then for every fixed integer interval `J`, with no translate average,

\[
 \#\{s\in J:s\bmod p\in[0,b-1]\ (p\in T)\}
 =D_T\sum_{S\subseteq T}C_S(J),                       \tag{3}
\]

where `C_emptyset(J)=|J|`.  This is the exact support decomposition.

For the absorbed affine coordinate, write
`g_p^Q(t)=g_p(Qt-(k+1))`.  The nonzero local Fourier coefficient is

\[
 \kappa_{p}(h)=\frac1b\sum_{j=0}^{b-1}e_p(-hj),
\]

and a support `S` contributes

\[
 C_S^{Q}(J)=
 \sum_{\substack{h_p\ne0\\p\in S}}
 \left(\prod_{p\in S}\kappa_p(h_p)e_p(-(k+1)h_p)\right)
 \sum_{t\in J}e\left(Q\sum_{p\in S}\frac{h_p}{p}\,t\right).      \tag{4}
\]

For full support in a dyadic block, changing to the global frequency `a`
turns the local coordinate into the already proved phase

\[
 h_{p,a}\equiv a(-1)^{A+|S|-1}
 \left({b-1\choose A}F_S'(b)\right)^{-1}\pmod p.       \tag{5}
\]

Thus (4) distinguishes proper support from the full inverse-binomial
Vandermonde term exactly.  The rank-two result below is for the undilated
common-start functions `G_p` and must not be silently transferred to
`g_p^Q` (or its scaled version): that transfer is part of the open affine
full-support problem.

## 2. A precise correlation theorem that would close the problem

It is useful to clear the local denominators.  Put

\[
 G_p(s)=b\,g_p(s)=
 \begin{cases}
 k,&s\bmod p\in[0,b-1],\\
 -b,&s\bmod p\in[b,p-1].
 \end{cases}                                           \tag{6}
\]

The required support induction would follow from the following uniform
signed statement.

> **Support-correlation conjecture (open).**  There are absolute `C,D` such
> that for every **nonempty** subset `S` and every integer interval `J`,
> \[
> |C_S(J)|\le k^D C^{|S|}\prod_{p=k+b\in S}\frac{k}{b}.             \tag{7}
> \]

This is not merely equivalent notation: it supplies an exact recursive
proper-support ledger.  Indeed, if (7) holds for every nonempty proper `S`,
their total error contribution to (3) is at most

\[
 D_T k^D\sum_{\emptyset\ne S\subsetneq T}C^{|S|}
       \prod_{p\in S}\frac{k}{b}
 \le k^D D_T\left(\prod_{p=k+b\in T}
       \left(1+\frac{Ck}{b}\right)-1\right)
 \le k^D\prod_{p=k+b\in T}\frac{b+Ck}{p}
 \le k^D C^{|T|}                                      \tag{8}
\]

for `C>=1`.  If (7) also holds for full support, (3) gives the pointwise
fixed-prefix count

\[
 \#(J\cap B_T)=|J|D_T+O(k^D C^{|T|}).                 \tag{9}
\]

Taking `|J|>2k^D C^{|T|}/D_T` would prove a successor.  An elementary split
at `b=k/(log k)^2` gives

\[
 \log D_T^{-1}
 \le O(k/\log k)+O((k/\log k)\log\log k)=o(k),       \tag{9a}
\]

using the trivial count in the short initial offset range and the standard
bound `pi(2k)-pi(k)=O(k/log k)` afterwards.  Therefore (9) implies
`n_k=exp(o(k))`.  A suitable dyadic short-interval sieve estimate would
sharpen (9a) to `O(k/log k)`, but that sharpening is not used here.

Therefore (7) is a decisive open theorem, not a proved lemma.  The argument
(8) does prove that **proper supports cost only the same `C^{|S|}` ledger**;
the unresolved content is the uniform signed bound for the current full
support.  Replacing `C^{|S|}` by `(log k)^{O(|S|)}` would still give
`exp(o(k))` and is also sufficient.

## 3. Exact rank-two carry formula

Let

\[
 p=k+b<q=k+c,qquad \Delta=q-p=c-b.
\]

Write a complete period in rows `s=jp+r`, where `0<=j<q` and `0<=r<p`.
In row `j`, the second residue is

\[
 s\bmod q=r-j\Delta\pmod q.                          \tag{10}
\]

For `x in Z/q`, let

\[
 C_x=\{0\le r<p:r-x\bmod q\in[0,c-1]\},
 \quad M(x)=|C_x|,
 \quad L(x)=|C_x\cap[0,b-1]|.                         \tag{11}
\]

> **Two-prime row identity.**  The scaled full-support correlation in the
> complete row `j` is exactly
> \[
> R_j:=\sum_{r=0}^{p-1}G_p(jp+r)G_q(jp+r)
> =q\bigl(pL(j\Delta)-bM(j\Delta)\bigr).              \tag{12}
> \]

**Proof.**  Split the row into the four cells determined by membership in
`[0,b)` and `C_{jDelta}`.  Their sizes are `L`, `b-L`, `M-L`, and
`p-b-M+L`.  Substitution of the values `k,-b` and `k,-c` gives

\[
 Lk^2-(b-L)kc-(M-L)bk+(p-b-M+L)bc=q(pL-bM).
\]

This proves (12).  `square`

Put `phi(x)=pL(x)-bM(x)`.  The overlap identities

\[
 \sum_{x\bmod q}L(x)=bc,\qquad
 \sum_{x\bmod q}M(x)=pc                              \tag{13}
\]

show that `phi` has mean zero.  If `V` denotes cyclic discrete total
variation, convolution with the two boundary deltas of an interval gives

\[
 V(L)\le2b,qquad V(M)\le2c,qquad V(\phi)\le6k^2.    \tag{14}
\]

Define the rational-rotation interval discrepancy

\[
 \mathcal D_q(\Delta)=
 \max_{0\le J\le q}\max_{I\subset\mathbb Z/q\ {\rm cyclic\ interval}}
 \left|\#\{0\le j<J:j\Delta\bmod q\in I\}-\frac{J|I|}{q}\right|.
                                                                    \tag{15}
\]

Discrete summation by parts (the one-dimensional Koksma inequality), (12),
and (14) prove

> **Gap-sensitive two-prime upper bound.**  For every integer interval `J`,
> \[
> \left|\sum_{s\in J}G_p(s)G_q(s)\right|
> \le4k^3+12k^3\mathcal D_q(\Delta).                 \tag{16}
> \]

The `4k^3` term covers the two incomplete end rows.  A direct partition of
the orbit into blocks of length `floor(q/Delta)` gives the elementary bound

\[
 \mathcal D_q(\Delta)
 \le \frac q\Delta+3\Delta+6.                        \tag{17}
\]

For `Delta<=q/2`, put `N=floor(q/Delta)`.  Each length-`N` block is a rotated
`Delta`-spaced grid.  Its cyclic gaps are at least `Delta`, so comparison with
an interval and its complement gives interval-count error at most three.
There are at most `Delta+1` complete blocks, and the final incomplete block
has at most `N` points.  This proves (17) in this range.  For `Delta>q/2`, it
follows directly from `\mathcal D_q(\Delta)\le q`.  The continued-fraction/
Ostrowski version replaces the right side by a constant times the sum of the
partial quotients of `q/Delta`.

In particular, in the neighboring-modulus regime `Delta^2<=q`, (17) gives

\[
 \mathcal D_q(\Delta)\le 4q/\Delta+6,
 \qquad
 \left|\sum_{s\in J}G_p(s)G_q(s)\right|
 =O\left(\frac{k^4}{\Delta}+k^3\right).              \tag{17a}
\]

This is a rigorous small-gap estimate; its proof uses no assertion about the
distribution of prime gaps.

The trivial inequality `\mathcal D_q(\Delta)\le q` in (16) already proves

\[
 \left|\sum_{s\in J}G_p(s)G_q(s)\right|\le28k^4.      \tag{18}
\]

Thus (7) is unconditionally true through rank two with `D=2` and an absolute
constant.  Rank two does not close the induction, but it is a genuine signed
proper-support theorem.

## 4. A matching carry-coherence lower bound

The factor `q/Delta` in (17) reflects a real coherent run.  Before the first
wrap, if `0<=x<=min(b,k-Delta)`, then

\[
 L(x)=b-x,qquad M(x)=c,qquad
 \phi(x)=b(k-\Delta)-px.                              \tag{19}
\]

Take

\[
 J_0=1+\left\lfloor\frac{b(k-\Delta)}{2p\Delta}\right\rfloor.
\]

For `0<=j<J_0`, (19) is valid and
`phi(jDelta)>=b(k-Delta)/2`.  Summing the first `J_0` complete rows yields the
proved lower bound

\[
 \sum_{s=0}^{J_0p-1}G_p(s)G_q(s)
 \ge\frac{q b^2(k-\Delta)^2}{4p\Delta}.               \tag{20}
\]

When `b,c` are fixed positive proportions of `k`, this is
`Omega(k^4/Delta)`.  Therefore the extra carry-coherence factor cannot be
removed from a rank-two estimate at the smaller `k^3` scale.

The guarded exact witness

\[
 k=70,\quad(p,q)=(137,139),\quad(b,c)=(67,69),\quad\Delta=2
\]

has maximum scaled interval correlation

\[
 11,495,874
 =33.515667\ldots\,k^3
 =0.9575905039566847\ldots\,\frac{k^4}{\Delta}.       \tag{21}
\]

The maximizing and minimizing prefix endpoints are `2329` and `16644`.
This is an exact lower witness, not floating-point evidence.  More generally,
(20) shows that any infinite bounded-prime-gap family forces an unbounded
`k/Delta` loss relative to `k^3`: for an odd upper prime `q`, take
`k=(q+1)/2`; then `p,q` lie in `(k,2k)` for all sufficiently large pairs and
both offsets are asymptotic to `k`.  The unconditional bounded-prime-gaps
theorem supplies such families, so `D=1` in (7) cannot hold with a fixed `C`;
the surviving conjecture must allow at least one global polynomial factor,
such as `D=2`.

Pairing the Fourier terms `a` and `-a` cannot remove this obstruction: (20)
is a positive signed partial sum of the complete real correlation after all
conjugate pairs have already been combined.

## 5. Why a pair-gap ledger does not yet close a dyadic block

Suppose optimistically that a block were reduced to independent prime pairs
and each pair paid the rotation factor suggested by (16).  Adjacent pairing
would produce a logarithmic ledger of the form

\[
 \sum_i\log\left(1+\frac{k}{\Delta_i}\right).         \tag{22}
\]

This failure can be quantified without assuming a typical prime gap.  For
`r` disjoint adjacent pairs across `(k,2k)`, one has
`sum_i Delta_i<=k`, while `f(x)=log(1+k/x)` is decreasing and convex.  Jensen
therefore gives

\[
 \sum_i f(\Delta_i)\ge r f(k/r)=r\log(1+r).          \tag{22a}
\]

Here `r=Theta(k/log k)` by the prime number theorem, so (22a) is `Theta(k)`,
not `o(k)`.  Bounded gaps only increase individual losses.  Thus no unproved
abundance of twin primes or assumed typical-gap law is used in this negative
adjacent-pair accounting.

Pairing primes from separated parts of the offset block could make
`Delta_i` comparable to `B`, so the first quotient `q/Delta_i` is at most
`k/B<=log^2 k`.  This is only a possible escape, not a proof.  The exact cost
is controlled by the complete continued fraction in (15), whose later
partial quotients can still be large.  Proving a matching of interval primes
with total continued-fraction cost `exp(O(r_B log log k))` requires new
distribution information about prime pairs and modular inverses that is not
implied by the prime number theorem in short intervals.

There is also no valid tensor rule that multiplies rank-two partial-sum bounds
to bound the full-support correlation: multiplying by the next pair changes
the signs at every point of the same interval.  Such a rule would itself be
the missing signed support-stratified theorem.

This kill range is deliberately narrow.  It rules out a constant bound at
the scaled `k^{r+1}` level, but it does **not** rule out `k^{r+D}C^r` for a
fixed `D>=2`.  Nor does it rule out paying one fixed `k^D` factor per dyadic
offset block: there are only `O(log log k)` blocks between
`k/(log k)^2` and `k`, so that polynomial block ledger is
`exp(O(log k log log k))=exp(o(k))`.  It is the multiplication of a
gap-dependent factor once per prime pair, not a fixed polynomial once per
block, that fails the budget audit above.

Hence the rank-two carry formula proves a real proper-support base case and
kills `D=1`, but neither adjacent-gap nor far-pair bookkeeping proves (7) for
unbounded support.

## 6. Third-stage closure boundary

- Proper supports are exactly recursive through (3), and a uniform bound (7)
  sums to only `k^D C^m` error.
- Rank one and rank two satisfy (7) with one global polynomial loss; rank two
  genuinely requires the extra loss because of carry coherence.
- Pairwise `a` versus `-a` cancellation is explicitly insufficient by (20).
- Summation by parts succeeds at rank two but exposes the rational-rotation
  discrepancy (15).  Multiplying its adjacent-gap costs is exponential in
  `k`, while a good far-pair matching is an unproved new input and still lacks
  a tensorization theorem.
- No full-support bound for unbounded `|S|` is proved, so neither (9) nor
  Erdos 451 is closed.

The exact remaining lemma is either (7) with `D>=2` for the undilated
common-start box, or its affine analogue for `g_p^Q` with the correlated
inverse-binomial Vandermonde phases in (4)--(5).  A weaker block version is
also sufficient if its accumulated logarithmic loss is `o(k)`.  Rank two
settles neither affine transfer nor high-rank tensorization.  On the direct
common-start route, the unbounded-rank extension of (7) is the sole new
mathematical gap; the affine inverse-binomial transfer is an alternative
absorbed-route gap, not an additional premise needed by the direct route.
