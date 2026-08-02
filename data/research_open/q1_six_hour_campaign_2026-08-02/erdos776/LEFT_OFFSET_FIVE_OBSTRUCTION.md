# A second adaptive wall: the fixed left offset \(b=5\)

## 1. Statement and scope

Put

\[
 L=224·2^{j-1},\qquad h=L/2,\qquad b=5,\qquad T=L+2=2h+2.
\]

Thus the moving-centre offset is \(k=b-h=5-h<0\).  Let the adjacent
low-tail orbit be

\[
\begin{aligned}
x_3&=\binom{h+3}{3}+\binom42+2-2h,\\
y_3&=\binom{h+4}{3}+\binom52+2-2h,\\
x_{p+1}&=U_p(x_p)-(2h+2),\\
y_{p+1}&=U_p(y_p)-(2h+3),\\
\gamma_p&=y_{p+1}-S_p(x_p).
\end{aligned}
\tag{1.1}
\]

The family is not a counterexample to Erdős #776.  It is a second,
two-sided obstruction to any **fixed** post-carry diagonal seed and refutes
the tempting interim claim that all negative offsets seed by rank five.

## 2. Stable canonical words

Define

\[
A_3=9,\qquad B_3=15
\tag{2.1}
\]

and, for \(p\ge3\),

\[
\boxed{
 A_{p+1}=\binom{A_p}{2}+11-6p,\qquad
 B_{p+1}=\binom{B_p}{2}+12-6p.}
\tag{2.2}
\]

The first constants are

\[
\begin{array}{c|rrrrrr}
p&3&4&5&6&7&8\\ \hline
A_p&9&29&393&77009&2965154511&4396070635569247274\\
B_p&15&99&4839&11705523&68509628498979&
2346784598534023539487771701.
\end{array}
\tag{2.3}
\]

### Theorem 2.1 (fixed-rank left-wall normal form)

Fix \(P\ge3\).  For all sufficiently large dyadic \(h\), and every
\(3\le p\le P\), the canonical words are

\[
\begin{aligned}
x_p={}&\binom{h+2}{p}
 +\sum_{r=3}^{p-1}\binom{h+3r-3p+2}{r}
 +\binom{h+9-3p}{2}+\binom{A_p}{1},\\
y_p={}&\binom{h+3}{p}
 +\sum_{r=3}^{p-1}\binom{h+3r-3p+3}{r}
 +\binom{h+10-3p}{2}+\binom{B_p}{1}.
\end{aligned}
\tag{2.4}
\]

Consequently

\[
\boxed{
\gamma_p=K_p-2h,\qquad
K_p=\binom{B_p}{2}-\binom{A_p+1}{2}-3.}
\tag{2.5}
\]

#### Proof

At rank three, two Pascal borrows give

\[
x_3=\binom{h+2}{3}+\binom h2+\binom91,\qquad
y_3=\binom{h+3}{3}+\binom{h+1}{2}+\binom{15}{1}.
\]

Suppose (2.4) holds at rank \(p\).  All terms of lower rank at least
three shift into the displayed next word.  If
\(d=h+9-3p\), the bottom of the \(x\)-word uses

\[
\binom d3+\binom{A_p}{2}-(2h+2)
=\binom{d-1}{3}+\binom{d-3}{2}
 +\binom{A_p}{2}+11-6p.
\]

The adjacent calculation, with \(d+1\) and tax \(2h+3\), leaves
\(\binom{B_p}{2}+12-6p\).  This is exactly (2.2), so induction proves
(2.4) once \(h\) exceeds the finitely many canonicality thresholds.

In \(U_p(y_p)-S_p(x_p)\), every \(h\)-dependent binomial cancels by
Pascal's identity.  The constant tails leave (2.5).  The same separated
high-block cancellation as in the inherited first-carry localization gives
\(\Gamma_{j+p-2}=\gamma_p\) for every fixed \(p\le P\), once \(h\) is
large enough. \(\square\)

### Corollary 2.2 (a second no-fixed-rank theorem)

For every fixed \(P\), arbitrarily large dyadic strips satisfy

\[
\gamma_3,\gamma_4,\ldots,\gamma_P<0
\]

at the negative offset \(b=5\).  In particular, no fixed-rank theorem can
dispose of the omitted half-strip \(k<0\).

This follows immediately by choosing \(2h>\max_{p\le P}K_p\) after
the words have become canonical.

## 3. Exact first failure of the rank-five candidate on this family

The first values of (2.5) are

\[
K_3=57,\quad K_4=4413,\quad K_5=11628117,\quad
K_6=68506663267455.
\tag{3.1}
\]

The first dyadic strip on the fixed family \(b=5\) with
\(\gamma_5<0\) is \(j=17\):

\[
(j,L,h,b)=(17,14680064,7340032,5),\qquad
\boxed{\gamma_5=-3051947}.
\tag{3.2}
\]

The next rank succeeds, after a genuine rank-one cap overflow in the
\(y_6\)-word:

\[
\boxed{\gamma_6=36463781155415>0.}
\tag{3.3}
\]

The complete integer state is frozen in
`left_b5_rank5_counterexample_certificate.json`.  Two Macaulay
implementations and the uncompressed global orbit verify

\[
\Gamma_{20}=\gamma_5=-3051947,\qquad
\Gamma_{21}=\gamma_6=36463781155415.
\]

Minimality in (3.2) is only **within the symbolic family \(b=5\)**.  The
six small cap-overflow strips \(2\le j\le6\) are checked exactly by the
verifier; from \(j=7\) onward (2.5) is literal, and
\(224·2^{15}<K_5<224·2^{16}\).  The asserted first strip then follows
directly from (2.5).  No
claim of global first failure over all negative offsets is made.

