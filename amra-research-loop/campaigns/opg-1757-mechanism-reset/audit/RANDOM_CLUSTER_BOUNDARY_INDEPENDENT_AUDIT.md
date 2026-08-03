# Independent audit: random-cluster boundary representation

Auditor: Erdős #776 lane (author-swapped; no participation in the OPG-1757
derivation)

Date: 2026-08-02

Verdict: **PASS AFTER EXECUTABLE LEAN REPAIR as an exact representation
bridge; REJECT as `global_interface_closed`.**

## 1. Independent scaling reconstruction

For a fixed finite simple graph `G=(V,E)`, use the multivariate
random-cluster partition function

\[
Z_G(q,\mathbf v)=\sum_{A\subseteq E}q^{k(A)}\prod_{a\in A}v_a,
\]

where `k(A)` is the number of connected components of the spanning
subgraph `(V,A)`, including isolated vertices.  For `q>0`, substitute
`v_a=q x_a` and divide by `q^|V|`.  Term by term,

\[
q^{-|V|}q^{k(A)}\prod_{a\in A}(q x_a)
=q^{|A|-|V|+k(A)}\mathbf x^A.
\tag{1.1}
\]

Thus the scaled expression for `q>0` has the polynomial extension

\[
P_q(\mathbf x)=
\sum_{A\subseteq E}q^{\nu(A)}\mathbf x^A,
\qquad
\nu(A)=|A|-|V|+k(A).
\tag{1.2}
\]

The wording `q^(-|V|) times` must not be evaluated literally at `q=0`;
`P_0` means the value of the polynomial extension (1.2).

## 2. Cyclomatic exponent

Let the connected components of `(V,A)` have vertex and edge counts
`(v_i,e_i)`.  Every component is connected, so `e_i>=v_i-1`.  Hence

\[
\nu(A)=\sum_i(e_i-v_i+1)\ge0.
\tag{2.1}
\]

Equality holds exactly when every `e_i=v_i-1`, equivalently when every
component is a tree.  Isolated vertices satisfy `(v_i,e_i)=(1,0)` and cause
no exception.  Therefore

\[
\nu(A)=0\quad\Longleftrightarrow\quad A\text{ is a forest}.
\tag{2.2}
\]

It follows immediately from (1.2) that

\[
P_0(\mathbf x)=\sum_{A\text{ forest}}\mathbf x^A=F_G(\mathbf x).
\tag{2.3}
\]

## 3. Marked derivatives and the Rayleigh limit

Fix distinct marked edges `e,f`.  Because (1.2) is a finite polynomial in
`q` and all edge variables, differentiation in `x_e,x_f`, coefficient
extraction, multiplication, and evaluation at `q=0` commute.  Consequently

\[
(P_q)_e\to(F_G)_e,\quad
(P_q)_f\to(F_G)_f,\quad
(P_q)_{ef}\to(F_G)_{ef}
\]

coefficientwise in the remaining activities, and hence

\[
\Delta_{ef}(P_q):=(P_q)_e(P_q)_f-P_q(P_q)_{ef}
\longrightarrow
\Delta_{ef}(F_G)
\tag{3.1}

coefficientwise and pointwise at every fixed activity vector.

Multiplication of the original random-cluster partition function by the
positive scalar `q^(-|V|)` multiplies its Rayleigh difference by a positive
square, so it does not change its sign for `q>0`.  Therefore, if for a
fixed graph and fixed positive activities one has
`Delta_ef(P_qj)>=0` along any sequence `q_j downarrow 0`, then (3.1) gives
`Delta_ef(F_G)>=0`.

No uniform convergence in the activities is needed for this fixed-point
passage.  What is missing is much stronger: a finite-`q` sign theorem for
all required graphs, marked pairs, and positive activities.

## 4. Bounded Lean replay

The author evidence file
`evidence/opg_triangle_random_cluster_probe.lean` does **not** currently
kernel-check.  Under a 12 GiB virtual-memory cap, two threads, and a
180-second timeout, Lean reports at line 30:

```text
error: failed to prove positivity/nonnegativity/nonzeroness
```

The polynomial identity is correct; the failure is the final `positivity`
tactic, which does not discharge `0<=1-q` from `q<=1` in this context.
Runs at 2 GiB, 5 GiB, and 8 GiB also failed earlier from import-time memory
or allocation limits and are not mathematical evidence.

The independent audit file
`audit/opg_triangle_random_cluster_independent.lean` repairs only the proof
script: it derives `0<=1-q` and `0<=1+z` explicitly by `linarith`, then uses
`mul_nonneg`.  It kernel-checks under the same 12 GiB/2-thread/180-second
wrapper:

```bash
env AMRA_MEMORY_KIB=12582912 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=2 \
  ../../amra-research-loop/scripts/run_bounded.sh lake env lean \
  ../../amra-research-loop/campaigns/opg-1757-mechanism-reset/audit/opg_triangle_random_cluster_independent.lean
```

The repaired file's SHA-256 is
`f7c85b813ace5769f635c628038817888b0bcc93ae7f1ea1d0a7889aa57e845e`.
This proves only the triangle identity and its sign for `0<=q<=1,z>=0`.

## 5. Independent K3--K5 corroboration

`audit/check_complete_graph_boundary.py` independently enumerates every
spanning subgraph, computes the cyclomatic exponent by disjoint-set union,
forms the four marked-edge cells, and performs exact integer polynomial
arithmetic.  It does not import the author script or SymPy.

For every marked-pair orbit of `K3`, `K4`, and `K5`, the unweighted scaled
Rayleigh polynomial equals `(1-q)` times a polynomial having strictly
positive integer coefficients.  The quotient coefficient lists, from low
to high degree, are:

```text
K3: [2]
K4: [44,38,13,1], [6,19,7]
K5: [1956,4151,4548,3163,1476,464,99,14,1]
    [210,1085,1579,1156,471,99,8]
```

Reproduction:

```bash
env AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=60 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/opg-1757-mechanism-reset/audit/check_complete_graph_boundary.py
```

Output SHA-256:
`08f4a0296ee2cb1e6fc4682eaa26eb35efd1318652a9b5ffc626ccf03ce90df8`.
These are finite, unweighted corroborations only.

## 6. Dependency and promotion audit

The representation lemma proves that forest negative dependence is the
`q=0` boundary value of the scaled random-cluster Rayleigh difference.  It
does not prove that the latter is nonnegative for any interval
`0<q<=epsilon`, let alone for every graph and positive activity vector.

Indeed, the triangle and complete-graph probes point toward the desired
finite-`q` statement for `0<=q<=1`, but proving random-cluster negative
dependence in precisely this direction is the surviving mathematical
problem, not an available premise.  Passing to `q=0` cannot create its own
one-sided sign control.

The lemma also does not connect the inherited complete-split coefficient
rows to arbitrary hosts or control all later rows.  Thus it closes only

```text
finite-q Rayleigh certificate, if supplied
    -> q-to-zero weighted-forest Rayleigh certificate.
```

The antecedent is open.  Consequently:

- `global_interface_closed` is not satisfied;
- OPG-1757 remains open;
- M008 remains a surviving route, not a proved mechanism;
- promotion is rejected.

## 7. Evidence classification

- `mathematical_status`: representation lemma proved and independently
  reconstructed.
- `statement_match`: exact for the boundary representation, not the public
  negative-correlation theorem.
- `machine_reproduced`: author Lean artifact failed; independently repaired
  Lean artifact passed; independent Python finite corroboration passed.
- `novelty`: not checked; this is a standard random-cluster/forest boundary
  expansion unless literature comparison shows otherwise.
- `publication_state`: private campaign audit.
