#!/usr/bin/python3
from __future__ import print_function
"""
polytope.py
"""

import math
from math import sin, cos

import sys

from schlafli import schlafli_interpreter
from render import generate_ply

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
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
    #print('n=%f' % numerator)

    lab = lb - la
    denominator = np.dot(-lab, plane_normal)
    #print('d=%f' % denominator)
    if denominator == 0.0:
      continue

    t = numerator / denominator
    #print('t=%f' % t)
    #print()

    inter = la + lab*t
    if 0.0 <= t <= 1.0:
      intersections.append(inter)
    else:
      #print('does not intersect')
      pass

  if 0:
    print('Intersections:')
    for p in intersections:
      print('  %s' % p)

    # We know we made the Z axis zero
    print('2D:')
    for p in intersections:
      p2 = np.array(p[0:2])
      print('  %s' % p2)

  return intersections


def Draw(ax, edges, plane, intersections):
  """Returns matplotlib objects that can be mutated for animation.

  Returns:
    mpl_lines: list of Line3D
    mpl_points: a single Path3DCollection
  """
  #p0, p1, p2 = plane

  mpl_lines = []
  for la, lb in edges:
    x = np.array([la[0], lb[0]])
    y = np.array([la[1], lb[1]])
    z = np.array([la[2], lb[2]])

    p = ax.plot(x, y, z, c='b')
    mpl_lines.append(p[0])  # Not sure why it's p[0]

  if 0:
    for v in (p1, p2):
      x = np.array([p0[0], v[0]])
      y = np.array([p0[1], v[1]])
      z = np.array([p0[2], v[2]])

      ax.plot(x, y, z, c='g')

  # Plot intersections all at once
  intersections = np.array(intersections)
  x = intersections[:, 0]  # all rows, first column
  y = intersections[:, 1]
  z = intersections[:, 2]
  mpl_points = ax.scatter(x, y, z, c='r')

  return mpl_lines, mpl_points


def Draw4dSlice(ax, intersections):
  """
  Args:
    intersections: a list of 4D points
  """
  inter  = np.array(intersections)
  x = inter[:, 0]  # all rows, first column
  y = inter[:, 1]
  z = inter[:, 2]
  mpl_points = ax.scatter(x, y, z, c='r')

  hull = ConvexHull(inter)

  # Plot each triangle
  for simplex in hull.simplices:
    # Make it a closed loop!
    to_plot = np.append(simplex, simplex[0])
    ax.plot(inter[to_plot, 0], inter[to_plot, 1], inter[to_plot, 2],
            c='b')


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


def Tilt3D(vertices):
  """
  Tilt the vertices so we get a more interesting intersection

  https://www.learnopencv.com/rotation-matrix-to-euler-angles/
  NOTE: do NOT use np.matrix ?
  """
  theta_z = math.pi / 8 # 30 degrees about Z axis

  rotation_z = np.array([
      [cos(theta_z), -sin(theta_z), 0.0],
      [sin(theta_z),  cos(theta_z), 0.0],
      [0.0,                    0.0, 1.0],
  ])

  theta_x = math.pi / 6
  rotation_x = np.array([
      [1.0,          0.0,           0.0],
      [0.0, cos(theta_x), -sin(theta_x)],
      [0.0, sin(theta_x),  cos(theta_x)],
  ])

  rotation = np.matmul(rotation_x, rotation_z)
  return [np.matmul(rotation, v) for v in vertices]


