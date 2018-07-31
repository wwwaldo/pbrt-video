#!/bin/bash

# Runs generate_ply and renders the resulting convex set in pbrt.
# Output is saved to temp.png.
PBRT=/home/caroline/recurse/pbrt-v3/build_debug/pbrt
python3 generate_ply.py temp.ply
$PBRT convex_render.pbrt
