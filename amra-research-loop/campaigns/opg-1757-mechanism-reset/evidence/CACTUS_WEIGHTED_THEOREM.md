# Weighted edge negative correlation for cactus graphs

Status: **PROVED NATURAL SUBFAMILY THEOREM; NOVELTY NOT CLAIMED**.

Let `G` be a finite cactus graph: every edge belongs to at most one simple
cycle.  Its nontrivial blocks are edge-disjoint cycles, with the remaining
blocks bridges.  A set of edges is a forest exactly when it omits at least one
edge from every cycle block.  Hence its multivariate forest polynomial
factorizes as

\[
F_G(\mathbf x)=
\prod_{b\text{ bridge}}(1+x_b)
\prod_{C\text{ cycle block}}
\left(\prod_{a\in C}(1+x_a)-\prod_{a\in C}x_a\right).
\tag{1}
\]

If the marked edges `e,f` lie in different block factors, the factors are
independent and their Rayleigh difference is zero.  A bridge block cannot
contain two distinct marked edges.  It remains to put `e,f` in one cycle
block and write

\[
R=\prod_{a\in C\setminus\{e,f\}}(1+x_a),\qquad
M=\prod_{a\in C\setminus\{e,f\}}x_a.
\]

The four marked cells of the cycle factor are

\[
P_{00}=P_{10}=P_{01}=R,\qquad P_{11}=R-M.
\]

Therefore

\[
P_{10}P_{01}-P_{11}P_{00}=R^2-(R-M)R=RM\ge0.
\tag{2}
\]

Multiplication by all other block factors multiplies (2) by their square, so
the sign remains nonnegative.  Thus every pair of distinct edges is
negatively correlated under every positive edge-activity forest measure on a
finite cactus graph; the uniform model is the specialization `x_e=1`.

The algebraic kernel is checked in `opg_cactus_cycle_probe.lean`.  The only
graph-theoretic input is the standard cactus block characterization used in
(1).  This proves an arbitrary-size host family, not arbitrary finite simple
graphs, and therefore does not satisfy `global_interface_closed`.
