# Erdős #776: fourth attack — the \(7V\) late-tail barrier

Date: 2026-07-31

## 1. Outcome and evidence levels

The target

\[
R_2(V)=D_{44}-J_{44}(V)\le7V
\qquad(V\ge288)
\tag{1.1}
\]

remains **OPEN**.  No counterexample was found.  This attack makes six
rigorous reductions and records a substantially larger exact falsifier
search without promoting that search to a proof.

### PROVED

1. There is an exact adjacent identity
   \[
   R_2(V+1)-R_2(V)
   =D^{[V]}_{43}-J_{43}(V)+1-L_{45}(V),
   \tag{1.2}
   \]
   where \(L_{45}\) is an explicitly defined rank-45 shadow loss.
   Consequently
   \[
   L_{45}(V)\ge D^{[V]}_{43}-J_{43}(V)-6
   \tag{1.3}
   \]
   implies \(R_2(V+1)-R_2(V)\le7\).  If (1.3) holds for every
   \(V\ge288\), then the exact anchor \(R_2(288)=1970<7\cdot288\)
   proves (1.1) by induction.
2. Galois adjunction converts (1.3) into an exact lower bound on the
   diagonal gap \(G_{45}\).  On the separated late-tail chart it simplifies
   to
   \[
   \boxed{
   G_{45}(V)\ge
   S_2(R_2)-U_2(R_2-V+6).
   }
   \tag{1.4}
   \]
   This is necessary and sufficient for the one-step \(+7\) propagation
   on that chart.
3. A one-rank-higher linear barrier is sufficient.  For an explicit
   block \(J_{45}\),
   \[
   \boxed{
   D_{45}\le J_{45}+109V
   \Longrightarrow
   D_{44}\le J_{44}+7V
   }
   \qquad(V\ge288).
   \tag{1.5}
   \]
   The proof uses the new uniform rank-three slope estimate
   \[
   \boxed{
   109\operatorname{KK}_3(x)\le6x
   \quad\left(x\ge\binom{58}{3}\right).
   }
   \tag{1.6}
   \]
4. Two stronger natural proposals have exact counterexamples:
   \(D_{45}\le J_{45}+108V\) already fails at \(V=288\), and the
   proposed adjacent bound \(R_2(V+1)-R_2(V)\le3\) first fails at
   \(V=17423\), where the jump is \(5\).
5. A sharper two-step affine lift is available.  For an explicit
   \(J_{46}\),
   \[
   \boxed{
   D_{46}\le J_{46}+458V+292894
   \Longrightarrow
   D_{44}\le J_{44}+7V-46.
   }
   \tag{1.7}
   \]
   Hence the rank-46 premise alone would close the rank-44 gate.  The
   anchored slope-one strengthening is false already at \(V=290\).
6. The carry-independent entry certificate from the second attack extends
   from residual rank \(28\) to rank \(43\) unchanged.  Replacing its
   factor-two rounding by an exact quotient--remainder bound extends it
   further to residual rank \(233\).  Consequently
   \[
   \boxed{D_{248}<H_{248}\Longrightarrow D_{18}<P_{18}}
   \qquad(V\ge288).
   \tag{1.8}
   \]
   This is much weaker than every previous fixed-rank closing target.

### COMPUTATIONAL, FINITE ONLY

- Every integer \(288\le V\le20000\) was evaluated with exact
  run-compressed Macaulay arithmetic.  There is no \(7V\) counterexample
  and no rank-44 template failure in this finite interval.
- The largest ratio is
  \[
  \max_{288\le V\le20000}\frac{R_2(V)}V
  =\frac{1970}{288}=\frac{985}{144},
  \]
  attained at \(V=288\).  Equivalently, the closest point to the \(7V\)
  line has margin \(7V-R_2=46\).
- Exact sparse evaluations at
  \[
  V=25000,50000,100000,200000,500000,10^6
  \]
  also satisfy (1.1) and the observed template.  These six isolated
  points do not fill the intervening intervals.

### OPEN

None of the following has an unbounded-parameter proof:

\[
R_2(V)\le7V,
\qquad
R_2(V+1)-R_2(V)\le7,
\qquad
D_{45}\le J_{45}+109V,
\qquad
D_{46}\le J_{46}+458V+292894,
\qquad
D_{59}<H_{59},
\qquad
D_{248}<H_{248},
\qquad
\text{the loss gate (1.3)}.
\]

