# Blind audit: Erdős #776 final chamber and leading-block theorem

Date: 2026-08-02

Audit window: 15:35--16:12 HKT

Auditor: OPG-1757 author lane, using an independent greedy combinadic
implementation

## 1. Verdicts

| theorem family | verdict | scope |
|---|---|---|
| `FINAL_CHAMBER_COUNTERFAMILY.md` | **PASS** | The displayed dyadic family really has `gamma_3,gamma_4,gamma_5<0` from `s=14`, and every member has `gamma_6>0`. |
| `LEADING_BLOCK_DEFICIT_THEOREM.md` | **PASS** | The deficit calculus, two convolution lifts, five positive conditional chambers, and bounded bases close exactly the stated conditional chart. |
| author verifiers and focused tests | **PASS** | Both verifiers reproduce their advertised exact constants; 10 focused tests pass. |

No mathematical or expository repair was required.  The verdicts are
limited by the firewall in Section 8.

## 2. Frozen sources

The files were hashed before their proofs or implementations were read:

| source | SHA-256 |
|---|---|
| `BLIND_AUDIT_PROTOCOL.md` | `caba67b3d62d113eb68c177b410adbf8d799ca58babfaed354cd1a2d0c03a76f` |
| `FINAL_CHAMBER_COUNTERFAMILY.md` | `d80527f53b6a74e523b07e87a03f3f1a36db43b4c3a46fb60e203bd63396dd23` |
| `LEADING_BLOCK_DEFICIT_THEOREM.md` | `b94b9c46993e200bc8120260aa008dafc8552a18e35d2c4a18aea434e1f95a9d` |
| `verify_final_chamber_counterfamily.py` | `c03f206d2c7b7a866a1bcdf55ab33549f5f94a501b24bd6fadf868859de06d17` |
| `test_verify_final_chamber_counterfamily.py` | `9919da84c452d524b234335f9b5dc2c32906566466688f083be0fd33a63541dd` |
| `verify_leading_block_deficit_theorem.py` | `7f1cf1ef9a1bc8b7dad52966f464c3696a3f1591b8c8f1e7cc7cacefe67d95ff` |
| `test_verify_leading_block_deficit_theorem.py` | `4dfaa14da64d00510dd4493ff7af96dee3f96fbf7aedf71ff020248b99aaf2be` |

The independent verifier is
`verify_final_chamber_counterfamily_blind.py`.  It imports none of the
author's verifiers or Macaulay engines.

## 3. Reconstruction from the Macaulay definition

For a nonnegative integer `N`, I independently formed its greedy
`j`-canonical word

\[
 N=\sum_{i=1}^j\binom{a_i}{i},
 \qquad a_j>\cdots>a_1,
\]

and defined

\[
 U_j(N)=\sum_{i=1}^j\binom{a_i}{i+1}.
\]

No chart or raising function was imported from the author lane.  Applying
this definition to the proposed family gives the following gates.

### 3.1 Dyadic integrality and the original lattice — PASS

Let

\[
 h=224\,2^s,
 \quad q=\frac{448\,2^s-2}{5},
 \quad b=q+6,
 \quad n=\binom q2+10.
\]

Because `448=3 (mod 5)` and powers of two have period four modulo five,

\[
 q\in\mathbb Z
 \Longleftrightarrow 3\,2^s=2\pmod5
 \Longleftrightarrow s=2\pmod4.
\]

Also `2h=5q+2`, and direct subtraction gives

\[
 \binom{b-1}{2}+2-n=5q+2=2h.
\]

Thus these are actual lattice points, not relaxed points.  The inequalities
`b<h`, `h>=224`, and `b>=31` already hold at `s=2`; for example
`b=(2h+28)/5<h`.  The tax is independently recovered as

\[
 \tau=\binom b2+1-n=2h+b-2=6q+6.
\]

### 3.2 Exactly one promotion — PASS

The two literal rank-two words are

\[
 n=\binom q2+\binom{10}{1},
 \qquad
 n+b-1=\binom{q+1}{2}+\binom{15}{1}.
\]

Their upper indices are legal for every family point.  Hence the family
has exactly one, not merely at most one, rank-two promotion.

