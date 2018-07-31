#!/usr/bin/python3
from __future__ import print_function
"""
polytope.py
"""

import math

import sys

from schlafli import schlafli_interpreter
from render import generate_ply

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
    #w = np.array([inter[3]])

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


SHAPES_3D = [
    (3, 3),  # tetrahedron
    (4, 3),  # cube
    (3, 4),  # octahedron
    (5, 3),  # dodecahedron
    (3, 5),  # icosahedron
]

SHAPES_4D = [
    (3, 3, 3),  # 4-simplex, like tetrahedron
    (4, 3, 3),  # 4-cube, like cube
    (3, 3, 4),  # 4-orthoplex, 16-cell, like octahedron.  dual of cube.
    (3, 4, 3),  # 24-cell, the one that is new in 4D!
    (5, 3, 3),  # 120-cell, like dodecahedron
    (3, 3, 5),  # 600-cell, like icosahedron
]

DIM_NAME = ['x', 'y', 'z', 'w']


# NOTE: The Z coordinate always appears to be positive in 3D.  But does that
# matter if we're rotating?
#
# In 4D, the w coordinate always appears to be positive.

def ShowBounds():
  for schlafli in SHAPES_3D + SHAPES_4D:
    vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)
    # Transpose.  TODO: Should schlafli return np.array, and then we do this
    # with numpy?
    dimensions = list(zip(*vertices))

    print(schlafli)
    for i, d in enumerate(dimensions):  # d is a vector
      print('%s: from %f to %f' % (DIM_NAME[i], min(d), max(d)))
    print()


def main(argv):
  try:
    action = argv[1]
  except IndexError:
    action = None

  if action == 'bounds':
    ShowBounds()
    return

  if action == 'ply':
    out_path = argv[2]
    points = np.random.rand(100, 3)
    vertices, edges_etc = schlafli_interpreter.regular_polytope([5, 3])
    vertices = [np.array(v) for v in vertices]

    # Rotate it a bit
    # TODO: Put these in a function.

    theta_z = math.pi / 8 # 30 degrees about Z axis

    rotation_z = np.array([
        [math.cos(theta_z), -math.sin(theta_z), 0.0],
        [math.sin(theta_z),  math.cos(theta_z), 0.0],
        [0.0,                          0.0, 1.0],
    ])

    theta_x = math.pi / 16
    rotation_x = np.array([
        [1.0,               0.0,                0.0],
        [0.0, math.cos(theta_x), -math.sin(theta_x)],
        [0.0, math.sin(theta_x),  math.cos(theta_x)],
    ])

    rotation = np.matmul(rotation_x, rotation_z)
    vertices = [np.matmul(rotation, v) for v in vertices]

    with open(out_path, 'w') as f:
      generate_ply.generate_ply(f, vertices,
                                template_path='render/ply-header.template')

    print('Wrote %s' % out_path)
    return

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

  # NOTE: There always seems to be a vertex at (0,0,0), but for dodecahedron
  # and others this means there are negative coordinates.  On the other hand,
  # the cube is confined to one quadrant / octant.
  #
  # I think this is because the base case in 1D is (0,), and then it gets
  # extended to (0,0), then (0,0,0), etc.

  vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)

  edge_numbers = edges_etc[0]
  vertices = [np.array(v) for v in vertices]
  print('Vertices:')
  for v in vertices:
    print(v)
    print(v.shape)
  print('')

  # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
  # NOTE: do NOT use np.matrix ?

  theta_z = math.pi / 8 # 30 degrees about Z axis

  rotation_z = np.array([
      [math.cos(theta_z), -math.sin(theta_z), 0.0],
      [math.sin(theta_z),  math.cos(theta_z), 0.0],
      [0.0,                          0.0, 1.0],
  ])

  theta_x = math.pi / 16
  rotation_x = np.array([
      [1.0,               0.0,                0.0],
      [0.0, math.cos(theta_x), -math.sin(theta_x)],
      [0.0, math.sin(theta_x),  math.cos(theta_x)],
  ])

  #rotation = np.matmul(rotation_z, np.eye(3))
  rotation = np.matmul(rotation_x, rotation_z)
  if 1:
    vertices = [np.matmul(rotation, v) for v in vertices]
  else:
    for v in vertices:
      print('V %s' % v)
      r = np.matmul(rotation, v)

  print('After rotation:')
  for v in vertices:
    print(v)
    print(v.shape)
  print('')

  # TODO: Apply rotation matrix here

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