Thus Erdős #776 remains **OPEN**.

## 2. Frozen late blocks

The fourth attack keeps the algebraic definition from
`THIRD_ATTACK.md`:

\[
\begin{aligned}
J_{44}(V)
={}&\binom{V-12}{44}
 +\sum_{i=31}^{43}\binom{V-57+i}{i}\\
&+\sum_{i=3}^{30}\binom{V-58+i}{i},
\\[2mm]
R_2(V)={}&D^{[V]}_{44}-J_{44}(V).
\end{aligned}
\tag{2.1}
\]

Two adjacent blocks will also be used:

\[
\begin{aligned}
J_{43}(V)
={}&\binom{V-12}{43}
 +\sum_{i=30}^{42}\binom{V-56+i}{i}\\
&+\sum_{i=2}^{29}\binom{V-57+i}{i},
\end{aligned}
\tag{2.2}
\]

and

\[
\begin{aligned}
J_{45}(V)
={}&\binom{V-12}{45}
 +\sum_{i=32}^{44}\binom{V-58+i}{i}\\
&+\sum_{i=4}^{31}\binom{V-59+i}{i}.
\end{aligned}
\tag{2.3}
\]

Termwise Pascal identities give

\[
\boxed{J_{44}(V+1)-J_{44}(V)=J_{43}(V).}
\tag{2.4}
\]

All three \(J\)'s are explicit integers.  Equations (2.1)--(2.4) do not
assume that an actual \(D_q\) has any particular canonical prefix.

## 3. Exact finite search

### 3.1 Method

For each parameter, the scan starts from

\[
D_{V-12}=0,
\qquad
D_{q-1}=V+\operatorname{KK}_q(D_q),
\]

and runs to rank 44 using the exact run-compressed engine.  A run
\((h,l,a)\) represents

\[
\sum_{i=l}^{h}\binom{i+a}{i}.
\]

All comparisons use integers.  In particular, ratios are compared by
cross multiplication; no floating-point value decides a maximum or a
pass/fail result.  Ordinary greedy Macaulay arithmetic independently
cross-checks selected parameters.

The dense interval was divided into eight work-balanced chunks.  Its wall
time was \(1039.19\) seconds with eight workers.  The exact chunk summary
is:

| interval | largest adjacent jump in the chunk | first location |
|---:|---:|---:|
| \(288\ldots7076\) | 3 | \(1361\to1362\) |
| \(7077\ldots10003\) | 3 | \(8019\to8020\) |
| \(10004\ldots12249\) | 3 | \(11748\to11749\) |
| \(12250\ldots14143\) | 3 | \(13689\to13690\) |
| \(14144\ldots15812\) | 3 | \(15671\to15672\) |
| \(15813\ldots17321\) | 2 | \(15823\to15824\) |
| \(17322\ldots18708\) | 5 | \(17423\to17424\) |
| \(18709\ldots20000\) | 3 | \(18765\to18766\) |

There are zero template mismatches in the interval.  The global summary is

\[
\begin{array}{c|c}
\text{quantity}&\text{exact result}\\
\hline
\max R_2/V&1970/288\\
\max(R_2-7V)&-46\text{ at }V=288\\
\max(R_2(V+1)-R_2(V))&5\text{ at }V=17423\\
\min(R_2(V+1)-R_2(V))&1\\
R_2(20000)&22398
\end{array}
\tag{3.1}
\]

The scan proves these statements only on the displayed finite interval.

### 3.2 The first failure of the overly strong jump conjecture

Every adjacent jump is at most \(3\) for \(288\le V<17423\), but

\[
R_2(17423)=19701,
\qquad
R_2(17424)=19706.
\tag{3.2}
\]

Thus \(V=17423\) is the smallest counterexample in the analytic range to
both proposed bounds

\[
R_2(V+1)-R_2(V)\le3
\quad\text{and}\quad
R_2(V+1)-R_2(V)\le4.
\]

The rank-three tail undergoes a genuine canonical carry there:

\[
\begin{aligned}
Z_3(17423)
&=\binom{67}{3}+\binom{66}{2}+\binom{42}{1},\\
Z_3(17424)
&=\binom{68}{3}+\binom{4}{2},
\end{aligned}
\tag{3.3}
\]

and its lower shadow jumps from \(2278\) to \(2282\).  Since
\(R_2=V+\operatorname{KK}_3(Z_3)\) on these two checked charts, this gives
the observed \(1+4=5\) jump.  Equation (3.3) is an exact finite
counterexample to a stronger adjacent conjecture, not a proof that all
later jumps are at most five.

