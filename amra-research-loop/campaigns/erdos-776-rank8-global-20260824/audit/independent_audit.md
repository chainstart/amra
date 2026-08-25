# Independent audit: all-parameter rank-8 entry campaign

## Verdict

The campaign's proved algebraic interface is correct, but its decisive lemma
is conditional.  The exact prefix-cancellation theorem, the one-sided
Kruskal--Katona carry inequality, the constant recursion, the \(V=125\)
join, and the implication

\[
 \text{(H1)--(H2)}\Longrightarrow
 D^{[V]}_8<\binom{V-11}{8}\quad(V\ge40)
\]

all pass independent reconstruction.  However, (H1)--(H2) themselves are
verified only for \(40\le V\le500\); no all-parameter proof is supplied.
Thus the rank-8 entry remains open.

The proper recommendation is **continue at survivor deepening**, with no
promotion.  M776G-01 and M776G-02 are concrete, noncosmetic all-parameter
targets and have not been falsified, so an exhaustion freeze is premature.
But a conditional implication plus a finite scan is neither
`standalone_decisive_lemma` nor `global_interface_closed`.  The exact public
threshold \(n_0(r)\) is even farther away: the all-\(V\) rank-8 entry would
still need the complete \((r,n)\mapsto V\) construction replay, every-larger-
\(n\) coverage, a sharp lower boundary, and the small-\(r\) reconciliation.

The original Erdős #776 problem, main term, and main exponent are unchanged.

## Blind protocol

Before opening any author evidence, verifier, `kill_tests.json`, or the
pre-existing `audit.json`, I independently reconstructed the requested
lemmas and their composition in `audit/blind_reconstruction.md`.  Its frozen
pre-unblinding SHA-256 is

```text
afba4e82c2eb7d9d45700767824cfc9ba9c18d5f0df823f8d742dfd3200109d6
```

The blind derivation recovered, before seeing the author constants, the
recursion

\[
 b_{14}=1,\qquad b_{r-1}=1+rb_r,
\]

and the endpoint \(b_6=130455928<\binom{112}{5}\).

## Prefix-cancellation lemma

Let \(q>s\ge1\), let

\[
 P=\sum_{i=s+1}^{q}\binom{a_i}{i},qquad
 a_q>\cdots>a_{s+1}\ge s+1,
\]

and let \(x\ge0\).  The exact separator condition is that every upper index
of the \(s\)-canonical expansion of \(x\) be strictly below
\(a_{s+1}\).  Equivalently,

\[
 0\le x<\binom{a_{s+1}}s. \tag{1}
\]

Under (1), uniqueness of the canonical expansion gives

\[
 \operatorname{KK}_q(P+x)
 =\sum_{i=s+1}^{q}\binom{a_i}{i-1}
  +\operatorname{KK}_s(x). \tag{2}
\]

If two suffixes satisfy the same strict separator behind the same prefix,
their shadow difference is exactly the difference of their suffix shadows.
The author statement has the correct quantifiers and strict separator.  It
also correctly warns that adjacent parameters do not automatically share a
prefix; the exact \(V=56\to57\) rank-7 carry wall refutes such a uniform
claim.

For

\[
 W_r(V)=D^{[V]}_{r+2}-\binom{V-12}{r+2}
                         -\binom{V-13}{r+1},
\]

the high-rank separator

\[
 0\le W_r(V)<\binom{V-13}{r}
\]

is exactly what places its \(r\)-canonical word below the two-term prefix.
Equation (2) then gives, for \(7\le r\le14\),

\[
 W_{r-1}(V)=V+\operatorname{KK}_r(W_r(V)). \tag{3}
\]

The last step uses only the rank-7 separator to produce \(W_6\).  It does
not assume a rank-6 separator, whose strict cap would be the desired result.
The refined bridge is therefore noncircular.

## One-sided carry inequality and constants

For \(r\ge2\), disjoint-ground-set families prove

\[
 \operatorname{KK}_r(x+h)
 \le\operatorname{KK}_r(x)+\operatorname{KK}_r(h),
 \qquad
 \operatorname{KK}_r(h)\le rh. \tag{4}
\]

Monotonicity covers a negative increment, so in all cases

\[
 \operatorname{KK}_r(y)-\operatorname{KK}_r(x)
 \le r\max(0,y-x). \tag{5}
\]

The author states (4) for \(r\ge1\).  The inequality is also true at rank
one, but one proof sentence is imprecise there: two nonempty 1-uniform
families on disjoint point sets have the same 0-shadow \(\{\varnothing\}\),
so their shadows are not disjoint and the union's shadow size is not the sum.
Replacing “has shadow size” by “has shadow size at most,” or checking rank one
directly, repairs the proof.  This has no impact because the campaign applies
(4)--(5) only at ranks 7 through 14.

Write \(\delta_r=W_r(V+1)-W_r(V)\).  From (3)--(5),

\[
 \delta_{r-1}\le1+r\max(0,\delta_r).
\]

Starting with \(\delta_{14}\le1\) gives the independently reproduced table

| \(r\) | 14 | 13 | 12 | 11 | 10 | 9 | 8 | 7 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| \(b_r\) | 1 | 15 | 196 | 2353 | 25884 | 258841 | 2329570 | 18636561 | 130455928 |

Every arithmetic entry is correct.  The large \(b_6\) is a conservative
symbolic bound from \(\operatorname{KK}_r(h)\le rh\), not a regression fit.

## Base case and off-by-one check

The rank-8 target is exactly

