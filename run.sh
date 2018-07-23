#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

deps() {
  pip3 install numpy matplotlib
}

render() {
  ../other/pbrt-v3-build/pbrt scenes/killeroo-simple.pbrt
}

frames() {
  mkdir -p _out
  ./frames.py 6 _out
  ls -l _out
}

"$@"
