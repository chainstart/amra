# The third active base-four Newton layer is positive for every \(k\)

Date: 2026-07-30

## 1. Statement

Retain the definitions
\[
C_k(s)=[x^k]\bigl(\Phi_1(x)^2-\Phi_0(x)\Phi_2(x)\bigr),
\qquad
c_k(s)=\frac{(k-2)!}{2}C_k(s),
\]
and
\[
c_k(s)=\sum_q a_{k,q}\binom{s-4}{q},
\qquad
q_0=\left\lfloor\frac{k-2}{2}\right\rfloor.
\]

### Theorem

For every \(k\ge3\),
\[
\boxed{a_{k,q_0+2}>0.}                               \tag{1}
\]

The coefficient has the following exact parity-dependent forms.  Define
\[
P_5(x)=x^3+12x^2+20x-225,
\]
\[
P_7(x)=x^6+25x^5+229x^4+211x^3
       -10101x^2-36081x+183330,
\]
\[
Q_6(x)=x^5+16x^4+52x^3-587x^2-3063x+12240,
\]
and
\[
\begin{aligned}
P_8(x)={}&x^8+29x^7+321x^6+459x^5-23239x^4\\
         &-161291x^3+565356x^2+5972364x-18174240.
\end{aligned}
\]

If \(k\) is odd, put \(n=(k+9)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+2}
={}&\frac{(k-2)!}{2}(n-4)(n-5)
\Bigl[
\frac{P_7(n)}6n^{2n-16}\\
&\quad-2P_5(n-1)(n-1)^{2n-14}
+2(n-2)^{2n-12}
\Bigr].
\end{aligned}}                                       \tag{2}
\]

If \(k\) is even, put \(n=(k+10)/2\).  Then
\[
\boxed{
\begin{aligned}
a_{k,q_0+2}
={}&\frac{(k-2)!}{2}(n-4)(n-5)
\Bigl[
\frac{P_8(n)}{30}n^{2n-18}\\
&\quad-\frac23Q_6(n-1)(n-1)^{2n-16}\\
&\quad+2(n^2-28)(n-2)^{2n-14}
\Bigr].
\end{aligned}}                                       \tag{3}
\]

Negative exponents in the finitely many smallest cases have their usual
rational meaning; the complete expressions are integers.  For \(k=2\),
\(c_2(s)=1\), so a third active layer does not exist.

## 2. A unified component-total generating function

Let
\[
F_h^{(n)}(y)=\sum_{c\ge1}W_{h,c}(n)y^c,
\qquad
A^{(n)}(y)=\sum_{c\ge1}A_c(n)y^c,
\]
where \(A_c(n)\) counts a prescribed adjacent edge pair.  Let \(T(z)\)
be the rooted-tree EGF, \(T=ze^T\), and put
\[
U(z)=T(z)-\frac{T(z)^2}{2}.
\]
The exponential formula gives the three uniform representations
\[
F_0^{(n)}(y)
=n![z^n]e^{yU(z)},                                    \tag{4}
\]
\[
F_1^{(n)}(y)
=(n-2)![z^{n-2}]\,y e^{2T(z)}e^{yU(z)},               \tag{5}
\]
\[
A^{(n)}(y)
=(n-3)![z^{n-3}]\,y e^{3T(z)}e^{yU(z)}.               \tag{6}
\]
For example, deleting a prescribed edge splits its special tree
component into two rooted trees, which accounts for \(e^{2T}\).
Contracting an adjacent prescribed pair gives a weight-\(3\) marked
vertex, and the generalized rooted-tree identity gives \(e^{3T}\).

Let \(\vartheta=y\,d/dy\).  Edge incidence and the adjacent/disjoint
pair-orbit identity give
\[
F_1^{(n)}
=\frac{2}{n(n-1)}(n-\vartheta)F_0^{(n)},              \tag{7}
\]
\[
F_2^{(n)}
=\frac{
\frac12(n-\vartheta)(n-\vartheta-1)F_0^{(n)}
-N_{\rm adj}A^{(n)}
}{N_{\rm dis}},                                       \tag{8}
\]
where
\[
N_{\rm adj}=\frac{n(n-1)(n-2)}2,\qquad
N_{\rm dis}=\frac{n(n-1)(n-2)(n-3)}8.
\]

Consequently every component-total determinant is generated at once by
\[
\boxed{
\mathscr C_n(y)
=F_1^{(n)}(y)^2-F_0^{(n)}(y)F_2^{(n)}(y),
\qquad
\mathcal C_t(n)=[y^t]\mathscr C_n(y).
}                                                       \tag{9}
\]
This is the promised uniform mechanism.  The earlier layers
\(\mathcal C_3,\ldots,\mathcal C_6\) and the new layers below are
coefficients of the same polynomial (9), rather than separate counting
ansätze.

## 3. Exact component-total layers seven and eight

Lagrange inversion in (4) and (6) gives, for every fixed \(c\),
\[
W_{0,c}(n)
=n^{n-c-1}(n-1)!
\sum_{r=0}^{\min(c-1,n-c)}
\frac{(-1/(2n))^r(c+r)}
 {r!(c-r-1)!(n-c-r)!},                               \tag{10}
\]
\[
A_c(n)
=\sum_{r=0}^{c-1}
\frac{(-1)^r(c+r+2)(n-3)!n^{n-c-r-3}}
 {2^rr!(c-r-1)!(n-c-r-2)!},                          \tag{11}
\]
with out-of-range factorial terms interpreted as zero.  Equations
(7)--(8) then determine \(W_{1,c}\) and \(W_{2,c}\).

