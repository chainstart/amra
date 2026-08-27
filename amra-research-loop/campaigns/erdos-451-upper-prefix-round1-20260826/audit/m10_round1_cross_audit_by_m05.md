# M10 round 1 cross-audit by the M05 agent

Date: 2026-08-26--27

Audit type: same-model cross-audit by an agent which did not author the M10
round-1 files.  This is not a human referee report and is not an independent
model audit.

Files audited without modification:

- `evidence/m10_anchored_successor_round1_checkpoint.md`;
- `evidence/m10_common_endpoint_fan_lemma.md`;
- the round-1 scripts present at the audit baseline:
  `anchored_block_submultiplicativity_search.py`,
  `anchored_full_successor_scan.py`, `anchored_pair_gap_scan.py`,
  `fan_lemma_check.py`, `high_support_vandermonde_search.py`,
  `m05_single_block_gap_scan.py`, and `syndetic_product_kill.py`;
- the two M10 replay JSON files used by those notes.

Files added to `work/m10_round1/` by the M10 author after this audit began are
outside this frozen round-1 snapshot and are not covered by the verdict.

## Verdict

**PASS, with one new strengthening and no mandatory correction.**

The pair-gap theorem, its actual-prime PNT consequence, the coherent fan,
the one- and multi-coordinate Dirichlet merges, and the top-block
common-quotient no-go all reconstruct.  The exact counterexamples to

```text
G(A intersect B) <= G(A)G(B)                               (SM)
```

also reproduce from an independent CRT implementation.  The strict
inequality (SM) is false even when the old block is a single actual
width-one prime and the new block is an actual dyadic pair.  A targeted
search found multiplier distortion `9.0605...` at `k=17098`, substantially
larger than the author's already sufficient `2+2` witness.  This is decisive
against (SM), but finite growth data do not prove unbounded distortion.

No theorem in the audited files changes the public Erdős 451 exponent.  M10
remains alive only as a distinguished-start/block-phase mechanism; neither a
single successor nor the displayed fan is a maximum-gap theorem.

## 1. Pair-gap theorem: independent reconstruction

Let `q=k+a`, `p=q+Delta`, and write a point in the `q`-block as
`s=jq+r`, `0<=r<a`.  With `u_j=j Delta mod p`, its second residue is

```text
s mod p = r-u_j mod p.
```

There are exactly two ways for this residue to lie in
`[0,a+Delta-1]`:

1. the nonwrapped branch has `r>=u_j`, and exists exactly when `u_j<a`;
2. the wrapped branch requires
   `r<=a+Delta-1+u_j-p=u_j-k-1`, and exists exactly when `u_j>k`.

Thus the block is empty iff

```text
a <= u_j <= k.                                               (1)
```

Inside a consecutive empty run no modular wrap is possible, because
`k+Delta<p` is equivalent to `k<q`.  The phases therefore advance by the
ordinary integer `Delta`, giving at most

```text
R=floor((k-a)/Delta)+1                                      (2)
```

empty blocks.  Allowing both boundary blocks gives the author's safe upper
bound `(R+2)q`.

For the lower witness,

```text
j0=floor((a-1)/Delta),       j1=floor(k/Delta)+1.
```

At `j0`, `r=a-1` is allowed; at `j1`, `r=0` is allowed by the
wrapped branch; and all intermediate phases lie in `[a,k]`.  Their gap is
exactly

```text
(j1-j0)q-a+1.                                                (3)
```

Hence, when `a` and `k-a=2k-q` are both macroscopic and `Delta=o(k)`,

```text
G(A_{q,p}) asymp q(2k-q)/Delta.                              (4)
```

The independent script exhaustively checked (1), (2), and (3) for all 732
actual prime pairs arising from `4<=k<=45`; this is diagnostic support, not
the proof.

## 2. PNT consequence and exponent ledger

PNT gives

```text
# {primes in (3k/2,7k/4)}=(1/4+o(1))k/log k.
```

The consecutive gaps in that list telescope to less than `k/4`, so one
globally adjacent pair has `Delta=O(log k)`.  For it,
`a>=k/2` and `2k-q>=k/4`; (3) gives

```text
G(A_{q,p}) >> k^2/log k.                                    (5)
```

Meanwhile both allowed widths are at least `k/2`, and both primes are below
`7k/4`, so

```text
pq/((q-k)(p-k)) <= 49/4 < 13.                               (6)
```

