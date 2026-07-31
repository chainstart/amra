# OPG-1757: candidate universal second symbol

Date: 2026-07-31

Status: `RESOLVED__SEE_SECOND_SYMBOL_THEOREM.md`

> **Resolution update.**  The conjecture below is now proved for every
> \(q\) and every offset in `SECOND_SYMBOL_THEOREM.md`.  This file is kept
> as the discovery and finite-evidence record.

The proved leading-symbol theorem suggests a sharper expansion.  Put
\[
A(z)=1+2z+2z^2
\]
and define
\[
M_q(z)=\sum_{r=0}^{2q}[s^{2q-1}]C_{q,r}(s)z^r.
\]
For \(q=1,\ldots,6\), exact extraction from the already proved layer
formulas gives
\[
\boxed{
M_q(z)=\frac4{q!}A(z)^{q-2}\,q\,P_q(z),
}
\tag{1}
\]
where
\[
\boxed{
\begin{aligned}
P_q(z)={}&4-\frac{2(q-10)}3z-(3q+4)z^2\\
&-2(2q+11)z^3-\frac{2(4q+29)}3z^4.
\end{aligned}
}
\tag{2}
\]
At \(q=1\), the apparent \(A^{-1}\) cancels because
\[
P_1(z)=-A(z)(11z^2+2z-4).
\]

This pattern is structurally plausible: one order below the leading
four-Poisson collapse should allow at most one additional local defect,
which explains an \(A^{q-2}\) background and a quartic defect symbol.
However, proving (1) for arbitrary \(q\) requires one more order of the
endpoint matching-curvature expansion.  The current curvature theorem
does not supply that order.  Thus (1)--(2) are not used in the proved
eventual-positivity theorem.

## Two all-\(q\) boundary checks

The constant and highest-offset coefficients of (1) are independently
proved for every \(q\), not merely checked through six.

At \(z^0\), the conjecture says
\[
[s^{2q-1}]C_{q,0}=\frac{16}{(q-1)!}\qquad(q\geq1).
\tag{3}
\]
This is exactly the previously proved second term of the fixed-component
ordinary-forest determinant with total component count \(q+3\):
\[
\frac4{q!}s^{2q}+\frac{16}{(q-1)!}s^{2q-1}
+O_q(s^{2q-2}).
\]

At \(z^{2q}\), use the exact all-depth top face
\[
C_{q,2q}(s)
=4\left(
{2s-5\brace 2s-5-q}
-{2s-6\brace 2s-5-q}
\right).
\tag{4}
\]
For fixed \(q\), partitions with \(q\) pairs and with one triple plus
\(q-2\) pairs give the two highest degrees
\[
{m\brace m-q}
=\frac{(m)_{2q}}{2^q q!}
+\frac{(m)_{2q-1}}{6\,2^{q-2}(q-2)!}
+O_q(m^{2q-2}).
\tag{5}
\]
The second displayed term is omitted when \(q=1\).
All other block profiles use at most \(2q-2\) non-singleton vertices.
The subtracted Stirling number in (4) also has degree at most \(2q-2\).
Putting \(m=2s-5\) in (5) therefore gives
\[
\boxed{
[s^{2q-1}]C_{q,2q}
=-\frac{2^{q+1}q(4q+29)}{3q!},
}
\tag{6}
\]
which is precisely the \(z^{2q}\) coefficient predicted by (1)--(2).

Thus the second-symbol conjecture has rigorous all-\(q\) support at both
ends of every row.  Its interior offsets remain conjectural.

If proved, the formula would provide the first quantitative correction to
the positive leading symbol and would be the natural starting point for a
growing-deficit window.  It would still not by itself control all higher
orders when \(q\) grows with \(s\).

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_second_symbol_conjecture.py
```
