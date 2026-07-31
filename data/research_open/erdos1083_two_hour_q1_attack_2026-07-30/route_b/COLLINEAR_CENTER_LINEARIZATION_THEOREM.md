# Erdős #1083 Route B, stage 4: collinear-centre linearization

Date: 2026-07-30

## 0. Outcome

For one fixed signed centre coordinate \(A\), the reverse circles are
not a general two-parameter family of circles.  Their centres are
collinear:
\[
C:\qquad (u-A)^2+(z-w)^2=\rho^2.
\]
The two-to-one parabolic lift
\[
\Phi_A(u,z)
=
\bigl(z,(u-A)^2+z^2\bigr)
\tag{1}
\]
turns every such circle into the line
\[
Y=2wZ+(\rho^2-w^2).
\tag{2}
\]
Consequently, for any finite collection \(\mathcal C_A\) of distinct
positive-radius circles with signed centre coordinate \(A\),
\[
\boxed{
I(P_\alpha,\mathcal C_A)
\ll
Q^{2/3}|\mathcal C_A|^{2/3}+Q+|\mathcal C_A|.
}
\tag{3}
\]

After summing over \(R\) signed values of \(A\), this becomes
\[
\boxed{
I(P_\alpha,\mathcal C)
\ll
Q^{2/3}R^{1/3}N^{2/3}+RQ+N,
}
\tag{4}
\]
where \(N=|\mathcal C|\).

Combining (4) with the tangent--label rich-line encoding, a second
dyadic decomposition by the number of circles over a signed
parameter line, and the global target-point capacity gives
\[
\boxed{
\kappa<\frac29
\quad\Longrightarrow\quad
\text{the Euclidean hub branch is impossible}.
}
\tag{5}
\]
This improves the previous Route B threshold \(9/41\), since
\[
\frac29-\frac9{41}=\frac1{369}.
\]

Thus, for every fixed \(\varepsilon>0\), the matching-or-hub theorem
now yields a matching of
\[
\boxed{t^{\,2/9-\varepsilon-o(1)}}
\]
rich axial-plane pairs for each of \(t^{1-o(1)}\) selected labels.
This remains a structural matching result.  No implication improving
the global \(3/5\) distinct-distance exponent is claimed.

## 1. Inherited setup

Use the setup and removals of
`TANGENT_LABEL_RICH_LINE_HUB_THEOREM.md`.  In particular:

- \(P_\alpha\) is a fixed source-plane set with
  \(|P_\alpha|\le Q\);
- every retained reverse circle has positive radius and is normalized;
- equal normalized circles are merged;
- \(A(C)\ne0\) is the signed radial coordinate of the centre;
- \(s(C)=|P_\alpha\cap C|\);
- \(\mu(C)\) is the number of producing target triples;
- \(\mu(C)\le M\);
- the selected squared-label set has size \(L\);
- the retained target union has at most \(MQ\) points;
- every circle has parameter line
  \[
  d=\rho(C)^2+A(C)^2\tau
  \]
  in \(\mathcal T_\alpha\times\mathcal D_0\), and
  \(\mu(C)\le2r(\ell_C)\).

At power scale,
\[
\begin{aligned}
M&=t^{1+o(1)},&
Q&=t^{3+o(1)},\\
L&=t^{2-2\kappa+o(1)},&
W&\ge t^{7-3\kappa-o(1)}.
\end{aligned}
\tag{6}
\]

## 2. Exact fixed-\(A\) linearization

### Lemma 1

Fix \(A\in\mathbb R\).  Define
\[
\Phi_A:P_\alpha\longrightarrow\mathbb R^2,
\qquad
\Phi_A(u,z)=(Z,Y)
=\bigl(z,(u-A)^2+z^2\bigr).
\tag{7}
\]
Every fibre of \(\Phi_A\) has cardinality at most two.

For a circle \(C\) with centre \((A,w)\) and radius \(\rho>0\), define
\[
\lambda_C:\qquad
Y=2wZ+(\rho^2-w^2).
\tag{8}
\]
Then
\[
p\in C\quad\Longrightarrow\quad \Phi_A(p)\in\lambda_C,
\tag{9}
\]
and distinct normalized circles with signed centre coordinate \(A\)
give distinct lines.

#### Proof

If \(\Phi_A(u_1,z_1)=\Phi_A(u_2,z_2)\), then \(z_1=z_2\) and
\[
(u_1-A)^2=(u_2-A)^2.
\]
There are at most two possible values of \(u\), proving the fibre
claim.

The circle equation expands as
\[
(u-A)^2+z^2=2wz+(\rho^2-w^2),
\]
which is exactly (9).  Finally, equality of the lines in (8) first
gives equality of their slopes, hence equality of \(w\), and then
equality of \(\rho^2\).  Positive radii give equality of \(\rho\), so
the circles are equal. \(\square\)

### Corollary 2

