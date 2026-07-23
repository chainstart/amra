# #679: shiftwise entropy tilts do not change the leading cutoff

Date: 2026-07-23

This note audits a remaining degree of freedom in the moving-conductor
argument: allowing a different local hit value for every shift.  The exact
optimizer is shift-dependent, but on a dyadic block its gain over the
single aggregate parameter is smaller than the proved error term.  Thus it
does not close #679 or move the leading conductor boundary.

## 1. General shiftwise product

Retain the notation

\[
 k_j=H+j\quad(0\le j<H),\qquad
 L=\sum_{H<p\le z}{1\over p},
\]

and let

\[
 r_j=\left\lceil(1+\varepsilon){\log k_j\over\log_2k_j}\right\rceil-1.
\]

Choose numbers \(0<y_j<1\).  At a prime \(p\in(H,z]\), give the local
factor the value \(y_j\) if \(p\mid n-k_j\), and the value one if no shift
is hit.  The residues are distinct because \(p>H\).  Put

\[
 A=\sum_{j<H}(1-y_j),\qquad
 Q=\sum_{j<H}(1-y_j)^2.                             \tag{1}
\]

If \(n\) is a #679 candidate, the number of selected primes hitting shift
\(j\) is at most \(r_j\).  Hence the resulting product satisfies

\[
 V_{\boldsymbol y}(n)\ge P_{\boldsymbol y}
 :=\prod_{j<H}y_j^{r_j}.                            \tag{2}
\]

## 2. Exact local moments and energy

At each prime the first and second local moments are

\[
 m_p=1-{A\over p},\qquad
 s_p=1-{2A-Q\over p}.                              \tag{3}
\]

The local centred variance is \(Q/p-A^2/p^2\).  After normalising ANOVA
energy by the complete second moment, the inclusion parameter is therefore

\[
 \theta_p={Q/p-A^2/p^2\over1-(2A-Q)/p}.             \tag{4}
\]

For the choices used below, \(y_j\asymp1/\log_3X\).  On \(H<p<2H\),
the first factor in (3) is \(\gg1/\log_3X\), the second is
\(\gg1/(\log_3X)^2\), and there are only \(O(H/\log H)\) such primes.
On \(p\ge2H\), Taylor remainders sum to \(O(H)\).  Consequently,
uniformly in these shiftwise choices,

\[
 \log\mu=-AL+O(H),\qquad
 \log M_2=-(2A-Q)L+O(H).                            \tag{5}
\]

Moreover the exact identity

\[
 \theta_p={Q\over p}
 -{(A-Q)^2/p^2\over1-(2A-Q)/p}
\]

for \(p\ge2H\), together with the crude lower segment estimate, gives

\[
 \Lambda:=\sum_p\theta_p=QL+O(H).                  \tag{6}
\]

## 3. Candidate-forced conductor threshold

Define the available exponent

\[
 S(\boldsymbol y)
 :=AL+\log P_{\boldsymbol y}
 =\sum_{j<H}\{L(1-y_j)+r_j\log y_j\}.              \tag{7}
\]

With \(\Delta=1/\log_3X\), take

\[
 \mathcal C_{\boldsymbol y}
 =\exp\{S(\boldsymbol y)-\Delta HL\}.              \tag{8}
\]

The condition \(c(T)\le\mathcal C_{\boldsymbol y}\) implies
\(|T|=O(H)\), whereas (6) is \(\asymp HL\).  The same exponential
Markov calculation as in the aggregate proof yields

\[
 \sum_{c(T)\le\mathcal C_{\boldsymbol y}}\sum_u^*
 |\widehat F_T(u)|^2
 \le\exp\{-2AL+O(H\log_3X)\}.                      \tag{9}
\]

The additive large sieve on an interval of length \(N\asymp X\) then
bounds the nonzero low-conductor signed sum by

\[
 \exp\{\log\mathcal C_{\boldsymbol y}-AL
              +O(H\log_3X+\log X)\}
 =P_{\boldsymbol y}
  \exp\{-(\Delta-o(\Delta))HL\}.                  \tag{10}
\]

The zero component is also \(o(P_{\boldsymbol y})\), because
\(S(\boldsymbol y)\asymp HL\gg\log X\).  Therefore any candidate again
forces a positive signed tail beyond (8).  This is a generalisation of the
aggregate cutoff, not a tail upper bound.

## 4. Exact optimizer and size of its gain

Each summand in (7) is strictly concave in \(y_j\), and

\[
 {d\over dy}\{L(1-y)+r_j\log y\}=-L+{r_j\over y}.
\]

Thus the exact shiftwise optimizer is

\[
 \boxed{y_j={r_j\over L}},
 \qquad
 \boxed{S_*=L\sum_{j<H}I(r_j/L)},
 \quad I(u)=1-u+u\log u.                            \tag{11}
\]

Let \(R=\sum_jr_j\) and \(\rho=R/(HL)\).  Convexity of \(I\) shows

\[
 S_*\ge HL I(\rho),                                \tag{12}
\]

so the aggregate choice does not secretly exceed the true optimum.
However, on \(H\le k<2H\), the continuous function
\((1+\varepsilon)\log k/\log_2k\) varies by
\(O(1/\log_2H)=o(1)\).  Hence the integers \(r_j\) take at most two
consecutive values for large \(H\), and \(|r_j-R/H|\le1\).  Since
\(r_j/L\sim(1+\varepsilon)d/\log_3X\), Taylor's theorem in (12) gives

\[
 0\le S_*-HL I(\rho)
 \ll {1\over\rho L}\sum_{j<H}(r_j-R/H)^2
 \ll {H\log_3X\over\log_2X}.                       \tag{13}
\]

The gain (13) is much smaller than both the retained margin
\(HL/\log_3X\) and the present \(O(H\log_3X)\) analytic error.  Therefore
shiftwise tilting cannot improve the established leading cutoff.  A real
advance still requires coefficient-sensitive control of the signed
high-conductor tail, or an essentially different construction.

