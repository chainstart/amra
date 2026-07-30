# Strong single-pair correlation: multiplicity, BSG, and the exact deficit

Date: 2026-07-30

## Purpose

The joint correlation dichotomy leaves a strong-pair branch
\[
 r\geq L^{5/6-\eta-o(1)}. \tag{1}
\]
This note stops the local-cycle strategy and asks whether one such block
pair can be converted, by signs, dyadic multiplicity and
Balog--Szemerédi--Gowers/Plünnecke, into enough additive structure to improve
the global parameter-line exponent.

The answer is negative under the present hypotheses, for two separate and
quantitative reasons.

1. A genuine shifted overlap satisfies a fixed-product hyperbola, not an
   additive-energy equation.  BSG does not apply.
2. Even in the fictitious zero-shift case where additive energy is present,
   the strongest possible representation multiplicities leave an energy
   deficit
   \[
   K\geq L^{1/6+\eta-o(1)}. \tag{2}
   \]
   With the automatic multiplicity one, the deficit is much worse.

An explicit real-height construction realizes \(r\) hyperbolic coincidences
with exactly one representation on each side.  Thus no dyadic argument can
manufacture the missing energy.  Finally, structure on the four height sets
of one block pair has local line capacity only \(O(L^2)\), versus the target
\(L^{8/3+\eta}\); a factor \(L^{2/3+\eta}\) of global propagation is also
missing.

## 1. Exact equation supplied by one shifted overlap

Let
\[
 S_1=C_1+(A-B)^2,\qquad S_2=C_2+(C-D)^2,
\]
where all four height sets have size at most \(m\), and let
\[
 T\subseteq S_1\cap S_2,\qquad |T|=r.
\]
For \(t\in T\), choose represented signed differences
\[
 x=a-b,\qquad y=c-d.
\]
Then
\[
 x^2-y^2=\Delta,\qquad \Delta=C_2-C_1, \tag{3}
\]
or equivalently
\[
 (a+d-b-c)(a+c-b-d)=\Delta. \tag{4}
\]

