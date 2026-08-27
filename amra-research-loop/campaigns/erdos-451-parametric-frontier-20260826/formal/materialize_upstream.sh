#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
source_url="https://raw.githubusercontent.com/Woett/ChatGPT-s-note-on-Erdos451/92a033fa99f0a53a3c16257c47e3d9e04dfc3f55/ErdosProblem451.lean"

curl --fail --location --silent --show-error "$source_url" --output "$here/ErdosProblem451.lean"

expected=$(cut -d' ' -f1 "$here/upstream.sha256")
actual=$(sha256sum "$here/ErdosProblem451.lean" | cut -d' ' -f1)
if [[ $actual != "$expected" ]]; then
  printf 'upstream checksum mismatch: expected=%s actual=%s\n' "$expected" "$actual" >&2
  exit 1
fi
printf 'upstream checksum OK: %s\n' "$actual"