Substitute (10)--(11) into
\[
\mathcal C_t(n)
=\sum_{c=1}^{t-1}
\left(W_{1,c}W_{1,t-c}-W_{0,c}W_{2,t-c}\right).       \tag{12}
\]
Collecting powers of \(n\) gives the polynomial identities
\[
\boxed{
\mathcal C_7(n)
=\frac{(n-4)(n-5)}6P_7(n)n^{2n-16},
}                                                       \tag{13}
\]
\[
\boxed{
\mathcal C_8(n)
=\frac{(n-4)(n-5)}{30}P_8(n)n^{2n-18}.
}                                                       \tag{14}
\]
These are finite algebraic consequences of (10)--(12).  Equivalently,
after removing the displayed factors, the two identities reduce to
\[
\frac{6n^{16-2n}\mathcal C_7(n)}{(n-4)(n-5)}=P_7(n),
\qquad
\frac{30n^{18-2n}\mathcal C_8(n)}{(n-4)(n-5)}=P_8(n),
\]
so they can be checked coefficient by coefficient as degree-six and
degree-eight polynomial identities.

## 4. Passage to the third Newton layer

Put \(n_0=4+q_0\).  Since every evaluation below \(n_0\) vanishes, the
\((q_0+2)\)-nd forward difference has only its last three terms:
\[
\begin{aligned}
a_{k,q_0+2}
=\frac{(k-2)!}{2}\Bigl[
&C_k(n_0+2)-(q_0+2)C_k(n_0+1)\\
&+\binom{q_0+2}{2}C_k(n_0)
\Bigr].                                               \tag{15}
\end{aligned}
\]
The plus sign in the third term is essential.

For odd \(k\), set \(n=n_0+2=(k+9)/2\).  Then
\[
q_0+2=n-4,
\]
and the three component totals are \(7,5,3\).  Inserting
\(\mathcal C_7(n)\), \(\mathcal C_5(n-1)\), and
\(\mathcal C_3(n-2)\) into (15) yields (2).

For even \(k\), set \(n=n_0+2=(k+10)/2\).  The component totals are
\(8,6,4\).  Here
\[
(n-2)^2+4(n-2)-24=n^2-28,
\]
and substitution of
\(\mathcal C_8(n)\), \(\mathcal C_6(n-1)\), and
\(\mathcal C_4(n-2)\) gives (3).

## 5. Human all-\(k\) positivity proof

### Odd \(k\)

First handle \(n=6,7\), corresponding to \(k=3,5\), by direct
substitution in (2):
\[
a_{3,2}=2,\qquad a_{5,3}=17832.                       \tag{16}
\]

Now let \(n\ge8\), put \(E=2n-16\), and set
\[
S(n)=P_5(n-1).
\]
Writing \(n=m+8\) shows
\[
S(n)=m^3+33m^2+335m+846>0.
\]
The first two terms in the bracket of (2) equal
\[
n^E\left[
\frac{P_7(n)}6
-2S(n)(n-1)^2
\left(1-\frac1n\right)^E
\right].
\]
Since \(E\ge0\) and the ratio is at most \(1\), this is bounded below by
\[
\frac{n^E}{6}
\left(P_7(n)-12P_5(n-1)(n-1)^2\right).               \tag{17}
\]
With \(n=m+8\), the polynomial in parentheses is
\[
\begin{aligned}
{}&m^6+61m^5+1625m^4+23627m^3\\
&\qquad+186503m^2+681307m+878130,
\end{aligned}
\]
which is strictly positive.  The final term
\(2(n-2)^{2n-12}\) in (2) is also positive.  This proves the odd case.

### Even \(k\)

The two cases below the stable exponent range are
\[
a_{4,3}=144,\qquad a_{6,4}=1864344.                  \tag{18}
\]

For \(n\ge9\), put \(E=2n-18\) and \(T(n)=Q_6(n-1)\).  With
\(n=m+9\),
\[
T(n)
=m^5+56m^4+1204m^3+11925m^2+50777m+75096>0.
\]
The first two terms in (3), after factoring \(n^E\), are bounded below
by
\[
\frac{n^E}{30}
\left(P_8(n)-20Q_6(n-1)(n-1)^2\right).               \tag{19}
\]
At \(n=m+9\), the remaining polynomial is
\[
\begin{aligned}
{}&m^8+81m^7+2976m^6+64666m^5+891176m^4\\
&\quad+7647574m^3+37680299m^2\\
&\quad+95096999m+94644648,
\end{aligned}
\]
again strictly positive.  Finally \(n^2-28>0\), so the third term of
(3) is positive.  This proves the even case and hence (1).

## 6. Human proof versus computation

The proof of (1) consists of:

1. the EGF identities (4)--(6);
2. the two edge-orbit identities (7)--(8);
3. Lagrange inversion (10)--(11);
4. the finite polynomial identities (13)--(14);
5. the exact forward difference (15); and
6. the positive-coefficient shifts in (17) and (19).

No finite regression is a premise of the all-\(k\) sign proof.

The companion verifier has two separate audit roles:

- SymPy reconstructs (13)--(14) from (10)--(12) and checks the two
  shifted gap polynomials coefficient by coefficient.
- The previously independent complete-edge-subset enumerator checks
  the genuinely small complete graphs:
  \[
  (c_3(4),c_3(5),c_3(6))=(2,12,24),
  \]
  \[
  (c_4(4),c_4(5),c_4(6),c_4(7))=(0,84,462,1278).
  \]
  Their second and third forward differences are \(2\) and \(144\).

An additional exact-integer regression checks (2)--(3) for
\(3\le k\le100\).  This catches transcription errors but is not used
to infer positivity.

Reproduction:

```bash
cd data/research_open/opg_erdos_eight_hour_campaign_2026-07-30/opg1757/third_layer_2026-07-30
pytest -q test_verify_third_active_newton.py
python3 verify_third_active_newton.py
```