### 3.3 Four tail signs, canonical words, and caps — PASS

Direct calculation gives

\[
 R=40-6q,
 \qquad S=99-6q,
\]

and hence `R<S<0`.  The single-borrow normalizations are

\[
 \alpha=\binom{q-7}{2}+\binom{13}{1},
 \qquad
 \beta=\binom{q-6}{2}+\binom{78}{1}.
\]

Raising these words and subtracting the tax gives

\[
 P=\binom{q-8}{3}+\binom{q-14}{2}+\binom41,
\]

\[
 Q=\binom{q-7}{3}+\binom{q-13}{2}+\binom{2934}{1}.
\]

For `q>=2948` these are literal canonical words, are positive, and lie
strictly below their next caps.  In particular every counterexample
parameter `s>=14` satisfies exactly

\[
 (R,S)=(--),\qquad(P,Q)=(++).
\]

All upper-index inequalities were checked directly, rather than inferred
from a finite sign scan.

## 4. Surpluses and the first failure

Pascal cancellation of the independently reconstructed words gives

\[
 \gamma_3=44-6q,
 \qquad
 \gamma_4=2906-6q,
\]

and, once `q>=2948`,

\[
 \gamma_5=\binom{2934}{2}-6q-16
 =4\,302\,695-6q.
\]

The threshold is exact:

\[
 4\,302\,695-6(717115)=5,
 \qquad
 4\,302\,695-6(717116)=-1.
\]

The dyadic values at `s=2,6,10,14` are respectively

\[
 q=358,5734,91750,1468006.
\]

Therefore the first negative family member is exactly `s=14`, not just an
eventual one.  An uncompressed orbit computation gives there

\[
 (\gamma_3,\gamma_4,\gamma_5)
 =(-8807992,-8805130,-4505341).
\]

This is a literal counterexample to NB/(2.13).

## 5. Rank-six recovery

The left second tail has the canonical word

\[
 P_2=\binom{q-8}{4}+\binom{q-15}{3}
 +\binom{q-22}{2}+\binom{q-132}{1}.
\]

For `q>=4302621`, the right word is

\[
 Q_2=\binom{q-7}{4}+\binom{q-14}{3}
 +\binom{q-20}{2}+\binom{4302600}{1}.
\]

The threshold is the strict canonical inequality
`q-20>4302600`.  The first dyadic point above it is `s=18`.  Exact
Pascal cancellation gives throughout this stable range

\[
 \gamma_6
 =\binom{4302600}{2}+104q-8421
 =9\,256\,181\,220\,279+104q>0.
\]

The first rank-five counterexample `s=14` lies below that stable threshold
and must be treated separately.  Its actual right word is

\[
 Q_2=\binom{1467999}{4}+\binom{1467992}{3}
 +\binom{1467988}{2}+\binom{1366627}{1},
\]

and direct greedy raising gives

\[
 \gamma_6=3\,088\,969\,555\,650>0.
\]

The independent orbit also reproduces the complete pre-stable table at
`s=2,6,10,14`.  Thus the claim `gamma_6>0` holds on the entire family;
the stable word was not illegally extrapolated down to `s=14`.

## 6. Leading-block deficit theorem

### 6.1 Deficit transport — PASS

Writing `C=binom(A,j)`, superadditivity applied to
`C-E=(C-D)+(D-E)` gives

\[
 \Lambda_{j,A}(D)-\Lambda_{j,A}(E)\ge U_j(D-E).
\]

For the vertical comparison, diagonally shifting the canonical word of
`X=C-E` increases its lower cost by at most `binom(A,j-1)` and its upper
cost by exactly `X`.  Monotonicity then gives

\[
 \Lambda_{j,A+1}(E)-\Lambda_{j,A}(E)\le E.
\]

The two displayed consequences in the author note follow with the correct
inequality directions.  A separate exhaustive check for ranks two and
three and caps through 11 found no counterexample.

### 6.2 Two convolution lifts — PASS

The finite bases were independently minimized with the new Macaulay engine:

| lemma | complete range | minimum margin | minimizer data |
|---|---:|---:|---|
| rank-two split then rank three | `32<=w<=421` | 178 | `(w,x,G)=(32,40,215)` |
| rank-three split | `32<=r<=277` | 258 | `(r,D,D+V)=(32,188,384)` |