For distinct radius pairs in one geometric-product fibre,
\(\Delta\ne0\).  Indeed, a positive unordered radius pair is determined by
its product and by
\[
 C=(\rho-\rho')^2=\rho^2+\rho'^2-2\rho\rho':
\]
equal product and equal \(C\) give equal sum, hence the same unordered pair.

Equation (4) is a multiplicative constraint between two four-variable
linear forms.  It is not an equation of the form
\[
 a+d=b+c+\text{constant}
\]
on a positive proportion of the solutions.  Once one factor in (4) is
chosen, the other is \(\Delta\) divided by it; over the reals there is no
divisor bound and the first factor may take \(r\) distinct values.

Thus “split the squares into signs” does not turn the actual strong-pair
branch into additive difference energy.

## 2. Exact dyadic multiplicity ledger

For \(t\in T\), define
\[
 \nu_1(t)=|\{(a,b)\in A\times B:C_1+(a-b)^2=t\}|,
\]
and define \(\nu_2(t)\) similarly.  Since a fixed signed difference has at
most \(m\) representations,
\[
 1\leq\nu_i(t)\leq2m. \tag{5}
\]

Dyadically partition both multiplicities.  Among the \(r\) common values
there is a class \(T'\) with
\[
 |T'|\geq
 \frac{r}{(2+\lceil\log_2m\rceil)^2}, \tag{6}
\]
and numbers \(\lambda_1,\lambda_2\), powers of two, such that
\[
 \lambda_i\leq\nu_i(t)<2\lambda_i
 \quad(t\in T'). \tag{7}
\]
This supplies between
\[
 |T'|\lambda_1\lambda_2
\quad\hbox{and}\quad
4|T'|\lambda_1\lambda_2 \tag{8}
\]
represented solutions of the hyperbolic equation (3).  Crucially, the
present hypotheses give no lower bound beyond
\(\lambda_1=\lambda_2=1\).

## 3. The fictitious zero-shift BSG benchmark

Suppose temporarily that \(\Delta=0\).  Then
\[
 (a-b)^2=(c-d)^2
\]
splits into the two additive equations
\[
 a-b=c-d,\qquad a-b=d-c. \tag{9}
\]
If
\[
 Q=\sum_{t\in T}\nu_1(t)\nu_2(t),
\]
at least \(Q/2\) represented quadruples obey one equation in (9).  This is
the first point at which an asymmetric BSG theorem is applicable.

The universal bounds (5) give
\[
 r\leq Q\leq4m^2r. \tag{10}
\]
Writing the usual energy parameter as
\[
 Q=\frac{m^3}{K},
\]
even the absolute maximum in (10) forces
\[
 K\geq\frac{m}{4r}. \tag{11}
\]

In the balanced regime \(m\asymp L\), at the strong-pair threshold (1),
\[
 K\geq L^{1/6+\eta-o(1)}. \tag{12}
\]
For the desired line bound \(M\geq F^{4/3+\varepsilon}\), one has
\(\eta=2\varepsilon\), hence
\[
 K\geq L^{1/6+2\varepsilon-o(1)}. \tag{13}
\]

Standard BSG and Plünnecke give subsets and doubling bounds with polynomial
losses in \(K\).  Equations (12)--(13) show that those losses are necessarily
a fixed power of \(L\), even under impossible best-case multiplicities.
They cannot yield the \(m^{1-o(1)}\) common cores required by the existing
identical-height/Sidon-offset route.

The exact multiplicity input that would be needed for subpolynomial BSG loss
is
\[
 r\lambda_1\lambda_2\geq m^{3-o(1)}. \tag{14}
\]
At (1), this asks for
\[
 \lambda_1\lambda_2
\geq m^{13/6+\eta-o(1)}, \tag{15}
\]
while (5) gives only \(\lambda_1\lambda_2\leq4m^2\).  The exponent shortfall
is exactly
\[
 m^{1/6+\eta-o(1)}. \tag{16}
\]
Thus no refinement of dyadic pigeonholing can reach the near-maximal energy
regime; the requested input exceeds the representation-capacity bound.

The upper bound in (10) is sharp in order in the zero-shift model.  Take
\(A=B=C=D=\{0,\ldots,m-1\}\) and select any \(r=o(m)\) nonzero difference
magnitudes \(d=o(m)\).  Each has \(\Theta(m)\) representations on both
sides, so \(Q=\Theta(rm^2)\) and \(K=\Theta(m/r)\).  Hence (11) is a genuine
capacity barrier, not a loose estimate.

## 4. A real-height multiplicity-one saturation example

The actual nonzero-shift setting can be much worse.

### Proposition 1 (hyperbolic overlap with no additive-energy gain)

For all integers \(m\geq r+1\), every nonzero real \(\Delta\), and four
independent height classes, there are \(m\)-point real sets
\(A,B,C,D\) and \(r\) distinct common shifted values such that every selected
value has exactly one point-pair representation in \(A\times B\) and exactly
one in \(C\times D\).

### Proof

Choose positive reals \(y_1,\ldots,y_r\) algebraically independent over
\(\mathbb Q(\Delta)\), and put
\[
 x_i=\sqrt{y_i^2+\Delta},
\]
choosing the \(y_i\) large enough if \(\Delta<0\).  Begin with
\[
 A_0=\{x_1,\ldots,x_r\},\quad B_0=\{0\},\qquad
 C_0=\{y_1,\ldots,y_r\},\quad D_0=\{0\}.
\]
The selected squared differences are \(x_i^2\) and \(y_i^2\), with
\[
 x_i^2-y_i^2=\Delta. \tag{17}
\]
Algebraic independence ensures that the displayed anchored pairs are the
only representations of these selected magnitudes in the initial sets.

Pad the four sets one point at a time.  At each step, creating an additional
representation of one of the finitely many selected magnitudes excludes
only finitely many candidate real values.  Choose outside that finite set.
This reaches cardinality \(m\) while preserving representation multiplicity
one.

Taking block offsets \(C_1=0,C_2=\Delta\) when \(\Delta>0\) gives
\[
 C_1+x_i^2=C_2+y_i^2.
\]
For the other sign, exchange the block names. \(\square\)

This proposition realizes
\[
 Q=r,\qquad
 K=\frac{m^3}{r}
  =m^{13/6+\eta+o(1)} \tag{18}
\]
at the threshold (1), if one formally records the represented coincidence
count as an energy.  More importantly, the \(r\) solutions lie on the
hyperbola (3), so even that weak quantity is not additive energy.

An entirely rational finite certificate for rational \(\Delta\) is obtained
from
\[
 x_i=\frac{s_i+\Delta/s_i}2,\qquad
 y_i=\frac{\Delta/s_i-s_i}2,\qquad
 x_i^2-y_i^2=\Delta, \tag{19}
\]
followed by greedy rational padding that avoids the finitely many forbidden
differences.  The accompanying verifier uses the actual radial offsets
\(16129\) and \(64\), hence \(\Delta=16065\), and constructs such examples.

## 5. Failure to return to the global exponent

There is an independent global-capacity obstruction.  One strong block pair
uses only four height sets, hence \(O(m)\) of the \(F=Lm\asymp L^2\) circle
fibres.  Even perfect knowledge of those four sets can expose at most
\[
 O(m^2)=O(L^2) \tag{20}
\]
pair parameters internally.  The desired target is
\[
 M\geq F^{4/3+\varepsilon}
   =L^{8/3+2\varepsilon}
   =L^{8/3+\eta}. \tag{21}
\]
Therefore a conclusion confined to one block pair misses the global target
by the factor
\[
 L^{2/3+\eta}. \tag{22}
\]

BSG structure is not itself a lower bound for \(M\); small doubling usually
describes compression.  To re-enter the global proof, a single-pair inverse
theorem would still need a propagation statement transferring the recovered
structure to at least \(L^{2/3+\eta}\) quantitatively independent
radius-pair contributions.  The strong-pair side of the current dichotomy
supplies no such network.

## 6. Final diagnosis

The strongest valid single-pair statement obtainable from the present data
is the dyadic hyperbolic relation (6)--(8).  It is not a BSG hypothesis.
There are two exact missing powers:

1. **energy:** even after replacing the hyperbola by additive equality and
   maximizing all multiplicities, the energy parameter loses
   \(L^{1/6+\eta}\);
2. **global propagation:** structure confined to the four participating
   height sets loses \(L^{2/3+\eta}\) against the target line count.

Accordingly the strong-pair branch cannot close the \(4/3+\varepsilon\)
target via standard BSG/Plünnecke.  A viable replacement must either exploit
the nonzero fixed-product equation (4) directly and force global propagation,
or strengthen the correlation dichotomy so that strong pairs occur on a
large network rather than in isolation.

## 7. Verification

`verify_strong_pair_bsg_audit.py` checks the factorization, all exponent
identities, the zero-shift interval saturation, and exact rational
multiplicity-one hyperbolic examples with greedy padding.
