# #679: polynomial-level Selberg denominator barrier in the ultra-small-tilt window

Date: 2026-07-22

This note tests whether the stronger complete-period moment from
ultrasmall_tilt_window.md can be transferred by a conventional
polynomial-level upper-bound sieve. It cannot: even the optimistic
soft-density Selberg denominator has exponentially too little mass. This is
a barrier for that interface, not a barrier to signed phase cancellation.

## 1. Parameters and the canonical denominator

Keep

\[
 H=e^{B L_2+o(1)},\qquad 2\le B=o(L_3),
 \qquad L=\sum_{H<p\le z}{1\over p}\sim L_2,
\]

where \(B\) may be fixed (in particular \(B=2\)) or moving, and let
\(a=C L_1/(HL)\). For an integer moment \(q\ge1\), put

\[
 b=1-(1-a)^q,
\]

and assume \(qa=o(1)\). Then

\[
 \kappa_q:=bH=qC{L_1\over L}\{1+o(1)\}.
\]

The most favourable conventional soft local density is

\[
 g_q(p)={\kappa_q\over p-\kappa_q}.
\]

At a polynomial sieve level \(D=X^\theta\), with fixed \(\theta>0\), its
Selberg denominator would be

\[
 G_q(D)=
 \sum_{\substack{d\le D\\d\ \mathrm{squarefree}\\
                  p\mid d\Rightarrow H<p\le z}}
 \prod_{p\mid d}g_q(p).                                \tag{1}
\]

Calling (1) “most favourable” does not assert that the fractional soft
weight automatically satisfies a hard-sieve theorem with this denominator.
The point is stronger for route triage: even granting this canonical
effective-density denominator, its level budget cannot reproduce the moment
gain.

## 2. A uniform upper bound for its mass

Because \(qa=o(1)\), eventually \(\kappa_q=o(H)\). Since every selected
prime exceeds \(H\),

\[
 g_q(p)\le {2\kappa_q\over p},\qquad
 S_q:=\sum_{H<p\le z}g_q(p)\le 2\kappa_qL
      =(2+o(1))qC L_1.                                 \tag{2}
\]

Every \(d\le D\) in (1) has

\[
 \omega(d)\le J:=\left\lfloor{\log D\over\log H}\right\rfloor
 \le (\theta+o(1)){L_1\over B L_2}.                    \tag{3}
\]

Dropping the product constraint inside each fixed degree and using the
elementary-symmetric-polynomial bound gives

\[
 G_q(D)\le\sum_{j\le J}{S_q^j\over j!}.
\]

Here \(S_q/J\gg qB L_2\to\infty\), so Stirling (or
\(j!\ge(j/e)^j\)) gives

\[
 \log G_q(D)
 \le O\!\left(J\log{eS_q\over J}\right)
 \le (\theta+o(1)){L_1\over B L_2}
       \log\{O(qB L_2)\}.                              \tag{4}
\]

On the other hand the complete-period \(q\)-moment gain is

\[
 E_q=(qC+o(q))L_1.                                    \tag{5}
\]

Uniformly for every \(q\ge1\) in the admissible range,

\[
 {\log G_q(D)\over E_q}
 \ll_\theta {\log\{O(qB L_2)\}\over qCBL_2}=o(1).      \tag{6}
\]

For the uniformity, the function \(q^{-1}\log(Aq)\) is decreasing for
\(q\ge1\) once \(A\to\infty\), so the worst case in (6) is \(q=1\).
Thus growing the moment does not repair the level deficit: it multiplies
the target exponent essentially linearly in \(q\), while a modulus
\(d\le X^\theta\) can contain only \(O(L_1/(BL_2))\) selected primes.

## 3. Consequence and scope

Equations (4)--(6) prove the strict comparison

\[
 \boxed{G_q(X^\theta)=\exp\{o(E_q)\}}
\]

for every fixed polynomial level and every admissible moment. In
particular, at fixed \(q\), \(G_q(X^\theta)=X^{o(1)}\), whereas the desired
complete-period saving is \(X^{-qC+o(1)}\). A standard upper-bound-sieve
output whose decisive gain is \(G_q(D)^{-1}\) therefore cannot transfer the
ultra-small-tilt estimate.

This does **not** rule out:

* cancellation among signed conductor layers;
* bilinear control of the stopping-line frontier and its free suffix;
* an interval theorem using more than a polynomial distribution level; or
* a structural argument not mediated by a Selberg denominator.

It does make the earlier “fundamental lemma is in the wrong dimension
regime” audit quantitative and uniform in the growing Markov moment.

## 4. Literature sanity check

The apparently relevant 2026 preprint by Olivier Ramaré, *The weighted
large sieve through Parseval*, arXiv:2605.29470, cannot be used: the current
arXiv record says that the paper was withdrawn on 2026-06-04 after an
“Important miscalculation” was discovered, and no current PDF is supplied.
No claim from its withdrawn first version is used above.

Strict status: **polynomial-level Selberg/large-sieve route excluded in this
parameter window; interval transfer and original #679 remain open**.
