# Blind reconstruction: rank-8 global campaign

## Protocol

This file was frozen before reading `kill_tests.json`, any campaign file under
`evidence/`, the campaign verifier, or the pre-existing `audit.json`.  The
inputs were the closure contract and state, information-loss map,
representation/mechanism/survivor registries, the statement and dependency
claims in `decisive_lemma.json`, and the read-only R004 source definitions of
the canonical/Kruskal--Katona operator.  In particular, no author proof of the
prefix or high-rank bridge was used in deriving the statements below.

## 1. Canonical expansion and prefix separation

For an integer \(x\ge0\), its \(q\)-canonical expansion is

\[
 x=\binom{a_q}{q}+\binom{a_{q-1}}{q-1}+\cdots+
   \binom{a_j}{j},
 \qquad a_q>a_{q-1}>\cdots>a_j\ge j,
\]

with absent trailing terms allowed.  Define the lower-shadow integer

\[
 \operatorname{KK}_q(x)=
 \binom{a_q}{q-1}+\binom{a_{q-1}}{q-2}+\cdots+
 \binom{a_j}{j-1}.
\]

The exact prefix lemma that is available without circularity is the
following concatenation statement.  Let \(q>s\ge1\), let

\[
 P=\sum_{i=s+1}^{q}\binom{a_i}{i},
 \qquad a_q>a_{q-1}>\cdots>a_{s+1}\ge s+1,
\]

be a legal canonical prefix, and let \(x\) be an integer satisfying

\[
 0\le x<\binom{a_{s+1}}s. \tag{PC-separator}
\]

The top index in the \(s\)-canonical expansion of \(x\) is then strictly
less than \(a_{s+1}\).  Indeed the sum of all admissible \(s\)-canonical
terms with top below \(a_{s+1}\) ranges exactly from zero through
\(\binom{a_{s+1}}s-1\).  Hence the canonical word of \(P+x\) is the
concatenation of the displayed prefix and the canonical word of \(x\), and

\[
 \operatorname{KK}_q(P+x)
 =\sum_{i=s+1}^{q}\binom{a_i}{i-1}
  +\operatorname{KK}_s(x). \tag{PC}
\]

For two suffixes \(x,y\) sharing the *same* prefix and each satisfying the
separator condition, subtraction of (PC) cancels the prefix exactly.  The
strict upper bound and nonnegativity are essential.  Prefix cancellation
cannot be invoked merely because two scalar states are close, and it cannot
assume the desired rank-6 cap in order to prove that same cap.

For the campaign's state

\[
 D^{[V]}_{V-12}=0,\qquad
 D^{[V]}_{q-1}=V+\operatorname{KK}_q(D^{[V]}_q),
\]

put

\[
 B_r(V)=\binom{V-12}{r+2}+\binom{V-13}{r+1},
 \qquad W_r(V)=D^{[V]}_{r+2}-B_r(V).
\]

If

\[
 0\le W_r(V)<\binom{V-13}{r}, \tag{S_r(V)}
\]

then (PC), with the two-term prefix at lower ranks \(r+2,r+1\), gives

\[
 \operatorname{KK}_{r+2}(D^{[V]}_{r+2})
 =\binom{V-12}{r+1}+\binom{V-13}{r}
  +\operatorname{KK}_r(W_r(V)).
\]

After adding the tax \(V\) and subtracting \(B_{r-1}(V)\), this becomes

\[
 W_{r-1}(V)=V+\operatorname{KK}_r(W_r(V)). \tag{1}
\]

No rank-6 separator is needed to derive \(W_6\): the last application of
(1) uses \(S_7(V)\).  Conversely, using \(S_6(V)\) as an input to prove the
rank-8 cap would be circular, since \(S_6(V)\)'s strict upper bound is exactly
the target.

## 2. One-sided KK carry bound and exact constants

For every rank \(r\ge2\) and nonnegative integers \(x,y\),

\[
 \operatorname{KK}_r(x+y)
 \le \operatorname{KK}_r(x)+\operatorname{KK}_r(y). \tag{2}
\]

One proof takes colex-minimal families of sizes \(x\) and \(y\) on disjoint
ground sets.  Their union is an \(r\)-uniform family of size \(x+y\) whose
two lower shadows are disjoint; the Kruskal--Katona minimum for size \(x+y\)
is no larger.  Monotonicity and (2) imply the one-sided carry inequality

\[
 y\le x+b\quad\Longrightarrow\quad
 \operatorname{KK}_r(y)-\operatorname{KK}_r(x)
 \le\operatorname{KK}_r(b)\le r b, \tag{3}
\]

where the last inequality follows termwise from
\(\binom ai{i-1}\le i\binom ai i\le r\binom ai i\).

