import math
import operator 

import sys

from schlafli import schlafli_interpreter

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# From squares.py
def solve_segment(line, plane):
    # These can also be done with dot products.
    a = np.matmul(plane.normal, line.direction)
    b = plane.d - np.matmul(plane.normal, line.translation)
    t = np.linalg.solve(a, b)

    solve_point = line.direction * t + line.translation

    if line.tstart > t and line.tend < t:
      return solve_point
    return None
    
class Plane:
    # input as lists.
    def __init__(self, normal, d):
        self.normal = np.array([normal])
        self.d = d
        return

class LineSegment:
    # parametric form of a line segment.
    def __init__(self, direction, translation, tstart=-math.inf, tend=math.inf):
        self.direction = np.transpose(np.array([direction]))
        self.translation = np.transpose(np.array([translation]))
        self.tstart = tstart 
        self.tend = tend
        return

    @classmethod
    def fromPoints(cls, line_segment):
      p1 = line_segment[0]
      p2 = line_segment[1]

      direction = p2 - p1 
      translation = p1
      return cls(direction, translation, 0, 1)

def getFaces(polygon):
  #TODO: get the faces dictionary output from schlafi.
  return


def FaceTupfromEdge(edge, faces):
  # return the faces that this edge belongs to.
  # faces is a dictionary of face IDs -> vertices.
  p1, p2 = edge 
  f1, f2 = None, None
  for f in faces.keys(): # VERY IMPORTANT PREASSUMPTION: the keys to faces is sorted by ID in ascending order
    if p1 in faces[f] and p2 in faces[f]:
      if f1 is None:
        f1 = f 
      elif f2 is None:
        f2 = f 
        break
  return f1, f2

def Intersect_memoize(edges, plane_normal, p0, faces):
  # edges are given as a tuple of np.arrays.

  plane = Plane(plane_normal, p0)
  temp = dict()

  for edge in edges:
    print(f"New edge: {edge}")

    # want to get the line segment for this edge.
    line_segment = LineSegment.fromPoints(edge)

    intersection_point = solve_segment(line_segment, plane)
    if intersection_point is None:
      print(f"No intersection with edge {edge}")
      continue
    else:
      # get the faceID corresponding to this point.
      face_id = FaceTupfromEdge(edge, faces)
      temp[edge] = face_id 

# get an ordered list of vertices which can be used to draw this polygon.
# 'mapping' is a map of vertices to (original!) face IDs
def OrderVertices(mapping):
  # sort 'mapping' on the faces.
  sorted_mapping = sorted(mapping.items(), key=operator.itemgetter(1))
  return sorted_mapping.keys() # Ha!


if __name__ == "__main__":
    print("Hello world!")

    for d in np.linspace( -1, 1, 10):
        line = Line([1, 0, 0], [1, 2, 3])
        plane = Plane([1, 1, 1], d)
        result = solve(line, plane)
        print(result)