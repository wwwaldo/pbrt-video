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

deps() {
  pip3 install numpy matplotlib
}

render() {
  local src=${1:-scenes/killeroo-simple.pbrt}
  ~andy/git/other/pbrt-v3-build/pbrt $src
  #../other/pbrt-v3-build/pbrt $src
}

readonly NUM_FRAMES=10

clean() {
  rm -v scenes/k-*.pbrt
}

frames() {
  mkdir -p _out/{exr,jpg}

  # has to be in scenes to include the geometry file
  local out_dir=scenes
  ./frames.py $NUM_FRAMES $out_dir
  ls -l $out_dir/k-*.pbrt
}

# Oops has to be in original dir
render-all() {
  # TODO: xargs
  # Or just use a single command to share?
  for input in scenes/k-*.pbrt; do
    render $input
  done
}

# On local machine

exr-to-jpg() {
  local exr=$1
  local name=$(basename $exr .exr)
  convert $exr _out/jpg/${name}.jpg
}

all-jpg() {
  echo _out/exr/k-*.exr | xargs --verbose -n 1 -P 2 -- $0 exr-to-jpg
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

"$@"
