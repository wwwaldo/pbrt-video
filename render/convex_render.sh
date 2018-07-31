#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

# Runs generate_ply and renders the resulting convex set in pbrt.
# Output is saved to temp.png.
if test $USER = 'andy'; then
  PBRT=/home/andy/git/other/pbrt-v3-build/pbrt
else
  PBRT=/home/caroline/recurse/pbrt-v3/build_debug/pbrt
fi
./generate_ply.py temp.ply
$PBRT convex_render.pbrt
