# M10 round 3 evidence: Fejer majorant and exact-fibre moment gate

Date: 2026-08-27

Status: **proved sufficient single-block bridge and scoped method no-goes;
the bridge itself remains open.**  Nothing here proves an Erdős 451 upper
bound or a single-block maximum-gap theorem.

The full derivations are in
`work/m10_round1/high_support_joint_correlation_round3.md`.

## Proved result 1: a valid one-sided carry relaxation

For smoothing order `L=2`, integer `1<=h<P/2`, local weights

\[
 u_i(n)=\operatorname{sinc}(\pi bn/p_i)^2,
 \qquad U_i(r)=\sum_m u_i(r+mp_i),
\]

and exact numerator fibres

\[
 W(A)=\sum_{\sum_i z_iP/p_i=A}\prod_i u_i(z_i),
\]

put `c_i=(P/p_i)^(-1) mod p_i`,
`V(r)=product_i U_i(c_ir)`, and

\[
 \Omega(r)=\sum_{ell\in\mathbb Z}
       \operatorname{sinc}(\pi h(r+ell P)/P)^2.
\]

The carry identity and positivity give

\[
 \prod_iU_i(c_ix)=\sum_ell W(x+ell P),\qquad
 E-1\le S-1,
\]

where `E=sum_A Phi_h(A)W(A)` is the complete positive box-spline Fourier
ledger and `S=sum_(r mod P)Omega(r)V(r)`.  Thus `S<2` is sufficient for the
single-block box-spline criterion.  It is not equivalent to it.

Poisson summation and the exact triangular local transform give

\[
 S={P\over hb^q}
 \sum_{\substack{|a_i|<b\\|H(a)|_P<h}}
 \left(1-{|H(a)|_P\over h}\right)
 \prod_i\left(1-{|a_i|\over b}\right),
\]

where `H(a)` is the global CRT lift of the small residues `a_i`.  Its phase
is still

\[
 {H(a)\over P}\equiv\sum_i{a_i c_i\over p_i}\pmod1,
 \qquad c_i=(-1)^{q-1}F'(d_i)^{-1}\pmod {p_i}.
\]

This corrects two tempting but false inferences: independent local carry
sums are not the exact fibre, and local residue untwisting does not erase
the joint inverse-derivative small-lift phase.

## Proved result 2: subset-period ledgers do not close the bridge

On the coefficient side the relevant interval has length `2h`; on the
real side the periodized Fejer kernel is concentrated on scale `P/h` and
obeys

\[
 \Omega(r)\ll\min\{1,P^2/(h^2(1+|r|_P)^2)\}.
\]

Dyadic transfer of the exact subset-period lemma gives, for a subset of
`s` coordinates,

\[
 {S\over\prod_iU_i(0)}
 \ll_L {P\over h}(C_L/b)^s+P_S.
\]

At `h=exp(O(q))P/b^q` in a macroscopic block, optimization has
`s=(1/2+o(1))q` and leaves
`exp((1/2+o(1))q log k)=exp(Theta(k))`.  This kills only complete-period
averaging on a subset followed by positive disposal of the complement.

For general even smoothing order `L`, the principal local coefficient
satisfies `beta_i(0)>=c sqrt(L)/b`.  At
`h=k^BC^qP/product_i d_i`, the principal term of the periodized majorant is
at least

\[
 k^{-B}(c\sqrt L/C)^q\prod_i(d_i/b).
\]

For fixed `C` and macroscopic `q`, unbounded `L` therefore makes the
principal term itself exceed two.  Growing smoothing order does not rescue
this particular majorant.

## Proved result 3: raw higher Holder moments are diagonal-dominated

For `s>=2`, the exact fibre moment has the carry-preserving identity

\[
 \sum_AW(A)^s=
 \sum_{\substack{t^{(2)},\ldots,t^{(s)}\in\mathbb Z^q\\
                 \sum_i t_i^{(nu)}=0}}
 \prod_i\sum_n u_i(n)\prod_{nu=2}^su_i(n+p_it_i^{(nu)}).
\]

It obeys

\[
 \sum_AW(A)^s\le C^q{P\over b^q}e^{Csq/b^2},
\]

while, provided `r_epsilon<q`, the all-identical tuple family, already
entirely in reduced support `q`, gives

\[
 \sum_AW_>(A)^s\ge(c_0^s/8)^q{P\over b^q},
 \qquad c_0=8/\pi^2.
\]

Consequently every fixed positive Holder order leaves an
`exp(Theta(k))` separated ledger (best at order two), and even slowly
growing order cannot meet the density-scale moment threshold: the diagonal
exceeds it by `exp(Omega(sq log k))` in the large dyadic blocks.

## Remaining executable interface

The strongest concrete surviving statement is the weighted joint
small-lift inequality displayed in Proved result 1.  It must use the
correlated phases `c_i=(-1)^(q-1)F'(d_i)^(-1)`; marginal discrepancy,
coordinate-subset period completion, and raw positive moments are
insufficient.  Within an exact-fibre moment approach, the only surviving
variant is a signed carry-preserving cumulant/factorial moment that cancels
all coincidence partitions, beginning with the diagonal family above.
