# Independent red-team audit of the second OPG attack

Date: 2026-07-31

> **Third-stage resolution.**  This document records the gap as it existed
> at audit time.  The gap has since been repaired in
> `ABEL_EXCEPTIONAL_PROFILE_LEMMA.md`: the exceptional-profile Abel lemma
> is proved by exact EGFs, Lagrange extraction, and coefficient-preserving
> pole reduction; the denominator-aware incidence ledger is then combined
> with all 180 required values in both the main and independent verifiers.
> The current claim ledger therefore classifies \(B_{2s-7}\) as
> **PROVED**.  The original audit text below is retained as a red-team
> record.

Audited files:

- `SECOND_ATTACK.md`;
- `SECOND_DEFICIT_COMPONENT_TABLE.md`;
- `verify_second_deficit.py`;
- `test_verify_second_deficit.py`.

The audit did not modify any of those four files.  Its independent
falsifier is `audit_second_raw_enum.py`.

## Verdict

No counterexample, missing excess species, factorial error, overlap error,
boundary error, or sign error was found.

The five displayed coefficients of \(B_{2s-7}\) have exceptionally strong
exact support.  In particular, an implementation which neither imports nor
calls either campaign verifier reproduces the whole layer for
\(4\leq s\leq16\).

There is nevertheless one important all-parameter proof gap in the current
write-up.  The claim
\[
\deg P_{h,e,c}\leq 2c+2e-2
\tag{A1}
\]
is the premise which turns interpolation into an identity for every
\(s\), but the two proof files only assert that one contraction of excess
\(a\) raises the normalized Abel degree by at most \(2a\).  They do not
derive that assertion.  The verifier assumes (A1); finite interpolation
and holdouts cannot prove their own degree bound.

Accordingly, the current main proof should be classified as

> **a bounded-degree-lemma conditional all-\(s\) theorem, backed by a
> strong independent exact certificate,**

until the weighted Abel/contraction degree lemma is written out.  This is
a proof-completeness issue, not evidence that the five formulas are false.
A denominator-aware repair requiring only one additional endpoint value is
given below.

## 1. Excess species are exhaustive and nonduplicated

Give a merge of arity \(r\) excess \(r-2\).  Binary merges have zero
excess.  Every nonbinary merge has positive integral excess, so for total
excess at most three the possible multisets are exactly
\[
\begin{array}{c|l}
e&\text{nonbinary arities}\\ \hline
0&\varnothing,\\
1&(3),\\
2&(4),\ (3,3),\\
3&(5),\ (3,4),\ (3,3,3).
\end{array}
\]
These are precisely the terms in equation (7).  There is no other
partition of \(e\), and arity labels make the mixed \((3,4)\) case
unambiguous.

A primitive chain record expands to a hypergraph on the initial core
blocks.  When a later merge selects a previously contracted block, its
block weight expands into the choice of one original endpoint.  Thus two
hyperedges can meet in one old vertex, but a new edge never contains two
vertices already in the same current component.  The expanded hypergraph
is therefore a hypergraphic forest.

Conversely, every edge of a hypergraphic forest can be contracted first:
every subset is independent, so the vertices of the next edge lie in
different current components in any edge order.  Hence:

- every unordered complete hyperforest with \(j\) edges has exactly \(j!\)
  valid chain orders;
- the product of the current block weights expands to the product of the
  original incidence weights, independently of the contraction order;
- the exponential \(1/m!\) for \(m\) nonbinary contractions removes
  exactly their \(m!\) internal orders;
- after those contractions, the binary edges are counted once by the
  ordinary forest polynomial.

This proves the combinatorial content of
\[
[\beta^{2j+e}]A_{h,j}
=j![x^j]\mathcal H_{h,e}(x).
\tag{A2}
\]

The independent program also checks (A2) semantically.  It enumerates
unordered labelled hyperedge sets, tests hypergraphic acyclicity with a
disjoint-set structure, and then brute-forces the remaining ordinary
forest.  At \(s=7\), all 30 required \((h,e,c)\) endpoints agree with a
separate direct-position primitive chain.  This includes the
three-ternary-edge species, not only the one-edge cases.

## 2. Ordered-chain and overlap factorials

