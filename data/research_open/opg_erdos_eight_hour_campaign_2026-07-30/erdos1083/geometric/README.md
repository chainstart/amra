# Erdős 1083 geometric campaign

This directory contains only new work from the 2026-07-30 geometric
campaign.  It does not modify or silently strengthen the inherited
\(n^{3/5-o(1)}\) theorem.

- `CRITICAL_ANISOTROPIC_GRID_BARRIER.md` proves an exact Euclidean
  interface extremizer with \(M=\Theta(F^{4/3})\) and
  \(\mathcal E=\Theta(F^{8/3})\), derives the sharp off-critical
  exponent \(3/5+(3/10)|\alpha-2/3|\), and proves \(2\)-adic and
  odd-prime rational nonresonant-angle subcases with
  \(D\ge N^{4/5-o(1)}\).
- `verify_critical_anisotropic_grid.py` exhaustively enumerates all circle
  pairs in small instances and compares the result with the closed forms.
- `test_critical_anisotropic_grid.py` is the regression suite.

Status: this is a rigorous obstruction theorem and scoped positive
dichotomy.  It is not an unconditional improvement of \(f_3(n)\).
