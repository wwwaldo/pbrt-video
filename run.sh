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

readonly NUM_FRAMES=10

clean() {
  rm -v _out/pbrt/* _out/exr/* _out/jpg/*
}

frames() {
  mkdir -p _out/{pbrt,exr,jpg}

  # has to be in scenes to include the geometry file
  local out_dir=_out
  ./frames.py $NUM_FRAMES $out_dir
  ls -l $out_dir/pbrt
}

# Oops has to be in original dir
render-all() {
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
  return

  time ffmpeg -f image2 -r 1/5 -i %04d.jpg -c:v libx264 -pix_fmt yuv420p out.mp4
}

ply-demo() {
  local ply=_out/demo.ply
  ./polytope.py ply $ply
  #pbrt $ply
  pbrt render/convex_render.pbrt
}

"$@"
