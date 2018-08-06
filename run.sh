#!/bin/bash
#
# Usage:
#   ./run.sh <function name>
#
# Examples:
#
#   ./run.sh frames      # generates .pbrt files
#   ./run.sh render-all  # generates .exr files
#   ./run.sh all-jpg     # generates .jpg files
#   ./run.sh make-video  # generate .mp4 file

set -o nounset
set -o pipefail
set -o errexit

# On local machine
mount-output() {
  # NOTE: Requires host defined in ~/.ssh/config
  sshfs broome: ~/broome

  ls ~/broome/git/pbrt-video
}

# OS X deps: https://www.xquartz.org/
# Ubuntu deps: ipython3
# TODO: Try Jupyter too

# ubuntu deps
deps() {
  # scipy: for ConvexHull
  pip3 install numpy matplotlib scipy
}

pbrt() {
  ~andy/git/other/pbrt-v3-build/pbrt "$@"
}

render-simple() {
  local src=${1:-scenes/killeroo-simple.pbrt}
  pbrt $src
  #../other/pbrt-v3-build/pbrt $src
}

render-hi() {
  local src=${1:-../other/pbrt-v3-scenes/contemporary-bathroom/contemporary-bathroom.pbrt}
  pbrt --quick $src
  #../other/pbrt-v3-build/pbrt $src
}

clean() {
  rm -v _out/pbrt/* _out/exr/* _out/jpg/*
}

frames() {
  mkdir -p _out/{pbrt,exr,jpg}

  local NUM_FRAMES=10

  # has to be in scenes to include the geometry file
  local out_dir=_out
  ./frames.py $NUM_FRAMES $out_dir
  ls -l $out_dir/pbrt
}

# Oops has to be in original dir
render-killeroo-frames() {
  # TODO: xargs

  # Or just use a single command to share?
  # Why does this segfault?
  # pbrt does seem to accept multiple args.
  #pbrt scenes/k-*.pbrt
  #return

  for input in _out/pbrt/k-*.pbrt; do
    pbrt $input
  done
}

# On local machine

exr-to-jpg() {
  local exr=$1
  local name=$(basename $exr .exr)
  convert $exr _out/jpg/${name}.jpg
}

readonly NPROC=$(( $(nproc) - 1 ))

all-jpg() {
  echo _out/exr/k-*.exr | xargs --verbose -n 1 -P $NPROC -- $0 exr-to-jpg
}


# NOTE: Tried 'convert' from imagemagick but it didn't seem to work

# https://superuser.com/questions/249101/how-can-i-combine-30-000-images-into-a-timelapse-movie

make-video() {
  # with imagemagick
  # http://jupiter.ethz.ch/~pjt/makingMovies.html 
  time convert -delay 6 -quality 95 _out/jpg/k-*.jpg _out/movie.mp4
  echo "Wrote $PWD/_out/movie.mp4"
}

ply-demo() {
  #local ply=_out/demo.ply
  local ply=render/temp.ply
  ./polytope.py pbrt $ply 5 3
  #pbrt $ply
  pbrt render/convex_render.pbrt
}

gen-pbrt-4d() {
  local out_dir=_out/4d
  mkdir -p $out_dir
  NUM_FRAMES=20 ./polytope.py pbrt $out_dir 5-3-3_frame%02d 5 3 3

  ls -l $out_dir
}

# Oops has to be in original dir
render-4d() {
  for input in _out/4d/*.pbrt; do
    pbrt $input
  done
}

video-4d() {
  time convert -delay 6 -quality 95 _out/4d/*.png _out/4d.mp4
  echo "Wrote $PWD/_out/4d.mp4"
}


"$@"
