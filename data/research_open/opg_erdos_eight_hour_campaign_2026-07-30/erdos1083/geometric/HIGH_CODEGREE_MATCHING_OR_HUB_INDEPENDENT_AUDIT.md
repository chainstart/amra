# Independent audit: high-codegree matching-or-hub theorem

Date: 2026-07-30

Audited file:
`HIGH_CODEGREE_MATCHING_OR_HUB_THEOREM.md`

## Verdict

**PASS.**  The dyadic extraction, the \(\lambda=5+\kappa\) split,
the hub pigeonhole exponent, and the finite-field \(K_{3,2}\)
obstruction are all correct.  I found no exponent gap or hidden use of
Euclidean realizability.

The only presentational point worth making explicit in a later
revision is that the two asymptotic cases around
\(\lambda=5+\kappa\) should be read with one common slack function.
This is not a mathematical gap: the proof can be made literal by
choosing a single \(\delta(t)=o(1)\) that dominates every preceding
exponent error and splitting at
\(\log_t T=5+\kappa-\delta(t)\).

## 1. Independent check of the weighted graph lemma

Let \(R\) be the rich edge set.  Since a simple graph on \(n\)
vertices has fewer than \(n^2\) edges, the nonrich mass is strictly
less than
\[
 n^2\frac{T}{4n^2}=\frac T4.
\]
Thus \(R\) carries at least \(3T/4\).

If a maximal rich matching has \(m<k\) edges, its \(2m<2k\)
endpoints cover \(R\).  Summing rich weighted degrees over these
endpoints counts every rich edge at least once, so one endpoint has
rich degree at least
\[
 \frac{3T/4}{2k}=\frac{3T}{8k}.
\]
For the automatic bound, the same vertex cover gives
\[
 \#R\leq 2mn,
 \qquad
 \#R\geq\frac{3T}{4U},
\]
and hence \(m\geq3T/(8Un)\).  No regularity or unweighted-degree
assumption is being smuggled into this step.

The repository's exhaustive certificate checks all
\(4^6-1=4095\) nonzero weightings of the six edges of \(K_4\), with
weights in \(\{0,1,2,3\}\), for the matching-or-hub alternative.

## 2. Dyadic-bin extraction

Write \(T_d=\sum_eW_{e,d}\).  Positivity gives
\[
 \sum_dT_d^2
 \geq
 \sum_d\left(T_d^2-\sum_eW_{e,d}^2\right)
 =\mathfrak C_{\rm plane}
 \geq t^{13-o(1)}.
\]
The integrality assumption matters here only to ensure that every
positive \(T_d\) is at least \(1\).  Together with
\[
 T_d\leq {|\mathcal A|\choose2}\max_eW_{e,d}
 \leq t^{6+o(1)},
\]
it leaves \(O(\log t)\) nonempty dyadic ranges.  In a bin
\(T\leq T_d<2T\), its contribution to \(\sum_dT_d^2\) is less than
\(4LT^2\).  Therefore one bin satisfies
\[
 LT^2\geq t^{13-o(1)};
\]
the factor \(4\) and the \(O(\log t)=t^{o(1)}\) bin loss are correctly
absorbed.

With \(\ell=\log_tT\), the two endpoint estimates are
\[
 \ell\geq5-o(1)
 \quad\text{from }L\leq|\mathcal D|\leq t^{3+o(1)},
 \qquad
 \ell\leq6+o(1),
\]
and
\[
 L\geq t^{13-2\ell-o(1)}.
\]
The label-dependent rich threshold is
\[
 \frac{T_d}{4|\mathcal A|^2}
 =t^{\ell-2-o(1)}
 \geq t^{3-o(1)},
\]
as claimed.

## 3. The \(\kappa\)-split and hub pigeonhole

Take an integer
\[
 k=\left\lfloor t^\kappa/t^{\delta(t)}\right\rfloor
\]
with \(\delta(t)=o(1)\) chosen large enough to absorb all existing
subpolynomial losses.

If \(\ell\geq5+\kappa-\delta(t)\), then the automatic matching bound
gives
\[
 m_d\gg\frac{t^\ell}{t^{4+o(1)}t^{1+o(1)}}
 =t^{\ell-5-o(1)}
 \geq t^{\kappa-o(1)}
\]
for every selected label.  Since \(\ell\leq6+o(1)\), the same bin has
\(L\geq t^{1-o(1)}\) labels.

In the complementary case, if at least \(L/2\) labels have a
\(k\)-matching, then
\[
 L/2\geq t^{13-2(5+\kappa)-o(1)}
 =t^{3-2\kappa-o(1)}
 \geq t^{1-o(1)}
\]
because \(\kappa<1\).

Otherwise, more than \(L/2\) labels have a hub with rich mass
\[
 \gg T/k
 \geq t^{5-\kappa-o(1)}.
\]
Assign one such hub to each of these labels.  Pigeonholing over
\(|\mathcal A|=t^{1+o(1)}\) planes gives one common hub for at least
\[
 \frac{L}{2|\mathcal A|}
 \geq t^{12-2\ell-o(1)}
 \geq t^{2-2\kappa-o(1)}
\]
labels.  This verifies both exponents in \(({\rm H}_\kappa)\).

## 4. Finite-field ledger and absence of \(K_{3,2}\)

For a row \((u,v)\), the equation
\[
 au^2+bu+c=v
\]
is one nonzero affine linear constraint on \((a,b,c)\), so exactly
\(q^2\) labels contain that row.  Each label contains one row for
each \(u\), hence \(q\) rows.  It follows independently that
\[
\begin{array}{c|c}
\text{quantity}&\text{value}\\ \hline
\text{support cells}&q^2q^2=q^4\\
\text{cell weight}&q^4\\
\text{row mass}&q^2q^4=q^6\\
\text{label mass}&qq^4=q^5\\
\text{total mass}&q^8\\
\sum W^2&q^4q^8=q^{12}\\
\sum_dT_d^2&q^3q^{10}=q^{13}\\
\mathfrak C_{\rm plane}&q^{13}-q^{12}.
\end{array}
\]

For three distinct rows:

* if two have the same input \(u\) and different outputs \(v\), no
  label contains both;
* otherwise their three inputs are distinct, and the three evaluation
  constraints have Vandermonde determinant
  \[
  (u_2-u_1)(u_3-u_1)(u_3-u_2)\ne0.
  \]
  Hence exactly one quadratic label contains all three.

Thus any three rows have at most one common label, which is precisely
the absence of a \(K_{3,2}\) in the row-label support graph.  The
argument remains valid for \(q=3\); “odd prime” is sufficient.

Finally, for a nonconstant quadratic, every output has at most two
preimages.  Its \(q\)-edge graph therefore has a matching of size at
least \(\lceil q/2\rceil\).  There are exactly \(q^3-q\) nonconstant
labels, so the claimed matching count is also exact.

## 5. Reproduction result

Executed:

```bash
pytest -q test_verify_high_codegree_matching_or_hub.py
python3 verify_high_codegree_matching_or_hub.py --prime 7
```

Result: all five tests passed; the exact verifier returned
`"status": "PASS"`.  The failed availability check for the optional
`jq` display utility did not affect either verifier.
