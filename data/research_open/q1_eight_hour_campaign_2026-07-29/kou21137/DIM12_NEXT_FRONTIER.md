# Dimension-twelve next profile frontier

Date: 2026-07-30

## Scope

This note enumerates the next necessary filtration profiles after the
dimension-eleven exclusion.  Let \(J\) be a twelve-dimensional
nilpotent associative \(\mathbb F_3\)-algebra with \(J^9=0\), and write
\[
A_i=J^i/J^{i+1},\qquad d_i=\dim A_i.
\]
Only lengths six through eight are in scope.  The calculation applies
the human theorems already used in the dimension-eleven proof; it does
not add a new closure theorem.

## Exact ledger

Positive-composition enumeration gives
\[
\binom{10}{5}+\binom{10}{6}+\binom{10}{7}
=252+210+120=582
\]
profiles.  The exact filter trace is

```text
DIM12_PROFILE_FRONTIER|total=582|length6=252|length7=210|length8=120|length9=0|after_layer_rank=136|after_quadratic_relation=117|after_one_layer=42|after_degree=37|after_tail_tensor=24|after_length7_power=20|after_cyclic_j3_tail=15|after_length8_cyclic_basis=11|after_length6_closure=8|profile_candidates=8|status=necessary_profiles_only
```

The eight branch inputs are
\[
\begin{aligned}
&(2,2,2,2,2,2),\quad (3,2,2,2,2,1),\\
&(2,2,2,2,2,1,1),\quad (2,2,2,3,1,1,1),\\
&(2,3,2,2,1,1,1),\quad (2,3,3,1,1,1,1),\\
&(3,2,2,2,1,1,1),\quad (2,2,2,2,1,1,1,1).
\end{aligned}
\]

## Filters used

The ledger uses, in order:

1. all graded product-rank inequalities \(d_{i+j}\le d_i d_j\);
2. the generalized normal-word lemma
   \(d_2=2\Rightarrow d_3\le2\);
3. the shift-tensor implication
   \(d_i=1\Rightarrow d_{i+1}\le1\) for \(i\ge2\);
4. degree-forced commutativity for length six with \(d_3=1\);
5. the pure length-six tail-tensor lemma;
6. the length-seven power lemma;
7. the cyclic-\(J^3\) tail lemma;
8. the length-eight cyclic-basis lemma;
9. the length-six raw-cube closure lemma when
   \(d_1=d_3=2\) and \(d_6=1\).

## Interpretation

These eight profiles are only the inputs to the subsequent closure-aware
branch analysis.  They are not explicit algebras, counterexamples, or
evidence of realizability.  `DIM12_CLOSURE_TRIAGE.md` now excludes three
and gives strict contracts for the other five.  In particular, this
initial ledger does not itself change the proved bound
\(\dim_{\mathbb F_3}J\ge12\); improving that bound now requires excluding
the five remaining contracts.

## Reproduction

```bash
python3 search_dim12_next_frontier.py
python3 -m unittest test_search_dim12_next_frontier.py
```
