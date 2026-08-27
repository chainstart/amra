# Many-seed fixed-prefix audit

This note stays in `survivor_deepening`.  It works with the actual fixed
window and does not average its translate.

## 1. Exact support, energy, and pair-collision ledger

Let `S` be a processed set of interval primes, let `B_S` be the corresponding
periodic CRT solution set, and let `J` be an integer interval of length at
most `H`.  Put

\[
 X=B_S\cap J,\qquad N=|X|.
\]

For every remaining prime `p`, define

\[
 c_{p,a}=|\{x\in X:x\equiv a\pmod p\}|,
\quad R_p=|\{a:c_{p,a}>0\}|,
\quad E_p=\sum_{a\bmod p}c_{p,a}^2.                   \tag{1}
\]

The local merge criterion proved in `density_sensitive_block_merge.md` is

\[
 R_p>k\quad\text{or}\quad N^2>kE_p.                   \tag{2}
\]

Either inequality forces `X` to meet the allowed interval at `p`, since its
forbidden complement has exactly `k` residues.

> **Pair-collision average lemma.**  For any set `T` of remaining interval
> primes,
> \[
> \sum_{p\in T}(E_p-N)
> \le N(N-1)\left\lfloor\frac{\log(H-1)}{\log k}\right\rfloor, \tag{3}
> \]
> with the right side interpreted as zero when `H=1`.

**Proof.**  The quantity `E_p-N` counts ordered distinct pairs `(x,y)` in
`X^2` for which `p` divides `x-y`.  If a fixed nonzero difference is divisible
by `r` distinct interval primes, their product is larger than `k^r` and at
most `|x-y|<=H-1`.  Thus at most the displayed number of primes divide that
difference.  Sum over the `N(N-1)` ordered pairs. `square`

This exact average is far too weak by itself.  If `X` misses the next allowed
interval for every `p in T`, then `R_p<=k` and Cauchy's inequality gives
`E_p>=N^2/k`.  Writing `t=|T|` and
`rho=floor(log(H-1)/log k)`, (3) yields only

\[
 (t/k-\rho)N\le t-\rho.                               \tag{4}
\]

But `t<k`, hence `t/k<1`.  As soon as `H-1>=k`, one has `rho>=1`, so the
coefficient on the left of (4) is nonpositive.  The pair ledger gives no
upper bound for `N` in any genuinely longer prefix, including both
`H=exp(Ck/log k)` and `H=exp(epsilon k)`.  Exact coordinate agreement is too
rare a statistic.

## 2. Candidate A: signed interval energy and the additive large sieve

Let `F_p=[1,k]` be the forbidden interval and

\[
 S_X(\alpha)=\sum_{x\in X}e^{2\pi i\alpha x}.
\]

If `X mod p subset F_p`, then `E_p>=N^2/k`, and finite Fourier inversion gives

\[
 \sum_{h=1}^{p-1}|S_X(h/p)|^2
 =pE_p-N^2\ge\frac{p-k}{k}N^2.                        \tag{5}
\]

The reduced fractions `h/p`, over distinct interval primes, are separated by
at least `1/(4k^2)`.  The additive large sieve therefore proves the genuinely
pointwise statement

> **Signed-energy large-sieve lemma.**  If `X` misses the allowed interval at
> every `p in T`, then
> \[
> \frac{N^2}{k}\sum_{p\in T}(p-k)
> \le(H-1+4k^2)N,                                     \tag{6}
> \]
> and hence
> \[
> N\le\frac{k(H-1+4k^2)}{\sum_{p\in T}(p-k)}.         \tag{7}
> \]

This is stronger than (3), but it still stalls after only logarithmically many
old half-density constraints.  For a macroscopic remaining set,
`sum(p-k)=Theta(k^2/log k)`, so when `H>>k^2`, (7) is only

\[
 N\ll H\frac{\log k}{k}.                              \tag{8}
\]

An old box of heuristic density `2^{-b}` violates (8) only while
`b<log_2 k-O(log log k)`.  The desired recursion has
`b=Theta(k/log k)`.  Moreover (5) is algebraically just the energy lower bound
`E_p>=N^2/k`; taking absolute squares has discarded the Fourier phases of the
common endpoint.  Thus this kills the *absolute signed-energy/large-sieve
bridge*, not a future theorem using cancellation between characters or
between primes.

