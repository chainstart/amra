# Independent audit: shared-owner fork counterbranch

Date: 2026-08-03

Verdict: **the exact fork kernel and transversal theorem pass; freeze without
public Erdős-809 promotion**.

The labelled graph, state constraints, bad-cycle traces and deletion
hypergraph were independently reconstructed before reading the author probe
or verifier.  The independent implementation imports no author code.

## 1. Owner and state-complex semantics

For every `m>=3,r>=0`, the base state has repeated pairs
`(bxi,cyi)`, `1<=i<=m`.  The two singleton alternatives replace the
`x1` edge of that pair by `wx1` or `ux1`, but both retain the same owner
`cy1`.  They are separate state constraints and are never asserted as one
joint colouring.  Taking the union of their bad-cycle trace constraints is
exact because one deletion set must make the base and each permitted
singleton state legal.

Both candidate vertices see `X`, `Y-{y1}` and `R`, and omit incidence with
`v,b,c,z` and with each other.  Old edges incident with `v` and all base
repeated-colour edges are frozen.  The independent graph agrees exactly with
the author model after the blind reconstruction.

The owner-incidence graph has two candidate vertices adjacent to one owner,
so matching rank one.  Its permitted state complex has the empty/base face
and two singleton faces but no two-candidate face.  The round-9 object has
two owners, matching rank two and a Boolean joint face.  A map preserving
owner rank and state faces cannot identify these objects; a block-count map
that does so would invent both an owner and a state.

## 2. Independent trace reconstruction

For each of the sixteen support representatives

```text
3<=m<=6, 0<=r<=3,
```

the independent enumerator builds every simple seven-cycle containing both
edges of one permitted repeated pair and intersects it with the admissible
old-edge domain.  It obtains:

- no empty trace;
- trace sizes only one and three;
- singleton set exactly

```text
F_fork = R x ({x1} union Y)
       union {x1} x (X-{x1,x2})
       union {y1,y2} x (Y-{y1,y2})
       union K(Y-{y1,y2});
```

- every trace meets `F_fork`.

Every bad `C7` contains the four distinct endpoints of one repeated pair,
leaving at most three free vertices.  Simultaneous relabelling of generic
paired indices and independent relabelling of `R` therefore reduces every
possible extra singleton, missing formula edge, empty trace or unhit trace
to the sixteen representatives.  Conversely each formula edge orbit has a
small-support singleton witness which embeds in every larger instance.
This closes the `m>=3,r>=0` quantifier; it is not extrapolation from sixteen
sizes.

## 3. Exact kernel and transversal

The four disjoint block sizes are

```text
r(m+1), m-2, 2(m-2), C(m-2,2).
```

Their sum is

```text
|F_fork|=r(m+1)+(m-2)(m+3)/2.
```

Each formula edge is a singleton trace, so every transversal contains all
of `F_fork`.  The same set hits every trace, giving the matching upper bound
and hence exact equality `tau=|F_fork|`.  Deleting this set makes all three
permitted states `C7`-legal because deletion cannot create cycles.

Compared with the independently audited round-9 kernel, the fork loses
exactly

```text
R x {x2} union {x2} x (X-{x1,x2}),
```

of size `r+m-2`.  This is precisely the block attached to the missing second
owner, so owner collision genuinely changes both the kernel and `tau`.

## 4. Scope firewall

The theorem is an infinite exact counterbranch to universality of the
two-independent-owner labelled architecture.  It identifies a necessary
hypothesis for any future reduction: distinct owner rank together with
Boolean joint compatibility.

It does not prove that the synthetic fork occurs in every public hard branch,
or even that one fork instance is a `floor(n^2/4)+1` threshold hard graph.
It supplies no output-expansion composition and changes neither the public
`F_3(n)~n^2/8` question nor its `1/8` constant.  External priority remains
uncertain.  The correct action is to freeze the scoped counterbranch without
public promotion.

## 5. Reproduction

```text
AMRA_MEMORY_KIB=3145728 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh python3 \
  amra-research-loop/campaigns/erdos-809-hard-branch-lift-round10/audit/verify_forked_owner_independent.py
```

Result: `PASS`; sixteen complete support representatives.  Independent
verifier SHA-256:
`da2634e9a90c5ed9c738cab761b68797700eddc9d2d3bb152a2fc42e0d4a7acc`.

After blind reconstruction, the author verifier was run under the same
3 GiB / 180 s bound and passed.  The implementations have different hashes.