The exact coefficient in the product of two binomial-basis terms is
\[
\binom tj\binom tq
=\sum_{\ell}
\frac{(j+q-\ell)!}
{\ell!(j-\ell)!(q-\ell)!}
\binom t{j+q-\ell}.
\]
At pooled depth \(n=j+q-\ell\), insertion of the two factors \(j!\) and
\(q!\) from (A2) gives
\[
\frac{n!}{\ell!}(j)_\ell(q)_\ell.
\tag{A3}
\]
If \(\mathcal H_e(x)=\sum_jH_{e,j}x^j\), the coefficient produced by
\(\ell\) derivatives is
\[
[x^{n-\ell}]
\mathcal H_e^{(\ell)}\mathcal H_f^{(\ell)}
=\sum_{j+q-\ell=n}(j)_\ell(q)_\ell H_{e,j}H_{f,q}.
\]
Thus both the \(1/\ell!\) and the two derivatives in equation (11) are
correct.

For \(n=2s-7\),
\[
2s-4-j-q=3-\ell
\]
and the total beta offset above \(2n\) is
\[
r=2\ell+e+f+a,
\]
where \(a\) is the degree selected from
\((1+s\beta)^{3-\ell}\).  Therefore:

- \(r=0,1\) force \(\ell=0\);
- \(r=2,3\) permit exactly \(\ell=0,1\);
- the \(r=4\) coefficient may also contain \(\ell=2\), but it is supplied
  independently by the already audited all-depth top-face theorem.

No overlap class is omitted from the four coefficients actually computed
with the hyperforest table.

The component relation is also correct.  In both determinant products it
is
\[
c+d+e+f=5-\ell.
\]
After including \(s^a\), every contribution therefore has the common
power \(s^{2s-12+r}\), exactly as claimed.

## 3. Independent algebra and boundary audit

The four table-derived factors and the top-face factor were independently
transcribed into exact rational arithmetic.  Expanding at \(s=u+5\)
gives
\[
\begin{array}{c|rrrrr}
 &u^0&u^1&u^2&u^3&u^4\\ \hline
P_0&600&1030&484&56&2\\
P_1&1360&7256/3&1232&544/3&8\\
P_2&1188&2288&1364&280&16\\
P_3&480&1032&736&200&16\\
P_4&76&566/3&166&184/3&8.
\end{array}
\tag{A4}
\]
Thus every \(P_r(s)\) is strictly positive for every integer \(s\geq5\).
At \(s=4\), every factor contains \(s-4\), and the independent primitive
calculation gives \(B_1=0\).

For the fifth factor, put \(n=2s-7\).  Directly classifying partitions of
\(n+2\) into \(n\) blocks gives
\[
{n+2\brace n}=\binom{n+2}{3}+3\binom{n+2}{4},
\qquad
{n+1\brace n}=\binom{n+1}{2}.
\]
Consequently
\[
4\bigl({2s-5\brace2s-7}-{2s-6\brace2s-7}\bigr)
=\frac23(s-4)(s-3)(2s-7)(6s-11),
\]
which independently confirms \(P_4\).

The direct-position chain reconstructs the complete five-coefficient row
for every \(s=4,\ldots,16\).  Five nonboundary values already determine
the displayed quartics; the remaining values are exact holdouts.  This is
an algebra/falsification check, not by itself an all-\(s\) proof.

## 4. The missing degree lemma

For a fixed exceptional profile
\[
\mathbf v=(v_1,\ldots,v_p),\qquad
\mathbf w=(1^{\,s-\sum v_i},\mathbf v),
\]
the required ordinary-forest input is the following weighted Abel lemma.

> **Exceptional-profile Abel lemma.**  If \(b=|\mathbf w|\), then
> \[
> \mathcal F_c(\mathbf w)
> =\left(\prod_i v_i\right)s^{b-2c}Q_{\mathbf v,c}(s),
> \qquad
> \deg Q_{\mathbf v,c}\leq2c-2.
> \tag{A5}
> \]

There is a standard EGF proof route.  Let \(T=ze^T\),
\(U=T-T^2/2\), and \(D=z\,d/dz\).  A tree containing a fixed set \(J\)
of \(p_J\geq1\) exceptional blocks of total weight \(a_J\) has unit-label
EGF
\[
\frac{\prod_{i\in J}v_i}{a_J}
(a_J+D)^{p_J-1}e^{a_JT},
\tag{A6}
\]
whereas a component containing no exceptional block has EGF \(U\).
Partitioning the exceptional blocks among at most \(c\) components and
using
\[
[z^N]F(T(z))
=[t^N](1-t)F(t)e^{Nt}
\tag{A7}
\]
reduces (A5) to Abel's binomial convolution.  Induction on the number of
unrooted components shows that each new component raises the residual
polynomial degree by at most two; exceptional-block operators in (A6)
raise the extracted base power and do not raise that residual bound.
This yields \(2(c-1)\).

