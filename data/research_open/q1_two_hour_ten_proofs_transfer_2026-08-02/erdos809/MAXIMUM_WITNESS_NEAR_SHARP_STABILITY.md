# Erdős #809 — quantitative stability below the parity-sharp barrier

Date: 2026-08-02

Status:
**PROVED CONDITIONAL STABILITY THEOREM; MAXIMUM-WITNESS B-OPPOSITE ONLY;
PUBLIC PROBLEM OPEN**

## 1. Why this is a ten-proofs transfer

Two lessons in the ten-proofs corpus are relevant here.  The Ehrhart
argument separates the sharp inequality from equality classification, and
the sphere-packing/coding arguments retain the complete nonnegative
remainder instead of discarding it after obtaining the headline bound.
Applying those lessons to the previously audited #809 factorization turns
the square-root estimate into a quantitative stability theorem.

No new graph hypothesis is introduced.  Retain the maximum-witness
B-opposite setting and notation of the parity-sharp theorem:

\[
 n=2\delta+\kappa,\qquad g=\Delta-\delta,\qquad
 a=2g-\kappa,\qquad h=\kappa-d-1,\qquad
 u=d(b)-\delta.
\]

Here \(d=\rho_c-1\) comes from any selected opposite leaf.  The inherited
centre-degree interval is \(\delta\le d(b)\le\delta+h\), so
\(0\le u\le h\).  The remaining constraints give \(h\ge0\), \(a\ge2\)
and even when \(n\) is even, and \(a\ge1\) and odd when \(n\) is odd.

## 2. Exact deficit energies

### Theorem 2.1 (even stability energy)

Suppose \(n\) is even and define

\[
 n_{\mathrm{ev}}^*(g)=2g^2-2g-6,\qquad
 T=n_{\mathrm{ev}}^*(g)-n.
\]

Then every maximum-witness B-opposite obstruction satisfies

\[
\boxed{
 T\ge
 \frac{(a-2)(a+4)}2+h(2g-h-1)+2u(h-u).
}
\tag{E}
\]

### Theorem 2.2 (odd stability energy)

Suppose \(n\) is odd and define

\[
 n_{\mathrm{odd}}^*(g)=2g^2-2g-3,\qquad
 T=n_{\mathrm{odd}}^*(g)-n.
\]

Then

\[
\boxed{
 T\ge
 \frac{(a-1)(a+3)}2+h(2g-h-1)+2u(h-u).
}
\tag{O}
\]

### Proof of both formulas

For even order, put \(\delta^*=g^2-2g-2\).  Before minimizing over the
centre degree \(p=d(b)\), the concave quadratic in the audited proof has
endpoints \(p=\delta\) and \(p=\delta+h\).  At
\(p=\delta+u\), its exact excess above either endpoint is
\(u(h-u)\).  Retaining that discarded nonnegative remainder strengthens
the comparison to

\[
0\ge\mathcal L_0-\overline M
 =\delta-\delta^*
 +\frac{a^2-4+2h(2g-h-1)}4
 +u(h-u).
\tag{1}
\]

Since \(\kappa=2g-a\),

\[
\begin{aligned}
T
 &=\{2\delta^*+(2g-2)\}-\{2\delta+\kappa\}\\
 &=2(\delta^*-\delta)+(a-2).
\end{aligned}
\tag{2}
\]

Twice the nonnegative remainder in (1), followed by (2), gives

\[
T\ge
\frac{a^2-4+2h(2g-h-1)}2+a-2+2u(h-u),
\]

which factors as (E), including the term \(2u(h-u)\).

For odd order use \(\delta^*=g^2-2g-1\), the baseline
\(\kappa^*=2g-1\), and the audited identity

\[
0\ge\delta-\delta^*
+\frac{a^2-1+2h(2g-h-1)}4+u(h-u).
\tag{3}
\]

Now \(T=2(\delta^*-\delta)+(a-1)\), which gives (O).  No relaxation
beyond the one already present in the audited square-root comparison is
made.  \(\square\)

## 3. Rigid near-equality bands

