# RESULT #1040

status_official: OPEN

status_mathematical_original: NOT_CLOSED

current_frontier: cap(K)>1 solved; general compact cap(K)=1 open

latest_capacity_one_special_case:
  Pendyala (arXiv:2606.17097, June 2026) proves the sharp
  Theta(1/log n) order for the unit disk/unit-circle zero constraint. This
  does not solve arbitrary capacity-one K.

rigorous_strict_partial:
  For cap(K)=1, the Fekete polynomials satisfy
  limsup area{|p_n|<1} <= planar_area(polynomial_hull(K)).
  Hence hull area zero implies mu(K)=0.

novelty_guard:
  The proof chain was checked, but this intake did not perform a sufficiently
  exhaustive novelty search to claim priority or standalone publishability.
  Register only as STRICT_PARTIAL.

rigorous_route_counterexample:
  Weak convergence to equilibrium plus convergence of logarithmic energy does
  not imply area{potential<0}->0, even for the unit disk. An explicit
  distinct-root polynomial sequence has near-optimal discrete energy and
  lemniscates containing disks of radii 1-1/j.

first_breakpoint:
  The equilibrium potential has a zero plateau on the polynomial hull, so
  energy control has no one-sided sign margin at level zero.

q2_assessment: NOT_YET; useful rigorous section, but a larger nonregular
  capacity-one class is needed for a standalone Q2 paper.

certificate:
  scripts/validate_1040.py