## 4. Sharp adaptive scale on the left wall

Let

\[
p_*(h)=\min\{p\ge3:K_p\ge2h\}.
\tag{4.1}
\]

### Lemma 4.1 (uniform canonicality and global localization)

For all sufficiently large dyadic \(h=112·2^{j-1}\), the following hold
simultaneously for every \(3\le p<p_*(h)\):

1. both words in (2.4) are canonical;
2. the local recurrences (1.1) equal those words, without a fixed-(P)
   quantifier;
3. the local tail remains separated from the inherited global high block,
   and

   \[
   \Gamma_{j+p-2}=\gamma_p.
   \tag{4.2}
   \]

At \(p=p_*(h)\), the \(x\)-word is canonical, the \(y\)-value is the
integer represented by its possibly noncanonical formal word, and the same
local-to-global equality remains valid.

#### Proof

The quadratic bounds (4.4) and (4.6) below imply

\[
p_*(h)=O(\log\log h),\qquad
B_p<\sqrt{8h}\quad(4\le p<p_*(h)).
\tag{4.3}
\]

Consequently, uniformly over all these growing ranks,

\[
3p=o(h),\qquad A_p<B_p<h+10-3p.
\]

The upper indices in (2.4) are therefore positive and strictly ordered:
the leading index is (h+2) (respectively (h+3)), the intermediate
indices drop by three when their lower rank drops by one, the rank-two
index is (h+9-3p) (respectively (h+10-3p)), and the rank-one constant
lies strictly below it.  Thus the induction in Theorem 2.1 applies
simultaneously up to \(p_*(h)-1\), rather than only for a fixed \(P\).

At the candidate rank, minimality and (4.5)--(4.6) below give

\[
B_{p_*(h)}\le4h,\qquad
A_{p_*(h)}\le(4h)^{3/4}<h+9-3p_*(h).
\]

Hence the (x)-word is still canonical.  The formal (y)-word is the
exact integer obtained by applying \(U_{p-1}\) to the preceding canonical
word and subtracting its tax; only its bottom suffix may need
normalization.

For completeness, the global separation is also uniform in this range.
Here \(M=T-221=2h-219\), and the lowest upper index in the inherited high
block at the first-carry row is

\[
M-A_{j-3}-2=\frac{3h}{2}+3,
\]

whereas the local leading upper indices are (h+2,h+3).  Subsequent upper
shifts change lower ranks but not these upper indices.  Since
\(p_*(h)=o(h)\), every subtraction is absorbed in the nonnegative local
tail and the gap to the high block stays at least \(h/2-O(p_*(h))\).
Pairwise Pascal cancellation of the separated high block therefore proves
(4.2), including the candidate cap row.  Finally
\(j+p_*(h)-2<M-42\), so every displayed row is legal. \(\square\)

### Theorem 4.2 (left-wall adaptive delay)

For all sufficiently large dyadic \(h\), the first successful rank on
\(b=5\) is exactly \(p_*(h)\), and

\[
\boxed{p_*(h)=\log_2\log h+O(1).}
\tag{4.4}
\]

#### Proof

For \(p\ge4\), direct induction from \(A_4=29,B_4=99\) gives

\[
A_p\le B_p/2,\qquad A_p^4\le B_p^3,\qquad
\frac25B_p^2\le B_{p+1}\le\frac12B_p^2.
\tag{4.5}
\]

For the lower quadratic bound, note that \(B_p\ge20p\); then (2.2)
gives \(B_{p+1}\ge(2/5)B_p^2\).  The two comparisons involving \(A_p\)
hold at \(p=4\).  They propagate using
\(A_{p+1}\le A_p^2/2\), the lower bound for \(B_{p+1}\), and
\(1/16<8/125\).  The estimate \(A_p\le B_p/2\), substituted directly
in the definition of \(K_p\), also gives the lower bound below (already
for \(B_p\ge99\)):

\[
\frac14B_p^2\le K_p\le\frac12B_p^2
\tag{4.6}
\]

for \(p\ge4\).  The doubly quadratic recurrence now proves existence of
\(p_*(h)\) and (4.4).

If \(p<p_*(h)\), Lemma 4.1 makes (2.5) literal, and its value is negative.

At \(p=p_*(h)\), Lemma 4.1 makes the \(x_p\)-word canonical and leaves
only the bottom of the \(y_p\)-word to normalize.  Its bounds are

\[
B_p\le4h,\qquad A_p\le B_p^{3/4}\le(4h)^{3/4}.
\tag{4.7}
\]

Put \(d=h+10-3p\), the upper
index of the formal rank-two term in \(y_p\).  If \(B_p<d\), the
\(y_p\)-word is also canonical and (2.5) gives \(\gamma_p\ge0\).

If \(B_p\ge d\), monotonicity permits replacing the \(y_p\) suffix

\[
\binom d2+\binom{B_p}1
\]

by the smaller canonical block \(\binom{d+1}{2}\).  Cancellation with
the canonical \(x_p\)-word gives

\[
\gamma_p\ge
\binom d2-\binom{A_p+1}{2}-(2h+3)>0
\tag{4.8}
\]

for all sufficiently large \(h\), by (4.4) and (4.7).  Therefore rank
\(p_*(h)\) succeeds and every earlier rank fails. \(\square\)

## 5. Consequence for the uniform programme

The negative half-strip cannot be assigned a bounded rank.  Any uniform
proof must be adaptive on both sides of the moving centre.  The new family
does not appear slower than the inherited \(b=h+5\) wall, but comparing the
two recurrences is not yet a proof that those two families dominate every
moving offset.  That comparison is the remaining pre-cap quantifier.
