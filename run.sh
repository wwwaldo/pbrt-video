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
#
# Quick polytope:
#
#   ./run.sh all-120-cell
#
# Bathroom:
#
# Once:
#   ./run.sh prepare-bathroom  # copy files into the right place
#   ./run.sh sky-exr           # run imgtool
#
# Each time:
#   ./run.sh gen-pbrt-bathroom  OR
#   ./run.sh gen-pbrt-bathroom-quick   (fewer frames)
#   ./run.sh render-bathroom           # takes a couple minutes
#   ./run.sh video-bathroom
#
# Distributed bathroom rendering:
#
# Once:
#   ./run.sh copy-pbrt-bin   # copy the binary (one-time setup)o
#
# On "master" machine:

#   - Check that MACHINES in this shell script is what you want.
#   - Set FRAMES_PER_MACHINE
#
#   ./run.sh gen-pbrt-bathroom to generates input files
#
#   MAYBE: ./run.sh remove-remote  # if there is anythinng left over
#   ./run.sh copy-pbrt-bathroom
#
# On each machine in a tmux session:j
#
#   cd ~/pbrt-video
#   ./run.sh dist-render-bathroom
#
# Back on the master machine:
#
#   ./run.sh copy-remote-png
#   ./run.sh video-remote-bathroom

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

# $USER is expanded on the local machine.
readonly PBRT_REMOTE=/home/$USER/bin/pbrt 
readonly ANDY_PBRT_BUILD=~andy/git/other/pbrt-v3-build/pbrt 

pbrt() {
  if [[ "$USER" == "caroline_lin" ]]; then
    ~/pbrt-exec "$@"
  elif [[ "$USER" == "andy" ]]; then
    $ANDY_PBRT_BUILD "$@"
  else
    echo "Caroline: please only run this on Heap!"
    exit 1
  fi
}