The three terms in (E) and (O) detect different departures from the sharp
core: parity/residual size, common-residual gap, and the position of the
centre degree inside its admissible interval.

- In even order, parity gives either \(a=2\) or \(a\ge4\).  The latter
  costs at least \(8\).
- In odd order, either \(a=1\) or \(a\ge3\).  The latter costs at least
  \(6\).
- If \(h\ge1\), its contribution together with the nonnegative
  \(a\)-term is at least \(2g-2\).
- The centre term vanishes exactly at \(u=0,h\); an interior centre
  \(1\le u\le h-1\) pays at least \(2(h-1)\).

For the last assertion, \(h\mapsto h(2g-h-1)\) is concave on the
admissible integer interval.  At \(h=1\) it equals \(2g-2\).  At the
other endpoint \(h=2g-a-3\), its excess over \(2g-2\) is

\[
 (a+1)(2g-a-4)\ge0
\]

whenever that endpoint is nonempty.

Therefore:

### Corollary 3.1 (near-sharp residual rigidity)

In even order, if

\[
 T<\min\{8,\,2g-2\},
\]

then

\[
 a=2,\qquad \kappa=2g-2,\qquad h=0,\qquad
 d=\rho_c-1=\kappa-1=2g-3.
\tag{4}
\]

In odd order, if

\[
 T<\min\{6,\,2g-2\},
\]

then

\[
 a=1,\qquad \kappa=2g-1,\qquad h=0,\qquad
 d=\rho_c-1=\kappa-1=2g-2.
\tag{5}
\]

Thus a fixed-width band below either parity-sharp vertex bound has the
same common-residual skeleton as the exact equality graph.  The theorem
does not assert graph isomorphism: the minimum degree may still be below
its equality value by \(T/2\).

Notice also that \(T\) is even (the sharp cap and \(n\) have the same
parity).  Once (4) or (5) holds, the remaining scalar freedom is exactly

\[
 \delta=\delta^*-T/2.
\]

In particular, scalar equality \(T=0\) forces the complete sharp
parameter profile, although it still does not classify the graph or its
colouring.

### Corollary 3.2 (quantitative localization at arbitrary deficit)

Without a fixed-width assumption, (E)--(O) give

\[
 a+1\le
 \begin{cases}
  \sqrt{2T+9},&n\text{ even},\\
  \sqrt{2T+4},&n\text{ odd},
 \end{cases}
 \qquad
 h(2g-h-1)\le T.
\tag{6a}
\]

If \(h>0\), the centre degree is quantitatively close to one endpoint:

\[
 \min\{u,h-u\}\le \frac{T}{h}.
\tag{6b}
\]

Indeed, the first inequalities are just the two parameter-shift energies
rewritten as \((a+1)^2-9\le2T\) and
\((a+1)^2-4\le2T\).  For (6b), put
\(m=\min\{u,h-u\}\le h/2\); then
\(2u(h-u)=2m(h-m)\ge mh\).  Thus the three coordinates of departure from
the sharp profile are controlled separately, rather than only through the
headline vertex bound.

If the selected pair is a genuine one-leaf repeated-colour zero shore
under reserve failure, the inherited defect-slack inequality
\(Z=D_B-h_c\ge d-g\) combines with (4)--(5) to give

\[
 Z\ge g-3\quad\text{in the even near-sharp band},\qquad
 Z\ge g-2\quad\text{in the odd near-sharp band}.
\tag{6c}
\]

This is a useful stability-to-colour interface: approaching the graph
bound forces the full residual skeleton and simultaneously requires
linear unpaid colour defect.

## 4. Certificate and scope

The self-contained arithmetic verifier checks the factorization of both
base costs, sampled endpoint/interior centre offsets, all parity profiles
through \(g=250\), the \(2g-2\) residual-gap threshold, and the first
nonbaseline costs \(8\) and \(6\).  It covers 10,323,118 base scalar
profiles.

This result is conditional on the inherited maximum-witness B-opposite
normal form.  It does not eliminate Branch A, B-same, configurations far
below the sharp bound, or other BCM branches.  It neither proves nor
refutes Erdős #809.
