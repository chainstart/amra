# Exceptional-profile Abel lemma and denominator-aware certificate

Date: 2026-07-31

This note supplies the all-parameter step that was missing from the second
attack.  It deliberately separates two statements:

1. an ordinary-forest Abel lemma for a fixed exceptional profile;
2. a weaker, denominator-aware bound after nonbinary contractions.

The second statement, together with the 180 exact values in the executable
certificate, is what proves the 30 displayed hyperforest endpoint formulas.
It does not assume that those normalized endpoints are polynomials.

## 1. Weighted forests and exceptional profiles

For a positive block profile
\[
\mathbf w=(w_1,\ldots,w_b),\qquad
s=\sum_{i=1}^b w_i,
\]
write
\[
\mathcal F_c(\mathbf w)
=\sum_{\substack{F\text{ a forest on }[b]\\c(F)=c}}
\prod_{\{i,j\}\in E(F)}w_iw_j.
\tag{1}
\]
If \(I\subseteq[b]\) is one component, weighted Cayley gives
\[
\sum_{T\text{ a tree on }I}\prod_{\{i,j\}\in E(T)}w_iw_j
=
\left(\sum_{i\in I}w_i\right)^{|I|-2}
\prod_{i\in I}w_i,
\tag{2}
\]
with value \(1\) for a singleton.

Fix positive integers
\[
\mathbf v=(v_1,\ldots,v_p),\qquad
a=\sum_{i=1}^p v_i,
\]
and let
\[
\mathbf w_N=(1^N,v_1,\ldots,v_p),\qquad
s=N+a,\qquad b=N+p.
\tag{3}
\]
The exceptional-profile Abel lemma is
\[
\boxed{
\mathcal F_c(\mathbf w_N)
=\left(\prod_{i=1}^p v_i\right)
s^{\,b-2c}Q_{\mathbf v,c}(s),
\qquad
\deg Q_{\mathbf v,c}\le 2c-2.
}
\tag{4}
\]
The empty exceptional profile \(p=0\) is allowed, with empty product \(1\).

## 2. Exact component exponential generating functions

Let
\[
T=ze^T,\qquad U=T-\frac{T^2}{2},\qquad D=z\frac d{dz}.
\tag{5}
\]
Thus \(T\) and \(U\) are the EGFs of rooted and unrooted labelled trees.

Let \(J\subseteq[p]\) be nonempty, put
\[
p_J=|J|,\qquad a_J=\sum_{i\in J}v_i.
\]
A tree component containing precisely the exceptional blocks in \(J\) and
\(n\) unit blocks has weight
\[
\left(\prod_{i\in J}v_i\right)
(a_J+n)^{n+p_J-2}.
\tag{6}
\]
Lagrange inversion gives
\[
[z^n]e^{a_JT}
=\frac{a_J(a_J+n)^{n-1}}{n!}.
\tag{7}
\]
Since \(D\) multiplies the coefficient of \(z^n\) by \(n\), (6)--(7)
give the exact EGF
\[
\boxed{
A_J(z)
=\frac{\prod_{i\in J}v_i}{a_J}
(a_J+D)^{p_J-1}e^{a_JT}.
}
\tag{8}
\]
A component containing no exceptional block has EGF \(U\).

Partition the exceptional indices among the components.  The complete EGF
for \(c\)-component forests is therefore
\[
\boxed{
\frac{\mathcal F_c(\mathbf w_N)}{N!}
=[z^N]
\sum_{\substack{\pi\text{ a set partition of }[p]\\|\pi|\le c}}
\frac{U^{c-|\pi|}}{(c-|\pi|)!}
\prod_{J\in\pi}A_J(z).
}
\tag{9}
\]
There is no asymptotic or interpolation step in (9).

## 3. A self-contained marked Abel extraction

We record the algebra that turns (9) into (4).  This is the
denominator-aware part that was abbreviated in the earlier write-up.

