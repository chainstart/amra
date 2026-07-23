# Erdős Problem #569 — independent evidence audit

## Verdict

`strong_candidate_needs_QA`

Cambie–Freschi, arXiv:2606.11174v1, states exactly the theorem needed to
close #569, and its new argument for cycle length at least \(7\) survived
line-by-line checking.  I do **not** upgrade the record to
`verified_closed`, because the only load-bearing \(C_5\) base case is
delegated to Theorem 4.5 of Jayawardene's 1999 dissertation.  The
dissertation is catalogued by its author and repeatedly cited by later
papers, but no fixed full text could be obtained for this audit.  Moreover,
Lemma 2.1 of the closing preprint prints the cited small-cycle bounds as
equalities for every connected \(H\), which is false as written; the proof
only needs, and evidently intends, upper bounds.

Thus CF26 is a very strong closure candidate, but this independent
first-source audit cannot certify the one missing \(q=5\) dependency.

## Exact statement mapping

The official question fixes \(k\geq1\) and asks for the least constant
\(c_k\) such that

\[
R(C_{2k+1},H)\leq c_km
\]

for every graph \(H\) with \(m\) edges and no isolated vertices.  CF26 uses
\(q\) for the cycle length and states, for every integer \(q\geq3\), every
integer \(m\geq1\), and every such \(H\),

\[
R(C_q,H)\leq(q-1)m+1\leq qm.
\]

Putting \(q=2k+1\) supplies \(c_k\leq2k+1\) for every official \(k\) and
every \(m\), with no “sufficiently large” qualification.  Conversely, take
\(H=K_2\), so \(m=1\).  Since \(R(C_q,K_2)=q\), every admissible constant is
at least \(q\).  Hence the claimed exact answer is

\[
c_k=2k+1.
\]

There is no mismatch in indexing, isolated vertices, connectedness, or the
quantifier over \(m\).

## Audit of the new proof

### Induction and disconnected graphs

The proof inducts on \(e(H)\) for fixed \(q\).  The base \(H=K_2\) is exact.
If \(H=H_1\sqcup H_2\), induction first embeds a blue \(H_1\).  Since a graph
without isolates has \(|H_1|\leq2e(H_1)\), and \(q-1\geq2\), the unused
vertices number at least \((q-1)e(H_2)+1\), so a disjoint blue \(H_2\)
follows.  This reduction is valid for all positive edge splits.

For connected \(H\neq K_2\), deleting a minimum-degree vertex \(u\) creates
no isolated vertex: otherwise both \(u\) and the newly isolated neighbour
would have degree one and form a separate \(K_2\) component.  Induction
therefore legitimately embeds \(H-u\).  Failure to extend that embedding
gives, by pigeonhole, the red star of the displayed size.

### Minimum degree one and the path bound

When \(\delta(H)=1\), a red \(P_{q-1}\) among the star leaves closes with
the centre to a red \(C_q\).  The lower bound on the leaf set and Corollary
2.3 give a red \(P_{q-1}\) or blue \(H\).  The algebra uses only
\(m\geq |H|-1\) and is sound.

The path-Ramsey lemma in Appendix A was checked directly.  Its induction
deletes a smallest colour class, embeds \(H\) minus that class in the
remaining clique, and either extends it in blue or obtains enough red
neighbours to attach to the inductively obtained red path.  The endpoint
and vertex-count inequalities have the required slack.

### Minimum degree at least two

Proposition 2.4 follows from a vertex-critical \(\chi(H)\)-chromatic
subgraph and the handshaking lemma:

\[
e(H)\geq |H|+\frac{(\chi(H)-3)\chi(H)}2.
\]

The estimates leading to the blue clique
\(U_1\) of size \(\lfloor |H|/2\rfloor+1\) check out.