Consequently a universal `C^m`-times-density maximum-gap theorem is false
already for `m=2`, and a polynomial repair `k^B` must have `B>=2`.  The
pair-factorized condition-number product is also correctly charged:
`r=(1/8+o(1))k/log k` disjoint pairs have total within-pair gap below
`k/4`, so AM--GM gives `exp(Omega(k))`; the trivial `Delta_i>=2` gives the
matching `exp(O(k))` scale.

These are maximum-gap statements only.  For the same close pair,
`s=p` is an allowed distinguished seed because `p mod q=Delta<a`, so its
distance after `k-1` is below `k+1`.  This exact separation is essential.

## 3. Common block and coherent fan

For a block `S`, write

```text
L=min S, P=max S, D=P-L, B=L-k.
```

For `s=P+h`, `0<=h<B-D`, every `q in S` has the ordinary residue

```text
P-q+h <= D+h < B <= q-k.
```

This proves the common distinguished interval.  More generally, for
`1<=t<=floor((B-1)/D)` and `0<=h<B-tD`,

```text
(tP+h) mod q=t(P-q)+h < B <= q-k,                            (7)
```

where the displayed quantity is below `q`, so no hidden wrap is present.
The intervals are disjoint because their lengths are below `B<L<P`, and the
triangular seed count is exactly

```text
TB-DT(T+1)/2.                                                (8)
```

When `B>=2D`, taking the first `floor(B/(2D))` rows gives the valid lower
bound `B^2/(8D)`.

The PNT density calculation for the top block is also correct:

```text
integral_{3/2}^2 log(t/(t-1)) dt = (3/2)log(4/3).             (9)
```

Thus the top block has an `O(k)` seed despite reciprocal density
`exp(((3/2)log(4/3)+o(1))k/log k)`.

## 4. Fan--Dirichlet merges

For one new modulus `r`, ordinary one-dimensional Dirichlet approximation
among `0,alpha,...,N alpha` supplies `1<=t<=N` with centered error at most
`1/(N+1)`.  If the residue is near zero, `tP` works; if it is near `r`, the
common correction `h=r-u` is positive, lies below `w=B-ND`, and makes the
new residue zero.  Both branches stay in the old fan.  All strict endpoint
inequalities in the author statement are in the correct direction.

For `h` new moduli, partitioning the `h`-torus into `M^h` cubes gives
`1<=t<=M^h` and centered errors at most `R/M`.  Taking the maximum backward
error `x` makes backward residues fall in `[0,R/M]` and forward residues in
`[0,2R/M]`.  The hypothesis

```text
2R/M < min(c,w)                                              (10)
```

therefore proves the simultaneous merge.  Since `M^h<=N<=k`, this absorbs
only `O(log k)` arbitrary coordinates when `M` is constant.  Reusing a
large `M` for `Theta(k/log k)` narrow coordinates has an
`exp(Theta(k))` ledger, as claimed.

## 5. Top-block common-quotient no-go

For a fixed quotient `t`, a local coordinate contributes exactly

```text
[tq,(t+1)q-k-1].
```

Their intersection is therefore exactly

```text
[tP,(t+1)L-k-1],                                             (11)
```

not merely a subset of the fan.  For the top prime block,
`L=(3/2+o(1))k`, `P=(2+o(1))k`, `D<B`, and `B/D->1`; hence eventually
`T=1`.  Uniformly for its sole positive interval `I_1`, one has

```text
(1.01k,1.49k) subset (s/2,(s+k)/2).                          (12)
```

PNT supplies a lower prime `r` in this fixed interval.  Then
`s<2r<s+k`, so the multiple `2r` lies in the forbidden window.  The
asymptotic containment and strict endpoints in this argument are valid.
The no-go is strictly for maintaining one common quotient throughout the
top block; it does not kill wrapped or phase-rich block mergers.

## 6. Exact failure of strict gap submultiplicativity

The independent CRT implementation reproduces both author witnesses.

For `k=22`, blocks `(23,29)` and `(31,43)` have

```text
(G_A,G_B,G_intersection)=(115,85,25691),
25691/(115*85)=2.628235294117647...
```

with exactly the reported periods, cardinalities, and maximizing endpoints.
For `k=88`, accumulated block `(89,97)` and dyadic block `(131,173)` have

