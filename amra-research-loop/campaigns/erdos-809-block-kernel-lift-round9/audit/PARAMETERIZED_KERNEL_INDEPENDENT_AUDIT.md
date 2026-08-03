# Independent audit: parameterized natural-switch kernel

Date: 2026-08-03

Verdict: **the scoped parameterized theorem passes; freeze without a public
Erdős-809 promotion**.

The reconstruction was completed before reading the round-9 author verifier.
It starts from the frozen labelled graph definition, rebuilds every simple
bad `C7`, and takes its intersection with the admissible-old deletion domain.
It neither imports the author probe nor uses the author's trace data.

## 1. Domain and colour quantifiers

For every `m>=3,r>=0`, the independent model uses

```text
X={x1,...,xm}, Y={y1,...,ym}, R={r1,...,rr}.
```

The old `A={v} union X union Y union R` graph has both same-shore cliques,
no `X-Y` edges, and precisely the two same-shore omissions `x1x2,y1y2`.
The typed outside edges are `b-X,c-Y,bz,z-X`.  Old edges incident with `v`
and the `2m` base repeated-colour edges are frozen; their complement is the
admissible deletion domain.

The audited obstruction family is the union of the `m` base repeated pairs
`(bxi,cyi)` and two switch-state pairs `(wx1,cy1),(ux2,cy2)`.  This is a
family of state constraints, not one assertion that the shared edge `cy1`
simultaneously receives two colours.  A deletion is legal only if it hits
the trace of every bad `C7` for every displayed pair.

Within this exact architecture, restoration of any one of `bw,bu,uw`
creates a protected bad cycle:

```text
bw: b-x1-u-y1-c-y2-w-b,
bu: b-x1-v-y1-c-y3-u-b,
uw: w-x1-v-y1-c-y3-u-w.
```

Every old edge in these cycles is repeated-colour or `v`-incident, so each
trace is empty.  The templates require only `m>=3` and are independent of
`r`.  Thus omission of all three edges is genuinely necessary under the
stated deletion interface.  It is not asserted for arbitrary recolourings
or for models allowed to delete frozen edges.

## 2. Blind trace reconstruction

In the branch omitting `bw,bu,uw`, the independent program exhausts the
sixteen support representatives

```text
3<=m<=6, 0<=r<=3.
```

On every representative:

- there is no empty trace;
- every trace has size one or three;
- the singleton set is exactly
  `R x (P union U union W) union P x Q union U x W union K(W)`;
- that singleton set meets every trace.

The locked specialization `(m,r)=(4,2)` independently reproduces 93 traces,
21 singletons and 72 triples.

## 3. Why sixteen representatives are complete

Every bad cycle contains both edges of a displayed repeated pair.  Those
edges have four distinct endpoints, leaving at most three vertices in a
seven-cycle.  After preserving the special indices `1,2`, a generic repeated
index when present, and at most three auxiliary vertices, simultaneous
relabelling of generic paired indices uses at most six indices; relabelling
of residual vertices uses at most three `R` labels.

Consequently any extra singleton, missing formula singleton, forbidden trace
size, or trace disjoint from the formula descends injectively to one of the
sixteen representatives.  Conversely each required singleton witness uses
only its displayed support and embeds in every larger instance in the same
edge orbit.  The grid is therefore a complete support reduction for all
`m>=3,r>=0`, rather than numerical extrapolation.

## 4. Kernel and transversal calculation

Writing `P={x1,x2}`, `Q=X-P`, `U={y1,y2}`, `W=Y-U`, the disjoint block count
is

```text
r(m+2) + 2(m-2) + 2(m-2) + C(m-2,2)
= r(m+2) + (m-2)(m+5)/2.
```

Every transversal contains all formula edges because each occurs as a
singleton trace.  The same formula set hits every trace, so the matching
lower and upper certificates prove

```text
tau(H(m,r))=r(m+2)+(m-2)(m+5)/2.
```

## 5. Scope and decision

The result is an infinite all-parameter theorem inside one labelled
natural-switch architecture.  The campaign supplies no reduction from an
arbitrary public hard branch to that architecture, no legal output
construction, and no asymptotic colour-count composition.  Hence it does
not prove `F_3(n)~n^2/8` and does not change the public `1/8` leading
constant.  External priority was not established, so novelty remains
`priority_uncertain`.  The correct campaign action is to freeze the audited
scoped theorem without public promotion.

## 6. Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-809-block-kernel-lift-round9/audit/verify_parameterized_kernel_independent.py
```

Result: `PASS`, three protected templates, sixteen support representatives.
Independent verifier SHA-256:
`2d16c406028f031a87129b64076a6a044cf5714059346a2b7cb9731966ad5779`.

After reconstruction, the author verifier was run under the same bound and
also passed.  The two implementations have different source hashes and the
independent implementation imports no author code.
