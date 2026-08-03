# Independent audit: `q=1` endpoint and the disjoint-`K4` complete channel

Date: 2026-08-02
Auditor: `/root/erdos809_lane` (author-swapped; no authorship of the OPG lane)
Verdict: **PASS AS ENDPOINT/FINITE MECHANISM EVIDENCE; NO NOVELTY OR PROMOTION**

This audit is separate from `RANDOM_CLUSTER_BOUNDARY_INDEPENDENT_AUDIT.md`
and does not alter or replace that audit.

## 1. Audited artifacts

- `evidence/Q_ONE_ENDPOINT_LEMMA.md`
  SHA-256 `bc050612816ff1e928961396b9c273d3897ec4fc79d129fe9d1787d9516b6351`
- `evidence/verify_q_one_endpoint.py`
  SHA-256 `a9f72ef673d7a88b6e8a2f8f59612c958c5466fd6aeea306f39e2e61885fe5eb`
- `evidence/K4_COMPLETE_CHANNEL_NOTE.md`
  SHA-256 `86a2c6487663e54f32bb9efecc05780faceae689c8cc74f45d46f14d5245fa48`
- `evidence/opg_k4_complete_channel_probe.lean`
  SHA-256 `47a2f7b9c800009182a6db7cd500fd8b65dac5506c61b4fbc73dfd7f620e5240`

## 2. Independent reconstruction of the `q=1` derivative

Let

\[
 P_q=P_{00}(q)+x_eP_{10}(q)+x_fP_{01}(q)+x_ex_fP_{11}(q),
 \qquad
 D_q=P_{10}P_{01}-P_{11}P_{00},
\]

where

\[
 P_{ij}(q)=\sum_{B\subseteq E\setminus\{e,f\}}
 q^{\nu(B\cup i e\cup j f)}\mathbf x^B.
\]

At `q=1`, all four cells equal

\[
 S=\prod_{a\ne e,f}(1+x_a),
\]

so `D_1=0`.  Since `D_q` is a polynomial in `q`, the factor theorem gives
divisibility by `1-q`, and

\[
 \left.\frac{D_q}{1-q}\right|_{q=1}=-D'_1.
\]

Differentiating the four factors at `q=1` gives exactly

\[
 -D'_1
 =S\sum_B\mathbf x^B
 \bigl(
 \nu(B+e+f)+\nu(B)-\nu(B+e)-\nu(B+f)
 \bigr).
\]

The sign is correct.  Matroid rank is submodular and
`nu(A)=|A|-r(A)`, hence nullity is supermodular.  Apply it to
`B+e` and `B+f`, whose union is `B+e+f` and intersection is `B`.
Every bracket is nonnegative.  More precisely, a nullity marginal for
adjoining one edge is zero or one, so the difference of the two nested
marginals is also zero or one.  Therefore `-D'_1` has nonnegative
coefficients, and it is nonnegative at every nonnegative activity vector.

This argument covers loops or dependent insertions as well; the public graph
is simple, so no extra case is needed.  It proves only the endpoint value of
the quotient.  It gives no sign control on an interval `0<q<1` and no passage
to the forest endpoint `q=0`.

## 3. Independent finite guard for the endpoint formula

`audit/check_q1_and_k4_complete_channel.py` was written without importing
the author implementation.  It uses disjoint-set rank and integer arithmetic.
It checked every marked pair and every base subset in `K3`, `K4`, and `K5`:

| graph | marked pairs | base subsets over all pairs | summed positive brackets |
|---|---:|---:|---:|
| `K3` | 3 | 6 | 3 |
| `K4` | 15 | 240 | 78 |
| `K5` | 45 | 11,520 | 2,130 |

Every bracket was in `{0,1}`, and the independently accumulated derivative
equalled `S` times the bracket sum.  The author script was also executed by
loading its definitions without invoking its file-writing `main`; it returned
the same pair and defect totals.

Reproduction used a 512 MiB virtual-memory cap, one thread, and a 120-second
timeout.  The independent script has SHA-256
`31d622d03cd13969da297a24d2e3e223f3d90959e1336aa607ccdcff365a6346`.
These finite checks guard the implementation; supermodularity is the
all-graph proof.

