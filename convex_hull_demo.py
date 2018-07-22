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
from scipy.spatial import ConvexHull


def main(argv):
  print('Hello from convex_hull_demo.py')
  points = np.random.rand(30, 2)   # 30 random points in 2-D
  hull = ConvexHull(points)

  plt.plot(points[:,0], points[:,1], 'o')
  for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

  plt.show()


if __name__ == '__main__':
  try:
    main(sys.argv)
  except RuntimeError as e:
    print('FATAL: %s' % e, file=sys.stderr)
    sys.exit(1)