For the exceptional set \(\Gamma\), make explicit the red auxiliary graph
consisting of all red edges within \(\Gamma\), the selected red
\(U_1\)-to-\(\Gamma\) edges, and the star edges from \(v\) to \(U_1\), while
omitting direct \(v\)-to-\(\Gamma\) edges.  Then every vertex of \(\Gamma\)
is at distance exactly two from \(v\).  Lemma 2.2 converts a red
\(P_{q+1}\) in \(\Gamma\) to a red \(C_q\).  This justifies the path-Ramsey
bound on \(|\Gamma|\); the paper's wording is compressed but the auxiliary
graph is legitimate.

The random split \(V(H)=H_1\sqcup H_2\) has
\(|H_1|=|U_1|\) and \(\mathbb E e(H_2)<m/4\).  Hence a split with
\(e(H_2)<m/4\) exists.  Although \(H_2\) can have isolated vertices, the
extended induction bound

\[
R(C_q,H_2)\leq
\max\{(q-1)e(H_2)+1,\ |H_2|\}
\]

is valid: delete those isolates, use induction on the remaining
isolate-free graph, then assign the isolates to unused vertices.  All
cross-edges to the already embedded \(H_1\) are blue.  The final size
inequalities were checked separately for even and odd \(|H|\); their only
residual case is \(|H|=3\), where \(H=C_3\) and symmetry plus Theorem 1.1
handles it.

### Second-neighbourhood lemma

Lemma 2.2 was checked at its boundary \(q=7\) and for \(q\geq8\).  The
identifications forced by the absence of a \(C_q\), followed by the three
displayed walk constructions, use distinct vertices and have exactly
\(q\) edges.  No parity assumption enters here.  Consequently the new
part of the proof covers every \(q\geq7\), not merely odd \(q\), and every
positive \(m\).

## Small-cycle dependency and blocking defect

- \(q=3\): Goddard–Kleitman (published in *Discrete Mathematics* 125
  (1994), 177–182) explicitly proves
  \(R(K_3,H)\leq2m+1\) for every isolate-free \(m\)-edge graph.  This is
  stronger than the required \(3m\) bound and is independently visible in
  the publisher's article record.
- \(q=5,\ H=K_2\): this is the induction base
  \(R(C_5,K_2)=5\).
- \(q=5,\ |H|=3\): connected \(H\) is \(P_3\) or \(K_3\), and the
  cited \(R(C_5,K_3)=9\) upper bound is sufficient.
- \(q=5,\ |H|\geq4\): the manuscript relies entirely on Jayawardene,
  Theorem 4.5, for \(R(C_5,H)\leq2m+2\).  The 1999 dissertation's metadata
  was verified on the author's institutional page, and #570 plus the 2026
  predecessor paper independently attribute the \(C_5\) result to it, but
  these are secondary attestations, not a check of its statement and proof.

There is also a real typesetting defect.  Lemma 2.1 displays
\(R(C_q,H)=2m+1\) or \(2m+2\) for *every* connected \(H\).  Such universal
equalities are false (for example \(R(C_5,C_5)=9\), not \(12\)); only the
corresponding upper inequalities can be intended and only those are used.
This does not damage the \(q\geq7\) argument, but it makes direct inspection
of Jayawardene's Theorem 4.5 essential before certifying all official
\(k\).

## Required QA to upgrade

Obtain a fixed scan of Jayawardene's 1999 dissertation and verify:

1. Theorem 4.5 says \(R(C_5,H)\leq2e(H)+2\), rather than an equality, for
   every connected graph \(H\) with \(|H|\geq4\).
2. Its graph conventions allow arbitrary simple connected \(H\), not only
   a narrower family.
3. Its proof has no hidden lower bound on \(m\) and covers all finite
   exceptional cases.

If those three checks pass, the audited CF26 argument is sufficient for
`verified_closed`, with exact answer \(c_k=2k+1\).

## Timing

- Start: `2026-07-23T19:49:17+08:00`
- End: `2026-07-23T19:59:24+08:00`
- Active agent time: `607 s = 0.168611 agent-hours`
- Budget ceiling: `1 agent-hour`