## 3. Candidate B: boundary variation

Let `g_p(n)=1_{I_p}(n)-d/p`, where `I_p` is a cyclic interval of length `d`.
The maximum absolute consecutive partial sum of this balanced `p`-periodic
word is exactly

\[
 D_0(p,d)=\frac{d(p-d)}p.                              \tag{9}
\]

If the indicator of `X` has `C(X)` connected integer components, summing over
the components gives the proved bound

> **Boundary-variation lemma.**
> \[
> \left||X\cap I_p|-\frac d pN\right|
> \le C(X)D_0(p,d).                                   \tag{10}
> \]

Equivalently, if the indicator is extended by zero outside `J` and has total
variation `V(X)=2C(X)`, the right side is `V(X)D_0/2`.

For an old CRT box, every old prime `q` contributes at most
`2 ceil(H/q)+2` possible boundary changes inside `J`.  The product indicator
therefore satisfies only

\[
 V(X)\le\sum_{q\in S}(2\lceil H/q\rceil+2),            \tag{11}
\]

which is of order `|S|H/k`.  Substitution in (10) is much larger than the
rare main term `N d/p`.

The linear dependence on component count cannot be replaced by automatic
square-root cancellation.  In the exact aligned counterexample

\[
 k=70,\quad q=137,\quad p=139,
\]

the fixed window is the union of `13` complete old blocks and its conditional
error is

\[
 |715-(69/139)871|=39286/139=282.63\ldots.             \tag{12}
\]

The exact phase formula shows that the block errors have the same sign over a
long coherent run.  Boundary variation is a valid local theorem, but an
absolute boundary ledger pays the number of old blocks and does not yield a
subexponential merge.  This kills only that absolute-variation bridge.

## 4. Candidate C: the exact start-equals-width representation

Write an interval prime as

\[
 p=k+a,\qquad 1\le a<k,
\]

and put `n=2k+t`.  Direct reduction gives the exact equivalence

> **Anchored width representation.**
> \[
> n\bmod p\notin[1,k]
> \quad\Longleftrightarrow\quad
> t\bmod p\in[a+1,2a].                                \tag{13}
> \]

Thus the interval has width `a=p-k` and starts exactly one point after its
width.  This is stronger structure than an arbitrary translated interval box.

Fix `t` and put `q=floor(t/p)`.  Solving

\[
 q(k+a)+a+1\le t\le q(k+a)+2a
\]

for the prime `p=k+a` gives

\[
 p\in I_q(t):=
 \left[\frac{t+2k}{q+2},\frac{t+k}{q+1}\right).       \tag{14}
\]

Between consecutive allowed intervals lies the open gap

\[
 G_q(t)=
 \left(\frac{t+k}{q+2},\frac{t+2k}{q+2}\right),       \tag{15}
\]

whose length is exactly `k/(q+2)`.

This representation is exact, but the immediate prime-gap bridge runs in the
wrong direction for an upper bound.  A solution `t` is equivalent to every
gap (15) being free of interval primes.  Multiplying (15) by `q+2` says that
there is no multiple `(q+2)p`, with `k<p<2k`, in `(t+k,t+2k)`.  Since
`n=2k+t`, this is precisely the original condition that the preceding
length-`k` interval `(n-k,n)` contain no multiple of an interval prime.

Known upper bounds for prime gaps can rule out some small `t` by forcing a
prime into (15); that supplies a lower-bound obstruction, not a construction
of `t`.  For the desired subexponential `t`, one has `q roughly t/k` and the
gap length `k/(q+2) roughly k^2/t`, quickly below one, so the condition becomes
arithmetically exact but analytically vacuous.  Without a simultaneous
prime-free-gap construction, (14)--(15) are an equivalent reindexing rather
than an upper-bound compression.

## 5. Candidate D: canonical narrow absorption and inverse-binomial dilates

Let `A` be an integer with `1<=A<k` and take the canonical absorber

\[
 Q_A={k+A\choose A}=\frac{\prod_{a=1}^A(k+a)}{A!}.     \tag{16}
\]

Every prime `k<p<=k+A` divides the numerator exactly once and does not divide
`A!`; hence it divides `Q_A`.  Thus `n=Q_A t` automatically satisfies all
those local conditions.  This uses no short-interval prime theorem, and

