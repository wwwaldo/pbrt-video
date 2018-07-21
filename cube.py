#!/usr/bin/python3
from __future__ import print_function
"""
cube.py
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
  u = np.array(VERTICES[u])
  v = np.array(VERTICES[v])
  EDGES.append((u, v))

print(EDGES)

# https://en.wikipedia.org/wiki/Line%E2%80%93plane_intersection
#
# triangle: p0, p1, p2 (9 params)
# vectors: p0 -> p1
#          p0 -> p2
# but really I want to start with a normal vector and distance d?
#   Then take any two vectors in the plane that the normal vector defines0


def LinePlaneIntersect():
  pass


def main(argv):
  print('Hello from cube.py')
  p0 = np.array([0.5, 0.5, 0.5])  # center of the cube
  p1 = np.array([1, 2, 3])
  p2 = np.array([2, 1, 3])
  p01 = p1 - p0
  p02 = p2 - p0

  for la, lb in EDGES:
    cr = np.cross(p01, p02)  # isn't this just the normal vector?
    numerator = np.dot(cr, la - p0)
    print('n=%f' % numerator)

    lab = la - lb
    denominator = np.dot(-lab, cr)
    print('d=%f' % denominator)
    if denominator == 0.0:
      continue

    t = numerator / denominator
    print('t=%f' % t)
    print()

  #print(np.dot([1,2,3], [4,5,6]))
  #print(np.cross([1,2,3], [4,5,6]))

  # OK now plot the plane, the edges, and the intersection points

  fig = plt.figure()
  ax = fig.gca(projection='3d')  # create 3d axes?
  x = np.array([0, 1])
  y = np.array([0, 1])
  z = np.array([0, 1])

  ax.plot(x, y, z)

  plt.show()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
