# Independent audit of the round-3 multiscale countermechanism

## Verdict

**PASS.**  The author proof gives an all-parameter infinite counterfamily to
the exact stored claim `M776G-02-logarithmic-carry-height`.  I recommend that
`M776G-02` be marked **killed/refuted**, with
`evidence/ROUND3_MULTISCALE_CARRY.md` and its verifier as status evidence.

This verdict is only a route classification.  It does not prove or refute the
rank-eight entry, determine the exact public threshold, or change the public
Erdos 776 statement, main term, or exponent.

## Blind protocol

Before opening the author evidence or verifier, I wrote and froze
`audit/round3_multiscale_blind.md`.  Its SHA-256 is

```text
ad3d988e1e81188e5dbf6b0631d678e2ea5fa3b550bb27932c4b5806d22bf95d
```

The blind reconstruction isolated exactly two interfaces: the actual-orbit
bound `W6(V)>=V` and the canonical interval
`top<=B => W6(V)<binom(B+1,6)`.  Both are supplied by the opened author
evidence.  The blind file still has the frozen hash above after the audit.

Opened author artifacts and hashes:

```text
276e2e9da20f06fa938922e4fea761c62042225c95f1169d11c22a7b2eb59cf1  evidence/ROUND3_MULTISCALE_CARRY.md
5e94f1ef8f36e17420278986d09166344ea568c033f64d5ea25a1886d84f7a42  evidence/verify_round3_multiscale_carry.py
```

## 1. Actual shortened orbit and the isolated first tax

Put `R=V-13`.  The executable orbit begins with zero at rank `V-12` and its
first taxed step gives value `V` at rank `R`.  Thus the author's indexing

\[
 D_R=V,\qquad D_{q-1}=V+\operatorname{KK}_q(D_q)
 \quad(R\ge q\ge9)
\]

matches the actual shortened orbit; there is no one-rank shift.  I also
replayed this recurrence against the run-based implementation at every rank
for every `40<=V<=120`.

For the first-tax comparison orbit,

\[
 F_R=V,\qquad F_{q-1}=\operatorname{KK}_q(F_q).
\]

The monotonicity direction is correct.  Since a colex initial segment of size
`x` is contained in one of size `y` when `x<=y`, their lower shadows give
`KK_q(x)<=KK_q(y)`.  Starting from `D_R=F_R`, induction therefore gives
`D_q>=F_q`.  Keeping the final actual `+V` tax yields

\[
 D_8=V+\operatorname{KK}_9(D_9)
     \ge V+\operatorname{KK}_9(F_9).
\]

There is no deletion/delay comparison in the wrong direction.

## 2. Twelve-term canonical word and hockey-stick endpoints

The proposed rank-`R` word is exactly

\[
 V={V-12\choose R}
   +\sum_{j=1}^{12}{V-13-j\choose R-j}.
\]

Here `R=V-13`; the first term is `R+1=V-12` and each of the
twelve summands is one.  The upper indices are
`V-12,V-14,V-15,...,V-25`, strictly decreasing, so this is a valid
rank-`R` canonical word.  Greedy uniqueness also checks directly: after the
first term the remainder is 12, while choosing upper index `R` at the next
rank would already cost `R>12` for `V>=40`.

After `R-12` lower shadows, the last of the twelve summands reaches lower
index zero exactly on the final shadow and contributes
`binom(V-25,0)=1`.  Hence no endpoint is discarded:

\[
 F_{12}={V-12\choose12}
 +\sum_{k=0}^{11}{V-25+k\choose k}.
\]

The exact hockey-stick identity is

\[
 \sum_{k=0}^{11}{V-25+k\choose k}={V-13\choose11},
\]

so `F_12=P_12(V)`.  The two terms
`binom(V-12,q)+binom(V-13,q-1)` remain a separated canonical word for
`12>=q>=8`; successive shadows therefore give `F_q=P_q(V)` all the way to
`P_8`, with no asymptotic or missing-boundary step.

## 3. The universal floor `W6(V)>=V`

From the comparison above,

\[
 D_9\ge F_9=P_9(V),
 \qquad
 D_8\ge V+\operatorname{KK}_9(P_9(V))=V+P_8(V).
\]

Using the exact definition `W_6(V)=D_8-P_8(V)` gives

\[
 W_6(V)\ge V
\]

for every integer `V>=40`, including the endpoint.  This is a symbolic
all-parameter proof.  The verifier's finite rows are appropriately labelled
as guards rather than as the source of the universal quantifier.

## 4. Canonical-top threshold and off-by-one check

For positive integer `x`, the leading upper index of its rank-six canonical
word is at most `B` exactly when

\[
 x<{B+1\choose6}.
\]

The strict inequality and `B+1` are correct: the greatest value with top at
most `B` is `binom(B+1,6)-1`, while `binom(B+1,6)` has leading upper index
`B+1`.  The actual stored mechanism says that for every `V>=40`, either
`W6(V)<=0` or this top is at most `ceil(log2 V)+13`.  Since the universal
floor makes `W6(V)>0`, the positive branch necessarily applies.

At `V=2^m`, the ceiling is exactly `m`, so the mechanism would imply

\[
 W_6(2^m)<{m+14\choose6}.                            \tag{A1}
\]

There is no ceiling or equality ambiguity.

## 5. Dyadic inequality for every `m>=21`

The exact base case is

\[
 2^{21}=2,097,152>1,623,160={35\choose6}.
\]

The induction quotient is

\[
 \frac{{m+15\choose6}}{{m+14\choose6}}
 =\frac{m+15}{m+9}<2
\]

for all `m>=21`.  Therefore

\[
 2^m>{m+14\choose6}\qquad(m\ge21).
\]

Together with `W6(2^m)>=2^m`, this contradicts (A1).  Consequently the
actual zero-seed orbit has

\[
 T_6(2^m)>m+13=\lceil\log_2(2^m)\rceil+13
 \qquad(m\ge21).
\]

This is an unbounded explicit family inside the exact quantifier range of
`M776G-02`, so one counterexample cutoff is not being extrapolated.

## 6. Reproduction and scope

Executed:

```text
python3 evidence/verify_round3_multiscale_carry.py
```

Result: `PASS`; reported source SHA-256
`5e94f1ef8f36e17420278986d09166344ea568c033f64d5ea25a1886d84f7a42`.
It checks the first-tax identity on independent finite instances, actual
`W6>=V` rows, canonical intervals, and the dyadic base.  I separately checked
the dyadic inequality for `21<=m<=10000`; its universal validity comes from
the quotient proof, not that scan.  Campaign validation also returned
`valid: true`.

The lower floor does **not** refute the much larger rank-eight capacity
`W6(V)<binom(V-13,6)`.  Accordingly, the correct state change is to kill the
logarithmic-carry-height mechanism only; no public-problem promotion follows.