Let \(P'_A=\Phi_A(P_\alpha)\), and let
\(\Lambda_A=\{\lambda_C:C\in\mathcal C_A\}\).  Lemma 1 gives
\[
I(P_\alpha,\mathcal C_A)
\le2I(P'_A,\Lambda_A).
\]
Since \(|P'_A|\le Q\) and
\(|\Lambda_A|=|\mathcal C_A|\), the real
Szemerédi--Trotter theorem proves (3).

For distinct signed values of \(A\), apply (3) separately.  If
\(N_A=|\mathcal C_A|\), then Hölder gives
\[
\sum_A N_A^{2/3}
\le R^{1/3}\left(\sum_A N_A\right)^{2/3}.
\]
This proves (4).  The values \(A\) and \(-A\) must be separated
because their lifts (7) differ.  This costs no exponent.

## 3. A simultaneous strengthening of the label-service cap

The fixed-\(A\) service theorem from
`NINE_FORTY_ONE_NEXT_ATTACK.md` can also be sharpened.

### Lemma 3

Let \(\mathcal C_A\) be a collection of circles with fixed signed
centre coordinate \(A\), let
\[
K_A
=
\bigl|\{\rho(C)^2:C\in\mathcal C_A\}\bigr|,
\]
and let \(X_A\) be the target points used by these circles.  Then
\[
\boxed{
\sum_{C\in\mathcal C_A}\mu(C)
\le
\min\{L,K_A\}|X_A|.
}
\tag{10}
\]

#### Proof

For \(q=(A,y,w)\), a fixed label \(d\) determines the squared radius
\[
b=d-y^2
\]
and therefore at most one circle.  Since an off-axis target point
belongs to a unique axial target plane, the producing triple is also
unique.  This gives the \(L|X_A|\) bound.

Independently, a fixed represented squared radius \(b\) and the point
\(q\) determine the centre \((A,w)\) and radius \(\sqrt b\), hence at
most one normalized positive-radius circle.  The label is then
uniquely \(d=b+y^2\), so again there is at most one producing triple.
This gives the \(K_A|X_A|\) bound.  Take the minimum. \(\square\)

The \(K_A\) side records a constraint that label cardinality alone
misses.  In a uniform signed-slope layer with \(t^j\) parameter lines,
\(t^h\) circles per line, circle multiplicity \(t^m\), and
\(|X_A|=t^x\), (10) gives
\[
j+h+m\le\min\{\ell,j\}+x.
\tag{11}
\]

## 4. Secondary dyadic line fibres

Choose a mass-carrying dyadic circle layer
\[
s\le s(C)<2s,\qquad
u\le\mu(C)<2u.
\]
Because every circle in this layer has comparable weight, a further
dyadic decomposition by
\[
\nu(A,b)
=
\#\{C:A(C)=A,\ \rho(C)^2=b\}
\tag{12}
\]
produces a subcollection losing only \(t^{o(1)}\) of the mass in
which
\[
\nu(A,b)=t^{h+o(1)}
\]
on every represented signed parameter line \((A,b)\).

Write
\[
\begin{aligned}
s&=t^{a+o(1)},&
u&=t^{m+o(1)},\\
N&=t^{b+o(1)},&
K&=t^{c+o(1)},&
R&=t^{r+o(1)}.
\end{aligned}
\tag{13}
\]
Here \(N\) is the number of retained circles, \(K\) is the number of
signed line copies \((A,b)\), and \(R\) is the number of represented
signed values of \(A\).  Then
\[
b=c+h.
\tag{14}
\]

The old point--circle analysis remains valid after this
polylogarithmic loss.  For \(\kappa<2/9\), its \(6/11,9/11\) term is
the only possible mass-carrying term, so
\[
11a+2b\le18+o(1).
\tag{15}
\]
The layer mass and total-triple capacity give
\[
\begin{aligned}
a+b+m&\ge7-3\kappa-o(1),\\
b+m&\le6-2\kappa+o(1).
\end{aligned}
\tag{16}
\]
Consequently,
\[
\boxed{
a\ge1-\kappa-o(1),\qquad
a\le\frac{4+6\kappa+2m}{9}+o(1),\qquad
m\ge\frac{5-15\kappa}{2}-o(1).
}
\tag{17}
\]

The signed copies \((A,b)\) map at most two-to-one to geometric
tangent--label lines, because only \(A\) and \(-A\) have the same
squared slope.  Every represented line is \(u/2\)-rich.  Equation
(17) gives \(m>5/6-o(1)\) for \(\kappa<2/9\), so \(u\to\infty\) and
the rich-line estimate applies.  Since \(m\le1+o(1)\), the cubic
rich-line exponent exceeds the linear exponent by
\[
(6-4\kappa-3m)-(3-2\kappa-m)
=3-2\kappa-2m
>\frac59-o(1).
\]
Thus the cubic term dominates:
\[
\boxed{
c\le6-4\kappa-3m+o(1).
}
\tag{18}
\]

For one signed line \((A,b)\), its \(t^{h+o(1)}\) circles have
different centre heights.  Their producing triples use
\(t^{h+m+o(1)}\) distinct target points in the plane \(x=A\).
Indeed, within one circle the off-axis point determines its target
plane and \(b+y^2\) determines its label, while points from different
circles have different height coordinate \(w\).
Choose one represented signed line for every represented \(A\).
The resulting target subsets lie in disjoint planes, so the global
target capacity \(MQ=t^{4+o(1)}\) gives
\[
\boxed{
r+h+m\le4+o(1).
}
\tag{19}
\]
Using (14) and (18),
\[
\boxed{
r\le10-4\kappa-b-4m+o(1).
}
\tag{20}
\]

This is also the one-line consequence of the \(K_A\) side of
Lemma 3, summed across the signed \(A\)-fibres.

## 5. Hub exclusion up to \(2/9\)

The source incidence of the secondary layer is
\[
I(P_\alpha,\mathcal C)=t^{a+b+o(1)}.
\]
Apply (4).  At exponent scale, one of the following three terms would
have to carry:
\[
2+\frac r3+\frac{2b}{3},
\qquad
3+r,
\qquad
b.
\tag{21}
\]

The last term cannot carry because (17) gives \(a>0\).

If the middle term carried, then
\[
a+b\le3+r+o(1).
\]
Combining this with (20) and the first inequality of (16) gives
\[
a\ge2m+1-2\kappa-o(1).
\tag{22}
\]
The upper bound for \(a\) in (17) would then imply
\[
m\le\frac{24\kappa-5}{16}+o(1).
\tag{23}
\]
For \(\kappa<2/9\), the right side is below \(1/48+o(1)\), whereas
(17) gives \(m>5/6-o(1)\).  Thus the middle term cannot carry.

The first term must therefore carry:
\[
3a+b\le6+r+o(1).
\tag{24}
\]
Insert (20):
\[
3a+2b+4m\le16-4\kappa+o(1).
\]
The mass inequality in (16) then gives
\[
\boxed{
a+2m\le2+2\kappa+o(1).
}
\tag{25}
\]
Using \(a\ge1-\kappa-o(1)\),
\[
\boxed{
m\le\frac{1+3\kappa}{2}+o(1).
}
\tag{26}
\]
Together with the lower bound for \(m\) in (17), a surviving hub
would require
\[
\frac{5-15\kappa}{2}
\le
\frac{1+3\kappa}{2}+o(1).
\]
The two sides cross exactly at
\[
\boxed{\kappa=\frac29.}
\tag{27}
\]
Every fixed \(\kappa<2/9\) leaves a fixed power gap.  This proves
(5).

## 6. Exact scalar method boundary

At \(\kappa=2/9\), the following exponent ledger satisfies every
scalar inequality used above:
\[
\boxed{
\begin{array}{c|c|l}
\text{symbol}&\text{exponent}&\text{meaning}\\ \hline
\ell&14/9&L=t^\ell\\
p&23/9&|\mathcal T_\alpha\times\mathcal D_0|=t^p\\
a&7/9&s=t^a\\
b&85/18&N=t^b\\
m&5/6&u=t^m\\
c&47/18&K=t^c\\
h&19/9&\text{circles per signed parameter line}\\
r&19/18&R=t^r\\
j&14/9&\text{signed parameter lines per }A\\
x&53/18&|X_A|=t^x
\end{array}}
\tag{28}
\]
Indeed,
\[
\begin{aligned}
a+b+m&=7-3\kappa=\frac{19}{3},\\
b+m&=6-2\kappa=\frac{50}{9},\\
11a+2b&=18,\\
b&=c+h,\qquad c=2p-3m,\\
r+h+m&=4,\qquad x=h+m,\\
c&=r+j,\qquad j=\ell,\\
j+h+m&=\ell+x,\\
3a+b&=6+r,\\
\frac{5-15\kappa}{2}
&=m=\frac{1+3\kappa}{2}.
\end{aligned}
\tag{29}
\]
The remaining capacities have slack:
\[
h+a=\frac{26}{9}<3,\qquad
j+m=\frac{43}{18}<\frac{23}{9}=p,\qquad
x=\frac{53}{18}<3.
\tag{30}
\]

Thus \(2/9\) is a sharp boundary for the scalar inequalities in this
note.  This is an exponent ledger, not a Euclidean construction.

## 7. Claim boundary

### Proved

- the exact fixed-\(A\) parabolic linearization (7)--(9);
- the fixed-\(A\) and summed source-incidence bounds (3)--(4);
- the strengthened service cap (10);
- the secondary signed-line dyadic target-capacity bound (19);
- exclusion of the Euclidean hub for every fixed
  \(\kappa<2/9\);
- the matching exponent \(2/9-\varepsilon\).

### Not proved

- exclusion at \(\kappa=2/9\);
- Euclidean realization of the ledger (28);
- an improvement of the global \(3/5\) distinct-distance exponent;
- a standalone Q1-level paper from this structural improvement alone.

## 8. Reproduction

```bash
cd data/research_open/erdos1083_two_hour_q1_attack_2026-07-30/route_b
python3 verify_collinear_center_linearization.py
pytest -q test_verify_collinear_center_linearization.py
```