### 3.3 Sparse large parameters

The exact sparse rows are:

\[
\begin{array}{r|r|r}
V&R_2(V)&R_2(V)-7V\\
\hline
25000&27546&-147454\\
50000&53267&-296733\\
100000&104486&-595514\\
200000&206522&-1193478\\
500000&511305&-2988695\\
1000000&1017530&-5982470
\end{array}
\tag{3.4}
\]

The ratios in (3.4) are close to one, but no asymptotic estimate is inferred
from them.

## 4. Exact adjacent propagation

For a \(p\)-canonical integer \(x\), write

\[
U_p(x)=\sum_i\binom{a_i}{i+1},
\qquad
S_p(x)=x+U_p(x).
\]

The inherited diagonal-suspension theorem gives, at the aligned rank 45,

\[
D^{[V+1]}_{45}\le S_{44}\!\left(D^{[V]}_{44}\right).
\tag{4.1}
\]

Define

\[
\begin{aligned}
N(V)&=S_{44}\!\left(D^{[V]}_{44}\right),\\
G_{45}(V)&=N(V)-D^{[V+1]}_{45}\ge0,\\
L_{45}(V)
&=\operatorname{KK}_{45}(N(V))
 -\operatorname{KK}_{45}(N(V)-G_{45}(V)).
\end{aligned}
\tag{4.2}
\]

The suspension identity

\[
\operatorname{KK}_{45}(S_{44}(x))
=x+\operatorname{KK}_{44}(x)
\tag{4.3}
\]

and the two defect recurrences give

\[
\begin{aligned}
D^{[V+1]}_{44}-D^{[V]}_{44}
&=V+1+\operatorname{KK}_{45}(N-G)-D^{[V]}_{44}\\
&=D^{[V]}_{43}+1-L_{45}.
\end{aligned}
\tag{4.4}
\]

Subtract (2.4) from (4.4).  This proves the unconditional identity

\[
\boxed{
R_2(V+1)-R_2(V)
=D^{[V]}_{43}-J_{43}(V)+1-L_{45}(V).
}
\tag{4.5}
\]

No stable-prefix assumption occurs in (4.5).

### Proposition 4.1

If

\[
\boxed{
L_{45}(V)\ge D^{[V]}_{43}-J_{43}(V)-6
}
\tag{4.6}
\]

for every \(V\ge288\), then

\[
R_2(V)\le7V
\qquad(V\ge288).
\]

Indeed, (4.5)--(4.6) give \(R_2(V+1)-R_2(V)\le7\), and the
anchor has \(R_2(288)=1970<2016\).  If the right side of (4.6) is
negative, the condition is automatic because \(L_{45}\ge0\).

### Exact Galois form

Put

\[
\ell(V)=\max\left(0,D^{[V]}_{43}-J_{43}(V)-6\right).
\]

Since

\[
L_{45}\ge\ell
\iff
\operatorname{KK}_{45}(N-G_{45})
\le\operatorname{KK}_{45}(N)-\ell,
\]

Galois adjunction gives the exact threshold

\[
\boxed{
G_{45}\ge
N-U_{44}\!\left(\operatorname{KK}_{45}(N)-\ell\right).
}
\tag{4.7}
\]

Suppose now only for this simplification that

\[
V-6\le R_2<\binom{V-55}{2}.
\tag{4.8}
\]

Then \(D_{44}=J_{44}+R_2\) is a legal separated expansion.  Suspending
its low tail and subtracting
\(\ell=V+\operatorname{KK}_2(R_2)-6\)
remain below the same cap.  The common high block cancels from (4.7),
leaving precisely

\[
\boxed{
G_{45}\ge S_2(R_2)-U_2(R_2-V+6).
}
\tag{4.9}
\]

Thus (4.9) is not a heuristic estimate: under (4.8), it is equivalent to
the \(+7\) adjacent propagation.

Selected exact diagnostics show that the inequality can be close:

