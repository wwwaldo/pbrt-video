#!/bin/bash
#
# Usage:
#   ./pres.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

matplot-3d() {
  ./polytope.py --num-frames 20 anim 5 3   # RED DOTS
}

# 3D wireframe, then animation
matplot-4d() {
  ./polytope.py --num-frames 20 anim 5 3 3
}

"$@"