```text
(G_A,G_B,G_intersection)=(1068,351,930139),
ratio=2.481244064577398....                                  (13)
```

The audit first found an even narrower actual-prime witness:

```text
k=222,
A: modulus 223, width 1,
B: moduli (239,251), widths (17,29),
G_A=223, G_B=4525, G(A intersect B)=1225608,
ratio=5496/4525=1.214585635359116....                         (14)
```

The right widths satisfy `17<=d<34`, so `B` is one genuine dyadic 451
block.  Its period is `59989`, the intersection period is `13377547`, and
the maximizing intersection gap is `7728065 to 8953673`.  Thus (SM) fails
even for a single-coordinate old block merged with one actual dyadic pair.

This is finite refutation of a universal claim, hence mathematically
decisive for (SM).  A targeted search through `k<=20000` then found 96
violations among 24,012 tested actual-prime width-one/dyadic systems.  Its
largest witness is

```text
k=17098,
A: modulus 17099, width 1,
B: moduli (17137,17159), widths (39,61),
G_A=17099, G_B=13315411,
G(17099^{-1}B)=120644930,
ratio=120644930/13315411=9.060548713066385....              (14a)
```

The two new widths lie in the same genuine dyadic block `[39,78)`.  The
record ratios at cutoffs `500,1000,2000,5000,20000` were respectively
`1.2146, 2.2340, 5.1390, 7.1127, 9.0605`.  This is genuine finite growth evidence,
but it does **not** prove divergence or rule out an absolute constant.

For comparison, 5,393 actual `2+2` dyadic merges with `k<=140` had (13) as
their largest ratio.  A separate general-coprime (not actual-prime) family
`k=2u^2`, moduli `k+1,k+u+1,k+2u+1`, was also tested; its distortion decayed
rather than grew.  That failed structural construction is recorded only to
prevent conflating general coprime diagnostics with actual 451 evidence.

## 7. The exact phase-sensitive repair

There is a universally valid replacement which exposes the lost data.  Let
`A subset Z/QZ`, `B subset Z/RZ` be nonempty and `gcd(Q,R)=1`.  For a unit
`u` and a periodic set `C`, write `u^{-1}C` for its multiplicative pullback.
Then

```text
G(A intersect B)
 <= min(Q G(Q^{-1}B), R G(R^{-1}A)).                         (15)
```

Proof.  Fix `a in A`.  The intersection contains all points
`a+Qt` for which

```text
t mod R in Q^{-1}(B-a).
```

Translation does not change cyclic gaps, so this subset has maximum gap
`Q G(Q^{-1}B)`.  Adding the remaining intersection points can only decrease
the maximum gap.  The other bound is symmetric.

Define the multiplier distortion

```text
kappa_Q(B)=G(Q^{-1}B)/G(B).                                  (16)
```

Since `Q<=|A|G(A)` and symmetrically for `B`, (15) implies

```text
G(A intersect B)
 <= min(|A| kappa_Q(B), |B| kappa_R(A)) G(A)G(B).            (17)
```

For the width-one old block `A={0} mod p`, equality holds in the first
bound:

```text
G(A intersect B)=p G(p^{-1}B),
G(A intersect B)/(G(A)G(B))=kappa_p(B).                      (18)
```

Thus (14)--(14a) are exactly multiplier-gap distortions, not numerical
artifacts.
For a `b`-point subset of a period `R`, the elementary bounds

```text
G(C)<=R-b+1,       G(C)>=ceil(R/b)
```

give only `kappa_u(C)<b`.  Consequently (17) can cost as much as the block
cardinality; for 451 blocks this has logarithm `Theta(k)` and does not meet
the `exp(o(k))` closure contract.  Formula (15) is therefore a rigorous
phase-preserving repair, but not an exponent-closing one.

For a dyadic pair `q=k+a`, `r=q+Delta`, put `b=a(a+Delta)`.  The pair theorem
and the same cardinality bound give the explicit finite estimate

```text
L_pair=(floor(k/Delta)+1-floor((a-1)/Delta))q-a+1,
kappa_p(B) <= (qr-b+1)/L_pair.                             (18a)
```

In a range where the displayed denominator is positive this is
`O(k Delta/(k-a))`; for `a=o(k)` it is `O(Delta)`.  Thus the available
elementary bound permits growth with the separation of the two new primes.
It neither supplies a constant bound nor proves that actual prime blocks
attain that upper scale.