| \(V\) | \(R_2\) jump | \(G_{45}\) | required \(G_{45}\) | gap surplus | loss surplus in (4.6) |
|---:|---:|---:|---:|---:|---:|
| 288 | 2 | 10,554 | 10,366 | 188 | 5 |
| 379 | 1 | 13,534 | 13,308 | 226 | 6 |
| 1,000 | 1 | 35,430 | 35,079 | 351 | 6 |
| 1,361 | 3 | 48,984 | 48,970 | 14 | 4 |
| 6,329 | 1 | 317,267 | 317,165 | 102 | 6 |
| 10,000 | 1 | 583,845 | 583,706 | 139 | 6 |
| 17,423 | 5 | 1,263,278 | 1,263,269 | 9 | 2 |

The last row shows why a coarse positive-gap theorem is unlikely to be
enough.  The missing all-parameter result is the precise quantitative
loss (4.6), not qualitative diagonal domination.

## 5. A one-rank-higher linear gate

Define the algebraic rank-three tail

\[
Z_3(V)=D^{[V]}_{45}-J_{45}(V).
\tag{5.1}
\]

The next proposition avoids assuming that \(Z_3\) is the actual canonical
tail.

### Lemma 5.1 (uniform rank-three slope)

For every integer \(x\ge\binom{58}{3}\),

\[
\boxed{109\operatorname{KK}_3(x)\le6x.}
\tag{5.2}
\]

### Proof

Write the 3-canonical expansion, omitting absent terms, as

\[
x=\binom a3+\binom b2+\binom c1.
\]

The hypothesis gives \(a\ge58\).  The contribution of the leading term to
\(6x-109\operatorname{KK}_3(x)\) is

\[
6\binom a3-109\binom a2
=\binom a2(2a-113)
\ge3\binom{58}{2}=4959.
\]

For an optional rank-two term,

\[
6\binom b2-109b=b(3b-112)\ge-1045,
\]

the integer minimum occurring at \(b=19\).  An optional rank-one term
contributes \(6c-109\ge-103\).  Therefore

\[
6x-109\operatorname{KK}_3(x)
\ge4959-1045-103=3811>0.
\]

This proves (5.2). \(\square\)

### Theorem 5.2 (rank-45 linear lift)

For every \(V\ge288\),

\[
\boxed{
D^{[V]}_{45}\le J_{45}(V)+109V
\Longrightarrow
D^{[V]}_{44}\le J_{44}(V)+7V.
}
\tag{5.3}
\]

### Proof

The candidate \(J_{45}+109V\) is canonically separated: at \(V=288\),
\(109V=31392<\binom{233}{3}\), and
\(\binom{V-55}{3}/V\) is increasing thereafter.  Hence

\[
\operatorname{KK}_{45}(J_{45}+109V)
=J_{44}+\operatorname{KK}_3(109V).
\]

Moreover \(109V\ge31392>\binom{58}{3}\), so Lemma 5.1 and monotonicity
give

\[
\operatorname{KK}_3(109V)\le6V.
\]

Using the defect recurrence and the hypothesis in (5.3),

\[
\begin{aligned}
D_{44}
&=V+\operatorname{KK}_{45}(D_{45})\\
&\le J_{44}+V+\operatorname{KK}_3(109V)\\
&\le J_{44}+7V.
\end{aligned}
\]

This proves (5.3). \(\square\)

The coefficient 109 is the smallest integer coefficient surviving the
analytic anchor.  At \(V=288\),

\[
Z_3(288)=31262,
\]

so

\[
Z_3(288)-108V=158>0,
\qquad
109V-Z_3(288)=130>0.
\tag{5.4}
\]

Thus \(D_{45}\le J_{45}+108V\) is rigorously false, while the \(109V\)
barrier remains open.  An exact finite scan over \(288\le V\le2000\)
finds no \(109V\) failure and places the largest \(Z_3/V\) ratio at the
anchor; this is again finite evidence only.

Unlike the rank-44 stable-template claim, legality of a rank-45 prefix
would only force the much weaker cubic cap

\[
Z_3<\binom{V-55}{3}.
\]

Therefore the quantitative \(109V\) bound is not automatically contained
in the template and is a noncircular, genuinely stronger target.

### 5.3 A sharper affine lift from rank 46

The linear slope estimate can be sharpened at the actual congruence
class.

### Lemma 5.3 (affine rank-three shadow)

For every \(V\ge288\),

\[
\boxed{
\operatorname{KK}_3(109V-130)\le6V-46.
}
\tag{5.5}
\]

### Proof

Put \(n=6V-46\).  By Galois adjunction, (5.5) is equivalent to

\[
109V-130\le U_2(n)
\iff
109n+4234\le6U_2(n).
\tag{5.6}
\]