For a constant \(x>0\), define rational functions
\[
r_{1,x}(t)=1,\qquad
r_{m+1,x}(t)
=\frac{(x+t\partial_t)r_{m,x}(t)}{1-t}.
\tag{10}
\]
Because
\[
D=\frac{T}{1-T}\partial_T,
\]
equation (8), after removing
\(\prod_{i\in J}v_i\,e^{a_JT}\), is
\[
\frac{r_{p_J,a_J}(T)}{a_J}.
\tag{11}
\]
After removing the common factor
\(\prod_i v_i\,e^{aT}\), denote the rational function in (9) by
\[
R_{\mathbf v,c}(t)
=
\sum_{\substack{\pi\vdash[p]\\|\pi|\le c}}
\frac{(t-t^2/2)^{c-|\pi|}}{(c-|\pi|)!}
\prod_{J\in\pi}\frac{r_{p_J,a_J}(t)}{a_J}.
\tag{12}
\]

Put \(N=s-a\) and define the coefficient functional
\[
\Lambda_{s,a}(f)
=N![t^N]e^{st}f(t).
\tag{13}
\]
Lagrange inversion in the form
\[
[z^N]F(T(z))
=[t^N](1-t)F(t)e^{Nt}
\tag{14}
\]
turns (9) into
\[
\frac{\mathcal F_c(\mathbf w_N)}{\prod_i v_i}
=\Lambda_{s,a}\bigl((1-t)R_{\mathbf v,c}(t)\bigr).
\tag{15}
\]

