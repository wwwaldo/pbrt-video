#!/usr/bin/python3
from __future__ import print_function
"""
cube.py
"""

import sys

from schlafli import schlafli_interpreter

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
  p0 = np.array([0.5, 0.5, 0.5])  # center of the cube
  # These are useful for plotting, but we don't quite need them (just use the
  # normal vector).
  # Does mplot3d have a plane primitive?  Or can we make a polygon/square from
  # a plane?

  p1 = np.array([1, 1, 0.5])
  p2 = np.array([1, 0.5, 1])

  plane = (p0, p1, p2)

  CUBE = [3, 5]
  vertices, edges_etc = schlafli_interpreter.regular_polytope(CUBE)

  edge_numbers = edges_etc[0]
  vertices = [np.array(v) for v in vertices]

  edges = []
  for a, b in edge_numbers:
    edges.append((vertices[a], vertices[b]))

  intersections = Intersect(edges, plane)

  Draw(edges, plane, intersections)


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