Write the 2-canonical expansion as

\[
n=\binom a2+\binom b1,
\qquad 0\le b<a,
\]

where the second term may be absent.  Since
\(n\ge1682=\binom{58}{2}+29\), either \(a=58,\ b\ge29\), or
\(a\ge59\).  The difference in (5.6), before subtracting \(4234\), is

\[
\binom a2(2a-113)+b(3b-112).
\tag{5.7}
\]

If \(a=58\), the second summand is increasing for integer \(b\ge29\),
and at \(b=29\) the two summands are \(4959\) and \(-725\), whose sum is
exactly \(4234\).  If \(a\ge59\), the first summand is at least \(8555\),
whereas the second is at least \(-1045\), its integer minimum at \(b=19\).
Thus (5.6), and hence (5.5), holds for every \(V\ge288\).
\(\square\)

The second ingredient is useful independently.

### Lemma 5.4 (superadditivity of the upper shift)

For \(p\ge1\) and nonnegative integers \(x,y\),

\[
\boxed{U_p(x+y)\ge U_p(x)+U_p(y).}
\tag{5.8}
\]

### Proof

Let \(a=U_p(x)\) and \(b=U_p(y)\).  Galois adjunction and
subadditivity of the lower shadow give

\[
\operatorname{KK}_{p+1}(a+b)
\le\operatorname{KK}_{p+1}(a)+\operatorname{KK}_{p+1}(b)
\le x+y.
\]

Another use of adjunction yields \(a+b\le U_p(x+y)\).
\(\square\)

At the analytic anchor,

\[
\begin{aligned}
U_3(108\cdot288-130)&=U_3(30974)=424803,\\
2\cdot288+424222&=424798.
\end{aligned}
\]

Moreover,

\[
108=\binom93+\binom72+\binom31,
\qquad
U_3(108)=\binom94+\binom73+\binom32=164.
\]

Therefore Lemma 5.4 and induction on \(V\) prove

\[
\boxed{
2V+424222\le U_3(108V-130)
\qquad(V\ge288).
}
\tag{5.9}
\]

Indeed, the left side grows by \(2\) per unit of \(V\), while the right
side grows by at least \(U_3(108)=164\).

Define

\[
\begin{aligned}
J_{46}(V)
={}&\binom{V-12}{46}
 +\sum_{i=33}^{45}\binom{V-59+i}{i}\\
&+\sum_{i=5}^{32}\binom{V-60+i}{i},
\\
Z_4(V)={}&D^{[V]}_{46}-J_{46}(V).
\end{aligned}
\tag{5.10}
\]

Termwise lower shadow sends \(J_{46}\) to \(J_{45}\).

### Theorem 5.5 (rank-46 affine lift)

For every \(V\ge288\),

\[
\boxed{
D^{[V]}_{46}\le J_{46}(V)+2V+424222
\Longrightarrow
D^{[V]}_{44}\le J_{44}(V)+7V-46.
}
\tag{5.11}
\]

### Proof

Both candidates are canonically separated from their fixed blocks.
For the rank-46 candidate, at the anchor

\[
424798<\binom{233}{4}=119666470,
\]

and the right side subsequently gains
\(\binom{V-55}{3}>2\) per unit of \(V\).  The rank-45 candidate
\(109V-130\) is similarly below \(\binom{V-55}{3}\) at the anchor,
and its cap gains \(\binom{V-55}{2}>109\) per step.

Under the premise, (5.9), canonical separation, and Galois adjunction give

\[
\begin{aligned}
D_{45}
&=V+\operatorname{KK}_{46}(D_{46})\\
&\le J_{45}+V+\operatorname{KK}_4(2V+424222)\\
&\le J_{45}+109V-130.
\end{aligned}
\]

Applying Lemma 5.3 once more,

\[
\begin{aligned}
D_{44}
&\le J_{44}+V+\operatorname{KK}_3(109V-130)\\
&\le J_{44}+7V-46.
\end{aligned}
\]

This proves (5.11). \(\square\)

The conclusion is stronger than the original \(7V\) gate and still closes
\(D_{44}<H_{44}\) for the full analytic range.  The new unproved premise is

\[
\boxed{Z_4(V)\le2V+424222\qquad(V\ge288).}
\tag{5.12}
\]

It is not hidden in template legality, which gives only the quartic cap
\(Z_4<\binom{V-55}{4}\).  Exact finite arithmetic on
\(288\le V\le2000\) finds no failure of (5.12), with equality at
\(V=288\).  The smaller integer slope through that anchor,

