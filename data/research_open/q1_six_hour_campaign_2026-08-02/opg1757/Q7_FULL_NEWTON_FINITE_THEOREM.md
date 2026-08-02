# Exact q=7 full base-four Newton layer

Date: 2026-08-02

Status: **FINITE THEOREM; NOT AN ALL-DEFICIT PROOF**.

## 1. Statement

For deficit (q=7), every one of the fifteen normalized polynomials

\[
C_{7,r}(s),\qquad0\le r\le14,
\]

has base-four Newton expansion

\[
C_{7,r}(s)=\sum_{j=3}^{14}\gamma_{7,r,j}
\binom{s-4}{j},
\]

with

\[
\boxed{\gamma_{7,r,j}>0\quad(0\le r\le14,\ 3\le j\le14).}
\]

The coefficients at orders (j=0,1,2) vanish exactly, as forced by
the boundary factor.  Across the full layer the census is

\[
180\text{ positive},\qquad45\text{ zero},\qquad0\text{ negative}.
\]

The smallest active coefficient is

\[
\gamma_{7,14,3}=512.
\]

## 2. Exact construction

The previous frozen table contains all endpoints with
(e+c\le8).  The (q=7) master formula needs (e+c\le9), so exactly
27 new triples

\[
(h,e,c),\qquad h=0,1,2,\quad e+c=9
\]

are required.  For each triple, `probe_q7_full_newton.py`:

1. computes exact hyperforest endpoint values by the anchored-component
   recurrence;
2. clears the known power (s^e);
3. interpolates with exactly one more value than the Abel degree bound;
4. checks one additional exact value not used in interpolation.

Together with the 108 inherited endpoints this gives 135 exact endpoint
polynomials.  Substitution in the normalized master identity constructs
all fifteen degree-fourteen (C_{7,r})'s.  Their leading coefficients
are independently checked against

\[
\frac4{7!}[z^r](1+2z+2z^2)^7.
\]

Forward differences at (s=4) then give every Newton coefficient.

## 3. Scope

This closes one additional complete deficit layer beyond the former
frozen range (q\le6).  It is exact finite mathematics, not evidence
that may be extrapolated to (q\ge8).  The full Newton conjecture and
the original OPG-1757 statement remain open.