def Tilt4D(vertices):
  """
  4D version of above:
  """
  theta_xy = math.pi / 8

  rotation_xy = np.array([
      [ cos(theta_xy), sin(theta_xy), 0, 0],
      [-sin(theta_xy), cos(theta_xy), 0, 0],
      [             0,             0, 1, 0],
      [             0,             0, 0, 1],
  ])

  theta_xz = math.pi / 20
  rotation_xz = np.array([
      [ cos(theta_xz), 0, sin(theta_xz), 0],
      [0,              1,             0, 0],
      [-sin(theta_xz), 0, cos(theta_xz), 0],
      [0,              0,             0, 1],
  ])

  theta_zw = math.pi / 16
  rotation_zw = np.array([
      [1, 0,             0,              0 ],
      [0, 1,             0,              0 ],
      [0, 0, cos(theta_zw), -sin(theta_zw) ],
      [0, 0, sin(theta_zw),  cos(theta_zw) ],
  ])

  # TODO: I think I should tilt it in 3 directions, every one except Z axis?
  # Actually there are 6 ways to rotate!  And we should rotate all of them
  # except 1?
  # http://hollasch.github.io/ray4/Four-Space_Visualization_of_4D_Objects.html#s2.2

  rotation = np.matmul(rotation_xy, rotation_xz, rotation_zw)
  return [np.matmul(rotation, v) for v in vertices]


def Translate3D(vertices, z_delta):
  offset = np.array([0, 0, z_delta])
  return [v + offset for v in vertices]


def Translate4D(vertices, w_delta):
  offset = np.array([0, 0, 0, w_delta])
  return [v + offset for v in vertices]


def PrintBounds(vertices):
  """For debugging."""
  x = [v[0] for v in vertices]
  y = [v[1] for v in vertices]
  z = [v[2] for v in vertices]
  w = [v[3] for v in vertices]
  print('x: %f - %f' % (min(x), max(x)))
  print('y: %f - %f' % (min(y), max(y)))
  print('z: %f - %f' % (min(z), max(z)))
  print('w: %f - %f' % (min(w), max(w)))
  #print('w: %s' % sorted(w))


# NOTE: It might be better to separate this into Plot3D and Plot4D.
def Plot(schlafli):
  #p0 = np.array([0.5, 0.5, 0.5])  # center of the cube

  p0 = np.array([0, 0, 0])
  # These are useful for plotting, but we don't quite need them (just use the
  # normal vector).
  # Does mplot3d have a plane primitive?  Or can we make a polygon/square from
  # a plane?

  #p1 = np.array([1, 1, 0.5])
  #p2 = np.array([1, 0.5, 1])

  p1 = np.array([1.0, 0.0, 0.0])
  p2 = np.array([0.0, 1.0, 0.0])

  plane = (p0, p1, p2)

  # NOTE: There always seems to be a vertex at (0,0,0), but for dodecahedron
  # and others this means there are negative coordinates.  On the other hand,
  # the cube is confined to one quadrant / octant.
  #
  # I think this is because the base case in 1D is (0,), and then it gets
  # extended to (0,0), then (0,0,0), etc.

  vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)

  vertices = [np.array(v) for v in vertices]
  if 0:
    print('Vertices:')
    for v in vertices:
      print(v)
      print(v.shape)
    print('')

  # TODO: We could probably generalize this.
  if len(schlafli) == 2:
    vertices = Tilt3D(vertices)
    # Move everything down a bit
    vertices = Translate3D(vertices, -0.1)

  elif len(schlafli) == 3:
    vertices = Tilt4D(vertices)

  else:
    raise AssertionError

  edge_numbers = edges_etc[0]
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

    mpl_lines, mpl_points = Draw(ax, edges, plane, intersections)
    if 0:
      print('Lines')
      for li in mpl_lines:
        print(li)
      print('points')
      print(mpl_points)
    plt.show()

  elif len(schlafli) == 3:
    num_frames = 40

    if 1:
      PrintBounds(vertices)

    # Calculate W range AFTER ROTATION.
    w = [v[3] for v in vertices]
    w_offsets = np.linspace(-max(w), -min(w), num=num_frames)

    print('w_offsets:')
    print(w_offsets)

    #p0 = np.array([0.5, 0.5, 0.5, 0.5])
    #plane_normal = np.array([1, 2, 2, 1])

    # Set W axis
    p0 = np.array([0, 0, 0, 0])
    plane_normal = np.array([0, 0, 0, 1])

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Set axes so they don't move between frames
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    z = [v[2] for v in vertices]
    ax.set_xlim(min(x), max(x))
    ax.set_ylim(min(y), max(y))
    ax.set_zlim(min(z), max(z))

    if 1:
      print('NEW w_offsets %s' % w_offsets)
      for i, w_offset in enumerate(w_offsets):
        print('--- OFFSET %d = %f' % (i, w_offset))

        translated = Translate4D(vertices, w_offset)
        PrintBounds(translated)

        edges = []
        for a, b in edge_numbers:
          edges.append((translated[a], translated[b]))

        intersections = Intersect(edges, plane_normal, p0)
        print('%d intersections' % len(intersections))

        # Remove w-axis to project onto hyperplane (not strictly necessary)
        intersections = [np.array(v[:3]) for v in intersections]

        Draw4dSlice(ax, intersections)
        plt.pause(0.001)

        # Remove previous plots
        del ax.collections[:]

    else:
     # A single plot
      vertices = Translate4D(vertices, -0.1)
      edges = []
      for a, b in edge_numbers:
        edges.append((vertices[a], vertices[b]))

      intersections = Intersect(edges, plane_normal, p0)
      print('%d intersections' % len(intersections))

      # Remove w-axis to project onto hyperplane (not strictly necessary)
      intersections = [np.array(v[:3]) for v in intersections]

      Draw4dSlice(ax, intersections)
      plt.show()

  else:
    raise AssertionError