### 7.1 The exponent-compatible target and what (15) does not imply

An absolute constant in (19) is stronger than the global ledger needs.  If a
new dyadic block has `h` prime coordinates, a direct merge loss

```text
k^B C^h                                                       (18b)
```

with fixed `B,C` would be affordable: across `L=O(log k)` blocks it contributes
`exp(O((log k)^2)+O(m))=exp(o(k))`.  The finite ratios above do not challenge
this weaker target.  Indeed, for every two-coordinate block, regardless of
the multiplier, the single-coordinate containment gives `G(B)>=k+1`, while
the numerator is below its period `qr<4k^2`.  Therefore

```text
kappa_u(B) < 4k                                                (18c)
```

for all units `u`.  Thus width-one versus pair data satisfy (18b) with
`B=1`; their apparent growth is not an exponent obstruction.

For an `h`-coordinate 451 box with widths `d_i=p_i-k`, the presently
available completely elementary extension is only

```text
kappa_u(B) <= min(product_i d_i,
                    (product_i p_i)/(k+1)).                   (18d)
```

The first term is the cardinality bound above.  The second again uses
`G(B)>=k+1` and `G(u^{-1}B)<product_i p_i`.  For a block with
`h=Theta(k/log k)` both can have logarithm `Theta(k)`, so (18d) does not prove
(18b).  No counterexample to (18b) is established either.

There is a separate ledger obstruction: **(15) plus (18b) for `kappa` alone
does not close block merging.**  From (15),

```text
G(A intersect B)/(G(A)G(B)) <= (Q/G(A)) k^B C^h
                             <= |A| k^B C^h.                  (18e)
```

For an accumulated 451 box, `log |A|=sum_{p in A} log(p-k)` can be
`Theta(k)`.  Equivalently, if `delta_A=|A|/Q` and
`G(B)<=F_B/delta_B`, (15) yields

```text
G(A intersect B) <= |A| k^B C^h F_B/(delta_A delta_B),       (18f)
```

again with the fatal `|A|`.  Closing the proposed ledger therefore needs a
**direct union-sensitive merge theorem**

```text
G(A intersect B) <= k^B C^h G(A)G(B),                        (18g)
```

or an additional argument recovering the interleaving gain from all
`a in A`.  A bound on `kappa_Q(B)` controls only the one-fibre argument in
(15), and cannot by itself supply that gain.

### 7.2 Exact all-fibres identity and the missing additive energy

The tempting strengthening

```text
G(A intersect B) <= G(A) G(Q^{-1}B)                         (18h)
```

is also false for actual 451 blocks.  Among the 5,393 `2+2` systems already
used above, 1,486 violate (18h).  One exact witness is

```text
k=130, A=(131,137), B=(223,241),
G(A)=3013, G(B)=800, G(Q^{-1}B)=37,
G(A intersect B)=610067,
610067/(3013*37)=5.472385428907168....                       (18i)
```

Here the widths are `(1,7)` and `(93,111)`, so the new pair is a genuine
dyadic block.  Extending the `2+2` scan through `k<=200` gave 3,667 failures
among 12,175 systems and a fibre-product factor `8.3277...` at `k=197`.  A
separate `3+2` scan found a factor `9.3863499...` at `k=75`.  Thus retaining
the exact gap of every translated fibre still loses essential joint phase
information.  In contrast, the largest *direct* factor in all these scans
remained the author's `2.4812...`; there is no finite counterexample here to
(18g).

That missing information has an exact finite Fourier formulation.  Put
`C=Q^{-1}B` in `Z/RZ`.  For an interval `[x,x+LQ)`, define

```text
t_x(a)=ceil((x-a)/Q),
phi_x(a)=t_x(a)+Q^{-1}a  (mod R),
nu_x(y)=#{a in A: phi_x(a)=y}.                              (18j)
```

Then the number of intersection points in the interval is exactly

```text
N(x,L)=sum_{a in A} sum_{ell=0}^{L-1} 1_C(phi_x(a)+ell).     (18k)
```

With unnormalised Fourier transform on `Z/RZ`, and
`D_L(j)=sum_{ell<L} exp(2 pi i j ell/R)`, this becomes

```text
N(x,L)=|A||C|L/R
 + (1/R) sum_{j != 0} Chat(j) D_L(j)
                         sum_{a in A} exp(2 pi i j phi_x(a)/R).  (18l)
```

