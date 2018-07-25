#!/usr/bin/python3
# https://matplotlib.org/examples/animation/simple_3danim.html
"""
============
3D animation
============

A simple example of an animated plot... In 3D!
"""
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


def Gen_RandLine(length, dims):
    """
    Create a line using a random walk algorithm

    length is the number of points for the line.
    dims is the number of dimensions the line has.
    """
    lineData = np.empty((dims, length))
    lineData[:, 0] = np.random.rand(dims)
    for index in range(1, length):
        # scaling the random numbers by 0.1 so
        # movement is small compared to position.
        # subtraction by 0.5 is to change the range to [-0.5, 0.5]
        # to allow a line to move backwards.
        step = ((np.random.rand(dims) - 0.5) * 0.1)
        lineData[:, index] = lineData[:, index - 1] + step

    return lineData


class Animation(object):
  def __init__(self, data, lines):
    self.data = data  # frames of raw data
    self.lines = lines  # raw line objects

  def __call__(self, num):
    """
    Args:
      num: from 0 to len(data)
    """
    for data, line in zip(self.data, self.lines):
      # NOTE: Weird API.  there is no .set_data() for 3 dim data...
      xy = data[0:2, num:num+2]
      z = data[2, num:num+2]

      line.set_data(xy)
      line.set_3d_properties(z)


NUM_LINES = 10
NUM_FRAMES = 50


def main():
  # Attaching 3D axis to the figure
  fig = plt.figure()
  ax = p3.Axes3D(fig)

  # 3 dimensions
  data = [Gen_RandLine(NUM_FRAMES, 3) for _ in range(NUM_LINES)]

  print('DATA:')
  for d in data:
    print(d)
  print(len(data))
  print('')

  # Create NUM_LINES line 2D objects.
  # NOTE: Can't pass empty arrays into 3d version of plot()
  lines = []
  for dat in data:
    # Not sure why we take a slice and then [0]
    p = ax.plot(dat[0, 0:1], dat[1, 0:1], dat[2, 0:1])
    print(p)
    lines.append(p[0])

  if 0:
    print('LINES:')
    for line in lines:
      print(line)
    print('')

  # Setting the axes properties
  ax.set_xlim3d([0.0, 1.0])
  ax.set_xlabel('X')

  ax.set_ylim3d([0.0, 1.0])
  ax.set_ylabel('Y')

  ax.set_zlim3d([0.0, 1.0])
  ax.set_zlabel('Z')

  ax.set_title('3D Test')

  anim_func = Animation(data, lines)

  # Just creating this object seems to mutate global state
  _ = animation.FuncAnimation(fig, anim_func, NUM_FRAMES, interval=20,
      blit=False)

  plt.show()


main()