For the infinite tails, the elementary lower envelopes

\[
 U_2(N)\ge\frac{(\sqrt{2N}-3)_+^3}{6},
 \qquad
 U_3(N)\ge\frac{((6N)^{1/3}-4)_+^4}{24}
\]

are increasing and convex on their positive supports.  Independent exact
arithmetic reproduces the two rational anchors

\[
 \frac{51111641}{9375000}>0,
 \qquad
 \frac{2674108561}{2929687500}>0.
\]

Differentiating before reading the author's checker gives exact slack over
the claimed derivative lower bounds:

\[
 \frac{3s^2(11421s+18688)}{224000(s+3)}>0
 \quad(s\ge32),
\]

\[
 \frac{12167s^2(s-37)}{699840(s+3)}\ge0
 \quad(s\ge37).
\]

The first lower bound uses `t>=5s/4` and `t>=40`; the second uses
`t>=3s/4>27`.  These inequalities follow immediately by cubing.  Hence
both infinite tails are analytic, not computational extrapolations.

### 6.3 The five positive chambers — PASS

The sign routing and cap gaps were rederived from the unified identity.

- `(++)->(--)`: adjacent deficits have
  `G>=U_2(3r+2)-1`, while `tau<=binom(r,2)+1`; Lemma 4.1 is strict.
- `(++)->(-+)`: the two-gap sum obeys
  `D+V>=U_2(3r+2)-1`; Lemma 4.2 beats the exact negative tail.
- `(-+)->(+-)`: the leading gap is two, not one.  With
  `rho+beta>=3u-7`, the retained full-block loss reduces it to Lemma 4.1.
- `(--)->(-+)`: for `q>=216`, the implication `P<0` gives
  `alpha<q^2/18`, hence `K>=q/3` and
  `beta-alpha>=q^2/18>=3(q+r)+2`; Lemma 4.2 applies.
- `(--)->(--)`: the same large separation gives an adjacent deficit gap,
  and Lemma 4.1 applies.

The complete independent `2<=q<=215` enumeration forms the antecedent
before filtering the first tails.  It finds 133 antecedents, exactly one
`(--)->(-+)` point with `gamma_5=4923`, and exactly three
`(--)->(--)` points with surpluses `4222,4599,9010`.  Thus no small
parameter hole remains in the last two proofs.

The sixth chamber `(--)->(++)` is not silently included: it is precisely
the refuted row audited in Sections 3--5.

## 7. Reproducibility

Independent audit command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 erdos776/verify_final_chamber_counterfamily_blind.py
```

Output:

```text
ERDOS776 FINAL-CHAMBER BLIND ARITHMETIC: PASS
first_negative_s 14
first_negative_gamma5 -4505341
first_negative_gamma6 3088969555650
stable_rank6_q 4302621
```

Author verifier and test commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 erdos776/verify_leading_block_deficit_theorem.py
PYTHONDONTWRITEBYTECODE=1 \
python3 erdos776/verify_final_chamber_counterfamily.py
PYTHONDONTWRITEBYTECODE=1 pytest -q \
  erdos776/test_verify_final_chamber_counterfamily.py \
  erdos776/test_verify_leading_block_deficit_theorem.py
PYTHONDONTWRITEBYTECODE=1 pytest -q erdos776
```

The focused tests report `10 passed in 9.38s`.  The author verifiers also
return the two finite convolution minima, 174206 deficit pairs, all four
small double-negative targets, the first negative dyadic point, and the
stable rank-six threshold.  After adding the three independent-audit
regressions, the complete lane reports `28 passed in 51.53s`.

## 8. Firewall

This audit proves that the explicit family refutes:

1. NB/(2.13), the proposed rank-five implication;
2. uniform rank-five positivity in the conditional `(--)->(++)` chamber;
3. the claim that every initial no-borrow negative point seeds by rank five.

It does **not** refute Erdős #776.  Every counterfamily member recovers by
rank six, so it also does not refute a variable-rank or uniform adaptive
seed theorem.  The global exhaustiveness of one promotion and one wall is
still open, as are the capacity interface and the original public problem.
