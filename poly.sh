#!/bin/bash
#
# Usage:
#   ./poly.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

schlafi() {
  schlafli/schlafli_interpreter.py "$@"
}

tetra() { schlafi 3 3; }

cube() { schlafi 4 3; }

octa() { schlafi 3 4; }

dodeca() { schlafi 5 3; }

icosa() { schlafi 3 5; }

"$@"
