#!/usr/bin/python
from __future__ import print_function
"""
cube.py
"""

import sys

# TODO: Generate these
VERTICES = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1),
]

# https://codegolf.stackexchange.com/questions/114280/schl%C3%A4fli-convex-regular-polytope-interpreter
v = VERTICES
EDGE_STR = """
0 1
0 2
0 4
1 3
1 5
2 3
2 6
3 7
4 5
4 6
5 7
6 7
"""

EDGES = []
for line in EDGE_STR.splitlines():
  if not line:
    continue
  u, v = line.split()
  u = int(u)
  v = int(v)
  EDGES.append((VERTICES[u], VERTICES[v]))

print(EDGES)


def main(argv):
  print('Hello from cube.py')


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
