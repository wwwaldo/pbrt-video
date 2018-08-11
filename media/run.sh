#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

# User must set DESTNAME

publish() {
  ssh $DESTNAME@$DESTNAME.org 'mkdir -p oilshell.org/recurse'
  rsync --archive --verbose \
    120-cell-bathroom.* $DESTNAME@oilshell.org:oilshell.org/recurse
}

"$@"
