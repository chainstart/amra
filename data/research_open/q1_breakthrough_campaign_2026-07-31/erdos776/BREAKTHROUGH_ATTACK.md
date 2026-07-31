# Erdős #776 breakthrough attack: a three-chart compression of the rank-248 gate

Date: 2026-07-31

## 1. Outcome

The named problem remains **OPEN**.  This attack does not promote a finite
scan to an unbounded statement.  It does, however, replace the 233-rank
moving-block obstruction behind

\[
D_{248}<H_{248}
\tag{1.1}
\]

by one new fixed rank-42 capacity gate with a transparent additive tax.
This is a genuine all-parameter implication, not another scan:

> **Three-chart compression theorem.**  Let \(V\ge288\), put
> \(M=V-221\), and define
> \[
> E_{M-1}=0,\qquad E_{q-1}=V+\operatorname{KK}_q(E_q).
> \tag{1.2}
> \]
> If
> \[
> \boxed{E_{42}<\binom M{42},}
> \tag{1.3}
> \]
> then
> \[
> \boxed{D_{248}<H_{248}.}
> \tag{1.4}
> \]

Combined with the proved rank-233 quotient--remainder certificate from the
fourth attack, (1.3) would imply \(D_{18}<P_{18}\), the inherited rank-eight
entry, and hence the proposed \(n_0(r)\le2r+5\) construction.

The compression exposes a much sharper possible headline theorem:

\[
\boxed{
E_{M-1}=0,\quad
E_{q-1}=M+221+\operatorname{KK}_q(E_q)
\quad\Longrightarrow\quad
E_{42}<\binom M{42}
\quad(M\ge67).
}
\tag{1.5}
\]

Statement (1.5) is still **OPEN**.  Exact falsifier search finds no failure
for \(67\le M\le279\) (equivalently \(288\le V\le500\)); this finite fact is
not used as a proof.

The new point of this attack is that the moving first carry in (1.5) is not
left as an unstructured rank-42 problem.  Section 6 proves that, outside the
finite bridge \(67\le M\le225\), it is equivalent to an explicit pair of
rank-three tails and that a single **fixed rank-five inequality** supplies
the seed needed for every later rank.  That last inequality is OPEN, but it
has only two scalar inputs on a transparent dyadic strip; no unbounded
Macaulay orbit remains inside it.

## 2. Frozen definitions

The shortened orbit and the 14-term moving block are

\[
D_{V-12}=0,
\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q),
\tag{2.1}
\]

and, for \(q=s+15\),

\[
H_q
=\binom{V-12}{q}
 +\sum_{j=1}^{14}\binom{V-28+j}{s+j}.
\tag{2.2}
\]

For a nonnegative integer with canonical expansion
\(x=\sum_i\binom{a_i}{i}\), write

\[
U_r(x)=\sum_i\binom{a_i}{i+1}.
\tag{2.3}
\]

The usual Galois adjunction and tail-complement identity are used with an
early-stop convention: once a proposed complement becomes nonpositive, the
old separated chart is not propagated formally.

## 3. The first exact gap chart

At ranks \(V-13\) and \(V-14\), direct canonical arithmetic gives

\[
H_{V-13}-D_{V-13}=2,
\qquad
H_{V-14}-D_{V-14}=V-53.
\tag{3.1}
\]

Put

\[
r=V-q-13.
\tag{3.2}
\]

Thus \(r=1\) at \(q=V-14\), and \(r=V-261\) at \(q=248\).  Before the
first moving-block entry, the tail-complement identity gives the exact gap
recurrence

\[
F^{(53)}_1=V-53,
\qquad
F^{(53)}_{r+1}=U_r(F^{(53)}_r)-V,
\tag{3.3}
\]

and

\[
H_q-D_q=F^{(53)}_{V-q-13}.
\tag{3.4}
\]

Once \(D_q\ge H_q\), the comparison cannot recover at a lower rank.  Hence
positive survival of (3.3) through \(r=V-261\) proves (1.1); a negative
formal continuation after an early stop has no meaning.

## 4. A general exact Pascal peel

For a nonnegative integer \(c\), define a legal forward-gap chart by

\[
F^{(c)}_1=V-c,
\qquad
F^{(c)}_{r+1}=U_r(F^{(c)}_r)-V.
\tag{4.1}
\]

### Lemma 4.1 (two-vertex Pascal peel)

While the two displayed charts remain nonnegative, for every \(r\ge2\),

\[
\boxed{
F^{(c)}_r
=\binom{V-c-2}{r}+F^{(2c+3)}_{r-1}.
}
\tag{4.2}
\]

