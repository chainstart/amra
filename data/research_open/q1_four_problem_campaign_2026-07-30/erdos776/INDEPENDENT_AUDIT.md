# Independent audit of the rank-16 linear gate

Date: 2026-07-30

## Verdict

**PASS.**  No indexing error, lost strict inequality, or hidden canonical
carry was found in the rank-16 implication stated in `FINAL_REPORT.md`:

\[
D_{16}\le \binom{V-12}{16}+\binom{V-13}{15}+V-1
\quad\Longrightarrow\quad
D_8<\binom{V-11}{8}
\qquad(V\ge175).
\]

This verdict concerns the conditional implication only.  It does not prove
its still-open premise for every \(V\ge175\).

## Checks performed

- The descent indices are consistent.  At a rank-\(q\) state the residual has
  rank \(q-2\); the eight steps \(q=16,\ldots,9\) therefore use residual ranks
  \(14,\ldots,7\) and end with a rank-6 residual at \(D_8\).
- Independent integer recomputation gives
  \[
  (c_{14},\ldots,c_6)=
  (1,15,196,2353,25884,258841,2329570,18636561,130455928),
  \]
  exactly as reported.
- Every separation inequality is strict at \(V=175\).  The smallest base
  margin is the rank-6 margin
  \[
  \binom{162}{6}-130455928\cdot175=30{,}529{,}184>0.
  \]
- For \(6\le r\le14\), the claimed monotonicity is strict: after cross
  multiplication, the excess in the ratio test is
  \[
  V(V-12)-(V+1)(V-12-r)=(r-1)V+r+12>0.
  \]
  Hence the \(V=175\) separation checks propagate to all \(V\ge175\).
- The bound \(w_r<\binom{V-13}{r}\) forces the leading upper index in the
  rank-\(r\) canonical expansion of \(w_r\) to be at most \(V-14\).  Thus it
  lies strictly below the displayed upper index \(V-13\), justifying the exact
  separated shadow recurrence and excluding a hidden carry.
- A standalone ordinary combinadic implementation, not importing the supplied
  verifier, replayed the endpoint majorizing orbit and confirmed both displayed
  canonical prefix terms at every step and the final strict Pascal bound.
- `python3 data/research_open/q1_four_problem_campaign_2026-07-30/erdos776/verify_rank16_linear_gate.py`
  completed with status `PASS`; its independent finite engine agreed on
  \(40\le V\le174\), with minimum rank-8 margin \(260{,}272\).
