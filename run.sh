#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

mount-output() {
  # NOTE: Requires host defined in ~/.ssh/config
  sshfs broome: ~/broome

  ls ~/broome/git/pbrt-video
}

deps() {
  pip3 install numpy matplotlib
}

render() {
  local src=${1:-scenes/killeroo-simple.pbrt}
  ~andy/git/other/pbrt-v3-build/pbrt $src
  #../other/pbrt-v3-build/pbrt $src
}

readonly NUM_FRAMES=10

frames() {
  mkdir -p _out
  local out_dir=scenes  # has to be in out dir
  ./frames.py $NUM_FRAMES $out_dir
  ls -l $out_dir/*.pbrt
}

# Oops has to be in original dir
render-all() {
  # TODO: xargs
  for input in scenes/*.pbrt; do
    render $input
  done
}


"$@"
