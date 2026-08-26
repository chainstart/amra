#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
generated="$here/.generated"
logs="$here/logs"
mkdir -p "$generated" "$logs"

"$here/materialize_upstream.sh" "$generated"

cd "$here"
lake update
lake exe cache get

/usr/bin/time -v lake env lean "$generated/ErdosProblem451.upstream.lean" \
  2>&1 | tee "$logs/upstream-replay.log"
grep -Fq "'main_theorem' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/upstream-replay.log"
if grep -Fq 'sorryAx' "$logs/upstream-replay.log"; then
  printf 'upstream axiom audit failed: sorryAx found\n' >&2
  exit 1
fi

patch --batch --forward "$generated/ErdosProblem451.upstream.lean" \
  < "$here/erdos451-c16.patch"

expected=$(cut -d' ' -f1 "$here/c16.sha256")
actual=$(sha256sum "$generated/ErdosProblem451.upstream.lean" | cut -d' ' -f1)
if [[ $actual != "$expected" ]]; then
  printf 'c16 checksum mismatch: expected=%s actual=%s\n' "$expected" "$actual" >&2
  exit 1
fi
printf 'c16 checksum OK: %s\n' "$actual"

/usr/bin/time -v lake env lean "$generated/ErdosProblem451.upstream.lean" \
  2>&1 | tee "$logs/c16-replay.log"
grep -Fq "'main_theorem_c16' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/c16-replay.log"
grep -Fq "'main_theorem_c16_two_k' depends on axioms: [bhp, propext, Classical.choice, Quot.sound]" \
  "$logs/c16-replay.log"
if grep -Fq 'sorryAx' "$logs/c16-replay.log"; then
  printf 'c16 axiom audit failed: sorryAx found\n' >&2
  exit 1
fi
