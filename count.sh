#!/bin/bash
#
# Usage:
#   ./count.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

code() {
  echo 'OUR PYTHON CODE'
  wc -l polytope.py rotate.py render/generate_ply.py
  echo

  echo 'OTHER'
  wc -l schlafli/*.py
  echo

  echo 'SHELL'
  wc -l run.sh
  echo

  echo 'MODEL'
  wc -l 4d-*.template scenes/contemporary-bathroom/*.pbrt
  echo

  du --si -s scenes/contemporary-bathroom/
  echo

  du --si -s scenes/contemporary-bathroom/*
  echo
}

"$@"
