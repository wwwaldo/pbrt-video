#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

readonly PLACEHOLDER='<!-- REPLACE HERE -->'

readonly ORIG_LINK='<p><a href="http://oilshell.org/recurse/120-cell-bathroom.original.html">Original Copy</a></p>'

readonly MIRROR_LINK='<p><a href="https://andychu.github.io/recurse/120-cell-bathroom.mirror.html">Github Mirror</a> (in case the video does not load)</p>'

build-html() {
  mkdir -p _tmp
  sed "s;$PLACEHOLDER;$MIRROR_LINK;" media/120-cell-bathroom.html \
    > _tmp/120-cell-bathroom.original.html
  sed "s;$PLACEHOLDER;$ORIG_LINK;" media/120-cell-bathroom.html \
    > _tmp/120-cell-bathroom.mirror.html
}

video() {
  local destname=$1

  ssh $destname@$destname.org 'mkdir -p oilshell.org/recurse'
  rsync --archive --verbose \
    media/120-cell-bathroom.mp4 \
    $destname@$destname.org:oilshell.org/recurse

  rsync --archive --verbose \
    _tmp/120-cell-bathroom.original.html \
    $destname@$destname.org:oilshell.org/recurse
}

github-mirror() {
  cp -v -f media/120-cell-bathroom.mp4 ../andychu.github.io/recurse
  cp -v -f _tmp/120-cell-bathroom.mirror.html ../andychu.github.io/recurse
}

"$@"
