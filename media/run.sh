#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

publish() {
  local destname=$1

  ssh $destname@$destname.org 'mkdir -p oilshell.org/recurse'
  rsync --archive --verbose \
    120-cell-bathroom.* $destname@oilshell.org:oilshell.org/recurse
}

"$@"
