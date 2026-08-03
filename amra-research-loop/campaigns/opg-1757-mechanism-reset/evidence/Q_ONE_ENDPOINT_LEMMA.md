# The `q=1` endpoint of the scaled random-cluster survivor

Status: **PROVED REPRESENTATION LEMMA; CONSISTENT WITH KNOWN 2025 WORK; NO
PROMOTION CLAIM**.

For a fixed graph and marked edges `e,f`, write

\[
 P_q=P_{00}(q)+x_eP_{10}(q)+x_fP_{01}(q)+x_ex_fP_{11}(q),
\]

where

\[
 P_{ij}(q)=\sum_{B\subseteq E\setminus\{e,f\}}
 q^{\nu(B\cup i e\cup j f)}\mathbf x^B
\]

and `nu(A)=|A|-|V|+k(A)` is graphic-matroid nullity.  Its Rayleigh
difference is

\[
 D_q=P_{10}P_{01}-P_{11}P_{00}.
\]

At `q=1`, every cell is

\[
 S=\prod_{a\ne e,f}(1+x_a),
\]

so `D_1=0` and `1-q` divides `D_q` as a polynomial in `q`.  Differentiating
at one gives

\[
 -D'_1=S\sum_B \mathbf x^B
 \big(\nu(B+e+f)+\nu(B)-\nu(B+e)-\nu(B+f)\big).
\]

Matroid rank is submodular, hence nullity is supermodular.  Every bracket is
therefore nonnegative (in fact zero or one).  Consequently

\[
 \left.\frac{D_q}{1-q}\right|_{q=1}=-D'_1\ge0.
\]

This proves the correct sign at the independent endpoint `q=1` for every
finite graph and every nonnegative activity vector.  It does not control the
quotient throughout `0<q<1`; in particular it supplies no uniform passage
from `q=1` to the forest endpoint `q=0`.

Nguyen--Pylyavskyy, *Correlations in random cluster model at q=1*
(https://arxiv.org/abs/2507.09520), is the relevant primary-source novelty
context.  No novelty beyond the campaign's exact reformulation is claimed.