Centered Parseval gives the following rigorous finite sufficient condition:
every interval of length `LQ` is nonempty if, for every `x`,

```text
|A|^2 |C|^2 L^2
 > (R E_x-|A|^2)
       sum_{j != 0}|Chat(j)|^2 |D_L(j)|^2,                  (18m)
E_x=sum_y nu_x(y)^2.                                        (18n)
```

The subtraction is essential:
`sum_{j != 0}|sum_a exp(2 pi i j phi_x(a)/R)|^2
=R E_x-|A|^2`.  Dropping it makes the bound vacuous even for perfectly
uniform phases.

This is also an exact additive-energy interface.  If

```text
E(C,I_L)=#{(c1,c2,l1,l2): c1-c2=l1-l2 (mod R)},
```

then

```text
sum_{j != 0}|Chat(j)|^2|D_L(j)|^2
 = R E(C,I_L)-|C|^2L^2.                                    (18n')
```

For the actual CRT box `B=product_p [0,d_p)` and `C=Q^{-1}B`, its Fourier
coefficient factors exactly into local interval sums:

```text
Chat(j)=product_{p|R} sum_{v=0}^{d_p-1}
 exp(-2 pi i j Q^{-1}(R/p)^{-1}v/p).                        (18n'')
```

Equivalently, when `L<R/2`, if `w_{p,d}(z)` is the cyclic overlap of
`[0,d)` with its translate by `z` modulo `p`, then

```text
E(C,I_L)=sum_{|u|<L}(L-|u|)
                    product_{p|R} w_{p,d_p}(Qu mod p).       (18n''')
```

Thus this is not an unspecified generic energy: it is a concrete weighted
count of simultaneous small multiples of the actual earlier period `Q`.

This is just Cauchy--Schwarz applied to (18l), so it is an interface rather
than a claimed new estimate.  It identifies the exact required datum.
Writing `x mod Q=xi`, split `A_-=A intersect [0,xi)` and
`A_+=A intersect [xi,Q)`, and let `n_-(y),n_+(y)` be their multiplicities
modulo `R`.  Since

```text
phi_x(a)=constant+Q^{-1}a+1_{a<xi},
```

the collision energy is exactly

```text
E_x=sum_y n_-(y)^2 + sum_y n_+(y)^2
       +2 sum_y n_-(y)n_+(y+Q).                             (18o)
```

This also gives an exact average and a uniform comparison.  Let
`r_A(t)=#{(a,b) in A^2:a-b=t (mod Q)}`.  For an actual CRT interval box,
`r_A(t)=product_{p|Q}w_{p,p-k}(t mod p)`.  Averaging over
`xi=0,...,Q-1` gives

```text
(1/Q)sum_xi E_xi
 = |A|+2 sum_{1<=mR<Q}(1-mR/Q) r_A(mR).                    (18p)
```

If `n(y)=#{a in A:a=y (mod R)}` and
`E_R(A)=sum_y n(y)^2`, then the exact boundary decomposition is

```text
E_xi=E_R(A)+2 sum_y n_-(y)(n_+(y+Q)-n_+(y)),                (18q)
E_R(A)=|A|^2/R+(1/R)sum_{j != 0}|sum_a exp(2 pi i ja/R)|^2,
max_xi E_xi <= 2 E_R(A).                                    (18r)
```

The last bound follows from Cauchy on the shifted cross term and
`||n_-||_2^2+||n_+||_2^2<=||n_-+n_+||_2^2`.  Hence the deviation from the
heuristic `|A|^2/R` is exactly an old-block Fourier discrepancy plus the
displayed moving-boundary correlation; it is not controlled by cardinality.

Neither individual fibre gaps nor their cardinalities control (18o): in an
abstract fibre-union model the same fibres may all receive the same phase,
giving `E_x=|A|^2`, or be dispersed.  Hence any proof using only those
one-fibre summaries cannot recover the missing factor.  This is a no-go only
for that information-restricted argument class.  In the actual CRT problem,
bounding (18o), together with the weighted Fourier energy in (18m), is the
remaining all-fibres interleaving problem; no such bound is proved here.

The actual `k=197` witness shows that collision energy alone is also
insufficient.  Inside its maximizing empty gap there are `L=29` complete
`Q`-rows; all 28 fibre phases are distinct, so `E_x=28`, the minimum possible,
and the density main term in (18l) is `57.237...`, yet the exact point count
is zero.  The obstruction is therefore the *alignment* of the phase spectrum
with `Chat(j)D_L(j)`, not merely excessive phase collisions.  Any viable
second-moment argument must retain this coefficient-weighted information.

