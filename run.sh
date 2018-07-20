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

# On local machine

readonly EXR_DIR=~/broome/git/pbrt-video

exr-to-jpg() {
  local exr=$1
  convert $exr $(basename $exr .exr).jpg
}

all-jpg() {
  echo $EXR_DIR/?.exr | xargs --verbose -n 1 -- $0 exr-to-jpg
}


# NOTE: Tried 'convert' from imagemagick but it didn't seem to work

# https://superuser.com/questions/249101/how-can-i-combine-30-000-images-into-a-timelapse-movie

make-video() {
  # with imagemagick
  # http://jupiter.ethz.ch/~pjt/makingMovies.html 
  time convert -delay 6 -quality 95 *.jpg movie.mp4
  return

  time ffmpeg -f image2 -r 1/5 -i %01d.jpg -c:v libx264 -pix_fmt yuv420p out.mp4
}

"$@"
