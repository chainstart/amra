# Independent audit: minimal Hall-deficiency lemma

Auditor: Erdős #776 lane (author-swapped; no participation in the #809
derivation)

Date: 2026-08-02

Verdict: **PASS for the abstract incidence lemma; FAIL as a campaign
promotion or a consequence for the \(1/8\) main term.**

## 1. Exact reconstruction

Let `C` and `T` be the two shores of a finite bipartite graph.  For
`S subset C`, let `N(S) subset T` be its full token neighbourhood.  Say
that `S` is deficient when

\[
|N(S)|<|S|,
\]

and inclusion-minimal deficient when it is deficient and no strict subset
is deficient.  This is the definition needed by the proof.  In particular,
minimality only among deficient sets of the same cardinality would not be
sufficient.

The empty set is not deficient, so an inclusion-minimal deficient `S` is
nonempty.  Fix `c in S`.  Since `S-{c}` is a strict subset and is not
deficient,

\[
|N(S\setminus\{c\})|\ge |S|-1.
\tag{1.1}
\]

Neighbourhood monotonicity gives

\[
N(S\setminus\{c\})\subseteq N(S),
\tag{1.2}
\]

while integrality and deficiency give

\[
|N(S)|\le |S|-1.
\tag{1.3}
\]

Combining (1.1)--(1.3), equality holds everywhere:

\[
|N(S)|=|S|-1,
\qquad
N(S\setminus\{c\})=N(S).
\tag{1.4}
\]

This proves deficiency exactly one and deletion-stability for every
`c in S`.

Finally, take `t in N(S)`.  It has at least one neighbour in `S`.  If it
had exactly one, say `c`, then
`t notin N(S-{c})`, contradicting (1.4).  Hence every incident token has
degree at least two inside `S`.  The assertion also handles `|S|=1`:
then `N(S)` is empty and the token-degree conclusion is vacuous.

No graph geometry, reserve theorem, or extremal estimate is used.  The
lemma is a direct consequence of the definition of inclusion-minimal Hall
deficiency.

## 2. Independent finite guard

The independent checker exhausts all bipartite incidence graphs with one
to four colours and zero to four tokens.  It checks inclusion-minimality
against every proper colour subset, not only one-deletions.

Result:

```text
graphs checked                         74,958
minimal deficient sets checked         39,253
counterexamples                        0
```

Reproduction under the campaign memory limit:

```bash
env AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=60 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-reserve-potential/audit/check_tight_deficiency.py
```

Output:
`audit/tight_deficiency_finite_check.json`, SHA-256
`b0232ef560793cbfa799c9f097a9772d3b39dc26255ac4a116dda486429f45ff`.
This finite guard is only a sanity check; the proof in Section 1 is the
unbounded evidence.

## 3. Survivor dependency audit

### M809-11

The lemma validates only the following abstract reduction: after choosing
an inclusion-minimal Hall-deficient colour set, one may assume its token
deficiency is one, deletion of any colour preserves its token union, and no
incident token has degree one.

It does **not** prove either decisive clause of M809-11:

1. that such an abstract transversal circuit can be uncrossed to a
   geometrically coherent zero-shore family while fixed endpoints and token
   provenance are preserved;
2. that its one-unit deficit can be charged injectively to the inherited
   A, B, or residual budgets.

Thus M809-11 remains a surviving research mechanism, not a proved bridge.
The phrase `minimum-rank deficient set` in M809-11 must be implemented by
selecting an inclusion-minimal deficient subset before invoking the lemma.

### M809-06

The lemma does not classify cuts in the typed three-budget capacitated
network.  A unit colour--token Hall cut may be reduced to a tight circuit,
but typed A/B/residual capacities and non-unit cut terms need not be the
neighbourhood cardinality of one incidence graph.  No argument in the
evidence shows that every sub-demand minimum cut is one of the inherited
A, B-same, or B-opposite scalar branches.

Therefore M809-06 also remains surviving but unproved.  The abstract lemma
supplies, at most, one normal form for an untyped Hall component of a cut.

## 4. Contract and main-term audit

The public problem asks, for `k=3`, to prove or refute

\[
F_3(n)\sim n^2/8.
\]

The audited lemma contains no `n`, no `C_7`, no graph edge threshold, no
colour lower bound, and no construction.  It closes only the structural
subinterface

```text
arbitrary Hall-deficient incidence set
    -> inclusion-minimal tight transversal circuit.
```

It does not close the campaign's frozen global interface: the circuit has
not been linked to the hard BCM geometry, the root-free branch
`|Q|<=D_B-1`, the outer-A residue, or all A/B branches.  Consequently:

- the original problem remains open;
- the coefficient `1/8` is unchanged;
- no upper or lower main term is improved;
- promotion under `global_interface_closed` is rejected.

## 5. Novelty and evidence classification

- `mathematical_status`: proved, independently reconstructed.
- `statement_match`: exact for the abstract lemma; fails the public and
  campaign closure statements.
- `evidence_strength`: independently reconstructed natural proof, with a
  finite exact sanity check.
- `novelty`: the lemma is an elementary Hall-minimality consequence; no
  novelty claim is justified or needed.
- `publication_state`: private campaign audit.
