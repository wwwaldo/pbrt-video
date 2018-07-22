#!/usr/bin/python3
from __future__ import print_function
"""
poly3d_demo.py
"""

# https://stackoverflow.com/questions/37585340/plotting-3d-polygons-in-python-3
#
# A short demo, but no shading here!

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
fig = plt.figure()
ax = Axes3D(fig)
x = [0,1,1,0]
y = [0,0,1,1]
z = [0,1,0,1]
verts = [list(zip(x,y,z))]
ax.add_collection3d(Poly3DCollection(verts), zs=z)
plt.show()
