# Conditional deletion layers and an unbounded transient amplifier

Let B_i be the full residue class a_i modulo n_i, let
C_i = B_i ∩ [n_i, ∞) be its delayed version, and put

    U_i = B_i \ (B_1 ∪ ··· ∪ B_(i−1)),
    D_i = C_i \ (C_1 ∪ ··· ∪ C_(i−1)).

Because the moduli are strictly increasing, n_j < n_i ≤ m for every j < i
and m ≥ n_i. At such an m, membership in C_j is therefore the same as
membership in B_j. Pointwise,

    D_i = U_i ∩ [n_i, ∞).

The D_i are disjoint. If e_i denotes the periodic density of U_i, then
e_i = δ_(i−1) − δ_i, where δ_i is the density of the finite-stage full
complement. Hence Σ_i e_i ≤ 1. The unresolved positive-limit problem is
exactly an archimedean tightness question for the truncated periodic layers
D_i.

There is no universal pointwise comparison between the transient logarithmic
mass of D_i and e_i. Let Q = 2^k. Use the previous moduli 2, 4, …, Q with
forbidden residues

    0 (mod 2), 1 (mod 4), 3 (mod 8), …, 2^(j−1)−1 (mod 2^j).

Their full complement is the single class −1 modulo Q. Add the modulus
n = Q+1 and residue a = Q−2 modulo Q+1. Solving

    m ≡ Q−1 (mod Q),  m ≡ Q−2 (mod Q+1)

gives the first active compatible point m = 2Q−1, and exactly one compatible
class modulo Q(Q+1). Thus

    e = 1 / (Q(Q+1)).

At the cutoff x = 2Q−1, this one layer already contributes

    1 / ((2Q−1) log(2Q−1))

to the normalised harmonic mass. Its ratio to e is

    Q(Q+1) / ((2Q−1) log(2Q−1))  ~  Q / (2 log Q),

which is unbounded. Consequently M25L-2, and every proof that charges each
layer's full transient to a universal constant times its eventual density,
is false.

This family has previous complement density 1/Q → 0, so it does not settle
the positive-limit case. The next question is aggregate: can many individually
amplified, pairwise target-isolated layers be packed over a previous complement
whose density is bounded away from zero? The guarded search addresses exactly
that finite certificate problem.
