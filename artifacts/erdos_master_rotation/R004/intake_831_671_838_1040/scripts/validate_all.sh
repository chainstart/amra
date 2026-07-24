#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
python3 "$here/validate_831.py"
python3 "$here/validate_838.py"
python3 "$here/validate_1040.py"
python3 "$here/validate_delivery.py"
echo "R004_ALL_CERTIFICATES_AND_DELIVERY_OK"
