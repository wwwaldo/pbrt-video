#!/bin/bash
#
# Usage:
#   ./quality.sh <function name>
#
# Example:
#   ./quality.sh prepare
#   ./quality.sh run-all

set -o nounset
set -o pipefail
set -o errexit

. run.sh

# tasks
#
# 4096 and 3 is 40 minutes
#
gen-tasks() {
  for depth in 3 5; do
    for dim in 500 1200; do
    #for dim in 400 600; do
      #for pixel_samples in 512 1024 2048; do
      for pixel_samples in 64 128 256;
      #for pixel_samples in 16 32; do
        echo $dim $pixel_samples $depth
      done
    done
  done
}

do-task() {
  local dim=$1
  local pixel_samples=$2
  local depth=$3

  local out_dir='_quality/out'

  ./polytope.py \
    --num-frames 1 \
    --frame-template 4d-contemporary-bathroom.template \
    --width $dim \
    --height $dim \
    --pixel-samples $pixel_samples \
    --integrator-depth $depth \
    --out-dir "$out_dir" \
    --out-template "quality-${dim}-${pixel_samples}-${depth}__frame%03d" \
    pbrt 5 3 3

  # Hack
  local input="$out_dir/quality-${dim}-${pixel_samples}-${depth}__frame000.pbrt"

  # 22 hyperthreads out of 24, or 11 out of 12 cores.
  time-py \
    --tsv \
    --output $TIMES_OUT \
    --field "$dim" \
    --field "$pixel_samples" \
    --field "$depth" \
    -- $PBRT_REMOTE --nthreads 22 $input
}

readonly HEADER=$'status\telapsed_secs\tdim\tpixel_samples\tdepth\t'
readonly TIMES_OUT='_quality/times.tsv'

readonly OUT_DIR=_quality/out

run-all() {
  echo $HEADER > $TIMES_OUT
  mkdir -p $OUT_DIR
  gen-tasks > _quality/tasks.txt
  cat _quality/tasks.txt | xargs -n 3 -- $0 do-task

  ls -l _quality
}

time-py() {
  ~/git/oilshell/oil/benchmarks/time.py "$@"
}

prepare() {
  mkdir -p $OUT_DIR
  prepare-bathroom $OUT_DIR
}


"$@"
