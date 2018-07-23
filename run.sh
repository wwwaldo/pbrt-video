#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

render() {
  ../other/pbrt-v3-build/pbrt scenes/killeroo-simple.pbrt
}

"$@"