Equivalently, one can use the rooted-component recurrence
\[
s\,\mathcal F_c(\mathbf w)
=\sum_{\varnothing\ne I\subseteq[b]}
\left(\sum_{i\in I}w_i\right)^{|I|-1}
\left(\prod_{i\in I}w_i\right)
\mathcal F_{c-1}(\mathbf w_{I^c})
\tag{A8}
\]
and Abel's identity at every induction step.  Formula (A8) follows by
choosing one root of weight \(w_i\) in one component; summing the root
weight over all components gives \(s\).

Equations (A5)--(A8) identify a short route to a complete proof, but the
induction and its degree ledger are not present in either audited proof
file.  A journal version should include them rather than cite the finite
verifier.

## 5. Denominator-aware exact repair

One can avoid first proving that the normalized endpoint is itself a
polynomial of degree (A1).

Fix an ordered list of \(m\) nonbinary arities \(r_i\), with
\[
e=\sum_i(r_i-2),\qquad m\leq e.
\]
After the contractions the number of blocks is
\[
b'=s-h-e-m.
\]
Classify the contraction record by its finite incidence type.  If it uses
\(\nu\) previously untouched unit blocks, its embedding multiplicity is a
falling-factorial polynomial of degree \(\nu\).  Since the sum of all
arities is
\[
\sum_i r_i=e+2m,
\]
one has \(\nu\leq e+2m\).  All created block weights are fixed constants
within an incidence type, so (A5) applies to the contracted profile.

Relative to the target factor \(s^{s-h-2c-e}\), a type therefore has the
form
\[
\frac{E_\tau(s)Q_{\tau,c}(s)}{s^m},
\qquad
\deg E_\tau\leq e+2m,\quad
\deg Q_{\tau,c}\leq2c-2.
\tag{A9}
\]
Taking the common denominator \(s^e\) over all \(m\leq e\) shows that the
normalized endpoint has denominator dividing \(s^e\) and numerator degree
at most
\[
(e+2m)+(2c-2)+(e-m)
\leq 2c+3e-2.
\tag{A10}
\]

After multiplying a proposed table identity by \(s^e\), it is therefore
enough to check
\[
2c+3e-1
\tag{A11}
\]
distinct positive values of \(s\).  The main verifier currently checks
\[
(2c+2e-2)+3=2c+2e+1
\]
values.  That is already sufficient for \(e=0,1,2\); for \(e=3\) it is
short by exactly one value.

The independent direct-position implementation checks the full count
(A11) for every one of the 30 table entries: 180 exact endpoint values in
total.  In particular, the three \(e=3,c=1\) entries are also checked at
\(s=16\).  All agree with the table.

Thus a rigorous repair can replace the unproved strong assertion (A1) by:

1. a complete proof of the exceptional-profile Abel lemma (A5);
2. the elementary incidence ledger (A9)--(A10);
3. the 180-value exact certificate.

This repair proves the displayed polynomial identities a posteriori and
does not need to assume their polynomiality before interpolation.

## 6. Executable results

The campaign tests pass:

```text
Ran 6 tests in 2.574s
OK
```

The independent audit command is

```bash
python3 audit_second_raw_enum.py \
  --minimum-s 4 --maximum-s 16 --species-s 7
```

Its result is:

```text
raw pooled s=4..16: PASS
unordered hyperforest / ordered chain: PASS (30 endpoints at s=7)
denominator-aware component certificate: PASS (180 exact endpoint values)
```

The independent implementation enumerates actual subsets of block
positions.  It does not import `verify_second_deficit.py`,
`verify_pooled_top_face.py`, or the inherited primitive transfer.

## 7. Scope firewall

Even after the degree lemma is supplied, the result proves one
complete-split pooled layer:
\[
B_{2s-7}>_{\rm coeff}0\quad(s\geq5),\qquad B_1=0\quad(s=4).
\]
It does not prove all \(B_n\), the full complete-split Rayleigh statement,
or arbitrary-host OPG-1757.
