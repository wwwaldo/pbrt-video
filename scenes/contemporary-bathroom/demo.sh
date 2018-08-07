#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

demo() {
 if [[ "$USER" == "caroline_lin" ]]
 then
	 local pbrt=~/pbrt-exec
 else
	 local pbrt=pbrt
 fi 
 $pbrt bathroom-demo.pbrt 
}

"$@"