### 7.3 Short-window correction: the actual late-merge interface

Equations (18j)--(18r) concern windows of length `LQ` with integer `L>=1`.
They are mathematically correct but quantitatively useless in the actual late
merge: the desired gap is `exp(o(k))`, whereas the accumulated period
`Q=exp(Theta(k))`, so the desired window has length `T<Q` and contains no
complete `Q`-row.

For arbitrary `T<Q`, let `X=X_{x,T}` be the multiset in `Z/RZ`

```text
X={x+t mod R:0<=t<T and x+t mod Q lies in A},
N=|X|,   E_X=sum_y multiplicity_X(y)^2.                     (18s)
```

Then the exact local identity is simply

```text
#((A intersect B) intersect [x,x+T))
 = N|B|/R+(1/R)sum_{j != 0} Xhat(-j) Bhat(j).               (18t)
```

Since centered Parseval gives

```text
sum_{j != 0}|Xhat(j)|^2=R E_X-N^2,
sum_{j != 0}|Bhat(j)|^2=R|B|-|B|^2,
```

separated Cauchy proves nonemptiness only under

```text
R E_X-N^2 < N^2 |B|/(R-|B|).                               (18u)
```

In the relevant regime `T<R`, the locations `x+t mod R` are distinct, so
`E_X=N`; (18u) is then exactly equivalent to

```text
N+|B|>R.                                                     (18v)
```

This is only the elementary cardinality pigeonhole bound.  For a large
dyadic block `|B|/R` is small, it forces `N` and hence `T` to be essentially
`R`.  With `h=Theta(k/log k)` new primes, `log R=Theta(k)`, so the separated
second-moment route pays `exp(Theta(k))` and fails the global ledger.

What genuinely survives is (18t) as a precise coefficient-weighted local
correlation problem.  Neither the long-row average (18p) nor its bound (18r)
controls it.  Obtaining cancellation in (18t) requires the joint signed phase
information already isolated by the campaign's P3/carry-phase obstruction;
this audit does not supply that open estimate.

The strongest same-form repair still compatible with the audit is the open
conjecture

```text
G(A intersect B) <= C G(A)G(B),                              (19)
```

where the actual-prime examples force

```text
C >= 120644930/13315411 = 9.060548713066385....              (20)
```

No universal `C` is proved here.  If (19), or the weaker direct form (18g),
did hold for dyadic 451 blocks,
its `C^{O(log k)}` merger cost would be polynomial and affordable.  But it
would still require a genuine max-gap theorem for each individual block.

## 8. Why a successor theorem cannot replace a max-gap theorem

A successor theorem controls one interval beginning at the distinguished
start.  A block merge generally begins at a CRT-dependent translated phase,
so it needs every interval of a specified length to meet the block—that is,
a maximum cyclic gap bound.  Blichfeldt differences or the fan beginning at
zero cancel/forget that translation.

The close-pair example makes the logical gap quantitative: its distinguished
successor is `O(k)`, while its maximum cyclic gap is
`Omega(k^2/log k)`.  Therefore substituting either the common seed theorem or
the one-block orthant successor for `G(B)` in (19) is invalid.  A hypothetical
block program would need both:

1. a single-block maximum-gap estimate such as
   `k^B C_0^{m_j} D_j^{-1}` with fixed `B`; and
2. a phase-aware merge such as (19) across `L=O(log k)` blocks.

Only then would the ledger

```text
k^{BL} C^{L} C_0^m D^{-1}
 = exp(O((log k)^2)+O(k/log k))=exp(o(k))                    (21)
```

close the target exponent.  Neither missing theorem is supplied by the
current successor/fan results.

## 9. Computational scope

All accepted exact searches used `openmath-memory-guard` with
`high=30G`, `max=34G`, `swap=4G`, and `tasks=512`.  Details, failed finite
attempts, source hash, and authoritative outputs are recorded in
`audit/m10_round1_cross_audit_replay.txt`.

The computations establish only finite identities and universal finite
counterexamples.  PNT asymptotics, the fan lemmas, (15), and the scope
separation between successor and maximum gap are proved in the text rather
than inferred from samples.
