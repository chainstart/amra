# Four-channel orientation quotient and Fourier matrix

## 1. Sum/difference coordinates

For each length-two page `i in {0,3,4}`, write its left and right activities
as

```text
x_iL=(p_i+d_i)/2,  x_iR=(p_i-d_i)/2.
```

The effective route activity satisfies

```text
q_i=x_iL*x_iR+x_iL+x_iR,
S_i:=d_i^2=p_i^2+4*p_i-4*q_i.                (1.1)
```

On the positive-edge-floor domain, `S_i>=0`, `p_i+2>0`, and `q_i+1>0`.
Conversely, these conditions and (1.1) reconstruct two positive floors.

Fresh substitution into the 178-term `Delta_b` produces 514 terms before
using (1.1).  Exact quotient reduction by the three relations (1.1) leaves
only four orientation characters:

```text
Delta_b = alpha000
        + alpha110*d0*d3
        + alpha101*d0*d4
        + alpha011*d3*d4.                    (1.2)
```

The four coefficient polynomials contain respectively `55,8,8,11` terms;
the whole reduced representative has 82 terms.  No odd one- or three-page
character survives, exactly as required by simultaneous hub exchange.

## 2. Coefficients from connection states

The verifier does not obtain the four coefficients by interpolation.  Put

```text
Fij = c*qk*(p_i+p_j+p_i*p_j/2) + (c+qk)*p_i*p_j,
k03 = c*q4/2,  k04=c*q3/2,

U0 = c*p0*p3*p4/4 + p0*p3*p4
   + c*(p3*p4+p0*p4+p0*p3),
W0 = F34-2*U0.
```

Here `Fij` is the orientation-even part of the connection polynomial `pij`,
while `U0` is the orientation-even part of the all-three-connected state.
The exact coefficients in (1.2) are

```text
alpha000 = F03*F04 + A*W0,
alpha110 = k03*F04 - A*c*p4/2,
alpha101 = k04*F03 - A*c*p3/2,
alpha011 = k03*k04*S0 + A*c*(q0-p0)/2.        (2.1)
```

Thus the four-channel quotient is tied directly to the three connection
Gram interfaces rather than being only a support observation.

## 3. A PSD-equivalent Fourier interface

Fix the magnitudes `D_i=sqrt(S_i)`.  Independent left/right swaps change the
three signs of `d_i`; simultaneous reversal changes none of the pair
characters, so there are four distinct values.  Put

```text
a=alpha000,
B=alpha110*D0*D3,
C=alpha101*D0*D4,
D=alpha011*D3*D4.
```

The four values of `Delta_b` are exactly the four Hadamard eigenvalues of

```text
G = [ a  B  C  D ]
    [ B  a  D  C ]
    [ C  D  a  B ]
    [ D  C  B  a ].                           (3.1)
```

Consequently, proving `Delta_b>=0` for every orientation at fixed
`(p_i,q_i,c)` is equivalent to `G>=0`.

This condition has a radical-free polynomial form.  Define

```text
g03=S0*S3,  g04=S0*S4,  g34=S3*S4,
T=S0*S3*S4.
```

Congruence by

```text
diag(1,sqrt(g03),sqrt(g04),sqrt(g34))
```

turns (3.1) into

```text
Q = [ a       alpha110*g03  alpha101*g04  alpha011*g34 ]
    [ *       a*g03         alpha011*T    alpha101*T   ]
    [ *       *             a*g04         alpha110*T   ]
    [ *       *             *             a*g34        ]. (3.2)
```

For positive `S_i`, `Q>=0` is equivalent to `G>=0`; zero-magnitude pages
follow by continuity.  Equation (3.2) is therefore a finite polynomial
matrix target on the exact spectrahedral route chamber, with no remaining
orientation quantifier.

## 4. Reproduction and scope

```sh
cd amra-research-loop/campaigns/opg-1757-transverse-lift-round7
ulimit -v 524288
timeout 120s python3 evidence/verify_orientation_fourier.py
```

The standard-library verifier reconstructs the original forest polynomials,
performs the rational sum/difference substitution, reduces the 514 terms in
the exact quadratic quotient, checks (1.2)--(2.1), and constructs the
radical-free symmetric matrix (3.2).

Mathematical status: exact author-verified orientation compression and a
PSD-equivalent proof interface.  Positivity of (3.2), its principal minors,
and hence the generic sign of `Delta_b` remain open.  No full marked-host or
OPG-1757 theorem is claimed.
