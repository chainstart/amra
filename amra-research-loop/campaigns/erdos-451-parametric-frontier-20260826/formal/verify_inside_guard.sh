#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
logs="$here/logs"
mkdir -p "$logs"

"$here/materialize_upstream.sh"

cd "$here"
lake update
lake exe cache get

/usr/bin/time -v lake build ErdosProblem451 2>&1 | tee "$logs/upstream-build.log"
/usr/bin/time -v lake env lean FrontierLemmas.lean 2>&1 | tee "$logs/frontier-build.log"
/usr/bin/time -v lake build ParametricInterface 2>&1 | tee "$logs/interface-build.log"
/usr/bin/time -v lake build ParametricRanges 2>&1 | tee "$logs/ranges-build.log"

grep -Fq "'large_asym_of_margins' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$logs/frontier-build.log"
grep -Fq "'erdos451_bhp_frontier' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/frontier-build.log"
if grep -Fq 'sorryAx' "$logs/frontier-build.log"; then
  printf 'frontier axiom audit failed: sorryAx found\n' >&2
  exit 1
fi
grep -Fq "'parametric_frontier_interface' depends on axioms: [propext, Classical.choice, Quot.sound]" \
  "$logs/interface-build.log"
grep -Fq "'erdos451_bhp_frontier_via_interface' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/interface-build.log"
if grep -Fq 'sorryAx' "$logs/interface-build.log"; then
  printf 'parametric interface axiom audit failed: sorryAx found\n' >&2
  exit 1
fi
for theorem in \
  ParametricSmall.case_small \
  ParametricMed.case_medium \
  ParametricML.case_mediumlarge
do
  grep -Fq "'$theorem' depends on axioms: [propext, Classical.choice, Quot.sound]" \
    "$logs/ranges-build.log"
done
if grep -Fq 'sorryAx' "$logs/ranges-build.log"; then
  printf 'parametric ranges axiom audit failed: sorryAx found\n' >&2
  exit 1
fi

sha256sum ErdosProblem451.lean FrontierLemmas.lean ParametricInterface.lean \
  ParametricRanges.lean \
  lakefile.toml lake-manifest.json \
  lean-toolchain upstream.sha256 > "$logs/final-sha256.txt"
