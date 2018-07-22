#!/usr/bin/python3
from __future__ import print_function
"""
convex_hull_demo.py

From:
https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html
"""

import sys

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull


def main(argv):
  action = argv[1]

  if action == '2d':  # 2d
    points = np.random.rand(30, 2)   # 30 random points in 2-D
    hull = ConvexHull(points)

    plt.plot(points[:,0], points[:,1], 'o')
    for simplex in hull.simplices:
      plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

  elif action == '3d':
    points = np.random.rand(30, 3)   # 30 random points in 2-D
    #print(points)
    #print(type(points))  # ndarray of (30, 3)
    #print(points.shape)
    #return

    hull = ConvexHull(points)

    fig = plt.figure()
    ax = fig.gca(projection='3d')  # create 3d axes?

    ax.plot(points[:,0], points[:,1], points[:,2], 'o')
    for simplex in hull.simplices:
      print('simplex = %s' % simplex)

    # Does this look right?
    for simplex in hull.simplices:
      ax.plot(points[simplex, 0], points[simplex, 1], points[simplex, 2], 'k-')

  else:
    raise AssertionError(action)


  plt.show()



if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