## 4. Independent `K4` forest enumeration

For vertices `0,1,2,3`, marked edges `01,23`, and remaining activities

\[
 a=x_{02},\quad b=x_{03},\quad c=x_{12},\quad d=x_{13},
\]

independent enumeration of all sixteen subsets of the remaining edges and
all four marked-edge cells gave cell support sizes

\[
 \begin{pmatrix}15&9\\9&5\end{pmatrix}.
\]

Forming `P10 P01-P11 P00` by exact monomial-dictionary convolution produced
exactly nine terms:

\[
 \Delta=a^2d^2+a^2d-2abcd+ad^2+ad
       +b^2c^2+b^2c+bc^2+bc.
\]

The coefficient of `abcd` is exactly `-2`; hence coefficientwise positivity
and any decomposition that refuses to couple the two perfect-matching
monomials are genuinely unavailable.  Exact expansion gives

\[
 \Delta=(ad-bc)^2+ad(a+d+1)+bc(b+c+1).
\]

For nonnegative `a,b,c,d`, all three summands are nonnegative.  The
decomposition is complete: the independently expanded right side equals the
full enumerated Rayleigh polynomial, not merely its homogeneous leading part.

## 5. Bounded Lean replay

The author Lean artifact kernel-checks unchanged.  It was the only heavy task
running during the replay:

```bash
AMRA_MEMORY_KIB=12582912 AMRA_TIMEOUT_SECONDS=180 LEAN_NUM_THREADS=2 \
  ../../amra-research-loop/scripts/run_bounded.sh lake env lean \
  ../../amra-research-loop/campaigns/opg-1757-mechanism-reset/evidence/opg_k4_complete_channel_probe.lean
```

Working directory: `ara_library/formal`.  Result: exit code `0`, with no
kernel errors.  The 12 GiB virtual cap is part of the evidence boundary;
lower-cap import failures are not mathematical counterevidence.

Lean proves the polynomial identity and its real nonnegativity under the four
activity hypotheses.  The independent enumeration above is still needed to
connect the displayed polynomial to the four forest cells; the Lean file does
not formalize that enumeration.

## 6. Nguyen--Pylyavskyy 2025 consistency and novelty

The primary source is Nguyen--Pylyavskyy, *Correlations in random cluster
model at q=1*, [arXiv:2507.09520](https://arxiv.org/abs/2507.09520).
It states that negative correlation for `0<=q<=1` remains conjectural, gives
a combinatorial formula for the quotient at `q=1`, and proposes the
positive-semidefinite `alpha-beta-gamma` ansatz for general `q`.

The present `q=1` derivative factorization is consistent with that endpoint
formula and should be treated as an exact reformulation/specialization, not a
novel theorem.  No literature-priority claim is accepted.

For the paper's disjoint marked-edge `K4` example, the `q=0` lowest/spanning
sector is

\[
 (x_gx_h-x_kx_\ell)^2.
\]

After relabelling the two perfect matching monomials as `ad` and `bc`, this is
the homogeneous degree-four channel `(ad-bc)^2` in the audited forest
decomposition.  The additional terms `ad(a+d+1)+bc(b+c+1)` are positive
channels from the all-forest polynomial.  Thus the mechanism is compatible
with the paper's `K4` PSD example, but the paper comparison must not be stated
as though it supplied a new arbitrary-host decomposition here.

## 7. Scope and promotion decision

- `q=1` endpoint derivative and sign: **PASS**, all finite graphs.
- Author Python guard: **PASS**, finite `K3`--`K5` corroboration.
- Disjoint marked-pair `K4` forest enumeration: **PASS**, one finite host/orbit.
- Complete-channel algebra and nonnegativity: **LEAN KERNEL PASS**.
- Novelty: **NOT CLAIMED**; consistency with Nguyen--Pylyavskyy only.
- Sign for all `0<q<1`: **OPEN**.
- Forest negative correlation for arbitrary hosts: **OPEN**.
- OPG-1757 promotion: **REJECTED**; `global_interface_closed` is unchanged.

These artifacts are useful route evidence: they reject coefficientwise and
fiber-separable mechanisms and support a moving PSD/Gram channel.  They are
not a promotion condition, a main-term change, or a proof of OPG-1757.