class Animation3D(object):

  def __init__(self, vertices, edge_numbers, z_offsets, mpl_lines,
               mpl_points):
    self.vertices = vertices  # list of nparray
    self.edge_numbers = edge_numbers
    self.z_offsets = z_offsets  # nparray of z offsets
    self.mpl_lines = mpl_lines  # drawn edges to mutate
    self.mpl_points = mpl_points  # drawn intersection points to mutate

  def __call__(self, frame_index):
    """Mutate line objects to create a new frame.

    Args:
      num: from 0 to len(data)
    """
    z_offset = self.z_offsets[frame_index]
    vertices = Translate3D(self.vertices, z_offset)

    edges = []
    for a, b in self.edge_numbers:
      edges.append((vertices[a], vertices[b]))

    p0 = np.array([0, 0, 0])
    plane_normal = np.array([0, 0, 1])
    intersections = Intersect(edges, plane_normal, p0)
    print('FRAME %d' % frame_index)
    print('# intersections: %d' % len(intersections))

    for edge, mpl_line in zip(edges, self.mpl_lines):
      # NOTE: Weird API.  there is no .set_data() for 3 dim data...
      a, b = edge
      xy = np.array([
        [a[0], b[0]],
        [a[1], b[1]]
      ])
      z = np.array([a[2], b[2]])

      mpl_line.set_data(xy)
      mpl_line.set_3d_properties(z)

    # This is horrible!  You have to mutate a private variable
    # https://stackoverflow.com/questions/41602588/matplotlib-3d-scatter-animations
    # Maybe I should use ax.plot(marker='o') instead of ax.scatter ?
    x = [i[0] for i in intersections]
    y = [i[1] for i in intersections]
    z = [i[2] for i in intersections]
    self.mpl_points._offsets3d = (x, y, z)

    # TODO: plot edges and intersections
    return
    # TODO:
    # - Do translation here!
    # - Do intersection here!
    # Set mpl_lines
    for data, line in zip(self.data, self.lines):
      # NOTE: Weird API.  there is no .set_data() for 3 dim data...
      xy = data[0:2, num:num+2]
      z = data[2, num:num+2]

      line.set_data(xy)
      line.set_3d_properties(z)


