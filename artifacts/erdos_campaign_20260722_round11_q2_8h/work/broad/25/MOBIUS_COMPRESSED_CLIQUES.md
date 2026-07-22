# Erdős #25: Möbius-compressed activated CRT intersections

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous sufficient conditions for natural and logarithmic density;
not a full solution of the official problem.

## 1. Activated intersection states

At cutoff `X`, retain the globally nonredundant forbidden classes with
`n_i<=X`.  For a nonempty compatible clique `Q`, write

\[
 L_Q=\mathop{\rm lcm}_{i\in Q}n_i,\quad
 1\le r_Q\le L_Q,\quad M_Q=\max_{i\in Q}n_i.
\]

Here `r_Q` is the least positive joint CRT representative, with zero
represented by `L_Q`.  Since `M_Q<=L_Q`, activation either keeps `r_Q` or
deletes precisely that first representative.  Put

\[
 \epsilon_Q={\bf1}_{r_Q<M_Q}\in\{0,1\}.
\]

The activated intersection is exactly

\[
 D_Q=\{r_Q+(k+\epsilon_Q)L_Q:k\ge0\}.             \tag{1}
\]

Different cliques can give the same triple `(L_Q,r_Q,epsilon_Q)`.  Paying an
endpoint error for every clique separately discards exact
inclusion--exclusion cancellation.

## 2. Compressed theorem

For every realised triple `D=(L,r,epsilon)`, define

\[
 \mu_X(D)=\sum_{\substack{Q\ne\varnothing\ {\rm compatible}\\
                    (L_Q,r_Q,\epsilon_Q)=D}}(-1)^{|Q|}.   \tag{2}
\]

Discard zero coefficients and set

\[
 {\cal B}_\mu(X)=1+\sum_D|\mu_X(D)|
 \left\{{2\over r_D}+{2+\log(2L_D)\over L_D}\right\}.   \tag{3}
\]

**Theorem.**  If

\[
 \boxed{{\cal B}_\mu(X)=o(\log X),}                       \tag{4}
\]

then the activated survivor set in Erdős #25 has logarithmic density
`delta=lim_(X->infinity) delta_X`, where `delta_X` is the density of the
finite complete periodic sieve.

## 3. Proof

Finite inclusion--exclusion and (1) give exactly

\[
 {\bf1}_{A}(m)=1+\sum_D\mu_X(D){\bf1}_D(m)
 \qquad(m\le X).                                      \tag{5}
\]

Classes with modulus above `X` are inactive on this interval.  The same
finite inclusion--exclusion over the complete periodic classes gives

\[
 \delta_X=1+\sum_D{\mu_X(D)\over L_D}.              \tag{6}
\]

Grouping by `epsilon` in (6) is harmless: all cliques in a fixed triple have
the same `L_D`, while complete-class density ignores activation.

The progression lemma in `HARMONIC_WEIGHTED_CLIQUES.md` applies to every
`D`; `epsilon=1` is exactly the one deleted representative paid for by its
second `1/r_D` term.  Hence (5)--(6) imply

\[
 \left|H_A(X)-\delta_X\log X\right|
 \le {\cal B}_\mu(X).                               \tag{7}
\]

Divide by `log X`, use (4), and use monotone convergence of `delta_X`.

### A sharper two-state compression

The activation bit can itself be eliminated before taking absolute values.
For each complete CRT state `(L,r)`, put

\[
 a_X(L,r)=\sum_{Q:(L_Q,r_Q)=(L,r)}(-1)^{|Q|},
\]

and let `b_X(L,r)` be the same sum restricted to cliques with
`r_Q<M_Q`.  If `S_(L,r)(X)` denotes the harmonic sum over the complete
progression, then `r_Q<M_Q<=X` implies the exact identity

\[
 \sum_{Q:(L_Q,r_Q)=(L,r)}(-1)^{|Q|}S_Q(X)
 =a_X(L,r)S_{L,r}(X)-{b_X(L,r)\over r}.            \tag{8}
\]

The complete finite-sieve density contribution is `a_X(L,r)/L`.  Using the
unactivated progression bound therefore gives

\[
\begin{aligned}
 |H_A(X)-\delta_X\log X|
 \le 1+\sum_{L,r}\bigg[&|a_X(L,r)|
 \left\{{1\over r}+{2+\log(2L)\over L}\right\}\\
 &+{|b_X(L,r)|\over r}\bigg]=:{\cal B}_*(X).      \tag{9}
\end{aligned}
\]

Thus `B_*(X)=o(log X)` is a no-more-restrictive sufficient condition.  It never
costs more than (3): first combine the two activation states in their common
complete progression and only then pay for the actually deleted first
representative.

The same two-state identity also yields a natural-density criterion.  A
complete progression count differs from `X/L` by less than one, while an
activated state deletes at most its first representative.  Hence

\[
 |A(X)-\delta_XX|
 \le\sum_{L,r}\bigl(|a_X(L,r)|+|b_X(L,r)|\bigr).   \tag{10}
\]

Consequently

\[
 \boxed{\sum_{L,r}(|a_X(L,r)|+|b_X(L,r)|)=o(X)}    \tag{11}
\]

implies that `A` has natural density `delta`.  This is the Möbius-compressed
counterpart of the raw `o(X)` clique theorem.

## 4. Exact separation from raw clique counting

The triangle inequality inside each fibre of
`Q -> (L_Q,r_Q,epsilon_Q)` shows that (3) never exceeds the uncompressed
harmonic clique boundary.

The saving can be exponential after global redundancy removal.  Let
`L=p_1...p_k` be squarefree and use zero classes with moduli `L/p_i`.
No one contains another.  Every clique of size at least two has the same
state `(L,L,0)`, whose compressed coefficient is

\[
 \sum_{j=2}^k(-1)^j\binom kj=k-1,                  \tag{12}
\]

whereas raw counting pays `2^k-k-1` copies of the same boundary term.
This is a realised congruence-system separation.

It is only a finite-block separation of the two error functionals.  We have
not constructed an infinite activated system for which the compressed
criterion holds and every earlier criterion fails; therefore no strict
separation of covered system classes is claimed.

## 5. Boundary

Condition (4) is not proved for every system.  Distinct activated states can
still have large total variation, and (7) discards cancellation between
different progressions.  Thus #25 remains open.  The next global target is a
total-variation or signed-discrepancy bound for the compressed intersection
poset, not another raw clique count.