Assume the decisive lemma's separators \(S_r(V)\) for every
\(7\le r\le14\) and every \(V\ge125\), and assume

\[
 W_{14}(V+1)-W_{14}(V)\le1. \tag{4}
\]

Define \(b_{14}=1\) and recursively

\[
 b_{r-1}=1+r b_r\qquad(7\le r\le14). \tag{5}
\]

Equations (1), applied separately at \(V\) and \(V+1\), together with
(3), show inductively that

\[
 W_r(V+1)-W_r(V)\le b_r\qquad(6\le r\le14). \tag{6}
\]

The exact integer ledger is

\[
\begin{array}{c|rrrrrrrrr}
r&14&13&12&11&10&9&8&7&6\\ \hline
b_r&1&15&196&2353&25884&258841&2329570&18636561&130455928.
\end{array}
\]

Thus the large final constant is a deliberately crude consequence of
\(\operatorname{KK}_r(b)\le rb\), not a finite fit.  Using the sharper
\(1+\operatorname{KK}_r(b_r)\) recursion would yield smaller constants, but
is unnecessary.

## 3. Base case, cap induction, and off-by-one audit

Pascal's identity gives

\[
 \binom{V-11}{8}-B_6(V)=\binom{V-13}{6}. \tag{7}
\]

Therefore the local rank-8 entry is exactly

\[
 D^{[V]}_8<\binom{V-11}{8}
 \quad\Longleftrightarrow\quad
 W_6(V)<\binom{V-13}{6}. \tag{8}
\]

The capacity increment from \(V\) to \(V+1\) is

\[
 \binom{V-12}{6}-\binom{V-13}{6}
 =\binom{V-13}{5}. \tag{9}
\]

At the first induction transition \(V=125\to126\),

\[
 b_6=130455928
 <\binom{112}{5}=134153712. \tag{10}
\]

The right side of (9) is nondecreasing thereafter, so (6) at rank six is
strictly smaller than every subsequent cap increment.  Consequently a
verified base inequality at \(V=125\) propagates to all \(V\ge125\).
A finite bridge covering every integer \(40\le V\le125\), inclusive, then
combines with this induction to cover every integer \(V\ge40\).

There is no off-by-one at the join provided the high-rank hypotheses are
asserted for *all* \(V\ge125\): the transition \(125\to126\) uses the
separator statements at both 125 and 126 and the jump clause indexed by 125.
A scan ending at 125 alone cannot verify those all-parameter hypotheses; it
can verify only the base rank-8 inequality.

## 4. What is and is not closed

The decisive lemma consists precisely of the unproved universal separator
and one-Lipschitz hypotheses.  If they are known only through a finite scan,
then the implication above is an exact conditional theorem but the all-\(V\)
rank-8 entry is not proved.  A scan through 500, 1000, or any other fixed
cutoff cannot cross the AMRA all-parameter gate.

Even a proof of (8) for all \(V\ge40\) would close only the local rank-8
interface.  The closure contract explicitly records that the following are
still separate obligations:

1. replay the inherited rank-8-to-rank-2 tail at its exact ranges;
2. supply a complete integer map from every relevant multiplicity \(r\) and
   every sufficiently large Boolean dimension \(n\) to an admissible \(V\);
3. prove the resulting construction for *every* \(n>n_0(r)\), not one
   parity or an unbounded subsequence;
4. establish the matching sharp nonexistence boundary and reconcile all
   exceptional small \(r\).

Thus the rank-8 entry alone neither determines exact \(n_0(r)\) nor, absent
the parameter replay, establishes the advertised scoped upper-term
improvement.

## 5. Blind mechanism-status assessment

The two survivors are honestly labelled conditional at the registry level:
M776G-01 requires a new all-parameter high-rank separator/one-Lipschitz
theorem, while M776G-02 has only finite top-height falsifier evidence and
also needs its stated capacity comparison.  Neither is a promotion result.

The advertised finite counterexamples to M776G-03--M776G-08 and M776G-11
are in principle decisive because their statements are universal and one
exact counterexample suffices; their values must be independently replayed
after unblinding.  M776G-09 is a circularity rejection, M776G-10 rejects an
unsupported implication from scalar order rather than the actual normalized
ratio, and M776G-12 correctly rejects the implication from local rank-8 entry
to exact public threshold.  Those scopes must not be broadened.

On the blind record, the correct provisional decision is **continue at
survivor deepening**, not promote: the bridge is conditional but the two
survivors are concrete all-parameter targets rather than exhausted cosmetic
variants.  Freeze would be justified only if unblinding reveals that their
stated mechanisms are circular or already falsified.  The original problem
and exact threshold remain unchanged.