\[
 D^{[V]}_8<\binom{V-11}{8}
 \quad\Longleftrightarrow\quad
 W_6(V)<\binom{V-13}{6}. \tag{6}
\]

The cap increment at the first analytic transition is

\[
 \binom{113}{6}-\binom{112}{6}
 =\binom{112}{5}=134153712,
\]

which exceeds \(b_6\) by \(3697784\).  The exact scan proves the base for
every integer \(40\le V\le125\), including margin
\(M(125)=2392397730\).  Since (H1)--(H2), if proved as stated, hold for every
\(V\ge125\), the jump indexed by 125 controls \(125\to126\); its separator
applications use H1 at both 125 and 126.  The induction therefore has no
off-by-one gap.

What it does have is an unproved premise.  The campaign scan observes no H1
failure and no H2 jump above one through 500, with the largest observed
rank-14 jump equal to one at \(V=460\).  Those 461 values cannot establish
the clauses for unbounded \(V\).

## Decisive-lemma and public-closure audit

`decisive_lemma.json` accurately labels the high-rank statement
`conditional`.  Its evidence proves only the implication from H1--H2 and a
finite falsifier scan.  It therefore does **not** close the all-\(V\) rank-8
entry.

The inherited R004 dependency was replayed.  It proves the exact local tail

\[
 V\ge40,quad D_8<\binom{V-11}{8}
 \Longrightarrow D_2\le\binom{V-9}{2}.
\]

Its analytic argument handles \(V\ge1000\), while its exact engine exhausts
\(40\le V\le999\).  This validates the local rank-8-to-rank-2 dependency;
it does not construct a public antichain by itself.

No complete audited mapping from multiplicity/order parameters \((r,n)\) to
\(V\) was found.  In particular, the current package does not establish:

* an admissible \(V\) for every required \(r\) and every \(n\) above a
  proposed threshold, including parity and finite ranges;
* the all-larger-\(n\) construction required by the strict definition of
  \(n_0(r)\);
* a matching sharp nonexistence boundary establishing minimality;
* a certified reconciliation of \(r=2,3\) with every \(r\ge4\).

The closure contract refers to “the public problem's domain” rather than
spelling it out; its remaining notes partition the intended domain into
\(r=2\), \(r=3\), and \(r\ge4\).  This is harmless for the local rank-8
audit but should be made explicit as \(r\ge2\) before any
`original_problem_closed` claim.

Consequently, even a future proof of H1--H2 would initially close only the
rank-8 route interface.  It cannot presently be promoted as a main-term
improvement, much less as the exact value of \(n_0(r)\), until the parameter
and construction interfaces are supplied.

## Survivor and kill honesty

The campaign is mostly careful about evidence strength.

* M776G-01 is a valid conditional all-parameter mechanism.  Its high-rank
  premise is new information and stops above the circular rank-6 cap.
* M776G-02 is a genuinely different conditional carry-height mechanism.  Its
  elementary closure comparison is correct.  There is a minor definitional
  omission: when \(W_6(V)=0\), its canonical word has no largest upper
  index.  The statement should use the three branches \(W_6<0\), \(W_6=0\)
  (both immediate success), and \(W_6>0\) with the top-index bound.  This
  repair does not change the route.
* M776G-03 through M776G-08 and M776G-11 have exact counterexamples at the
  scopes claimed.  The values \(V=288\), \(V=40\), \(40\to41\),
  \(50\to51\), and \(42\to43\) were all reproduced.
* M776G-09 is correctly killed as a circular restatement rather than a false
  missing-set theorem.
* M776G-10 correctly kills only a derivation from scalar order; it explicitly
  leaves the actual normalized \(W_6\) inequality open.
* M776G-12 correctly kills the implication to exact public threshold because
  the parameter map, every-larger-order construction, sharp lower boundary,
  and small cases are independent missing obligations.

Thus the recorded 100% kill ratio among the ten non-survivors is honest at
its stated scopes, and the two survivors are honestly conditional.  Neither
finite survivor scan is misreported as proof.

## Machine replay

Environment: Python 3.12.3.

```text
python3 evidence/verify_rank8_obstructions.py
PASS
```

This reproduced 92,242 prefix concatenations, 82,008 one-sided carry checks,
all displayed exact route kills, the 86-point base \(40\le V\le125\), and
the 461-point survivor falsifier range \(40\le V\le500\).  The verifier
SHA-256 is

```text
633fdbce20f78e5341f9683b977d7515ae5173cee423132654e694e33590fc2a
```

I separately compared the compressed-run orbit against a direct canonical
recurrence for every \(40\le V\le150\); every rank value agreed.

The inherited tail was also replayed:

```text
python3 /home/biostar/work/projects/amra/artifacts/erdos_master_rotation/R004/core_776_635/776/verify_rank8_five_term_barrier.py
PASS
```

Its verifier SHA-256 is
`144514997d0c44b82700222c4ae31a2c74c0d4112a4f05539ac2128d792ff0a6`.
Both scripts correctly label strategic finite orbit values as falsifier
evidence rather than universal proof.

## Novelty and recommendation

No public search for an exact solution was performed.  Priority for the
prefix/carry bridge is `priority_uncertain`, and the publication state is
`private_note`.

Recommended action:

> Continue at survivor deepening because the noncircular high-rank and logarithmic-carry mechanisms remain concrete and unfalsified, while the decisive H1--H2 lemma is still conditional and supports no AMRA promotion.

The audit content completes the independent reconstruction, statement,
dependency, novelty, and promotion-decision checks.  Per scope, I did not
modify `campaign_state.json`, `decision.json`, author evidence, mechanisms,
or survivors.