#### Proof

At \(r=2\),

\[
\begin{aligned}
F^{(c)}_2
&=\binom{V-c}{2}-V\\
&=\binom{V-c-2}{2}+V-(2c+3),
\end{aligned}
\]

which is (4.2).  Moreover, until early stop,

\[
0\le F^{(2c+3)}_{r-1}
 \le\binom{V-(2c+3)}{r-1}
 <\binom{V-c-2}{r-1}.
\tag{4.3}
\]

Thus the residual is canonically separated below
\(\binom{V-c-2}{r}\).  Applying \(U_r\), subtracting \(V\), and using
(4.1) proves the next row.  The first capacity comparison in (4.3) is an
equality at the base row \(r=2\), and is therefore deliberately written
non-strictly.  The separation from the large block is strict (for the
nonnegative constants used here) and is preserved until the explicit
early-stop event. \(\square\)

Twice applying Lemma 4.1 uses the constants

\[
53\longmapsto109\longmapsto221.
\tag{4.4}
\]

If the last chart survives to the required row, then with
\(R=V-261\),

\[
\boxed{
H_{248}-D_{248}
=\binom{V-55}{R}
 +\binom{V-111}{R-1}
 +F^{(221)}_{R-2}.
}
\tag{4.5}

The two explicit terms have complementary degrees 206 and 151.  This
explains why the observed rank-248 margin is enormous: it is not a fragile
numerical accident at the endpoint.

## 5. Tail complement to rank 42

Put \(M=V-221\).  The last residual in (4.5) starts at

\[
F^{(221)}_1=M
\tag{5.1}
\]

and is needed at rank

\[
R-2=V-263=M-42.
\tag{5.2}
\]

Complement it inside \(\binom Mr\).  If

\[
F^{(221)}_r=\binom Mr-E_{M-r},
\tag{5.3}
\]

then the tail-complement identity turns (4.1) into exactly

\[
E_{M-1}=0,
\qquad
E_{q-1}=V+\operatorname{KK}_q(E_q).
\tag{5.4}
\]

At \(r=M-42\), equation (5.3) is

\[
F^{(221)}_{M-42}=\binom M{42}-E_{42}.
\tag{5.5}
\]

A failed capacity cannot recover under (5.4).  Consequently (1.3) makes
every required chart in Sections 3--4 legal, and substituting (5.5) into
(4.5) proves the three-chart compression theorem.

At \(V=288\), the exact decomposition is

\[
\begin{aligned}
H_{248}-D_{248}
={}&158881156584013468538566287277873712\\
 &+10067844551443295371152629094864\\
 &+147405541057332121,
\end{aligned}
\tag{5.6}
\]

whose sum is the previously reported rank-248 margin.  Equation (5.6) is
an audit row, not the unbounded proof.

## 6. A propagation mechanism and the remaining seed problem

The new rank-42 gate has an adjacent-parameter mechanism that is stronger
than a raw scan.  Let

\[
f_1=M,qquad f_{r+1}=U_r(f_r)-(M+221)
\tag{6.1}
\]

and let \(g\) be the same sequence at parameter \(M+1\):

\[
g_1=M+1,qquad g_{r+1}=U_r(g_r)-(M+222).
\tag{6.2}
\]

Define the diagonal surplus

\[
\Gamma_r=g_{r+1}-S_r(f_r),
\qquad S_r(x)=x+U_r(x).
\tag{6.3}
\]

### Lemma 6.1 (one positive diagonal seed persists)

If \(\Gamma_r\ge0\) at one legal row and
\(M+221\ge r+2\), then \(\Gamma_{r+1}\ge0\).

#### Proof

The suspension identity gives

\[
U_{r+1}(S_r(x))=S_{r+1}(U_r(x)).
\tag{6.4}
\]

Upper shifts are superadditive.  Since \(M+221\ge r+2\), the
\((r+1)\)-canonical upper shift of \(M+221\) is at least one.  Therefore

\[
\begin{aligned}
g_{r+2}
&\ge U_{r+1}(S_r(f_r))-(M+222)\\
&=S_{r+1}(f_{r+1}+M+221)-(M+222)\\
&\ge S_{r+1}(f_{r+1}).
\end{aligned}
\]

This is \(\Gamma_{r+1}\ge0\). \(\square\)

There is also an exact formula before the first auxiliary carry.  Put

\[
A_j=224(2^j-1),
\qquad A_0=0,
\qquad A_{j+1}=2A_j+224.
\tag{6.5}
\]

### Lemma 6.2 (complete pre-carry chart)

Whenever \(A_{r-1}<M\),

\[
\boxed{
f_r=
\sum_{k=2}^{r}
 \binom{M-A_{r-k}-2}{k}
 +\binom{M-A_{r-1}}1.
}
\tag{6.6}
\]

The corresponding sequence \(g_r\) is obtained by replacing every \(M\)
in (6.6) by \(M+1\).

#### Proof

At \(r=1\), (6.6) is \(f_1=M\).  Apply \(U_r\) termwise.  The only
subtraction occurs in the last two terms, where

\[
\begin{aligned}
\binom{M-A_{r-1}}2-(M+221)
={}&\binom{M-A_{r-1}-2}2\\
 &+M-(2A_{r-1}+224)\\
={}&\binom{M-A_{r-1}-2}2+M-A_r.
\end{aligned}
\tag{6.7}
\]

The hypothesis \(A_r<M\) makes the next row canonical and positive; the
boundary row follows with the usual early-stop interpretation.  The same
calculation with \(M+1\) and tax \(M+222\) proves the adjacent formula.
\(\square\)

In particular, if \(A_r<M\), the two pre-carry canonical words differ by
raising every upper index by one.  Pascal's identity then gives

\[
\boxed{\Gamma_r=-(M+222)<0.}
\tag{6.8}
\]

Thus an all-parameter proof no longer needs to control every later carry:
it is enough to prove that one diagonal seed becomes nonnegative before
rank \(M-42\).  Exact experiments show that this happens at a very low
rank and then Lemma 6.1 propagates it to the endpoint.

The exact dense falsifier scan \(67\le M\le10000\) finds

\[
\boxed{\min\{r:\Gamma_r\ge0\}\le j(M)+3,}
\]

where \(j(M)\) is the unique first-carry index
\(A_{j-1}<M\le A_j\).  The verifier also checks the right endpoint
\(M=A_j\) of each of the first 30 exponentially growing carry intervals;
every such endpoint has delay exactly three.  These are deliberately
labelled **finite falsifier evidence**, not a proof of this bound for all
intervals.

There is an important warning.  No fixed seed rank can work for all \(M\):
equation (6.8) holds on arbitrarily large parameter intervals.  The first
possible seed rank moves on the explicit logarithmic scale

\[
r=\log_2(M/224)+O(1).
\tag{6.9}
\]

### Theorem 6.3 (exact fixed-rank post-carry localization)

Let \(M\ge225\), and let \(j\ge2\) be the unique integer such that

\[
A_{j-1}<M\le A_j.
\tag{6.10}
\]

Write

\[
a=A_{j-2},\qquad b=M-A_{j-1},\qquad
c=a+b+222,\qquad T=M+221=2a+b+445.
\tag{6.11}
\]

Thus \(1\le b\le2a+448\).  Define two rank-three integers

\[
\begin{aligned}
x_3&=\binom c3+\binom b2-T,\\
y_3&=\binom{c+1}3+\binom{b+1}2-(T+1),
\end{aligned}
\tag{6.12}
\]

and, only for the three fixed ranks \(p=3,4,5\), put

\[
x_{p+1}=U_p(x_p)-T,
\qquad
y_{p+1}=U_p(y_p)-(T+1),
\qquad
\gamma_p=y_{p+1}-S_p(x_p).
\tag{6.13}
\]

Then the global adjacent diagonal surpluses satisfy the exact identities

\[
\boxed{\Gamma_{j+p-2}=\gamma_p\quad(p=3,4,5).}
\tag{6.14}
\]

In particular, the fixed-rank statement

\[
\boxed{y_6\ge S_5(x_5)}
\tag{6.15}
\]

for all \(a=224(2^{j-2}-1)\), \(j\ge2\), and
\(1\le b\le2a+448\), produces a nonnegative seed at rank at most \(j+3\).
By Lemma 6.1, it then proves the rank-42 capacity theorem (1.5), after the
finite bridge \(67\le M\le225\).

#### Proof of the localization

At rank \(j\), Lemma 6.2 is still valid.  Apply \(U_j\) and subtract \(T\).
All terms whose lower index is at least three shift into a separated high
block.  The complete remaining tail is

\[
\binom{M-A_{j-2}-2}{3}
 +\binom{M-A_{j-1}}2-T=x_3.
\]

The adjacent parameter gives exactly \(y_3\).  The top upper index in either
tail is strictly below the lowest upper index of the separated high block.
Upper shift preserves that separation, while subtraction is absorbed in
the low tail.  The one-borrow estimate (6.18)--(6.19) gives
\(x_3\ge\binom{c-1}3\).  Monotonicity of the upper shift and Pascal's
identity then give the explicit chain

\[
\begin{aligned}
x_4&\ge \binom{c-1}4-T\ge\binom{c-2}4,\\
x_5&\ge \binom{c-2}5-T\ge\binom{c-3}5,\\
x_6&\ge \binom{c-3}6-T\ge\binom{c-4}6.
\end{aligned}
\]

Indeed the last three comparisons reduce respectively to
\(\binom{c-2}3\ge T\), \(\binom{c-3}4\ge T\), and
\(\binom{c-4}5\ge T\).  Each is weakest at the smallest allowed pair
\((a,b)=(0,1)\), where it is immediate; across every allowed strip the
binomial left side grows faster than the linear quantity \(T\).
For the adjacent tail, (6.12) directly gives
\(y_3\ge\binom c3\).  The same three Pascal comparisons, now with tax
\(T+1\), give
\(y_4\ge\binom{c-1}4\),
\(y_5\ge\binom{c-2}5\), and
\(y_6\ge\binom{c-3}6\).
Thus every displayed low tail is nonnegative and evolves by (6.13).

Every high-block binomial \(\binom h\ell\) for \(f\) is paired with
\(\binom{h+1}\ell\) for \(g\).  In
\(g_{r+1}-S_r(f_r)\), their upper shifts cancel by Pascal's identity:

\[
\binom{h+1}{\ell+1}
-\left(\binom h\ell+\binom h{\ell+1}\right)=0.
\]

Only the low tails remain, proving (6.14).  Finally \(j+3<M-42\) for
\(M\ge225\), so Lemma 6.1 propagates a seed from (6.15) to the required
endpoint.  At that endpoint it gives
\(f^{M+1}_{M-41}\ge S_{M-42}(f^M_{M-42})>0\).  Induction in \(M\), based
at the finitely verified \(M=225\), proves the stated consequence. \(\square\)

There is a useful one-borrow normal form for (6.12).  Put

\[
L=A_j-A_{j-1}=224\,2^{j-1},
\qquad x=L-b,
\qquad c=b+L/2-2.
\tag{6.16}
\]

Then, with \(\binom z2=z(z-1)/2\) interpreted polynomially at \(z=-1\),

\[
\boxed{
x_3=\binom c3+\binom{b-2}2-x,
\qquad
y_3=\binom{c+1}3+\binom{b-1}2-(x-1).
}
\tag{6.17}
\]

If the signed tail in \(x_3\) is negative, exactly one leading borrow gives

\[
x_3=\binom{c-1}3+
 \left[\binom{c-1}2+\binom{b-2}2-x\right].
\tag{6.18}
\]

The bracket is nonnegative on the entire strip, including \(b=1\): it is
convex and increasing in \(b\), and at the smallest endpoint is

\[
\binom{L/2-2}2+2-L>0
\qquad(L\ge448).
\tag{6.19}
\]

Thus the first carry is literally one borrow, not a cascade.  Formula
(6.17) also survives the opposite endpoint \(b=L\), where \(x=0\).  This
removes the main ambiguity in the old phrase “canonicalize the rank-two
borrow”: what remains is the concrete fixed-rank inequality (6.15).

The status of (6.15) is **OPEN**.  Exact arithmetic finds
\(\gamma_5>0\) for every \(225\le M\le10000\), and at both endpoints of
each of the first 30 carry strips.  This is falsifier evidence only.  It is
not promoted to a proof for arbitrary \(j\).

### Proposition 6.4 (signed-lift localization)

Keep \(L,b,c,T\) from (6.16), and write \(x_p(b)\) for the low-tail
recurrence (6.12)--(6.13). Then \(y_p(b)=x_p(b+1)\). If
\[
x_p(b)=\binom cp+z_p(b),
\]
and
\[
\Lambda_{p,c}(z)
=U_p\!\left(\binom cp+z\right)-\binom c{p+1},
\]
then
\[
z_3=\binom{b-2}{2}-(L-b),\qquad
z_{p+1}=\Lambda_{p,c}(z_p)-T.
\tag{6.20}
\]
Moreover, with
\[
\delta_p:=\gamma_p+T+1
=U_p(y_p)-S_p(x_p),
\tag{6.21}
\]
one has \(\delta_3,\delta_4,\delta_5\ge0\) on every strip.

For \(\delta_3\), Macaulay adjunction reduces the assertion to
\(y_3\ge x_3+\operatorname{KK}_3(x_3)\). Here
\[
y_3-x_3=\binom c2+b-1.
\]
If \(z_3\ge0\), then
\(\operatorname{KK}_3(x_3)=\binom c2+\operatorname{KK}_2(z_3)\) and
\(z_3\le\binom{b-2}2\), so the claim follows. If \(z_3<0\), the
one-borrow form (6.18) gives
\(\operatorname{KK}_3(x_3)\le\binom{c-1}2+c-1\), which is again at most
\(y_3-x_3\).

For propagation, the highest canonical upper index of \(x_p\) is at most
\(c<T\). Hence
\[
U_p(x_p)-U_p(x_p-1)<T,
\]
so \(x_{p+1}\le U_p(x_p-1)\) and adjunction gives
\(\operatorname{KK}_{p+1}(x_{p+1})\le x_p-1\). From
\[
y_{p+1}=x_p+x_{p+1}+\delta_p-1
\]
it follows that \(\delta_p\ge0\Rightarrow\delta_{p+1}\ge0\).

This does not yet prove (6.15): that target is exactly the stronger bound
\[
\delta_5\ge T+1
\quad\Longleftrightarrow\quad
\gamma_5=\Delta_bz_6-z_5-T\ge0.
\tag{6.22}
\]
Thus the remaining obstruction is one rank-six lower-shadow carry, not
the earlier three ranks. At the right endpoint it closes explicitly:
\[
\gamma_5(L,L)=\binom{L-14}{2}+2L-144>0.
\tag{6.23}
\]

## 7. Falsification of two tempting shortcuts

Two simple routes fail exactly.

1. A fixed-simplex lower barrier is too strong.  At \(V=288\), with
   \(M=67\),
   \[
   F^{(221)}_{25}<\binom{M-3}{25}.
   \]
   Hence positivity cannot be proved by preserving a complete simplex on
   \(M-3\) vertices through every row.
2. The forward gap is not monotone in rank.  At \(V=301\),
   \[
   F^{(221)}_{37}=3612014796037017570710,
   \]
   but
   \[
   F^{(221)}_{38}=3599951240723699028267.
   \]
   Positivity therefore needs a capacity or diagonal-surplus argument, not
   the assertion \(F_{r+1}\ge F_r\).

## 8. Evidence levels and next decisive lemma

### PROVED

- the moving-block gap conjugacy (3.3)--(3.4), with early stop;
- the general two-vertex Pascal peel (4.2);
- the exact decomposition (4.5) whenever the last chart survives;
- the all-parameter implication (1.3) \(\Rightarrow\) (1.4);
- the diagonal-seed persistence Lemma 6.1;
- the complete auxiliary pre-carry chart (6.6) and its logarithmic first
  carry scale;
- the exact fixed-rank post-carry localization Theorem 6.3 and the
  one-borrow normal form (6.17)--(6.19);
- the signed-lift localization Proposition 6.4, including
  \(\delta_3,\delta_4,\delta_5\ge0\) and the exact remaining rank-six
  carry gate (6.22);
- both explicit counterexamples in Section 7.

### FINITE ONLY

- \(E_{42}<\binom M{42}\) for \(67\le M\le279\);
- throughout that interval the exact 42-canonical expansion starts with
  \(\binom{M-1}{42}+\binom{M-2}{41}\);
- the minimum rank-42 capacity margin in that interval is
  \(147405541057332121\), at \(M=67\);
- every \(67\le M\le10000\) obtains a nonnegative diagonal seed by
  \(j(M)+3\);
- the fixed-rank surplus \(\gamma_5\) is positive for
  \(225\le M\le10000\), and at both endpoints of the first 30 carry
  intervals.

### OPEN

- the universal rank-42 capacity theorem (1.5);
- the fixed rank-five inequality (6.15), now the explicit form of the
  moving first-carry seed problem, equivalently the strengthened
  rank-six carry bound \(\delta_5\ge T+1\);
- \(D_{248}<H_{248}\) for every \(V\ge288\);
- Erdős #776.

The next decisive step is not a larger scan.  It is an all-strip proof of
(6.15), using the one-borrow normal form (6.17)--(6.19).  Lemma 6.1 then
handles every subsequent rank automatically.

## 9. Reproduction

Run

```bash
python3 \
  data/research_open/q1_breakthrough_campaign_2026-07-31/erdos776/\
verify_rank248_compression.py
```

The guard independently checks the two Pascal peels, the moving-gap
conjugacy, the rank-248 decomposition, the rank-42 complement, the two
counterexamples, and the finite falsifier interval.  Its finite interval is
explicitly labelled as such.
