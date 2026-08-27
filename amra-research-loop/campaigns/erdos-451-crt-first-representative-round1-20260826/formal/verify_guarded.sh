#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
guard=/home/biostar/work/projects/openmath/bin/openmath-memory-guard

exec "$guard" -- bash "$here/verify_inside_guard.sh"
