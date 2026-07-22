# Erdős #635 (`t=2`): odd-neighbour collisions are chains

Date: 2026-07-22 (Asia/Hong_Kong)

Status: rigorous reformulation and route narrowing; it does not prove the
candidate exact formula or `N/2+O(log N)`.

## 1. Poset

For every even non-power of two write

\[
 x=2^{a(x)}u(x),\qquad u(x)\ge3\text{ odd}.
\]

Define

\[
 x\preceq y
 \quad\Longleftrightarrow\quad
 a(x)\le a(y)\ \hbox{and}\ u(x)\ge u(y).          \tag{1}
\]

Thus moving upward in the poset means increasing the 2-adic layer and
decreasing the odd part.

## 2. Chain-neighbour theorem

Let `S` be an independent set in the `t=2` conflict graph, consisting of even
non-powers of two.  For every odd vertex `b`, the set

\[
 N_S(b)=\{x\in S:x\sim b\}
\]

is a chain under (1).

Indeed, take distinct `x=2^a u` and `y=2^c v` in `N_S(b)`.  If `a=c`, the two
vertices are automatically comparable under (1), since their odd parts are
distinct.  If `a!=c`, apply the round-7 all-odd-divisor inversion theorem to
the common neighbour `b`: after assuming `a<c`, it gives `v<u`.  Hence
`x prec y`.  This proves the assertion.

Equivalently:

> two incomparable vertices of an independent even set have disjoint odd
> conflict-neighbourhoods.

This packages all the separate lower/upper canonical collision inequalities
into one order-theoretic statement and uses *every* odd-divisor edge, not only
the full-odd-part neighbours.

## 3. Immediate matching consequence

If `T subset S` is an antichain, choose for each `x=2^a u in T` its always
legal lower odd neighbour

\[
 L(x)=(2^a-1)u.
\]

The chosen neighbours are distinct: equality would make two members of `T`
share an odd neighbour, contradicting the theorem.  Thus every antichain has
an explicit matching into the odd vertices.  In particular,

\[
 |N_{\rm odd}(S)|\ge \operatorname{width}(S).      \tag{2}
\]

The earlier "no inversion" private-neighbour result is precisely the regime
where the relevant vertices behave antichain-like in this order.

## 4. Exact remaining obstruction

Formula (2) alone is far too weak: a large independent set may contain long
chains

\[
 a_1<a_2<\cdots,qquad u_1>u_2>\cdots.
\]

Every collision is confined to such chains, so the original number-theory
problem has now become a chain-expansion problem:

\[
 \text{prove that the union of odd neighbourhoods of every independent
 chain has size at least its length, up to the power-of-two exceptions.}
\]

Chain-neighbourhood incidence by itself does not imply Hall expansion; an
abstract chain hypergraph can have many left vertices with the same right
neighbour.  The arithmetic still has to rule that out using divisor sizes,
boundary control, or the forced lower-fibre-to-upper-fibre escape from round
6.  Therefore this reformulation is a genuine simplification of where the
hard case lives, but not an upper bound.

## 5. Status correction for the official problem

The official asymptotic question `|A| <= (1/2+o_t(1))N` already has an
affirmative proof.  Any publishable continuation must concern the exact
extremum, the `t=2` secondary term/stability, or another genuinely sharper
quantitative theorem.  Reproving the `o_t(1)` statement cannot count as new
progress.
