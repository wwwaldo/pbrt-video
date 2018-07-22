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


# mplot3d examples
# https://matplotlib.org/examples/mplot3d/

# TODO:
# - change representation of plane: normal and d
# - animate the plane in matplotlib?  Just change d.
#   - allow user to rotate the plane?
# - could make the intersection nicer?  Use a polygon to plot?

def Intersect(edges, plane):
  p0, p1, p2 = plane

  p01 = p1 - p0
  p02 = p2 - p0
  normal = np.cross(p01, p02)

  intersections = []
  for la, lb in edges:
    numerator = np.dot(normal, la - p0)
    print('n=%f' % numerator)

    lab = lb - la
    denominator = np.dot(-lab, normal)
    print('d=%f' % denominator)
    if denominator == 0.0:
      continue

    t = numerator / denominator
    print('t=%f' % t)
    print()

    inter = la + lab*t
    if 0.0 <= t <= 1.0:
      intersections.append(inter)
    else:
      print('does not intersect')
  return intersections


def Draw(edges, plane, intersections):
  p0, p1, p2 = plane

  fig = plt.figure()
  ax = fig.gca(projection='3d')  # create 3d axes?

  #x = np.array([0, 1])
  #y = np.array([0, 1])
  #z = np.array([0, 1])
  #ax.plot(x, y, z)

  for la, lb in edges:
    x = np.array([la[0], lb[0]])
    y = np.array([la[1], lb[1]])
    z = np.array([la[2], lb[2]])

    ax.plot(x, y, z)

  for v in (p1, p2):
    x = np.array([p0[0], v[0]])
    y = np.array([p0[1], v[1]])
    z = np.array([p0[2], v[2]])

    ax.plot(x, y, z)

  for inter in intersections:
    print(inter)
    x = np.array([inter[0]])
    y = np.array([inter[1]])
    z = np.array([inter[2]])
    ax.scatter(x, y, z)  # scatter plot of a single point

  plt.show()


def main(argv):
  #poly = (VERTICES, EDGES)

  p0 = np.array([0.5, 0.5, 0.5])  # center of the cube
  # These are useful for plotting, but we don't quite need them (just use the
  # normal vector).
  # Does mplot3d have a plane primitive?  Or can we make a polygon/square from
  # a plane?

  p1 = np.array([1, 1, 2])
  p2 = np.array([2, 1, 2])

  plane = (p0, p1, p2)

  intersections = Intersect(EDGES, plane)

  Draw(EDGES, plane, intersections)

  #print(np.dot([1,2,3], [4,5,6]))
  #print(np.cross([1,2,3], [4,5,6]))

  # OK now plot the plane, the edges, and the intersection points


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
