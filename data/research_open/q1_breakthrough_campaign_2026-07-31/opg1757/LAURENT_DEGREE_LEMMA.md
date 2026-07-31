# OPG-1757: filtered-ring lemma for endpoint Laurent coefficients

Date: 2026-07-31

Status: `PROVED__ALL_LAURENT_ORDERS__TOTAL_DEGREE_AT_MOST_TWICE_ORDER`

## 1. Statement

Put \(\rho=c-1\).  For \(h\in\{0,1,2\}\), write

\[
Q_{h,e,c}(s)=A_{e,c}s^{2\rho+2e}
 \left(1+\sum_{k\ge1}q_{h,k}(e,\rho)s^{-k}\right),
\qquad
A_{e,c}=\frac1{2^{\rho+e}\rho!e!}.
\tag{1}
\]

Coefficients beyond the degree of the endpoint are zero.  Then

\[
\boxed{q_{h,k}\in\mathbb Q[e,\rho],
\qquad \deg_{e,\rho}q_{h,k}\le2k.}
\tag{2}
\]

In particular, the coefficients \(g_h\) and \(j_h\) in
`SECOND_SYMBOL_THEOREM.md` have total degrees at most four and six.

## 2. One exact formula for all three markings

Set \(\epsilon=s^{-1}\), \(u=\epsilon v\), and

\[
\Phi_\epsilon(t,v)=\frac{e^{\epsilon vt}-1}{\epsilon v},
\quad V_\epsilon(t,v)=V(t,\epsilon v),
\quad J_\epsilon(t,v)=1-te^{\epsilon vt}=\partial_tV_\epsilon(t,v).
\tag{3}
\]

For \(P(t)=\sum_dp_dt^d\), define

\[
\mathcal L_{\alpha,\epsilon}P
=\sum_dp_d\frac{(s-\alpha)_d}{s^d}
=\sum_dp_d\prod_{i=0}^{d-1}\{1-\epsilon(\alpha+i)\}.
\tag{4}
\]

At fixed \([v^e]\), all sums truncate.  Designate one fixed block of
weight one for \(h=0\), use the one-block formula of weight two for
\(h=1\), and use the two-block formula after its path pole cancels the
Lagrange Jacobian for \(h=2\).  The derivative form of Lagrange inversion
gives, with \(N=s-a\),

\[
H^{(a)}_{e,c}
=\frac{(N-1)!}{\rho!}[t^{N-1}u^e]e^{s\Phi}
 \{a e^{ut}V^\rho+\rho J V^{\rho-1}\},
\tag{5a}
\]

whereas the cancelled two-block formula is

\[
H^{(2,2)}_{e,c}
=\frac{(s-4)!}{\rho!}[t^{s-4}u^e]e^{s\Phi}
 \{4e^{ut}V^\rho+\rho J V^{\rho-1}\}.
\tag{5b}
\]

For \(h=0\), fix one unit block and regard it as distinguished of weight
one.  This is weight-preserving, so \(H_{0,e,c}=H^{(1)}_{e,c}\).  In
(5a), \(a=1\) and \(N=s-1\), hence its rank is \(N-1=s-2\).  This is
equivalent to the original rank-\((s-1)\) unmarked formula: that formula
uses \(J=\partial_tV\), whereas (5a) is the derivative Lagrange form.
Similarly, \(a=2\) gives rank \(s-3\) for \(h=1\), and (5b) has rank
\(s-4\).

For \(M=s-\alpha\), separating \(e^{st}\) gives exactly

\[
M![t^M]e^{st}P(t)
=s^M\sum_dp_d\frac{(s-\alpha)_d}{s^d}
=s^M\mathcal L_{\alpha,\epsilon}P.
\tag{5c}
\]

The substitution \(u=\epsilon v\) contributes \(s^e\).  Dividing
(5a)--(5b) by the powers of \(s\) and the marked weights \(1,2,4\) in
\(Q_h\) leaves \(s^{2\rho+2e}\), shift \(\alpha=h+2\), and Jacobian
coefficient \(2^{-h}\rho\).  Thus one obtains the single exact identity

\[
\boxed{
Q_{h,e,\rho+1}(s)
=\frac{s^{2\rho+2e}}{\rho!}[v^e]\,
\mathcal L_{h+2,\epsilon}
\left[
e^{(\Phi_\epsilon-t)/\epsilon}
\left{
e^{\epsilon vt}V_\epsilon^\rho
+2^{-h}\rho J_\epsilon V_\epsilon^{\rho-1}
\right}
\right].
}
\tag{5}
\]

