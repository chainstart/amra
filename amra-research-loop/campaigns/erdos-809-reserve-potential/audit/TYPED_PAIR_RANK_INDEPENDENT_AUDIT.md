# Independent audit of M809-11 typed pair rank

Date: 2026-08-02

Verdict: **the two coverage ranks, the fourteen-vertex swap pair, and the
typed-capacity no-go pass.  The result is a local interface obstruction, not
the global closure required for Erdős #809.**

The audit did not modify the author evidence.  The author probe was rerun from
a byte-identical temporary copy under the stated 512 MiB / 120 second guard;
its output reproduced SHA-256
`8e7f518a5ae2813648bb9528107effc5ad84ebf73cb036e8acb61b7bf6c8027e`.

## 1. Reconstruction of the two ranks

For every atom `u`, let `C_u` be the colours whose owner or reserve set
contains `u`.  Its contribution to a coverage rank is

```text
h_u(T) = 1 if T intersects C_u, and 0 otherwise.
```

For any `X,Y`, a four-case check according to which of `X,Y` meets `C_u`
gives

```text
h_u(X)+h_u(Y) >= h_u(X union Y)+h_u(X intersection Y).
```

Therefore sums of these hit indicators are normalized, monotone and
submodular.  Taking singleton owner sets gives

```text
rho_A(T)=|{a_gamma: gamma in T}|,
```

and taking the actual reserve neighbourhoods gives

```text
rho_B(T)=|union_(gamma in T) K(e_gamma)|.
```

This proof permits coincident A owners, repeated base pairs and arbitrarily
overlapping B reserves.  The independent checker additionally exhausts all
512 set-valued coverage maps from three colours to a three-atom universe and
all 27 singleton-owner maps.

Audit note: the author probe calls its submodularity checker only on the two
A-owner maps in the minimal recolouring example.  It does not separately
enumerate B-reserve set systems, so the sentence saying that the probe checks
both ranks is slightly broader than the machine test.  This is an evidence
scope issue, not a mathematical defect: the coverage proof above applies
verbatim to `rho_B`, and the independent audit fills the finite check.

## 2. Independent reconstruction of the n=14 pair

The audit rebuilt the graph directly from the prose, without importing the
pair-rank probe.  Both graphs have

```text
n=14, e=50, |B|=3, minimum degree 4,
A=N[v], L4(2), and every C7 rainbow.
```

The tight graph has 11,136 seven-cycles, all rainbow.  Its three distinct
owned A diagonals are missing, while

```text
K(bc)={bc,cz}, rho_A=3, rho_B=M_B=2, D_B=3.
```

Replacing the B edge `bz` by the previously missing A edge `x1x2` preserves
`n,e,A,B`, the three repeated colours and their owned diagonals.  The paid
graph has 11,892 seven-cycles, again all rainbow, and

```text
K(bc)={bc,bz,cz}, rho_A=3, rho_B=M_B=3, D_B=3.
```

Since `n,e,|B|` agree, the scalar

```text
S_m=e-binomial(|B|,2)-Phi(n,e)
```

is identical without needing the numerical value of `Phi`.  Thus the pair
really has the same `(S_m,rho_A)` and different B-reserve outcomes.

## 3. Exact scope of the untyped no-go

On the tight graph,

```text
D_B=3 <= rho_A+rho_B=5,
but M_B=rho_B=2 < D_B.
```

Hence `rho_A+rho_B` cannot be interpreted as capacity for a B-only demand.
The A summands name missing edges inside `A`; they do not name missing B
edges.  The failure is semantic typing, not formal rank theory:
`rho_A+rho_B` is itself monotone and submodular.

The witness does **not** refute any of the following:

- a theorem for a genuinely combined A-and-B demand with a correspondingly
  typed combined target budget;
- an injective A-to-B conversion, owned slack atomization, or outer-gate
  theorem proved from additional rectangle geometry;
- a graph-dependent decomposition of `S_m` using more information than the
  unchanged scalars `(n,e,|B|,rho_A)`;
- the complete hard BCM/outer-A contract or the public `1/8` asymptotic.

In particular, a numerical expression such as
`rho_B(T)+min(S_m,rho_A(T))` may be submodular when the slack is nonnegative,
but it is not a capacity certificate until one of those conversion theorems
supplies typed atoms.

## 4. Promotion decision

The audit accepts the typed-pair result as an exact local no-go and rejects
promotion.  It neither closes the fixed-endpoint reserve/Hall interface nor
changes the main coefficient in Erdős #809.

Independent reproduction:

```bash
AMRA_MEMORY_KIB=524288 AMRA_TIMEOUT_SECONDS=120 LEAN_NUM_THREADS=1 \
  amra-research-loop/scripts/run_bounded.sh \
  python3 amra-research-loop/campaigns/erdos-809-reserve-potential/audit/verify_typed_pair_rank_no_go.py
```

The independent script completed in about 2.6 seconds.  No Lean process was
started.
