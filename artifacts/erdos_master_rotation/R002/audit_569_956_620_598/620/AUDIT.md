# Erdős Problem #620 — independent evidence audit

## Verdict

`verified_closed`

Evidence class: **fixed preprint, not yet peer reviewed**.  The fixed object audited here is
Morris–Sahasrabudhe–Verstraëte, arXiv:2607.16118v1 (submitted 17 July
2026).  Its theorem, if read at \(s=3\), settles the asymptotic question on the
official page.  The website still labels #620 `OPEN`; that label predates, or has
not yet incorporated, this six-day-old preprint.

This verdict means “the v1 manuscript contains a complete proof sufficient to
classify the problem as closed by preprint evidence”.  It does **not** mean
peer-review acceptance or formal verification.

## Exact statement mapping

The official question asks for the guaranteed order of the largest
triangle-free induced subgraph in every \(n\)-vertex \(K_4\)-free graph.
Equivalently, if

\[
f_3(n)=\min_{\substack{|V(G)|=n\\K_4\nsubseteq G}}
       \max\{|S|:K_3\nsubseteq G[S]\},
\]

then it asks for the order of \(f_3(n)\).  The preprint defines \(f_s(n)\) as
the largest \(K_s\)-free vertex set guaranteed in every \(K_{s+1}\)-free
\(n\)-vertex graph, and explicitly identifies it with
\(f_{s,s+1}(n)\).  “A \(K_3\)-free set of vertices” means exactly that the
induced graph on that set is triangle-free.  Thus its \(s=3\) specialization
has no induced/non-induced or extremal-function mismatch.

Theorem 1.1 states, for every fixed \(s\ge2\),

\[
f_s(n)=\Theta(\sqrt{n\log n})\qquad(n\to\infty).
\]

Consequently #620 has the answer
\(f(n)=\Theta(\sqrt{n\log n})\).

## Lower bound and cited-source audit

The lower bound is not merely asserted.  The manuscript invokes Corollary 2 of
Joret–Micek–Reed–Smid, *Tight bounds on the clique chromatic number*, EJC
28(3) (2021), P3.51.  The published paper defines a clique colouring as one
with no monochromatic inclusion-wise maximal clique of size at least two and
proves that every \(n\)-vertex graph has such a colouring with
\(O(\sqrt{n/\log n})\) colours.

For a \(K_{s+1}\)-free graph, every copy of \(K_s\) is inclusion-wise maximal:
an additional common neighbour would form a \(K_{s+1}\).  Therefore no colour
class contains a \(K_s\).  The largest colour class has size

\[
\Omega\!\left(n/\sqrt{n/\log n}\right)
=\Omega(\sqrt{n\log n}).
\]

This transfer is valid for every \(s\ge2\), with an absolute implicit
constant.  The isolated-vertex exception in the definition of clique
colouring is irrelevant because \(s\ge2\).

## Upper-bound proof audit

### Lemma 2.3

The construction is the union of two random blow-ups of balanced
\(s\)-partite graphs, followed by two deletion steps.  The first deletion
ensures that every surviving edge belongs to a unique blow-up \(J^*\).  If a
putative \(K_{s+1}\) lies in one \(J^*\), it contradicts \(s\)-partiteness.
Otherwise, choose an edge \(xy\), its unique \(J^*\), and a vertex
\(z\notin V(J^*)\); the triangle \(xyz\) is not contained in a single
blow-up and the second deletion removes one of its edges.  Both cases cover
all possibilities.  The argument also works at \(s=2\).

### Lemma 3.4

For a set whose \(A\)-projection has at least \(k\) elements, monotonicity
reduces to a transversal \(k\)-set.  Lemma 4.1 gives at least \(m/2\) sampled
blow-ups meeting it in a \(K_s\), except with probability \(e^{-m}\).
Revealing \(B\) first and the \(A\)-blow-ups in random order, every destroyed
candidate clique has a deletion witness exposed earlier with probability at
least \(1/3\).  On the event \(\mathcal E_\beta\), a uniform candidate
\(s\)-set contains an already closed pair with conditional probability at
most