For \(\rho=0\), the second summand is absent.  The coefficient ranks in
the three cases are respectively \(s-2,s-3,s-4\), explaining the shift
\(h+2\).  Division by the marked-block weights \(1,2,4\) explains the
coefficient \(2^{-h}\rho\).  This representation has a nonzero leading
integrand and avoids any hidden Laurent-order shift.

At \(\epsilon=0\),

\[
V_0=t-\frac{t^2}{2},\qquad J_0=1-t,qquad
e^{(\Phi_\epsilon-t)/\epsilon}\big|_{\epsilon=0}=e^{vt^2/2}.
\tag{6}
\]

At \(t=1\), the Jacobian summand vanishes, and (5) has leading coefficient

\[
\frac1{\rho!}[v^e]2^{-\rho}e^{v/2}=A_{e,c}.
\tag{7}
\]

## 3. Filtered proof

Factor out \(V_0^\rho e^{vt^2/2}\).  Direct expansion gives

\[
e^{(\Phi_\epsilon-t)/\epsilon}
=e^{vt^2/2}\sum_{j\ge0}\epsilon^jE_j(t,v),
\qquad \deg_vE_j\le2j,
\tag{8}
\]

and

\[
e^{\epsilon vt}V_\epsilon^\rho
=V_0^\rho\sum_{j\ge0}\epsilon^jP_j(t,v,\rho),
\qquad \deg_{v,\rho}P_j\le2j.
\tag{9}
\]

For (8), an order-\(r\) atom beyond \(vt^2/2\) has \(v\)-degree
\(r+1\); a product of total order \(j\) has at most \(j\) atoms.  For
(9), an order-\(r\) correction of \(V_\epsilon\) has \(v\)-degree
\(r\).  Choosing \(p\) corrected copies contributes \((\rho)_p\), and
\(p\le j\), so the combined degree is at most \(j+p\le2j\).

Split the marked term into \(J_\epsilon-J_0\) and \(J_0=1-t\).  After
the same factors are removed, the positive-order part
\(\rho(J_\epsilon-J_0)V_\epsilon^{\rho-1}\) has order-\(j\) degree at
most \(2j\): the explicit \(\rho\) costs one degree, but this part starts
at order one.  The \(J_0\) part has degree at most \(2j+1\), together with
an explicit factor \(1-t\).

The coefficient of \(\epsilon^i\) in (4) is

\[
(-1)^i e_i(\alpha,\alpha+1,\ldots,\alpha+d-1),
\tag{10}
\]

a polynomial in \(d\) of degree at most \(2i\).  Hence the order-\(i\)
part of \(\mathcal L\) is a polynomial in \(D=t\partial_t\), of order at
most \(2i\), evaluated at \(t=1\).  Each Euler derivative raises total
\((v,\rho)\)-degree by at most one: differentiating \(V_0^\rho\) supplies
at most one \(\rho\), and differentiating \(e^{vt^2/2}\) supplies at most
one \(v\).

Thus a regular integrand term of order \(j\), acted on by functional order
\(i\), has degree at most \(2j+2i\).  For the \(J_0\) term, evaluation at
\(t=1\) is zero unless at least one Euler derivative hits \(1-t\); at most
\(2i-1\) derivatives remain to raise parameter degree.  Its bound is

\[
(2j+1)+(2i-1)=2(i+j).
\tag{11}
\]

Summing over \(i+j=k\), the coefficient of \(\epsilon^k\) after applying
the functional is \(2^{-\rho}e^{v/2}\) times a polynomial in
\((v,\rho)\) of total degree at most \(2k\).  Finally,

\[
\frac{[v^e]v^m e^{v/2}}{[v^e]e^{v/2}}=2^m(e)_m,
\tag{12}
\]

which has degree \(m\) in \(e\).  Coefficient extraction therefore
preserves total degree, proving (2). \(\square\)

## 4. Second-symbol consequence

At \(k=2,3\), (2) gives \(\deg g_h\le4\) and \(\deg j_h\le6\).
The lattice \(e+\rho\le6\) in the exact \(q=6\) endpoint table is
therefore unisolvent, while its extra boundary \(e+\rho=7\) is a regression
check.  The endpoint formulas in `verify_second_symbol_theorem.py`, the
degree-four determinant kernel, and its Touchard collapse consequently
hold for every endpoint profile.  This closes the former conditional
all-\(q\) step in the second-symbol theorem.
