#!/bin/bash
#
# Usage:
#   ./run.sh <function name>

set -o nounset
set -o pipefail
set -o errexit

to-html() {
  local path=$1
  local title=$2
  local date=$3

  cat <<EOF
<html>
  <head>
    <title>$title</title>
    <style>
      body {
        margin: 1em auto;
        width: 40em;
        font-size: x-large;
      }
      h2 {
        text-align: center;
      }
      table {
        font-size: x-large;
      }
      thead {
        font-weight: bold;
        color: green;
      }
      .table-row-label{
        font-weight: bold;
        color: green;
      }
      td {
        padding: 0.5em;
        border-bottom: solid 1px grey;
      }

      code {
        color: green;
      }
      pre {
        color: green;
    }
    </style>
  </head>
  <body>
    <p style="text-align: right; font-style: italic">Andy Chu and Caroline Lin &mdash; $date</p>
EOF

  cmark $path

  cat <<EOF
  </body>
</html>
EOF
}

build() {
  to-html slides.md "" "2018/08/29" > ~/vm-shared/08-09-pres.html
}


"$@"
