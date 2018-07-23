#!/usr/bin/python3
from __future__ import print_function
"""
cube.py
"""

import math

import sys

from schlafli import schlafli_interpreter

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull


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


def Intersect(edges, plane_normal, p0):
  """Intersect a list of edges with a plane.

  The plane is defined by a point and a normal vector.
  """
  intersections = []
  for la, lb in edges:
    numerator = np.dot(plane_normal, la - p0)
    print('n=%f' % numerator)

    lab = lb - la
    denominator = np.dot(-lab, plane_normal)
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


def Draw(ax, edges, plane, intersections):
  p0, p1, p2 = plane

  for la, lb in edges:
    x = np.array([la[0], lb[0]])
    y = np.array([la[1], lb[1]])
    z = np.array([la[2], lb[2]])

    ax.plot(x, y, z, c='b')

  for v in (p1, p2):
    x = np.array([p0[0], v[0]])
    y = np.array([p0[1], v[1]])
    z = np.array([p0[2], v[2]])

    ax.plot(x, y, z, c='g')

  for inter in intersections:
    print(inter)
    x = np.array([inter[0]])
    y = np.array([inter[1]])
    z = np.array([inter[2]])
    ax.scatter(x, y, z, c='r')  # scatter plot of a single point


def Draw4dSlice(ax, intersections):
  """
  Args:
    intersections: a list of 4D points
  """
  for inter in intersections:
    print(inter)
    x = np.array([inter[0]])
    y = np.array([inter[1]])
    z = np.array([inter[2]])
    # TODO: How to project it?  SVD?  Or just change the axes?
    ax.scatter(x, y, z, c='r')  # scatter plot of a single point

  return

  # Change intersections to ndarray of shape (N, 3)
  print('number of intersections: %d' % len(intersections))
  inter_array = np.array(intersections)
  # No intersections?
  print(inter_array)

  hull = ConvexHull(inter_array)

  #ax.plot(intersections[:,0], intersections[:,1], intersections[:,2], 'o')
  for simplex in hull.simplices:
    ax.plot(points[simplex, 0], points[simplex, 1], points[simplex, 2], 'k-')


def main(argv):
  p0 = np.array([0.5, 0.5, 0.5])  # center of the cube
  # These are useful for plotting, but we don't quite need them (just use the
  # normal vector).
  # Does mplot3d have a plane primitive?  Or can we make a polygon/square from
  # a plane?

  p1 = np.array([1, 1, 0.5])
  p2 = np.array([1, 0.5, 1])

  plane = (p0, p1, p2)

  schlafli = [int(a) for a in sys.argv[1:]]  # e.g. 4 3 for cube
  if len(schlafli) not in (2, 3):
    raise RuntimeError('2 or 3 args required (e.g. "4 3" for cube)')
  vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)

  edge_numbers = edges_etc[0]
  vertices = [np.array(v) for v in vertices]
  print('Vertices:')
  for v in vertices:
    print(v)
  print('')

  edges = []
  for a, b in edge_numbers:
    edges.append((vertices[a], vertices[b]))

  if len(schlafli) == 2:
    p01 = p1 - p0
    p02 = p2 - p0
    plane_normal = np.cross(p01, p02)

    intersections = Intersect(edges, plane_normal, p0)

    fig = plt.figure()
    ax = fig.gca(projection='3d')  # create 3d axes?

    Draw(ax, edges, plane, intersections)

  elif len(schlafli) == 3:
    # NOTES:
    # 3 3 3 - has no intersections
    # 4 3 3 - QHull gives verbose error!  Less than 4 dimensional!

    p0 = np.array([0.5, 0.5, 0.5, 0.5])
    plane_normal = np.array([1, 2, 2, 1])

    intersections = Intersect(edges, plane_normal, p0)

    fig = plt.figure()
    ax = fig.gca(projection='3d')  # create 3d axes?

    Draw4dSlice(ax, intersections)

  else:
    raise AssertionError

  plt.show()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
