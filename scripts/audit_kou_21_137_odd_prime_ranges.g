# Independent explicit audit for the bounded KOU-21.137 odd-prime scans.
#
# Run with the repository's isolated GAP installation:
#
#   GAP_BIN=/home/biostar/.cache/amra/tools/gap-4.12.1/usr/lib/x86_64-linux-gnu/gap/gap
#   GAP_ROOT=/home/biostar/.cache/amra/tools/gap-4.12.1/usr/share/gap
#   "$GAP_BIN" -l "$GAP_ROOT" -q scripts/audit_kou_21_137_odd_prime_ranges.g

LoadPackage("smallgrp");;

CheckOddPowerOrder := function(p, order)
  local groupCount, exponentCount, closedCount, maxImage, candidates,
        id, G, image, closed, noncommuting, a, b;

  groupCount := NumberSmallGroups(order);
  exponentCount := 0;
  closedCount := 0;
  maxImage := 0;
  candidates := 0;

  for id in [1..groupCount] do
    G := SmallGroup(order, id);
    if Exponent(G) = p^2 then
      exponentCount := exponentCount + 1;
      image := Set(Elements(G), g -> g^p);
      maxImage := Maximum(maxImage, Length(image));
      closed := true;
      noncommuting := false;
      for a in image do
        if not a^-1 in image then
          closed := false;
        fi;
        for b in image do
          if not a*b in image then
            closed := false;
          fi;
          if a*b <> b*a then
            noncommuting := true;
          fi;
        od;
      od;
      if closed then
        closedCount := closedCount + 1;
        if noncommuting then
          candidates := candidates + 1;
        fi;
      fi;
    fi;
  od;

  Print(
    "ORDER|", p, "|", order, "|", groupCount, "|", exponentCount,
    "|", closedCount, "|", maxImage, "|", candidates, "\n"
  );
  return [groupCount, exponentCount, closedCount, candidates];
end;;

specs := [
  [3, 27], [3, 81], [3, 243], [3, 729],
  [5, 125], [5, 625], [7, 343], [11, 1331],
  [13, 2197], [17, 4913], [19, 6859], [23, 12167]
];;
totals := [0, 0, 0, 0];;

for spec in specs do
  row := CheckOddPowerOrder(spec[1], spec[2]);;
  for index in [1..4] do
    totals[index] := totals[index] + row[index];
  od;
od;

Print(
  "TOTAL|", totals[1], "|", totals[2], "|", totals[3], "|",
  totals[4], "\n"
);
QUIT;