\[
\beta k^2\binom{s}{2}/\binom{k}{2}\le\beta s^2=2^{-7}.
\]

The binomial-union estimate then gives \(6e^{-m/12}\le e^{-m/15}\);
together with the \(e^{-m}\) exceptional event this is at most
\(e^{-m/16}\) for the stated large-\(n\) regime.  Conditioning on the set of
successful blow-ups preserves the uniformity used in this calculation; no
independence stronger than the sequential conditional bound is needed.

### Lemma 3.5

The proof first obtains a simultaneous bound for closed pairs in every
eligible set \(T\subset V(A)\), using four global pseudorandom properties of
the sampled family of blow-ups.  Dyadic decomposition of the intersection
sizes then yields

\[
|X_A(T)|\le C^6s^2t\ell\log n/r+t^2n^{-c/6}
          \le(\beta/8)\binom t2.
\]

For an arbitrary \(k\)-set \(S\) in the \(r\)-blow-up, the auxiliary random
set \(T\) selects each base vertex with probability
\(|U_i\cap S|/r\).  Hence \(\mathbb E|T|=k/r\), and weighted closed pairs in
\(S\) equal \(r^2\mathbb E|X_A(T)|\), apart from at most \(rk\) within-part
pairs.  Chernoff concentration puts \(|T|\) in
\([k/(2r),2k/r]\); the exponentially small tail and the displayed constant
slack absorb both its contribution and \(rk\).  Because the base-graph
properties hold simultaneously for all \(T\), this conclusion is uniform
over all \(S\), as Lemma 3.5 requires.  Symmetry supplies the corresponding
\(B^*\) bound.

The manuscript compresses the negligible-tail term in this last expectation
and does not spell out integer rounding of \(r,\ell,m,k\).  Both are routine:
the bad-tail contribution is exponentially small compared with \(k^2/r^2\),
and floors/ceilings are absorbed by the large fixed slack.  Neither changes a
quantifier or the asymptotic conclusion.

### Theorem 3.1 and quantifiers

Two independent random equipartitions have, simultaneously for every
\(|I|\ge4k\), at least one projection of size \(k\).  A transversal
\(k\)-subset \(S\subset I\) is then eligible for Lemma 3.4.  Lemma 3.5 makes
\(\mathcal E_\beta(S)\) hold simultaneously for all \(k\)-sets, and

\[
\binom nk e^{-m/16}+o(1)=o(1)
\quad\text{because}\quad m=16k\log n.
\]

Thus a realization exists that is \(K_{s+1}\)-free and in which every
\(4k\)-set contains \(K_s\).  The factor \(4\) is absorbed into the absolute
constant in Theorem 3.1.  Its quantifiers are
\(\exists C\,\forall s\ge2\,\forall n\ge s^C\,\exists G\); fixing \(s=3\)
therefore covers every sufficiently large integer \(n\), which is precisely
what the asymptotic \(\Theta\)-statement needs.  Finitely many smaller \(n\)
are absorbed into constants.

## Adversarial checks

- No reversal of the minimax definition was found.
- “Induced triangle-free” matches \(K_3\nsubseteq G[S]\).
- The lower bound applies to arbitrary graphs, hence to all \(K_4\)-free
  graphs.
- The upper construction supplies exactly \(n\) vertices and excludes
  \(K_4\) at \(s=3\); it is not only an infinite-subsequence claim.
- “Every sufficiently large \(n\)” and “every fixed \(s\)” are both present.
- The result is order-of-magnitude closure, not a sharp leading-constant
  result; that matches the open problem as recorded.
- No Lean/formal artifact is claimed for #620.

## Timing

- Start: `2026-07-23T19:33:14+08:00`
- End: `2026-07-23T19:37:50+08:00`
- Active agent time: `276 s = 0.076667 agent-hours`
- Budget ceiling: `1 agent-hour`

