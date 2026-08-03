# Strong upstream carry gap

The discrete-convexity note proves `A>=a+2` for the relaxed `s>=2`
multi-cap problem.  The same exact inequalities give the sharper bound

\[
\boxed{A\ge a+s.}
\]

Indeed `beta>alpha` and `beta<=C(r,2)` imply `r>a`, hence `r>=a+1`.
The complement increment is

\[
\Delta=sr+\binom s2-1
\ge sa+\binom s2+s-1.
\]

If `A<=a+s-1`, canonical cap bounds instead give

\[
\Delta=\beta-\alpha
<\binom{A+1}2-\binom a2
\le\binom{a+s}2-\binom a2
=sa+\binom s2,
\]

contradicting `s>=2`.  Therefore `A>=a+s`.  Since actual dyadic legality
already forces `s>=3`, every actual target state has at least the stronger
three-level upstream separation `A>=a+3`.

This is a proved reduction, not the multi-cap theorem.  The top-only bound
from the preceding note still need not close cells with small `c`; the new
gap only replaces the residual range

`a+2<=A<A_*(a,c)`

by

`a+s<=A<A_*(a,c)`.

Thus any remaining endpoint counterexample must simultaneously lie in one
of the five endpoint families and in this shorter top interval.