\[
Z_4(V)\le V+424510,
\]

is false at the exact point \(V=290\), where \(Z_4=424801\) but the
right side is \(424800\).  Thus slope \(2\) is the smallest integer
slope among affine gates constrained to pass through the anchor.  This
is a finite counterexample to the stronger line, not a proof of (5.12).

### 5.4 A looser gate with a much larger admissible slope

For proof search, the tight line (5.12) is unnecessarily demanding.  The
following strengthening of upper-shift superadditivity gives a larger
sufficient envelope.

### Lemma 5.6 (large-leading incremental shift)

Suppose the leading term of the \(p\)-canonical expansion of \(x\) is
\(\binom ap\), and

\[
0\le y\le\binom a{p-1}.
\]

Then

\[
\boxed{
U_p(x+y)-U_p(x)\ge U_{p-1}(y).
}
\tag{5.13}
\]

### Proof

Use the clique form of Kruskal--Katona: \(U_p(t)\) is the maximum number
of supported \((p+1)\)-cliques in a \(p\)-uniform family of size \(t\).
The colex extremizer of size \(x\) contains every \(p\)-subset of an
\(a\)-element set \(A\), because its leading term is \(\binom ap\).
Choose on \(A\) a \((p-1)\)-uniform family of size \(y\) supporting
\(U_{p-1}(y)\) \(p\)-cliques, add a new vertex \(w\), and adjoin the
\(p\)-sets \(\{w\}\cup e\) indexed by that family.  The old
\((p+1)\)-cliques remain, while every supported \(p\)-clique on \(A\)
creates a new \((p+1)\)-clique containing \(w\).  The resulting
\(p\)-family has size \(x+y\) and at least
\(U_p(x)+U_{p-1}(y)\) supported \((p+1)\)-cliques.  Extremality gives
(5.13). \(\square\)

Apply Lemma 5.6 with

\[
p=3,\qquad x=108V-130,\qquad y=108.
\]

The leading index of \(x\) is at least \(58\), so
\(108<\binom{58}{2}\).  Also

\[
108=\binom{15}{2}+\binom31,
\qquad
U_2(108)=\binom{15}{3}+\binom32=458.
\]

Starting from the same five-unit anchor margin as in (5.9), induction now
gives the much looser envelope

\[
\boxed{
458V+292894\le U_3(108V-130)
\qquad(V\ge288).
}
\tag{5.14}
\]

Indeed, the two sides at \(V=288\) are \(424798\) and \(424803\);
thereafter the left side gains \(458\), while Lemma 5.6 says that the
right side gains at least \(U_2(108)=458\).

Repeating the proof of Theorem 5.5 with (5.14) proves the more useful
conditional theorem

\[
\boxed{
D^{[V]}_{46}\le J_{46}(V)+458V+292894
\Longrightarrow
D^{[V]}_{44}\le J_{44}(V)+7V-46.
}
\tag{5.15}
\]

The candidate remains canonically separated: it equals \(424798\) at the
anchor, and its slope \(458\) is far below the first cap increment
\(\binom{233}{3}\).  Thus the recommended rank-46 target is the weaker
premise

\[
\boxed{Z_4(V)\le458V+292894\qquad(V\ge288),}
\tag{5.16}
\]

not the tighter slope-two line.  It still has equality at \(V=288\), but
already has margin \(325009\) at \(V=1000\) and margin \(45524932\) at
\(V=100000\).  Those two margins are exact finite evidence only.

## 6. A strict failure of the residual-only reverse proof

The \(7V\) barrier can be reversed while its residual remains separated.
Start

\[
B_3=U_2(6V),
\qquad
B_{r+1}=U_r(B_r-V).
\tag{6.1}
\]

If every \(B_r\ge V\) until the top, (6.1) would propagate the late tail
without borrowing from \(J\).  This route fails even at the anchor.  For
\(V=288\), exact arithmetic gives

\[
B_{56}=1549\ge288,
\qquad
B_{57}=29<288.
\tag{6.2}
\]

Thus the next subtraction is illegal at rank 57.  The full reverse orbit
from \(J_{44}+7V\) still succeeds at \(V=288\), but only by borrowing from
the fixed block.  Any proof of (1.1) must therefore include the borrow
transition in its invariant; a residual-only scalar recurrence is
provably insufficient.

