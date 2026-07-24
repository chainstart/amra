# RESULT #831

status_official: OPEN

status_mathematical_original: NOT_CLOSED

current_bounds:
  lower: h(n) >= (n-2)/2
  public_2026_upper_claim: h(n) <= n^2 exp(O(sqrt(log n)))

rigorous_new_route_audit:
  Fixed-radius multiplicity is exactly the general-position version of
  Erdős #104 (unit circles through at least three points). The pair-codegree
  argument cannot improve without new geometry.

local_certificates:
  An exact orthocentric K4 realizes four equal circumradii, has no three
  collinear/no four concyclic, and saturates every pair codegree.
  Six- and seven-vertex twofold triple systems saturate the combinatorial
  bound while containing no K4^3.
  The six-vertex system is rigorously non-realizable: its C5 link
  parametrization reduces two circle conditions to |X+e|=|-X+e|=|e|=1,
  forcing two nominal points to coincide.

first_breakpoint:
  Extract a global realizability constraint for triple intersections of
  congruent circles; equivalently make progress on Erdős #104.

q2_assessment:
  This intake did not create a Q2 result. The already-public
  n^2 exp(O(sqrt(log n))) upper bound is paper-worthy if fully written, with
  priority belonging to its 2026-06-16 forum author.

certificate:
  scripts/validate_831.py
