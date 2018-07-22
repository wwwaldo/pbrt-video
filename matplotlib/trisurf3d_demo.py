#!/usr/bin/python3

# From
# https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html#surface-plots

'''
======================
Triangular 3D surfaces
======================

Plot a 3D surface with a triangular mesh.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


n_radii = 8
n_angles = 36

# Make radii and angles spaces (radius r=0 omitted to eliminate duplication).
radii = np.linspace(0.125, 1.0, n_radii)
angles = np.linspace(0, 2*np.pi, n_angles, endpoint=False)

# Repeat all angles for each radius.
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)

# Convert polar (radii, angles) coords to cartesian (x, y) coords.
# (0, 0) is manually added at this stage,  so there will be no duplicate
# points in the (x, y) plane.
if 0:
  x = np.append(0, (radii*np.cos(angles)).flatten())
  y = np.append(0, (radii*np.sin(angles)).flatten())

# Compute z to make the pringle surface.
  z = np.sin(-x*y)
else:
  points = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 0],
    #[1, 1, 1],
    [2, 2, 2],
  ])

  print(points)
  print(points.shape)

  x = points[:, 0]
  y = points[:, 1]
  z = points[:, 2]

  print(x)
  print(y)
  print(z)

#import sys
#sys.exit()

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot_trisurf(x, y, z, linewidth=0.2, antialiased=True)

plt.show()