## 7. Extending the entry certificate from rank 28 to rank 43

The carry-independent certificate in SECOND_ATTACK.md was stopped at
residual rank \(28\), but its argument does not intrinsically stop there.
Fix \(V_0=288\).  For a proposed top residual rank \(s_\star\), define
exact rational constants by

\[
\begin{aligned}
K_{s_\star}&=1,\\
M_r&=\left\lceil288K_r\right\rceil,\\
K_{r-1}&=1+\frac{2\operatorname{KK}_r(M_r)}{288}
\qquad(r=s_\star,\ldots,4).
\end{aligned}
\tag{7.1}
\]

For \(s_\star=43\), an exact 41-row rational audit gives

\[
K_3=\frac{167965}{18},
\qquad
\left\lceil288K_3\right\rceil=2687440
<\binom{261}{3}=2929290.
\tag{7.2}
\]

Every other row also satisfies

\[
\left\lceil288K_r\right\rceil<\binom{261}{r}
\qquad(3\le r\le43),
\tag{7.3}
\]

and the smallest margin is the rank-three margin

\[
2929290-2687440=241850.
\tag{7.4}
\]

### Theorem 7.1 (uniform rank-43 entry gate)

Let \(V\ge288\).  If there is no moving-block entry through rank 18, or
if its first entry has residual rank \(s\le43\), then

\[
\boxed{D_{18}<P_{18}.}
\tag{7.5}
\]

### Proof

At first entry the exact crossing argument gives \(Z_s\le V\le K_sV\).
Suppose inductively that \(Z_r\le K_rV\), and put
\(\mu=\lceil V/288\rceil\).  Then \(Z_r\le\mu M_r\), while
\(\mu\le2V/288\).  Monotonicity and lower-shadow subadditivity give

\[
\begin{aligned}
Z_{r-1}
&\le V+\operatorname{KK}_r(Z_r)\\
&\le V+\mu\operatorname{KK}_r(M_r)\\
&\le K_{r-1}V.
\end{aligned}
\tag{7.6}
\]

For fixed \(r\), the ratio \(\binom{V-27}{r}/V\) is increasing in \(V\).
Thus the base inequalities (7.3) imply

\[
Z_r\le K_rV<\binom{V-27}{r}
\qquad(3\le r\le s).
\tag{7.7}
\]

This validates every separated descent step, rules out a later collision,
and at rank three gives \(D_{18}<P_{18}\), exactly as in the original
rank-28 proof. \(\square\)

The endpoint \(43\) is sharp for this specific recurrence (7.1), not
necessarily for the theorem.  Repeating the exact construction with
\(s_\star=44\) gives

\[
K_3=\frac{1499497}{144},
\qquad
\left\lceil288K_3\right\rceil=2998994
>\binom{261}{3}
\tag{7.8}
\]

by \(69704\).  Hence the unchanged scalar majorizer cannot certify rank
44; a different invariant could still do so.

The non-recovery property of the moving-block comparison now gives the
new fixed-rank reduction

\[
\boxed{
D_{59}<H_{59}
\iff
\text{first entry has }s\le43\text{, or no entry through rank }18,
}
\tag{7.9}
\]

because moving-block rank and residual rank differ by \(15\).
Combining (7.9) with Theorem 7.1 proves the rank-59 implication.  This is
a strictly weaker closing target than the previous \(D_{44}<H_{44}\),
but it is superseded below by the rank-248 implication (1.8).

Selected exact values are positive by enormous margins:

\[
\begin{array}{r|r}
V&H_{59}-D_{59}\\
\hline
288&27182131121200991691886495\\
379&8764445804610594193185873764\\
1000&929830135046718452208534886661864899
\end{array}
\tag{7.10}
\]

These rows are finite falsifier evidence only.  The all-parameter
inequality \(D_{59}<H_{59}\) remains open.

### 7.2 Removing the factor-two rounding loss

The failure in (7.8) comes from the coarse estimate
\(\lceil V/288\rceil\le2V/288\), not from shadow subadditivity itself.
Write every \(V\ge288\) uniquely as

\[
V=288m+t,\qquad m\ge1,\quad0\le t<288.
\tag{7.11}
\]

For a current rational coefficient \(\widehat K_r\), define