\[
 \log Q_A\le A\log\frac{e(k+A)}A.                     \tag{17}
\]

For `A=floor(k/log^2 k)`, the right side is
`O(k log log k/log^2 k)=o(k)`.

The important gain over an arbitrary absorber is an exact algebraic phase.
For a remaining prime `p=k+b`, where `b>A`, reduction of every numerator
factor modulo `p` gives

> **Canonical absorber congruence.**
> \[
> Q_A\equiv(-1)^A{b-1\choose A}\pmod p.               \tag{18}
> \]

Consequently the transformed local set is the anchored progression

\[
 t\bmod p\in
 \{0,-c_p,-2c_p,\ldots,-(b-1)c_p\},
 \quad
 c_p=\left((-1)^A{b-1\choose A}\right)^{-1}\pmod p. \tag{19}
\]

This proves that the dilates are correlated inverse-binomial phases, not
arbitrary units.  It also makes the exact limitation visible.  Put
`R_A(x)=(-1)^A {x-1 choose A}`.  Pascal's identity gives, over every fixed
field,

\[
 \Delta R_A(x)=(-1)^A{x-1\choose A-1},\qquad
 \Delta^{A+1}R_A=0,\qquad
 (x-A)R_A(x+1)=xR_A(x).                               \tag{20}
\]

These are genuine degree-`A` coherence identities.  They do **not** directly
relate `c_p` at two actual primes, because `p=k+b` changes together with `b`.
A Weil bound for one polynomial over one fixed field therefore does not apply
to the varying-modulus sum in this problem.  Likewise the local additive
Fourier coefficient remains only the geometric sum

\[
 \sum_{j=0}^{b-1}e_p(-h c_pj)
 =\frac{1-e_p(-h c_pb)}{1-e_p(-h c_p)},                \tag{21}
\]

and (18) alone supplies no cancellation between different primes.

There is nevertheless a small unconditional phase-counting consequence.

> **Low one-frequency phase counting lemma.**  Let `Q>L>=1`, `L<k`, and
> `1<=R<Q`.  Among primes `k<p<2k` with `p` not dividing `Q`, let `B_+` count
> those for which `hQ congruent a (mod p)`, and let `B_-` count those for
> which `hQ^{-1} congruent a (mod p)`, for some `1<=h<=L` and some nonzero
> integer `a` with `|a|<=R`.  Then
> \[
> |B_+|\le2LR\frac{\log(LQ+R)}{\log k},\qquad
> |B_-|\le2LR\frac{\log(RQ+L)}{\log k}.               \tag{22}
> \]

Indeed, the first congruence makes `p` divide `hQ-a`, which is nonzero because
`|a|<Q<=hQ`.  The second makes it divide `h-aQ`, which is nonzero because
`h<Q<=|a|Q` for positive `a` and is immediate for negative `a`.
For a fixed pair `(h,a)`, bound the product of its distinct prime divisors
exceeding `k`, then sum over the `2LR` pairs.
For the canonical `Q_A` with `A=k/log^2 k`, and for the polylogarithmic
choices `L,R<Q_A` used below, (22) is `o(k/log k)` provided

\[
 LR=o\left(\frac{\log^2 k}{\log\log k}\right).        \tag{23}
\]

This controls a finite band of exact small primal or inverse phases for almost
all remaining primes.  It is still below the natural discrepancy threshold:
an Erdos--Turan treatment of a progression of length `b>=A` needs both a
frequency cutoff and phase separation on roughly the `k/b<=log^2 k` scale.
The union bound (22) no longer gives an exceptional set `o(k/log k)` when
the product `LR` reaches that scale (up to the necessary logarithmic loss).
Thus (22) is a reusable lemma, not a fixed-prefix merge theorem.

For comparison, three other natural absorbers have the exact phases

\[
\begin{aligned}
 Q_{\rm pp}&=\prod_{\substack{1\le a\le A\\k+a\ {\rm prime}}}(k+a),
 &Q_{\rm pp}&\equiv(-1)^s\prod_{k+a\ {\rm prime}}(b-a),\\
 Q_{\rm rise}&=\prod_{a=1}^A(k+a),
 &Q_{\rm rise}&\equiv(-1)^A A!{b-1\choose A},\\
 Q_{\rm lcm}&={\rm lcm}(k+1,\ldots,k+A),
 &Q_{\rm lcm}&\equiv Q_{\rm rise}D^{-1},
 \quad D=Q_{\rm rise}/Q_{\rm lcm},
\end{aligned}                                                        \tag{24}
\]