copy-pbrt-bin() {
  local dir=$(dirname $PBRT_REMOTE)
  for machine in ${MACHINES[@]}; do
    ssh $machine "mkdir -v -p $dir"
    rsync --archive --verbose $ANDY_PBRT_BUILD $machine:$dir/
  done
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

join-frames() {
  local out=$1
  shift

  # 41.66 ms is 24 fps
  # ticks are 10ms, so delay is 4.166
  #local delay=4.1666
  local delay=10

  #local delay=50

  time convert -delay $delay -quality 95 "$@" $out
  echo "Wrote $out"
}

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

# TODO: Parameterize over different polytopes!  Give them different names.
gen-pbrt-4d() {
  local sch=${1:-'5-3-3'}  # schlafli number
  local num_frames=${2:-48}

  local out_dir=_out/4d/$sch
  mkdir -p $out_dir
  rm -v -f $out_dir/*

  # split 5 3 3 into 5 3 3
  local -a sch_array=( ${sch//-/ } )
  ./polytope.py \
    --num-frames $num_frames \
    --camera '120cell' \
    --out-dir $out_dir \
    --out-template ${sch}_frame%02d \
    pbrt "${sch_array[@]}"

  ls -l $out_dir
}

gen-all-4d() {
  # This one gives a Convex Hull error
  #gen-pbrt-4d 3-3-3
  gen-pbrt-4d 4-3-3
  gen-pbrt-4d 3-4-3
  gen-pbrt-4d 3-3-4
  gen-pbrt-4d 5-3-3
  gen-pbrt-4d 3-3-5
}

render-4d() {
  # 3:38 for 5 low quality videos
  time for input in _out/4d/*/*.pbrt; do
    pbrt $input
  done
}

video-4d() {
  for dir in _out/4d/*; do
    if ! test -d $dir; then
      continue
    fi
    local name=$(basename $dir)
    local out=_out/4d/$name.mp4
    join-frames $out $dir/*.png 
    echo "Wrote $out"
  done
}

# A particular one

gen-120-cell() {
  gen-pbrt-4d 5-3-3 20
}

# 1:01 at low quality
render-120-cell() {
  rm -v -f _out/4d/5-3-3/*.png
  time for input in _out/4d/5-3-3/*.pbrt; do
    pbrt $input
  done
}

video-120-cell() {
  join-frames _out/4d/5-3-3.mp4 _out/4d/5-3-3/*.png 
}

all-120-cell() {
  gen-120-cell
  render-120-cell
  video-120-cell
}

# Must be a relative path
readonly BATHROOM_OUT=_out/4d/bathroom

# Put everything in the right dirs.
prepare-bathroom() {
  local out_dir=${1:-$BATHROOM_OUT}
  rm -r -f $out_dir
  mkdir -p $out_dir

  for dir in scenes/contemporary-bathroom/{geometry,spds,textures}; do
    cp -r $dir $out_dir
  done

  cp scenes/contemporary-bathroom/contemporary_bathroom.blend $out_dir

  cp scenes/contemporary-bathroom/geometry.pbrt $out_dir/geometry
  cp scenes/contemporary-bathroom/materials.pbrt $out_dir/geometry

  ls -l $out_dir
}

#readonly -a MACHINES=( {spring,mercer,crosby}.cluster.recurse.com )
# crosby is down
readonly -a MACHINES=( {spring,mercer,broome}.cluster.recurse.com )
#readonly -a MACHINES=( {spring,mercer}.cluster.recurse.com )
readonly NUM_MACHINES=${#MACHINES[@]}

readonly FRAMES_PER_MACHINE=30
#readonly FRAMES_PER_MACHINE=10
readonly NUM_BATHROOM_FRAMES=$(( FRAMES_PER_MACHINE * NUM_MACHINES ))

# Run log:
#  5 frames/machine,  64 pixel samples, 3 depth: 3 minutes on each machine
#                   This is 30 seconds/frame instead of 10 seconds with 32.
#     
# 30 frames/machine, 128 pixel samples, 3 depth: 30 minutes on each machine
#                   This is 60-70 seconds/frame
#                   90 frames ended up at about 11 seconds.  Looks OK.
#
# samples=128,depth=6, 500x500: 120 seconds per frame

# samples=512,depth=6, 500x500: I think this should be 8 minutes per frame.
# 8 minutes * 30 frames = 240 minutes = 4 hours

gen-pbrt-bathroom() {
  local out_dir=$BATHROOM_OUT
  rm -v -f $out_dir/frame*.{ply,pbrt,png}

  ./polytope.py \
    --num-frames $NUM_BATHROOM_FRAMES \
    --frame-template 4d-contemporary-bathroom.template \
    --width 4800 \
    --height 4800 \
    --pixel-samples 32 \
    --integrator-depth 3 \
    --out-dir $out_dir  \
    --out-template 'frame%03d' \
    --camera bathroom \
    pbrt 5 3 3

  ls $out_dir
}

gen-pbrt-bathroom-quick() {
  local out_dir=$BATHROOM_OUT
  rm -v -f $out_dir/frame*.{ply,pbrt,png}

  ./polytope.py \
    --num-frames 10 \
    --frame-template 4d-contemporary-bathroom.template \
    --width 400 \
    --height 400 \
    --pixel-samples 16 \
    --integrator-depth 3 \
    --out-dir $out_dir  \
    --out-template 'frame%03d' \
    --camera bathroom \
    pbrt 5 3 3
    #--camera fixed \

  ls $out_dir
}

gen-pbrt-bathroom-pngtest() {
  local out_dir=$BATHROOM_OUT
  rm -v -f $out_dir/frame*.{ply,pbrt,png}

  ./polytope.py \
    --num-frames 1 \
    --frame-template 4d-contemporary-bathroom.template \
    --width 4800 \
    --height 4800 \
    --pixel-samples 16 \
    --integrator-depth 3 \
    --out-dir $out_dir  \
    --out-template 'frame%03d' \
    --camera bathroom \
    pbrt 5 3 3
    #--camera fixed \
    #--exr \

  ls $out_dir
}


# Normally we rsync but this is if you want to start over.
remove-remote-dirs() {
  for machine in "${MACHINES[@]}"; do
    echo "=== $machine"
    ssh $machine "rm -r -f -v /home/$USER/pbrt-video/"
  done
}

remove-remote-old() {
  for machine in "${MACHINES[@]}"; do
    echo "=== $machine"
    ssh $machine "rm -r -f -v /home/$USER/pbrt-video/$BATHROOM_OUT/*.{ply,pbrt,png}"
  done
}

readonly JOIN_DIR=_out/4d/remote-bathroom

copy-remote-png() {
  local dir=$JOIN_DIR
  mkdir -p $dir
  rm -f -v $dir/*
  for machine in "${MACHINES[@]}"; do
    echo "=== $machine"
    rsync --archive --verbose \
      "$machine:/home/$USER/pbrt-video/$BATHROOM_OUT/*.png" $dir/
  done
}

copy-pbrt-bathroom() {
  local i=0
  for machine in "${MACHINES[@]}"; do
    echo "=== $machine"

    ssh $machine "mkdir -p /home/$USER/pbrt-video/$BATHROOM_OUT/"

    # TODO: I think this needs a job ID.  Because we render locally and then
    # copy the files to the remote machines, which isn't right.
    rsync --archive --verbose \
      $BATHROOM_OUT/ "$machine:/home/$USER/pbrt-video/$BATHROOM_OUT/"

    # So we can run ./run.sh dist-render-bathroom on each machine
    rsync --archive --verbose \
      $0 "$machine:/home/$USER/pbrt-video/"

    echo $i > worker-id.txt

    rsync --archive --verbose \
      worker-id.txt "$machine:/home/$USER/pbrt-video/"

    (( i++ )) || true  # bash annoyance with errexit!
  done
}

# Do mod-sharding on worker ID!
should-render-frame() {
  local path=$1
  local worker_id=$2

  python3 -c '
import re
import sys

num_workers = int(sys.argv[1])
path = sys.argv[2]
worker_id = int(sys.argv[3])

m = re.search("frame(\d+)", path)
if not m:
  print("INVALID PATH %s" % path)
  sys.exit(2)

frame_number = int(m.group(1))

# mod sharding!
should_render = (frame_number % num_workers == worker_id)
sys.exit(0 if should_render else 1)

  ' $NUM_MACHINES $path $worker_id
}

dist-render-bathroom() {
  local worker_id=$(cat worker-id.txt)
  local hostname=$(hostname)
  time for input in ~/pbrt-video/$BATHROOM_OUT/frame*.pbrt; do
    if should-render-frame $input $worker_id; then
      echo
      echo "=== $input on $hostname ==="
      echo
      # 22 hyperthreads out of 24, or 11 out of 12 cores.
      $PBRT_REMOTE --nthreads 22 $input
    fi
  done

  # So we can inspect each machine
  date > finish-time.txt
  echo
  echo FINISHED
  cat finish-time.txt
}

# 1:01 at low quality
render-bathroom() {
  rm -v -f $BATHROOM_OUT/*.png
  time for input in $BATHROOM_OUT/frame*.pbrt; do
    pbrt $input
  done
}

video-bathroom() {
  join-frames _out/4d/bathroom.mp4 $BATHROOM_OUT/*.png 
}

video-remote-bathroom() {
  #join-frames _out/4d/remote-bathroom.mp4 $JOIN_DIR/*.png 
  join-frames _out/4d/remote-bathroom.mp4 $JOIN_DIR/*.800x800.png 
}

backup-mp4() {
  ssh spring.cluster.recurse.com 'mkdir -p backup'

  # Wow this has a horrible syntax!  Not sure why I need the first --include.
  # For subdirectories?

  # https://stackoverflow.com/questions/11111562/rsync-copy-over-only-certain-types-of-files-using-include-option
  rsync --archive --verbose --recursive \
    --include '*/' --include '*.mp4' --exclude '*' \
    _out/4d/ spring.cluster.recurse.com:backup/
}

# ORIGINAL COMMAND
make_sky () {
  ~/andy-pbrt/imgtool makesky -elevation 40 --outfile textures/sky.exr 
}

sky-exr() {
  local out=$BATHROOM_OUT/textures/sky.exr 
  time ~/git/other/pbrt-v3-build/imgtool makesky \
    -elevation 40 --outfile $out
  ls -l $out
}

resize-one() {
  local in=$1
  local out=${in//.png/.800x800.png}
  # targeting 1280x800
  time convert $in -resize '800x800' $out
}

resize-remote() {
  echo $JOIN_DIR/*.png | xargs --verbose -n 1 -P $NPROC -- $0 resize-one
}

if test $(basename $0) = 'run.sh'; then
  "$@"
fi