def Animate4D(schlafli, num_frames):
  vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)
  vertices = [np.array(v) for v in vertices]

  # Tilt everything a bit
  vertices = Tilt4D(vertices)

  # Calculate W range AFTER ROTATION.
  w = [v[3] for v in vertices]
  w_offsets = np.linspace(-max(w), -min(w), num=num_frames)
  print('w_offsets:')
  print(w_offsets)

  edge_numbers = edges_etc[0]
  edges = []
  for a, b in edge_numbers:
    edges.append((vertices[a], vertices[b]))

  p0 = np.array([0, 0, 0, 0])
  plane_normal = np.array([0, 0, 0, 1])

  # TODO: Do we need initial intersections?  We could just make
  # dummy Line3D instances?  Just create a fake data set.
  intersections = Intersect(edges, plane_normal, p0)


def Animate3D(schlafli, num_frames):
  vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)
  vertices = [np.array(v) for v in vertices]

  # Tilt everything a bit
  vertices = Tilt3D(vertices)

  # Calculate Z range AFTER ROTATION.
  z = [v[2] for v in vertices]
  z_offsets = np.linspace(-max(z), -min(z), num=num_frames)
  print('z_offsets:')
  print(z_offsets)

  edge_numbers = edges_etc[0]
  edges = []
  for a, b in edge_numbers:
    edges.append((vertices[a], vertices[b]))

  # TODO: Do we need initial intersections?  We could just make
  # dummy Line3D instances?  Just create a fake data set.
  p0 = np.array([0, 0, 0])
  plane_normal = np.array([0, 0, 1])
  intersections = Intersect(edges, plane_normal, p0)

  fig = plt.figure()
  ax = fig.gca(projection='3d')  # create 3d axes?

  # Draw the initial frame -- calls ax.plot()0
  plane = None
  mpl_lines, mpl_points = Draw(ax, edges, plane, intersections)

  # Now mutate these objects to animate.
  anim_func = Animation3D(vertices, edge_numbers, z_offsets, mpl_lines,
                          mpl_points)

  # Just creating this object seems to mutate global state.
  anim = animation.FuncAnimation(fig, anim_func, num_frames, interval=300)

  if 0:
  # https://jakevdp.github.io/blog/2013/02/16/animating-the-lorentz-system-in-3d
    out_path = '%d-%d.mp4' % tuple(schlafli)
    anim.save(out_path, fps=15, extra_args=['-vcodec', 'libx264'])
    print('Wrote %s' % out_path)
  else:
    plt.show()


def main(argv):
  try:
    action = argv[1]
  except IndexError:
    raise RuntimeError('Action required: bounds, plot, or pbrt')

  if action == 'bounds':
    ShowBounds()

  elif action == 'pbrt':
    # Example: ./polytope.py pbrt foo.ply 4 3

    out_path = argv[2]
    schlafli = [int(a) for a in sys.argv[3:]]  # e.g. 4 3 for cube
    if len(schlafli) not in (2, 3):
      raise RuntimeError('2 or 3 args required (e.g. "4 3" for cube)')

    points = np.random.rand(100, 3)
    vertices, edges_etc = schlafli_interpreter.regular_polytope(schlafli)
    vertices = [np.array(v) for v in vertices]

    vertices = Tilt3D(vertices)

    with open(out_path, 'w') as f:
      generate_ply.generate_ply(f, vertices,
                                template_path='render/ply-header.template')

    print('Wrote %s' % out_path)

  elif action == 'plot':
    schlafli = [int(a) for a in argv[2:]]  # e.g. 4 3 for cube
    if len(schlafli) not in (2, 3):
      raise RuntimeError('2 or 3 args required (e.g. "4 3" for cube)')

    Plot(schlafli)

  elif action == 'anim':  # animate
    schlafli = [int(a) for a in argv[2:]]  # e.g. 4 3 for cube
    if len(schlafli) not in (2, 3):
      raise RuntimeError('2 or 3 args required (e.g. "4 3" for cube)')

    num_frames = 20
    if len(schlafli) == 2:
      Animate3D(schlafli, num_frames)
    elif len(schlafli) == 3:
      Animate4D(schlafli, num_frames)
    else:
      raise AssertionError

  else:
    raise RuntimeError('Invalid action %r' % action)

if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