The key reduction identity is elementary.  Coefficient extraction gives
\[
\Lambda_{s,a}(tf')
=\Lambda_{s,a}\bigl((s(1-t)-a)f\bigr),
\]
and hence
\[
\boxed{
\Lambda_{s,a}\!\left(
tf'-(s(1-t)-a)f
\right)=0.
}
\tag{16}
\]
Thus poles at \(t=1\) can be removed without changing (15).  Explicitly,
if the current expression has leading Laurent term
\[
\frac{\gamma}{(1-t)^k},\qquad k\ge2,
\]
subtract
\[
\left[
t\partial_t-(s(1-t)-a)
\right]
\frac{\gamma}{(k-1)(1-t)^{k-1}}.
\tag{17}
\]
The pole order falls by one.  Repeating (17) is a finite canonical
reduction.

To make the degree bookkeeping explicit, put \(u=1-t\) and
\[
\mathscr D_{a,s}=t\partial_t-(su-a).
\]
For a Laurent coefficient \(\gamma(s)\) independent of \(u\), one
reduction step is the exact identity
\[
\begin{aligned}
\mathscr D_{a,s}
\left(
\frac{\gamma}{(k-1)u^{k-1}}
\right)
={}&
\frac{\gamma}{u^k}
+
\left(\frac{a}{k-1}-1\right)
\frac{\gamma}{u^{k-1}}\\
&-
\frac{s\gamma}{(k-1)u^{k-2}}.
\end{aligned}
\tag{17a}
\]
Thus cancelling a pole of order \(k\) creates only:

- a pole of order \(k-1\) with the same \(s\)-degree; and
- a pole of order \(k-2\) with one additional factor of \(s\).

Also
\[
U=t-\frac{t^2}{2}=\frac{1-u^2}{2}.
\tag{17b}
\]
Consequently adjoining one unmarked component changes the Laurent
filtration only by shifts \(0\) and \(2\), exactly matching the increase
\(c\mapsto c+1\).  Equations (17a)--(17b) are the two transitions used in
the induction below; there are no hidden analytic estimates.

For completeness, here is the degree ledger for this reduction.  It is
often called the marked Abel--Rényi convolution lemma.

> **Marked Abel--Rényi lemma.**  Apply (17) to
> \((1-t)R_{\mathbf v,c}(t)\).  No simple pole remains.  If the polynomial
> remainder is
> \[
> \rho_{\mathbf v,c}(t,s)=\sum_d q_d(s)t^d,
> \tag{18}
> \]
> then, for \(p\ge2\),
> \[
> s^{\,2c-p-d}q_d(s)\in\mathbb Q(\mathbf v)[s],
> \qquad
> \deg_s\!\left(s^{\,2c-p-d}q_d(s)\right)
> \le 2c-2-d.
> \tag{19}
> \]
> For every \(p\ge0\), including the two elementary boundary cases treated
> below,
> \[
> s^{2c-p}
> \sum_d q_d(s)(s-a)_d s^{-d}
> \tag{20}
> \]
> is a polynomial of degree at most \(2c-2\).

Here is a direct induction proof.  Choose the least exceptional index
\(i_0\).  The component containing it gives the exact recursion
\[
R_{P,c}
=\sum_{\substack{J\subseteq P\\i_0\in J}}
\frac{r_{|J|,a_J}}{a_J}\,
R_{P\setminus J,c-1},
\tag{21}
\]
with
\[
R_{\varnothing,c}=\frac{(t-t^2/2)^c}{c!},
\qquad
R_{\varnothing,0}=1.
\tag{22}
\]
Equations (10), (17a)--(17b), and the product rule are the full induction.
Filter a Laurent monomial \(q_d(s)t^du^{-k}\) by the two requirements
\[
\deg q_d\le p-2,\qquad
\operatorname{ord}_s q_d\ge\max(0,p-2c+d).
\tag{22a}
\]
The first lower-pole term in (17a) preserves both indices; the second
lowers the pole by two while raising the \(s\)-degree and
\(s\)-valuation by one.  Multiplication by either term of (17b) changes
the component index by one and the Laurent index by respectively zero or
two.  Hence both transitions preserve (22a).  The remaining operations
are:

1. the numerator \(x+t\partial_t\) in (10) either contributes one factor
   of \(s\), by (16), or differentiates a factor already present;
2. its denominator \(1-t\) is removed by one application of (17);
3. multiplication by \(t-t^2/2\), corresponding to one new unmarked
   component, increases the available \(t\)-degree by at most two and
   changes \(2c-p\) by exactly two;
4. in (21), the terms in which the distinguished exceptional index joins
   each possible block are all present.  Their simple-pole residues are
   the product-rule sum
   \[
   (a+t\partial_t)\prod_J r_{|J|,a_J}
   -\sum_J
   (a_J+t\partial_t)r_{|J|,a_J}
   \prod_{K\ne J}r_{|K|,a_K}=0,
   \tag{23}
   \]
   so the reduction never stops at a simple pole.

Start with (22).  For \(p=0\), (14) gives
\[
\frac{N!}{c!}[t^N](1-t)(t-t^2/2)^ce^{Nt}.
\tag{24}
\]
After extracting \(N^{N-2c}\), the possible degree is \(2c\).
The degree-\(2c\) term vanishes because the polynomial multiplying the
exponential vanishes at \(t=1\); the degree-\((2c-1)\) term vanishes
because its second derivative at \(t=1\) is zero
(\(U'(1)=0\)).  Thus the degree is at most \(2c-2\).

For \(p=1\), the complete forest EGF before the common exponential is
\[
\frac{U^{c-1}}{a(c-1)!}.
\]
The same calculation has degree at most \(2c-1\), and its leading term
vanishes because \((1-t)U^{c-1}\) vanishes at \(1\).  It is therefore at
most \(2c-2\).

For \(p\ge2\), assume (19) for the smaller pairs in (21).  Steps 1--3
preserve
\[
\deg q_d\le p-2,\qquad
s^{\max(0,p-2c+d)}\mid q_d;
\tag{25}
\]
this is (22a) after all poles of order at least two have been eliminated.
Step 4 removes the only possible simple-pole obstruction.  Equation
(17a) shows that no other pole order or \(s\)-degree transition exists.
These two relations are precisely (19), completing the induction.
Notice that the induction uses all terms of the set-partition recursion;
applying it to only selected exceptional-component placements would not
prove (23).

Finally, for a polynomial remainder,
\[
\Lambda_{s,a}(t^d)
=(s-a)_d\,s^{N-d}.
\tag{26}
\]
Substituting (18)--(20) into (15) proves (4), including the bound
\(\deg Q_{\mathbf v,c}\le2c-2\).

## 4. Nonbinary contractions and the denominator bound

Fix an ordered list of \(m\) nonbinary contractions of arities
\(r_1,\ldots,r_m\), and let
\[
e=\sum_{i=1}^m(r_i-2).
\tag{27}
\]
Every contraction has positive excess, so \(m\le e\).  Starting from
\[
(2^h,1^{s-2h}),
\]
the contracted profile has
\[
b'=s-h-e-m
\tag{28}
\]
blocks.

Classify a contraction record by its finite incidence type \(\tau\):
which old exceptional blocks it uses, which later hyperedges meet earlier
ones, and which slots are occupied by previously untouched unit blocks.
If \(\nu_\tau\) untouched units occur, the embedding multiplicity is a
falling-factorial polynomial \(E_\tau(s)\) with
\[
\deg E_\tau=\nu_\tau
\le\sum_i r_i=e+2m.
\tag{29}
\]
This remains exact below the stable range: if fewer than \(\nu_\tau\)
unit blocks are available, the relevant falling factorial is zero.  Thus
the incidence classification is one algebraic identity, not a separate
case split for every small \(s\).
Once \(\tau\) is fixed, all exceptional weights in the contracted profile
are constants.  Applying (4) to that profile and comparing with
\(s^{s-h-2c-e}\) shows that its normalized contribution has the form
\[
\frac{E_\tau(s)Q_{\tau,c}(s)}{s^m},
\qquad
\deg Q_{\tau,c}\le2c-2.
\tag{30}
\]
The ordering factor \(1/m!\) is constant and changes no bound.

Taking the common denominator \(s^e\) over \(m\le e\), (29)--(30) give
\[
\boxed{
\frac{H_{h,e,c}}
{2^h s^{s-h-2c-e}}
=\frac{N_{h,e,c}(s)}{s^e},
\qquad
\deg N_{h,e,c}\le2c+3e-2.
}
\tag{31}
\]
Indeed, a type with \(m\) contractions contributes numerator degree at
most
\[
(e+2m)+(2c-2)+(e-m)
\le2c+3e-2.
\tag{32}
\]
This is weaker than asserting in advance that the left side of (31) is a
polynomial.  It is also exactly the bound needed for an honest finite
certificate.

## 5. Why 180 values prove the 30 displayed identities

Let \(P_{h,e,c}(s)\) be a displayed table entry.  Its degree is at most
\(2c+2e-2\).  After multiplying the proposed identity by \(s^e\), both
sides have degree at most
\[
D_{e,c}=2c+3e-2.
\tag{33}
\]
Therefore equality at
\[
D_{e,c}+1=2c+3e-1
\tag{34}
\]
distinct positive values proves the identity.

For each \(h=0,1,2\), the required endpoint pairs are
\[
(e,c)=(0,1\ldots4),(1,1\ldots3),(2,1\ldots2),(3,1).
\]
The number of values is
\[
3\left[
\sum_{c=1}^4(2c-1)
+\sum_{c=1}^3(2c+2)
+\sum_{c=1}^2(2c+5)
+10
\right]
=180.
\tag{35}
\]
They are checked at consecutive values starting at \(s=7\); the largest is
\(s=16\).  Thus the three \(e=3,c=1\) identities receive the one value that
was missing from the old strong-degree interpolation.

Two implementations now check all 180 values:

- `verify_second_deficit.py`, using aggregated contraction and weighted
  component sums;
- `audit_second_raw_enum.py`, using direct block positions and primitive
  chains and importing neither campaign verifier.

Consequently the 30 table identities, and hence all five coefficients of
\(B_{2s-7}\), are proved without assuming the stronger polynomial endpoint
lemma.

## 6. Scope

The proof concerns complete weighted profiles with finitely many fixed
exceptional blocks and the complete-split pooled model.  It does not
establish positivity at arbitrary pooled depth and makes no
arbitrary-host claim.