all modulo `p=k+b`.  The prime product divides `Q_A` and is the cheapest of
these absorbers, but its polynomial deletes the composite offsets.  The
canonical binomial retains every linear factor after the single normalization
by `A!`.  The rising factorial and interval lcm also cost only
`exp(O(A log k))`, hence `exp(o(k))` at the chosen `A`, but cost more than is
needed for the clean binomial phase.

No pointwise phase separation follows.  If `p=k+A+1` is prime, then

\[
 Q_A\equiv(-1)^A\pmod p.                              \tag{25}
\]

For even `A` this is the maximally coherent unit step.  The guarded exact
case `k=1000,A=20,p=1021` has `Q_A mod p=c_p=1` and local cyclic gap `1001`.
This kills a claim that inverse-binomial phases are uniformly away from
short rational phases; it does not kill a block-average theorem.

Exact global CRT scans also show no finite dominance among the four choices.
The values of `G/(P/|B|)` for `(k,A)=(18,5),(20,5),(24,7)` were respectively

\[
\begin{array}{c|ccc}
 & (18,5)&(20,5)&(24,7)\\ \hline
 Q_{\rm pp}&4.454&2.935&6.458\\
 Q_A&2.068&5.819&15.593\\
 Q_{\rm rise}&2.545&10.979&3.465\\
 Q_{\rm lcm}&1.750&4.503&5.229.
\end{array}                                                       \tag{26}
\]

At `k=10000,A=117`, among `1020` remaining primes the canonical centered
phase has mean absolute normalized size `0.2598`, but the exact prime
`p=13873` has `Q_A mod p=-3` and local gap `931.05` density units.  These are
falsification tests only: they show neither uniform separation nor an
empirical advantage, but do not decide a correlated block theorem.

The precise sufficient dependency is now the following.

> **Correlated inverse-binomial gap lemma (open).**  There are absolute
> `B,C` such that the CRT set (19) has forward covering radius
> \[
> W\le k^B(\log k)^{C m_A}
>       \prod_{k+A<p<2k}\frac p{p-k},                 \tag{27}
> \]
> where `m_A` is the number of remaining primes.

If (27) held, start the covering search at `floor(2k/Q_A)+1`; then

\[
 n_k\le2k+Q_A(W+1).                                   \tag{28}
\]

The prime number theorem gives `m_A=O(k/log k)` and

\[
 \sum_{k+A<p<2k}\log\frac p{p-k}=O(k/\log k).
\]

Thus (17), (27), and (28) would prove `n_k=exp(o(k))`.  This is a genuine
sufficient bridge, but it is not proved: (18), (20), and (22) do not yet
control the maximum gap of the many-seed fixed-prefix product.

For arbitrary anchored dilates, a separate guarded scan showed that dilation
can materially enlarge finite gaps.  On moduli `(5,7,11,13)` with balanced
widths `(3,4,6,7)`, the unit-step ratio `G/(Q/|B|)=4.12867...` rises to
`8.55944...` at steps `(1,2,5,5)`.  Across all `32400` width/step systems on
`(5,7,11)`, the maximum was `6.35844...`.  These finite values refute no
fixed-base theorem.

## 6. Current closure assessment

- Pair collisions are proved and quantitatively vacuous once `H>k`.
- Absolute signed-energy/large-sieve control is proved but stalls after
  `O(log k)` old constraints.
- Absolute boundary variation is proved and can accumulate coherently.
- The start-equals-width quotient representation is exact but, without a new
  simultaneous prime-free-gap construction, is equivalent to the original
  covering problem and is more naturally a lower-bound obstruction.
- Canonical narrow-prime absorption has genuinely subexponential cost and
  yields the exact inverse-binomial AP system (19).  The low-phase counting
  lemma (22) is unconditional but misses the discrepancy scale; the
  correlated gap lemma (27) would close the upper bound and remains the
  precise new dependency gap.

No original exponent has changed, and `closes=[]` remains correct.