\[
\begin{aligned}
M_r&=\left\lceil288\widehat K_r\right\rceil,
&A_r&=\operatorname{KK}_r(M_r),\\
R_{r,t}&=\left\lceil t\widehat K_r\right\rceil,
&A_{r,t}&=\operatorname{KK}_r(R_{r,t}),
\end{aligned}
\tag{7.12}
\]

and set

\[
\boxed{
\widehat K_{r-1}
=1+\max\left\{
\frac{A_r}{288},
\max_{1\le t<288}\frac{A_r+A_{r,t}}{288+t}
\right\}.
}
\tag{7.13}
\]

This is again an all-parameter majorizer, despite using a finite residue
table.  Indeed, if \(Z_r\le\widehat K_rV\), then

\[
Z_r\le mM_r+R_{r,t}
\]

and subadditivity gives

\[
\operatorname{KK}_r(Z_r)\le mA_r+A_{r,t}.
\tag{7.14}
\]

For fixed \(t\), the ratio

\[
\frac{mA_r+A_{r,t}}{288m+t}
\]

is monotone in \(m\), because its cross-multiplied step difference has
constant sign.  Its supremum over integers \(m\ge1\) is therefore the
larger of its value at \(m=1\) and its limit \(A_r/288\), exactly the two
terms in (7.13).  Hence

\[
Z_{r-1}\le\widehat K_{r-1}V.
\tag{7.15}
\]

Start this refined recurrence at
\(\widehat K_{233}=1\).  An exact audit of all \(230\) transitions and
all \(288\) residue classes per transition gives

\[
\widehat K_3=\frac{903709}{89},
\qquad
\left\lceil288\widehat K_3\right\rceil=2924362.
\tag{7.16}
\]

Every base separation holds for \(3\le r\le233\), and the smallest is
again at rank three:

\[
\binom{261}{3}-2924362
=4928>0.
\tag{7.17}
\]

The proof of Theorem 7.1, with (7.15) replacing (7.6), now proves:

### Theorem 7.2 (quotient--remainder rank-233 gate)

For every \(V\ge288\), if there is no moving-block entry through rank
\(18\), or its first entry has residual rank \(s\le233\), then

\[
\boxed{D_{18}<P_{18}.}
\tag{7.18}
\]

Since moving-block and residual ranks differ by \(15\), non-recovery gives
the much weaker fixed-rank closing target

\[
\boxed{
D_{248}<H_{248}
\Longrightarrow
D_{18}<P_{18}.
}
\tag{7.19}
\]

Thus (7.19) proves the advertised implication (1.8).

At the analytic anchor the exact finite margin is

\[
H_{248}(288)-D_{248}^{[288]}
=158891224428564911981342980964300697.
\tag{7.20}
\]

The verifier also checks positive rows at \(V=379\) and \(V=1000\).
They remain falsifier evidence; the unbounded statement
\(D_{248}<H_{248}\) is **OPEN**.  The next start
\(\widehat K_{234}=1\) fails at rank three by exactly \(31997\), so
residual rank \(233\) is the exact endpoint of this quotient--remainder
certificate.

## 8. Honest next target

The fourth attack has not found a \(7V\) counterexample, but the finite
search cannot establish the unbounded quantifier.  The best next theorem
is one of:

1. prove the weakest current fixed-rank gate \(D_{248}<H_{248}\);
2. prove the stronger but simpler fixed-rank gate \(D_{59}<H_{59}\);
3. prove the rank-46 affine barrier (5.16), with its eventual borrow
   transition included;
4. prove the sharp shadow-loss inequality (4.6), or equivalently (4.9)
   on the separated branch;
5. prove the one-rank-higher barrier
   \(D_{45}\le J_{45}+109V\); or
6. find the first \(V\) with adjacent jump at least \(8\), which would
   kill the simple induction even if the absolute \(7V\) barrier survived.

Until then, \(R_2\le7V\), \(D_{44}<H_{44}\), and Erdős #776 all remain
**OPEN**.

## 9. Reproduction

The quick regression is

```bash
python3 \
  data/research_open/q1_three_hour_campaign_2026-07-31/erdos776/verify_rank44_fourth_attack.py \
  --scan-limit 1000 --workers 2
```

The full dense and sparse falsifier run reported above is

```bash
python3 \
  data/research_open/q1_three_hour_campaign_2026-07-31/erdos776/verify_rank44_fourth_attack.py \
  --deep --workers 8
```

The deep mode takes roughly 20--25 minutes on the current host.  Both modes
label every finite scan as falsifier evidence and print `"status": "PASS"`.
