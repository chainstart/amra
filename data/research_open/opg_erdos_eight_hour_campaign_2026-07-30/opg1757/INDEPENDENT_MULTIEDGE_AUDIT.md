# Independent audit of the \(q=2,k=5\) multiedge attack

Date: 2026-07-30

Reviewed artifacts:

- `MULTIEDGE_RECOLORING_ATTACK.md`;
- `verify_multiedge_recoloring_attack.py`;
- `test_verify_multiedge_recoloring_attack.py`;
- `multiedge_recoloring_attack_certificate.json`.

The audit verifier does not import the reviewed verifier, its candidate
generator, or the old Hopcroft--Karp routine.  It rebuilds all \(2932\)
forests of \(K_6\) as edge bit masks and uses a separately implemented
greedy-plus-alternating-BFS matcher.

## 1. Verdict

The mathematical and finite \(q=2,k=5\) conclusions pass independent
audit:

\[
\begin{array}{c|r|r}
&\text{reviewed result}&\text{independent result}\\ \hline
\text{negative objects}&43648&43648\\
\text{positive objects}&45620&45620\\
\text{direct/single edges}&112556&112556\\
\text{direct/single maximum matching}&43642&43642\\
\text{expanded edges}&1987196&1987196\\
\text{expanded maximum matching}&43648&43648.
\end{array}
\]

The independent matcher starts from a maximal greedy matching, repeatedly
finds alternating BFS paths, and finally checks the alternating Hall
neighbourhood of every unmatched source.  In the base graph it recovers a
\(12\)-source, \(6\)-target Hall witness.  In the expanded graph it explicitly
matches every source, so maximality follows without relying on an optimality
implementation: no matching can exceed the number of left vertices.

The result remains **finite evidence** for this enumerated layer.  It is not
an all-\(q,k\) injection.

## 2. Definition and completeness audit

The independently reconstructed candidate graph uses exactly:

1. every positive target obtained by moving \(E\) directly;
2. every positive target obtained by exchanging \(E\) with one red edge;
3. the deterministic global cycle-opening target;
4. every positive target obtained from that deterministic target by
   replacing one non-protected edge of one colour by one edge of \(K_6\),
   provided the result is a forest and preserves the active vertex set.

The verifier loops over all 15 possible incoming edges and every eligible
outgoing edge in both colours.  Set deduplication is performed only after
the complete loops.  Hence the count \(1987196\) exhausts the stated move
family; it does not claim to exhaust all conceivable multiedge moves.

For reproducibility, the independent certificate adds canonical CSR hashes:

```text
direct/single adjacency:
35b46e1a0860356582fa5b0b3084bd58d39c487c0a64ce7620ded38724c04405

expanded adjacency:
b9e6d009ea3fb154d9926e83996817c87b557059c716b2f9b8be87436b1633cd
```

These hashes use the independent bit-mask ordering, so they need not equal
an internal hash from a differently ordered enumerator.

## 3. Kernel and support-change audit

The 12-source witness and all six old targets were reconstructed from their
edge lists, without trusting their stored numerical indices.  Each source
has exactly its stated single neighbour.

The set is not inclusion-minimal.  Its collision graph is the union of six
inclusion-minimal \(2\)-source, \(1\)-target Hall components.  The reviewed
note now states this distinction correctly.

The same-union exhaustion also reproduces exactly:

\[
\begin{array}{c|c|c|c}
\text{block}&\text{sources}&\text{same-union targets}&\text{deficiency}\\
\hline
U_1&8&4&4\\
U_2&4&6&0.
\end{array}
\]

Thus arbitrary repeated recolouring whose final support remains \(U_1\)
cannot be injective on its eight sources.  A support-changing move is
genuinely necessary.

All 12 stored reserve assignments replay from their edge descriptions,
have distinct ordinary targets, and invert to their sources.

## 4. Human-proof audit

### Forest preservation

After deterministic opening, both colour classes are forests.  For a
reserve exchange \(C-a+b\), the stated admissibility condition puts the
endpoints of \(b\) in different components of \(C-a\).  Therefore adding
\(b\) cannot create a cycle.  This proof is valid on every finite graph.

### Weight, support and marked edges

The reserve removes and inserts one edge copy in the same colour.  It
preserves both colour sizes and changes union membership only at \(a,b\):
\[
(U\mathbin{\triangle}U')\subseteq\{a,b\}.
\]
Protecting red \(E\), excluding blue \(E\), and protecting blue \(F\)
preserves the reduced sign class.  Active labels are preserved only because
this is imposed as an explicit admissibility condition; they are not an
automatic consequence of a basis exchange.

### Tagged inverse

The target and tag \((x,C,a,b)\) first recover the deterministic-opening
target by replacing \(b\) with \(a\), and then recover the source using the
opening tag \(x\).  The argument is injective and valid for every finite
graph.

This proves only tagged reversibility.  Removing the tag uniformly still
requires a matching or canonical-choice theorem.

## 5. Hash audit and precision corrections

The saved value

```text
648d0237235a5e40ebf85a9251172feed5ae232f7b003396266c173abd1c56a6
```

is reproduced exactly.  Its precise scope is the JSON payload consisting
of `scope`, `layer`, and `hall_kernel`.  It does **not** cover `schema`,
`claim_labels`, or the `sha256_payload` field.  It should therefore be
called the payload hash, not the whole-certificate file hash.

The SHA-256 of the complete reviewed JSON file is:

```text
817915a3868d7d9288e9ca2297162751bddafe4b4c3cbe6812d764edd3417916
```

The old certificate records the kernel objects, reserve targets, aggregate
graph counts, and six augmenting paths.  It does not serialize all
1,987,196 candidate edges or all 43,648 matched pairs.  Completeness is
therefore reproducible by rerunning the generator, not verifiable from the
old JSON alone.  The independent certificate supplies adjacency and
matching hashes to make that rerun comparison exact.

## 6. Claim boundary

The audited claim hierarchy is:

```text
protected reserve preserves forests          HUMAN PROOF
tagged two-stage move is reversible           HUMAN PROOF
expanded q=2,k=5 graph has a full matching    FINITE EVIDENCE
canonical untagged map for every q,k          OPEN GAP
complete first coefficient / OPG-1757         OPEN GAP
```

No reviewed statement crosses this boundary after the inclusion-minimal and
hash-scope qualifications above.

## 7. Reproduction

```bash
python3 independent_verify_multiedge_and_k6.py
pytest -q test_independent_multiedge_and_k6.py
```

The independent \(k=5\) certificate is
`independent_multiedge_audit_certificate.json`.
