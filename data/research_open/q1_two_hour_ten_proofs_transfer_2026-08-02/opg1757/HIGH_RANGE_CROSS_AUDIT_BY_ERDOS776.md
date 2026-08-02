# Independent audit of high-range effectivity

Date: 2026-08-02

Auditor: Erdős #776 lane

## Verdict

**PROMOTE.**  The provisional bound in
`HIGH_RANGE_EFFECTIVITY_BLOCKER.md` is mathematically valid, and the same
117-digit `S_gap` already proved for the low logarithmic gap is an explicit
upper bound for coefficientwise positivity of both complete candidate
third-active transports.

This is an effective eventual transport theorem, not positivity for every
finite stable parameter and not a proof of the original OPG-1757
proposition, which remains **OPEN**.

## Independent reconstruction

The companion `cross_audit_high_range_by_erdos776.py` imports neither author
certificate program.  It checks the old recurrence source hash

```text
a4c8bbf5a261e8d478358fa6ec8136affd0258f324049beec2f61f93b7994125
```

and additionally pins the digest of all four fully expanded component
families:

```text
60088139bd17a2a3e52f643896ca46b6708a87ab090c2658e28656569b02ed70.
```

The second pin closes a provenance weakness in pinning only the top-level
recurrence file, whose formulas use imported fixed-page kernels.

For every lower-base coefficient polynomial, the audit independently sums
the absolute integer coefficients, then reconstructs

\[
C_{\rm obj}=2^q\sum_{a<p,j}A_{a,j}\frac{p^{i_*}}{a^j}.
\]

It obtains exactly:

| object | terms | exact constant | least strict threshold |
|---|---:|---:|---:|
| odd sufficient | 80 | `32263317969653120815494524068429824/48828125` | 102 |
| even sufficient | 120 | `13640357738883598259403345884706295095651860375632/2101890673828125` | `182963662611742278515145357606424176862843` |
| odd page | 68 | `537834204620338688824696369053696/48828125` | 75 |
| even page | 105 | `16379880062727150667612377994429058027750150674/129746337890625` | `1494048895141509478550315587139453832856` |

The beta-degree and lower-base `s`-degree pairs are independently recovered
as `(19,11)`, `(23,13)`, `(18,8)`, and `(22,10)`.

For either legal retained endpoint, direct adjacent-binomial products give

\[
\frac{\binom L{k-j}}{\binom L{k-i}}
\le (L+1)^{|i-j|}\le(2s)^q,
\]

and

\[
\frac{a^{k-j}}{p^{k-i}}
\le \left(\frac{p-1}{p}\right)^k\frac{p^{i_*}}{a^j}.
\]

The dominant kernels are coefficientwise nonnegative after the claimed
shifts, and each retained coefficient is at least one.  Hence the total
lower-base absolute contribution divided by the retained term is at most

\[
C_{\rm obj}s^{M+q}\left(\frac{p-1}{p}\right)^k.
\]

Using `k>=d>=241 log s`, the exact rational margins are `669/50` for
`p=6` and `59/72` for `p=7`.  For `C=N/D` and margin `u/v`, the program
finds the least integer satisfying

\[
D^v s^u>N^v
\]

by exact integer binary search and verifies failure at the preceding
integer.  The maximum is the 42-digit even-sufficient threshold displayed
above, strictly smaller than `S_gap`.

## Endpoint and transport splice

The low/high retained shifts are respectively `(0,19)`, `(0,23)`, `(2,18)`,
and `(2,22)`.  If the low binomial index is illegal, the high residual index
at the bulk endpoint is exactly `L-8`, `L-10`, `L-8`, or `L-10`; its lower
endpoint is nonnegative already for `d>=31`.  Thus a retained term is legal
throughout every high-range bulk interval.

The previously author-swapped old sources are unchanged at their audited
hashes.  They give the exact implications from the two page and two
sufficient certificates to the actual transports, together with the
all-parameter top bands.  The integer interfaces are contiguous:

- odd bulk ends at `2s-12`, and the top band starts at `2s-11`;
- even bulk ends at `2s-14`, and the top band starts at `2s-13`.

Combining the universal columns `0<=d<=30`, the effective gap
`31<=d<241 log s`, the now-effective high bulk `d>=241 log s`, and these top
bands covers every integer in the natural support `0<=d<=2s-4` for every
integer `s>=S_gap`.  Equality at `241 log s`, if integral, belongs to the
high range, so there is no endpoint gap.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  data/research_open/q1_two_hour_ten_proofs_transfer_2026-08-02/opg1757/\
cross_audit_high_range_by_erdos776.py
```

The run terminates with

```text
INDEPENDENT OPG HIGH-RANGE EFFECTIVITY AUDIT: PROMOTE
S_high_digits 42
dominated_by_S_gap True
```

