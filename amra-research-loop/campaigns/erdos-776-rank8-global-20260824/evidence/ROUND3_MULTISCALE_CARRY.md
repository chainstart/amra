# Round 3 multiscale carry route: an infinite actual-orbit obstruction

## Scope and outcome

This route studies only `M776G-02-logarithmic-carry-height`. It does not use
the adjacent `B_2`/H2 route or any round-3 artifact from the other author.

The proposed dichotomy is **refuted on the actual shortened orbit**. In fact,
for every `V>=40`,

\[
W_6(V)\ge V.                                           \tag{1}
\]

Consequently, for every `m>=21`, the actual parameter `V=2^m` has
`W_6(V)>0` and six-canonical top

\[
T(V)>m+13=\lceil\log_2V\rceil+13.                     \tag{2}
\]

This is an infinite all-parameter counterfamily, not an extrapolation from a
finite scan.

## The first tax already gives the complete two-term baseline

Write

\[
P_q(V)={V-12\choose q}+{V-13\choose q-1}.
\]

Let `R=V-13`. Isolate the first tax by defining

\[
F_R=V,\qquad F_{q-1}=\operatorname{KK}_q(F_q)
\quad (q=R,R-1,\ldots,9).                              \tag{3}
\]

We claim that

\[
F_q=P_q(V)\qquad(8\le q\le12).                        \tag{4}
\]

The `R`-canonical expansion of the first tax is exact:

\[
V={V-12\choose R}
  +\sum_{j=1}^{12}{V-13-j\choose R-j}.                \tag{5}
\]

Indeed, the first term is `V-12` and every summand in the sum is one.
The upper indices strictly decrease, so (5) is canonical. Apply `R-12`
successive lower shadows. Until the last step the displayed terms remain a
valid separated canonical list. At the last step the final lower-one term
contributes its numerical shadow `{a choose 0}=1`. Thus

\[
F_{12}={V-12\choose12}
 +\sum_{j=1}^{12}{V-13-j\choose12-j}.                 \tag{6}
\]

With `k=12-j`, the second sum is the hockey-stick sum

\[
\sum_{k=0}^{11}{V-25+k\choose k}={V-13\choose11}.
\]

This proves `F_12=P_12(V)`. The two displayed terms of `P_q` form a
separated canonical word, and one more lower shadow sends `P_q` exactly to
`P_(q-1)`. Hence (4) follows down to rank eight.

## Monotonicity forces a linear residual floor

The actual shortened orbit satisfies

\[
D_R=V,
\qquad D_{q-1}=V+\operatorname{KK}_q(D_q).            \tag{7}
\]

Since Macaulay shadow is monotone, (3) and (7) give `D_q>=F_q` at every
common rank by induction. In particular `D_9>=F_9=P_9(V)`. The last actual
step retains its own positive tax:

\[
\begin{aligned}
D_8
 &=V+\operatorname{KK}_9(D_9)\\
 &\ge V+\operatorname{KK}_9(P_9(V))\\
 &=V+P_8(V).
\end{aligned}                                         \tag{8}
\]

By definition `W_6(V)=D_8-P_8(V)`, so (8) proves (1). Notice that this
argument never assumes a residual separator, H1, H2, adjacent coupling, or
the target rank-eight cap.

## Dyadic parameters contradict logarithmic top height

For a positive integer `x`, if the top upper index of its six-canonical
expansion is at most `B`, then

\[
x<{B+1\choose6}.                                      \tag{9}
\]

This is the defining interval for the leading combinadic digit (equivalently,
the maximum word with top at most `B` is `{B+1 choose 6}-1`).

Take `V=2^m`. If M776G-02 held, its positive branch and (9) would give

\[
W_6(2^m)<{m+14\choose6}.                              \tag{10}
\]

But

\[
2^{21}=2097152>{35\choose6}=1623160.                 \tag{11}
\]

Moreover

\[
\frac{{m+15\choose6}}{{m+14\choose6}}
=\frac{m+15}{m+9}<2                                  \tag{12}
\]

for every `m>=21`. Equations (11)--(12) inductively give
`2^m>{m+14 choose 6}` for every `m>=21`. Combining this with (1)
contradicts (10) and proves (2).

More generally, (1) implies

\[
T(V)\ge\max\{t:{t\choose6}\le V\},                  \tag{13}
\]

so actual record carry walls have an unavoidable scale of order
`V^(1/6)`, not `log V`. No dyadic-spacing injection can prove the frozen
logarithmic claim.

## Exact classification

- `M776G-02-logarithmic-carry-height`: **refuted**, by the infinite actual
  orbit family `V=2^m`, `m>=21`.
- The earlier finite scan through `V=500` remains consistent: its parameters
  lie far below the first dyadic member of this symbolic counterfamily.
- The rank-eight entry `W_6(V)<{V-13 choose 6}` is not refuted. A linear
  lower floor is vastly smaller than its sixth-degree capacity.
- The public Erdős 776 statement, its exact threshold, main term, and main
  exponent are unchanged.

`evidence/verify_round3_multiscale_carry.py` guards the exact first-tax
identity on independent finite instances, the actual-orbit lower bound on
falsifier instances, the dyadic base arithmetic, and the canonical-top
interval. The universal content is the symbolic proof above.
