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
    <p style="text-align: right; font-style: italic">Andy Chu &mdash; $date</p>
EOF

  cmark $path

  cat <<EOF
  </body>
</html>
EOF
}

05-24-pres() {
  mkdir -p _tmp
  to-html 05-24-pres/05-24-pres.md "xargs -P" "2018/05/28" > ~/vm-shared/05-24-pres.html
}

2-pres() {
  mkdir -p _tmp
  to-html 05-31-pres/slides.md "Regular Languages" "2018/6/7" > ~/vm-shared/05-31-pres.html
}

share2() {
  scp ~/vm-shared/05-31-pres.html chubot@chubot.org:oilshell.org/share/
}

3-pres() {
  to-html 06-14-pres/slides.md "Unicode" "2018/6/21" > ~/vm-shared/06-14-pres.html
  cp -v 06-14-pres/escaped.html ~/vm-shared
}


"$@"
